import logging
logger = logging.getLogger(__name__)

import copy

# Byte reveral look up.
OCTET_REV_LUT = [int("{:08b}".format(oi)[::-1], 2) for oi in range(0xff+1)]

# AX.25 Protocol IDs.
AX25_PID_X25_PLP     = 0x01
AX25_PID_TCPIP_CMP   = 0x06
AX25_PID_TCPIP       = 0x07
AX25_PID_SEGFRAG     = 0x08
AX25_PID_TEXNET      = 0xc3
AX25_PID_LINKQUAL    = 0xc4
AX25_PID_APPLTK      = 0xca
AX25_PID_APPLTK_ARP  = 0xcb
AX25_PID_ARPA_IP     = 0xcc
AX25_PID_ARPA_ADDRES = 0xcd
AX25_PID_FLEXNET     = 0xce
AX25_PID_NETROM      = 0xcf
AX25_PID_NONE        = 0xf0
AX25_PID_ESC         = 0xff

AX25_PID_L3_BIT_MASK = 0x6f
AX25_PID_L3_BIT_SEQS = [0x10, 0x20]

AX25_PID =\
{
    AX25_PID_X25_PLP     : "ISO 8208/CCITT X.25 PLP",
    AX25_PID_TCPIP_CMP   : "TCP/IP (compressed)",
    AX25_PID_TCPIP       : "TCP/IP",
    AX25_PID_SEGFRAG     : "Segmentation fragment",
    AX25_PID_TEXNET      : "TEXNET datagram",
    AX25_PID_LINKQUAL    : "Link Quality",
    AX25_PID_APPLTK      : "Appletalk",
    AX25_PID_APPLTK_ARP  : "Appletalk ARP",
    AX25_PID_ARPA_IP     : "ARPA IP",
    AX25_PID_ARPA_ADDRES : "ARPA Address Resolution",
    AX25_PID_FLEXNET     : "FlexNet",
    AX25_PID_NETROM      : "NET/ROM",
    AX25_PID_NONE        : "Raw",
    AX25_PID_ESC         : "Escape"
}


def reverseOctets(octets):
    """
    Bit reverse the bytes in the array.

    Args:
        octets (list)   : List of bytes to reverse.

    Returns:
        List of reversed bytes.
    """
    return [OCTET_REV_LUT[oi & 0xff] for oi in octets]


def octetsToBits(octets, lsbFirst=True):
    data = octets
    if not lsbFirst:
        data = reverseOctets(octets)

    out = []
    for oi in data:
        for b in range(8):
            bi = (oi >> b) & 0x1
            out.append(bi)

    return out


def bitsToOctets(bitSeq, lsbFirst=True):
    out   = []
    cnt   = 0
    octet = 0x00
    for bi in bitSeq:
        octet = (octet << 1) & 0xff
        octet = octet | bi
        cnt  += 1
        if cnt == 8:
            out.append(octet)
            cnt = 0

    if lsbFirst:
        out = reverseOctets(out)

    return out


def nrzToNrzi(bitSeq, init=1):
    delay = int(not (init & 0x1))

    nrzi = []
    for bi in bitSeq:
        nbi   = int(not (bi & 0x1))
        delay = nbi ^ delay
        nrzi.append(int(not delay))

    return nrzi


def nrziToNrz(bitSeq, init=1):
    delay = int(init & 0x1)

    nrz = []
    for bi in bitSeq:
        nrz.append(int(not ((bi & 0x1) ^ delay)))
        delay = int(bi & 0x1)

    return nrz

def Ax25_bytesToPacket(octets):
    """
    Parse AX.25 packet from an array of bytes.

    Args:
        octets (bytearray)  : Byte array containing an AX.25 packet (w/o HDLC framing).

    Returns:
        Dictionary containing all parsed fields.

        packet =
        {'src'      : <source address info>,
         'dest'     : <destination address info>,
         'repeaters': <list of repeater address info(s)>,
         'ctrl'     : <control info>,
         'proto'    : <prototype ID> (if found),
         'info'     : <array of information bytes>,
         'raw'      : <raw input bytes>}

    """
    packet   = {}
    packet["raw"] = copy.deepcopy(list(octets))

    # Get destination and source.
    last, destInfo = Ax25_bytesToAddr(octets[0:7])
    if last:
        line = "Address section ended early."
        logger.error(line)
        return packet
    if len(destInfo) == 0:
        line = "Destination address parsing error."
        logger.error(line)
        return packet
    packet["dest"] = destInfo
    octets = octets[7:]

    last, srcInfo  = Ax25_bytesToAddr(octets[0:7])
    if len(srcInfo) == 0:
        line = "Source address parsing error."
        logger.error(line)
        return packet
    packet["src"] = srcInfo
    octets = octets[7:]

    # Parse repeaters.
    packet["repeaters"] = []
    while not last:
        if len(octets) < 7:
            line = "Address section too short."
            logger.error(line)
            return packet

        last, rptrInfo = Ax25_bytesToAddr(octets[0:7])
        if len(rptrInfo) == 0:
            line = "Repeater address parsing error."
            logger.error(line)
            return packet

        packet["repeaters"].append(rptrInfo)
        octets = octets[7:]

    if len(octets) < 1:
        line = "Short packet, could not decode control octet."
        logger.error(line)
        return packet

    # Parse control.
    ctrl   = Ax25_byteToCtrl(octets[0])
    if len(ctrl) == 0:
        line = "Failed to parse control."
        logger.error(line)
        return packet

    octets = octets[1:]
    packet["ctrl"] = ctrl

    # Parse protocol.
    if packet["ctrl"].get("type", None) in ["UI", "I"]:
        if len(octets) < 1:
            line = "Short packet, could not decode protocol octet."
            logger.error(line)
            return packet

        packet["proto"] = Ax25_byteToProto(octets[0])
        octets = octets[1:]

    # Get data.
    print("len=%u" % len(octets))
    packet["info"] = copy.deepcopy(list(octets))

    return packet


