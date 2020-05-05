import copy
import logging
logger = logging.getLogger(__name__)

##########################
# KISS Special Characters.
##########################
KISS_FEND  = 0xc0
KISS_FESC  = 0xdb
KISS_TFEND = 0xdc
KISS_TFESC = 0xdd

KISS_SPECIAL_PACK = {
    KISS_FEND: [KISS_FESC, KISS_TFEND],
    KISS_FESC: [KISS_FESC, KISS_TFESC]
}

KISS_SPECIAL_UNPACK = {
    KISS_TFEND: [KISS_FEND],
    KISS_TFESC: [KISS_FESC]
}

KISS_SPECIAL_TYPES = [KISS_FEND, KISS_FESC, KISS_TFEND, KISS_TFESC]

##########################
# KISS Control.
##########################
KISS_CTRL_DATA       = 0x00
KISS_CTRL_TXDELAY    = 0x01
KISS_CTRL_P          = 0x02
KISS_CTRL_SLOTTIME   = 0x03
KISS_CTRL_TXTAIL     = 0x04
KISS_CTRL_FULLDUPLEX = 0x05
KISS_CTRL_SETHW      = 0x06
KISS_CTRL_RETURN     = 0x0F

KISS_CTRL_DEFAULT = {
    KISS_CTRL_DATA       :    0,
    KISS_CTRL_TXDELAY    :   50,
    KISS_CTRL_P          :   63,
    KISS_CTRL_SLOTTIME   :   10,
    KISS_CTRL_TXTAIL     :    0,
    KISS_CTRL_FULLDUPLEX :    0,
    KISS_CTRL_SETHW      :    0,
    KISS_CTRL_RETURN     : KISS_CTRL_RETURN
}

KISS_CTRL_TYPES = KISS_CTRL_DEFAULT.keys()

##########################
# Unpacked message format.
##########################
KISS_PACKET_TEMPLATE = {
    "ctrl"  : KISS_CTRL_DATA,
    "port"  : 0,
    "param" : KISS_CTRL_DEFAULT[KISS_CTRL_DATA],
    "data"  : []
}


def KISS_unpack(data):
    """
    Unpack a raw bytearray from KISS format.

    Args:
        data (bytearray|str):   Byte array to unpack from KISS.

    Returns:
        List of dictionaries unpacked from input array.
    """
    # Convert to bytearray.
    if isinstance(data, str):
        data = bytearray(data)

    # States.
    STATE_DELIM = 0x00
    STATE_ESC   = 0x01
    STATE_DATA  = 0x02

    # Check that first byte is delimiter.
    if len(data) < 1:
        logger.error("Empty data array.")
        return []
    if data[0] != KISS_FEND:
        logger.warning("KISS starting frame delimiter not found. Searching...")
        if KISS_FEND in list(data):
            logger.warning("Frame delimiter found. Attempting to parse...")
        else:
            logger.error("Frame delimiter not found in array.")
            return []

    # Unpack state machine.
    state = STATE_DELIM
    frames = []
    info   = []
    for octet in data:
        # Gather all starting delimiters.
        if state == STATE_DELIM:
            if octet == KISS_FEND:
                if len(frames) > 0:
                    logger.warning("Multiple frames detected in array.")
                continue

            state = STATE_DATA

        # Check for escape character.
        if octet == KISS_FESC:
            state = STATE_ESC
            continue

        if octet == KISS_FEND:
            # Check for valid control byte.
            if len(info) == 0:
                logger.error("Empty frame.")
                continue

            # Parse control byte and parameter.
            ctrl = (info[0] >> 0) & 0x0f
            port = (info[0] >> 4) & 0x0f
            info = info[1:]
            if ctrl not in KISS_CTRL_DEFAULT.keys():
                logger.error("Invalid control type \'0x{:02x}\'.",format(ctrl))
                continue

            parm = KISS_CTRL_DEFAULT.get(ctrl, 0)
            if ctrl not in [KISS_CTRL_DATA, KISS_CTRL_RETURN]:
                if len(info) < 2:
                    logger.error("Short frame (%u bytes)." % len(info))
                    continue
                parm = info[0] & 0xff
                info = info[1:]

            # Create packet.
            packet          = {}
            packet["ctrl"]  = ctrl
            packet["port"]  = port
            packet["param"] = parm
            packet["data"]  = copy.deepcopy(bytearray(info))
            frames.append(packet)
            # Reset state machine.
            info = []
            state = STATE_DELIM
            continue

        if state == STATE_ESC:
            if octet in KISS_SPECIAL_UNPACK.keys():
                # Get sequence.
                seq = KISS_SPECIAL_UNPACK.get(octet, [])
                # Insert sequence.
                info += seq
                state = STATE_DATA
            else:
                logger.error("Invalid escaped character \'0x{:02x}\', ignoring...".format(octet))
                continue
        else:
            state = STATE_DATA
            info += [octet]

    return frames


