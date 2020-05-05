#!/usr/bin/env python

import logging
logger = logging.getLogger()

import os
import sys
import shutil
import time
import re
import uuid
import argparse
import subprocess
import ConfigParser


# Defaults.
AX25_DFLT_VPORT   = "/tmp/ttyS99"
AX25_DFLT_IPPROTO = "tcp"
AX25_DFLT_IPADDR  = "127.0.0.1"
AX25_DFLT_IPPORT  = "15331"
AX25_DFLT_DEVICE  = "ax0"
AX25_DFLT_AXPORT  = "radio0"
AX25_DFLT_NETADDR = "44.254.120.1"
AX25_DFLT_NETMASK = "255.255.255.0"


def parseConfig(config):
    """
    Parse an INI configuration file into a dictionary.

    Args:
        config (str)    : Path to INI file.

    Returns:
        Dictionary containing all parsed sections/options.
    """
    confParser = ConfigParser.ConfigParser()
    confParser.read(config)

    confDict = {}
    for section in confParser.sections():
        if section not in confDict:
            confDict[section] = {}

        for opt in confParser.options(section):
            try:
                val = confParser.get(section, opt)
            except Exception as e:
                logger.error("Failed to get \'(%s, %s)\': %s" % (section, opt, str(e)))
                continue

            confDict[section][opt] = val

    return confDict


def getStringNumber(s):
    """
    Get the integer number at the end of a string.

    Args:
        s (str) : String to search.

    Returns:
        Parsed number on success, None on error.
    """
    grp = re.search(r'\d+$', s)
    return int(grp.group()) if grp else None