def Ax25_bytesToAddr(octets):
    """
    Convert byte array to address.

    Args:
        octets (list)   : List of bytes to convert to address (length >= 7).

    Returns:
        Dictionary containing address information.

        addr =
        {"callsign" : <callsign string>,
         "ssid"     : <ssid>,
         "rsvd"     : <reserved bits>,
         "ch"       : <CH bits>}
    """
    if len(octets) < 7:
        line = "%u octets required for address (%u provided)." % \
               (7, len(octets))
        logger.error(line)
        return True, {}

    # Parse address fields.
    callsign = "".join([chr(ci >> 1) for ci in octets[0:6]]).strip()
    last     = (octets[6] >> 0) & 0x01
    ssid     = (octets[6] >> 1) & 0x0f
    rsvd     = (octets[6] >> 5) & 0x03
    ch       = (octets[6] >> 7) & 0x01

    # Create dictionary w/ info.
    addr = {
        "callsign"  : callsign,
        "ssid"      : ssid,
        "rsvd"      : rsvd,
        "ch"        : ch
    }

    return bool(last), addr


def Ax25_byteToCtrl(ctrl):
    """
    Convert a list of bytes to control information.

    Args:
        ctrl (list) : List of bytes to convert to control.

    Returns:
        Dictionary containing the control information.

        ctrl =
        {"type" : <type identifier>,
         "pf"   : <P/F value>,
         "snum" : <sent sequence number> (if found),
         "rnum" : <recv sequence number> (if found),
         "supv" : <supv bits> (if found),
         "fmod" : <field modifier bits, masked version*> (if found)}

    * masked version meaning the 'fmod' field is masked from the control byte and returned
      directly without any modification (i.e. <fmod> = <ctrl byte> & 0xEC).
    """
    field = {}
    if (ctrl & 0x1) == 0x00:
        field["type"] = "I"
        field["snum"] = (ctrl >> 1) & 0x07
        field["pf"]   = (ctrl >> 4) & 0x01
        field["rnum"] = (ctrl >> 5) & 0x07
    else:
        if (ctrl & 0x03) == 0x01:
            field["type"] = "S"
            field["supv"] = (ctrl >> 2) & 0x03
            field["pf"]   = (ctrl >> 4) & 0x01
            field["rnum"] = (ctrl >> 5) & 0x07
        else:
            field["fmod"] = ctrl & 0xec
            field["pf"]   = (ctrl >> 4) & 0x01
            field["type"] = "U" if (field["fmod"] > 0) else "UI"

    return field


def Ax25_byteToProto(octet):
    """
    Convert byte to protocol identifier string.

    Args:
        octet (byte)    : Byte to convert.

    Returns:
        Protocol identifier string.
    """
    octet = int(octet) & 0xff

    for patt in AX25_PID_L3_BIT_SEQS:
        if (octet & AX25_PID_L3_BIT_MASK) == patt:
            return "AX.25 - L3"

    return AX25_PID.get(octet, "Unknown")


if __name__ == "__main__":
    # Octets <-> Bits
    octets = range(4)
    print(octets)
    print(octetsToBits(octets, lsbFirst=True))
    print(bitsToOctets(octetsToBits(octets, lsbFirst=True), lsbFirst=True))
    print(octetsToBits(octets, lsbFirst=False))
    print(bitsToOctets(octetsToBits(octets, lsbFirst=False), lsbFirst=False))

    # NRZ <-> NRZI
    bitSeq = [1, 1, 0, 1, 1, 0, 0, 0]
    print(bitSeq)
    print(nrzToNrzi(bitSeq))
    print(nrziToNrz(nrzToNrzi(bitSeq)))