def KISS_pack(frame):
    """
    Pack a dictionary into KISS format.

    Args:
        data (dict):    Dictionary w/ frame information to packet into KISS format.

    Returns:
        Byte array packed as KISS packet.
    """
    # Convert to bytearray.
    if not isinstance(frame, dict):
        logger.error("KISS_pack: Input type invalid (type=%s)." % type(frame))
        return bytearray([])

    data = frame.get("data", [])
    if len(data) == 0:
        logger.warning("No data detected in frame, skipping...")
        return bytearray([])

    info = []
    # Check for special characters.
    for octet in data:
        if octet in KISS_SPECIAL_PACK.keys():
            # Get sequence.
            seq = KISS_SPECIAL_PACK.get(octet, [])
            # Insert sequence.
            info += seq
        else:
            info += [octet]

    # Control type.
    ctrl = frame.get("ctrl", KISS_CTRL_DATA)
    if ctrl not in KISS_CTRL_DEFAULT.keys():
        logger.error("Invalid control type \'0x{:02x}\'.".format(ctrl))
        return bytearray([])
    port = frame.get("port", 0)
    if ctrl == KISS_CTRL_RETURN:
        ctrlWord = KISS_CTRL_RETURN
    else:
        ctrlWord = ((port & 0x0f) << 4) | (ctrl & 0x0f)
    parm = frame.get("param", 0)

    # Pre-pend frame delimiter.
    packet  = [KISS_FEND]
    # Add control byte.
    packet += [ctrlWord]
    # Add parameter (if necessary).
    if ctrl not in [KISS_CTRL_DATA, KISS_CTRL_RETURN]:
        packet += [int(parm) & 0xFF]
    # Add data.
    packet += info
    # Post-pend frame delimiter.
    packet += [KISS_FEND]

    return bytearray(packet)


def KISS_P_intToFloat(P):
    """
    Convert persistence byte to float.

    Args:
        P (int) : Persistence byte.

    Returns:
        Mapped float in the range [0.0, 1.0].
    """
    # Clip to range.
    P = min([max([0, P]), 255])
    return float(P+1)/256


def KISS_P_floatToInt(p):
    """
    Convert persistence float to byte.

    Args:
        p (float)   : Persistence value ([0.0, 1.0]).

    Returns:
        Mapped byte.
    """
    # Clip to range.
    p = min([max([0.0, p]), 1.0])
    return max([int(p*256 - 1), 0])


def KISS_byteToMsec(param):
    """
    Convert time byte to milliseconds.

    Args:
        param (byte)    : Time parameter byte.

    Returns:
        Time in milliseconds.
    """
    return float(param)*10.0


def KISS_msecToByte(interval):
    """
    Convert time (in milliseconds) to byte.

    Args:
        interval (float)    : Time in milliseconds.

    Returns:
        Time byte.
    """
    return max([min([int(round(interval / 10.0)), 255]), 0])