class AX25_Interface_Manager(object):
    AX25_TOOLS_AXPORTS_PATH = "/etc/ax25/axports"

    def __init__(self, config=None):
        super(AX25_Interface_Manager, self).__init__()

        # Check configuration file path (if provided).
        if config != None:
            self.setConfig(config)

    def get_axports(self):
        """
        Read all the AX.25 ports from the system configuration file.

        Returns:
            List of dictionaries containing the fields of each valid entry.
        """
        if not os.path.exists(self.AX25_TOOLS_AXPORTS_PATH):
            line = "AX.25 \'axports\' file not found. Check if \'ax25-tools\' package is installed."
            logger.error(line)
            return []

        ports = []
        with open(self.AX25_TOOLS_AXPORTS_PATH, "r") as f:
            for k,line in enumerate(f.readlines()):
                # Skip comments.
                if line.startswith("#"):
                    continue

                fixed = " ".join(line.strip().split())
                # Skip blank lines.
                if len(fixed) == 0:
                    continue

                # Parse options.
                opts = re.split(" ", fixed, 5)
                if len(opts) < 5:
                    msg = "Invalid line detected in %s (line=%u,raw=%s)." % \
                          (self.AX25_TOOLS_AXPORTS_PATH, k+1, line)
                    logger.error(msg)
                    continue

                # Create port entry.
                try:
                    port = {"name"       : opts[0],
                            "callsign"   : opts[1],
                            "baud"       : int(opts[2]),
                            "paclen"     : int(opts[3]),
                            "window"     : int(opts[4]),
                            "description": "" if (len(opts) < 6) else opts[5],
                            "meta"       : {"entry"      : fixed,
                                            "entrynum"   : len(ports)+1,
                                            "linenum"    : k}
                            }
                except Exception as e:
                    msg = "Failed to create port entry: %s." % str(e)
                    logger.error(msg)
                    continue

                ports.append(port)

            return ports

    def get_axport(self, **kwargs):
        """
        Read the AX.25 port settings from the system configuration file.

        Returns:
            Dictionary containing the fields of the valid entry, empty dictionary on error/not found.
        """
        name     = kwargs.get("name", None)
        callsign = kwargs.get("callsign", None)

        ports = self.get_axports()
        port  = {}
        if name != None:
            for entry in ports:
                if name.lower() == entry.get("name", "").lower():
                    port = entry
                    break

        if callsign != None:
            for entry in ports:
                if callsign.lower() == entry.get("callsign", "").lower():
                    port = entry
                    break

        return port

    def add_axport(self, name, callsign, baud=0, paclen=512, window=2, description="Automatically generated w/ AX25_Interface_Manager."):
        """
        Add a new port definition to the Linux AX.25 interface.
        Writes a new line in the configuration file (usually /etc/ax25/axports).

        Args:
            name (str)          : Name of the new interface (must be unique).
            callsign (str)      : Callsign of the new interface (must be unique).
            baud (int)          : Baud rate of the interface (0 for software/networked modems) [default=0].
            paclen (int)        : Maximum packet length of interface [default=512].
            window (int)        : Window size [default=2]
            description (str)   : Description field.

        Returns:
            0 on success, -1 on error.
        """
        port = self.get_axport(name=name, callsign=callsign)
        if len(port.keys()) > 0:
            entry   = port.get("meta", {}).get("entry", "")
            linenum = port.get("meta", {}).get("linenum", -1)
            msg     = "Port \'%s\' or callsign \'%s\' already defined in \'%s\' (line %u: \'%s\'), please select a different name." % \
                      (name, callsign, self.AX25_TOOLS_AXPORTS_PATH, linenum, entry)
            logger.error(msg)
            return -1

        try:
            with open(self.AX25_TOOLS_AXPORTS_PATH, "a") as f:
                entry = "{} {} {} {} {} {}\n".format(name, callsign, baud, paclen, window, description)
                f.write(entry)

        except Exception as e:
            msg = "Failed to open and write \'%s\': %s (check installation/permissions)." % (self.AX25_TOOLS_AXPORTS_PATH, str(e))
            logger.error(msg)
            return -1

        return 0

    def remove_axport(self, name):
        """
        Remove a port definition from the Linux AX.25 interface.
        Removes a line from the configuration file (usually /etc/ax25/axports).

        Args:
            name (str)  : Name of the interface.

        Returns:
            0 on success, -1 on error.
        """
        ret = 0
        port = self.get_axport(name=name)
        if len(port.keys()) == 0:
            logger.warning("\'%s\' port not found." % name)
            return ret

        try:
            # Temporary file.
            tmp = "/tmp/axports-%s" % str(uuid.uuid1())
            with open(self.AX25_TOOLS_AXPORTS_PATH, "r") as f:
                with open(tmp, "w") as fw:
                    for line in f.readlines():
                        line = line.strip()

                        # Add comments back to file.
                        if line.startswith("#"):
                            fw.write("%s\n" % line)
                            continue

                        # Check for entry.
                        if line.startswith(name):
                            # Remove.
                            continue

                        fw.write("%s\n" % line)

            # Copy back to '/etc/ax25/axports'.
            try:
                shutil.move(tmp, self.AX25_TOOLS_AXPORTS_PATH)
            except Exception as e:
                msg = "Failed to write \'%s\': %s (check installation/permissions)" % \
                      (self.AX25_TOOLS_AXPORTS_PATH, str(e))
                logger.error(msg)
                ret = -1

        except Exception as e:
            msg = "Failed to open and write \'%s\': %s (check installation/permissions)." % (self.AX25_TOOLS_AXPORTS_PATH, str(e))
            logger.error(msg)
            ret = -1

        # Remove temporary file.
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except Exception as e:
            msg = "Failed to remove temporary file \'%s\': %s." % (tmp, str(e))
            logger.error(msg)

        return ret

    def create_interface_file(self,
                              axport=None,
                              callsign=None,
                              serialPort=None,
                              tcpPort=None,
                              **kwargs):
        """
        Create an interface file for /etc/network/interfaces.d (Debian-specific).

        Args:
            axport (str)    : Name of the AX.25 port from Linux configuration. Default is the first entry in the configuration [default=auto].
            callsign (str)  : Callsign of the AX.25 por from the Linux configuration. Default is the first entry in the configuration. [default=auto].
            serialPort (str): Name of the virtual serial port to use. Default is auto-generated [default=auto].
            tcpPort (str)   : TCP listen port for AX.25 forwarding from virtual serial port [default=15331].
            iface (str)     : Name of network interface (shows up in 'ifconfig') [default=ax0].
            address (str)   : IP address of the network interface [default=44.254.120.1].
            netmask (str)   : Netmask of the network interface [default=255.255.255.0].

        Kwargs:
            All remaining kwargs will be added to interface as:
                iface <iface> inet static
                    ...
                    <key>   <value>

            i.e
                create_interface_file(broadcast="44.254.120.255")
                -->
                iface <iface> inet static
                    ...
                    broadcast   44.254.120.255

        Returns:
            String representing the interface entry for the AX.25 device (to be placed in /etc/network/interfaces, /etc/network/interfaces.d, ...).
        """
        # Get default port.
        ports = self.get_axports()
        if len(ports) > 0:
            port = ports[0]
            name = port.get("name",     "none")
            call = port.get("callsign", "none")
        else:
            logger.warning("No entries in AX.25 port file (\'%s\')" %
                           self.AX25_TOOLS_AXPORTS_PATH)

        # Check virtual serial ports.
        vportNum = 0
        vports = []
        for fname in os.listdir("/tmp"):
            vports.append(fname.lower())
            if fname.lower().startswith("ttys"):
                num = getStringNumber(fname.lower())
                if num != None:
                    vportNum = max([vportNum, num+1])
        vportTmp = "/tmp/ttyS{}".format(vportNum)

        # Get defaults (if necessary)
        if axport == None:
            axport = name
        if callsign == None:
            callsign = call
        if serialPort == None:
            serialPort = vportTmp
        if tcpPort == None:
            tcpPort = AX25_DFLT_IPPORT

        # Check serial port isn't already opened.
        if serialPort.lower() in vports:
            logger.error("Requested serial port \'%s\' in use." % serialPort)
            return -1

        # Get interface configuration.
        dev       = kwargs.pop("iface",     AX25_DFLT_DEVICE)
        ipAddr    = kwargs.pop("address",   AX25_DFLT_NETADDR)
        netmask   = kwargs.pop("netmask",   AX25_DFLT_NETMASK)

        # Pre-up commands.
        fwdUp = ["socat",
                 "pty,link={},raw,echo=0".format(serialPort),
                 "tcp-listen:{},reuseaddr,fork".format(tcpPort),
                 "&"]
        slpUp = ["sleep",
                 "3"]
        perUp = ["chmod",
                 "666",
                 serialPort]
        kssUp = ["kissattach",
                 "-l",
                 serialPort,
                 axport,
                 ipAddr]

        preCmd = [" ".join(fwdUp), " ".join(slpUp), " ".join(perUp), " ".join(kssUp)]

        # Post-down commands.
        fwdDown = ["pkill",
                   "socat",
                   "||",
                   "pkill",
                   "-9",
                   "socat"]
        kssDown = ["pkill",
                   "kissattach",
                   "||",
                   "pkill",
                   "-9",
                   "kissattach"]

        postCmd = [" ".join(fwdDown), " ".join(kssDown)]

        interface =("manual {}\n"
                    "iface {} inet static\n"
                    "    {:12s} {}\n"
                    "    {:12s} {}\n").format(
                        dev,
                        dev,
                        "address",   ipAddr,
                        "netmask",   netmask)

        for cmd in preCmd:
            interface += "    {:12s} {}\n".format("pre-up", cmd)

        for cmd in postCmd:
            interface += "    {:12s} {}\n".format("post-down", cmd)

        # Add any additional settings.
        for key in kwargs.keys():
            if key == "":
                continue
            value = kwargs.get(key, "")
            interface += "    {:12s} {}\n".format(key, value)

        return interface

    def setConfig(self, config):
        if not os.path.exists(config):
            line = "Configuration file \'%s\' not found." % str(config)
            logger.error(line)
            return -1

        self.configPath = config
        self.config = parseConfig(self.configPath)



def AX25_Interface_Config(config):
    """
    Configure the Linux AX.25 settings.

    Args:
        config (str)    : Path to configuration file (.ini).

    Returns:
        0 on success, -1 on error.
    """




def AX25_Interface_Up(config):
    """
    Bring up the AX.25 Linux network interface.
    """
    params = parseConfig(config)
    logger.debug("Params: %s" % str(params))

    # Get variables.
    forwarding = params.get("forwarding", {})
    vPort   = forwarding.get("serial",  AX25_DFLT_VPORT)
    ipProto = forwarding.get("ipproto", AX25_DFLT_IPPROTO)
    ipAddr  = forwarding.get("ipaddr",  AX25_DFLT_IPADDR)
    ipPort  = forwarding.get("ipport",  AX25_DFLT_IPPORT)

    interface = params.get("interface", {})
    device  = forwarding.get("device", AX25_DFLT_DEVICE)
    axPort  = forwarding.get("axport", AX25_DFLT_AXPORT)
    netAddr = forwarding.get("ipaddr", AX25_DFLT_NETADDR)

    # Create virtual serial port.
    cmd = ["socat",
           "pty,link={},raw,echo=0".format(vPort),
           "tcp-listen:{},reuseaddr,fork".format(ipPort)]
    logger.info("    Starting virtual port forwarding (%s <--> %s)..." %
                (vPort, ipPort))
    try:
        proc = subprocess.Popen(cmd)
    except Exception as e:
        line = "Failed to start virtual serial port forwarding: '%s' (%s)" % \
                (str(cmd), str(e))
        logger.error(line)
        return -1

    # Wait for interface to stand up.
    time.sleep(3.0)

    # Change permissions.
    cmd = ["chmod",
           "666",
           vPort]
    logger.info("    Changing virtual serial port permissions (%s)..." %
                (str(cmd)))
    try:
        subprocess.check_call(cmd)
    except Exception as e:
        line = "Failed to change virtual serial port permissions: '%s' (%s)" % \
                (str(cmd), str(e))
        logger.error(line)
        return -1

    # Attach AX.25 network device (via KISS).
    cmd = ["kissattach",
           "-l",
           vPort,
           axPort,
           netAddr]
    logger.info("    Creating AX.25 network interface w/ KISS wrapper as %s (axport=%s)..." %
                (netAddr, axPort))
    try:
        subprocess.check_call(cmd)
    except Exception as e:
        line = "Failed to change virtual serial port permissions: '%s' (%s)" % \
                (str(cmd), str(e))
        logger.error(line)
        return -1

    return 0