def unittest():
#    logging.basicConfig()
#    logger.setLevel(logging.DEBUG)

    print("#" * 40)
    print("Test 1 - Simple frame")
    data    = bytearray(range(16))
    frame   = {"ctrl": KISS_CTRL_DATA, "param": 0, "data": data}
    packet  = KISS_pack(frame)
    uframes = KISS_unpack(packet)
    if len(uframes) > 0:
        uframe = uframes[-1]
        udata  = uframe.get("data", [])
    else:
        uframe = {}
        udata  = []
    check = (data == udata)

    print("TX Frame: %s" % str(frame))
    print("Sent:     %s" % (", ".join(["0x{:02x}".format(bi) for bi in data])))
    print("Pack:     %s" % (", ".join(["0x{:02x}".format(bi) for bi in packet])))
    print("Recv:     %s" % (", ".join(["0x{:02x}".format(bi) for bi in udata])))
    print("RX Frame: %s" % str(uframe))
    print("Status: %s" % ("PASS" if check else "FAIL"))

    print("#" * 40)
    print("Test 2 - Frame w/ special character")
    data    = bytearray(range(16))
    data[4] = KISS_FEND
    frame   = {"ctrl": KISS_CTRL_DATA, "param": 0, "data": data}
    packet  = KISS_pack(frame)
    uframes = KISS_unpack(packet)
    if len(uframes) > 0:
        uframe = uframes[-1]
        udata  = uframe.get("data", [])
    else:
        uframe = {}
        udata  = []
    check = (data == udata)

    print("TX Frame: %s" % str(frame))
    print("Sent:     %s" % (", ".join(["0x{:02x}".format(bi) for bi in data])))
    print("Pack:     %s" % (", ".join(["0x{:02x}".format(bi) for bi in packet])))
    print("Recv:     %s" % (", ".join(["0x{:02x}".format(bi) for bi in udata])))
    print("RX Frame: %s" % str(uframe))
    print("Status: %s" % ("PASS" if check else "FAIL"))

    print("#" * 40)
    print("Test 2 - Frame w/ all special characters")
    data    = [KISS_SPECIAL_TYPES[i % len(KISS_SPECIAL_TYPES)] for i in range(20)]
    data    = bytearray(data)
    frame   = {"ctrl": KISS_CTRL_DATA, "param": 0, "data": data}
    packet  = KISS_pack(frame)
    uframes = KISS_unpack(packet)
    if len(uframes) > 0:
        uframe = uframes[-1]
        udata  = uframe.get("data", [])
    else:
        uframe = {}
        udata  = []
    check = (data == udata)

    print("TX Frame: %s" % str(frame))
    print("Sent:     %s" % (", ".join(["0x{:02x}".format(bi) for bi in data])))
    print("Pack:     %s" % (", ".join(["0x{:02x}".format(bi) for bi in packet])))
    print("Recv:     %s" % (", ".join(["0x{:02x}".format(bi) for bi in udata])))
    print("RX Frame: %s" % str(uframe))
    print("Status: %s" % ("PASS" if check else "FAIL"))


    print("#" * 40)
    print("Test 2 - Multiple frames within a buffer")
    data0   = bytearray(range(16))
    data1   = bytearray(range(17, 23))
    frame0  = {"ctrl": KISS_CTRL_DATA, "param": 0, "data": data0}
    frame1  = {"ctrl": KISS_CTRL_DATA, "param": 0, "data": data1}
    packet0 = KISS_pack(frame0)
    packet1 = KISS_pack(frame1)
    packet  = bytearray(list(packet0)+list(packet1))
    frames  = [frame0, frame1]
    uframes = KISS_unpack(packet)
    for frame, uframe in zip(frames, uframes):
        data  = frame.get("data", [])
        udata = frame.get("data", [1])
        check = (data == udata)

        print("TX Frame: %s" % str(frame))
        print("Sent:     %s" % (", ".join(["0x{:02x}".format(bi) for bi in data])))
        print("Recv:     %s" % (", ".join(["0x{:02x}".format(bi) for bi in udata])))
        print("RX Frame: %s" % str(uframe))
        print("Status: %s" % ("PASS" if check else "FAIL"))


if __name__ == "__main__":
    import sys
    sys.exit(unittest())