def main():
    # Set logging configuration.
    logging.basicConfig()

    mgr = AX25_Interface_Manager()
    ports = mgr.get_axports()
    print(ports)

#    mgr.add_axport("radio1", "KC3ECG-2")
#    mgr.remove_axport("radio1")
    ifc = mgr.create_interface_file(iface="ax0",
                                    address="44.254.120.1",
                                    network="44.254.120.0",
                                    broadcast="44.254.120.255")
    print(ifc)

#    # Parse arguments.
#    parser = argparse.ArgumentParser(prog="AX.25 Interface Handler",
#                                     description="Handles bringing-up and tearing-down AX.25 network interface on Linux.")
#
#    parser.add_argument(dest="config",
#                        default="ax25_config.ini",
#                        type=str,
#                        help="Configuration file containing all relevant information for desired AX.25 interface.")
#
#    parser.add_argument("-u", "--up",
#                        dest="up",
#                        default=False,
#                        const=True,
#                        action="store_const",
#                        help="Bring up the AX.25 network interface.")
#
#    parser.add_argument("-d", "--down",
#                        dest="down",
#                        default=False,
#                        const=True,
#                        action="store_const",
#                        help="Tear down the AX.25 network interface.")
#
#    parser.add_argument("--log-level",
#                        dest="logLevel",
#                        default="info",
#                        choices=["debug", "info", "warning"],
#                        help="Desired log level.")
#
#    params = parser.parse_args()
#
#    config = params.config
#    up     = params.up
#    down   = params.down
#    level  = params.logLevel
#
#    logger.setLevel(logging.DEBUG)
#
#    if up and down:
#        logger.error("Cannot perform \'up\' and \'down\' in same call.")
#        return -1
#
#
#    if up:
#        return AX25_Interface_Up(config)
#
#    if down:
#        pass
#
#    return 0


if __name__ == "__main__":
    sys.exit(main())
