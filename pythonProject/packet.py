import struct

# Constants for start and end delimiters that mark the boundaries of a packet
START_DELIMITER = 0x7E  # Marks the beginning of the packet (1 byte)
END_DELIMITER = 0x7F  # Marks the end of the packet (1 byte)

def calculate_checksum(payload):
    """
    Calculates a simple checksum by summing all the bytes of the payload and returning the sum.
    The result is limited to 2 bytes using '& 0xFFFF'.
    """
    return sum(payload) & 0xFFFF  # Sum of payload bytes, restricted to 2 bytes

def parse_packet(packet):
    """
    Parses a packet and validates its structure, checksum, and delimiters.
    Returns (data_type_id, payload) if successful.
    Raises ValueError if packet structure is invalid or checksum fails.
    """
    try:
        start_delimiter, data_type_id, packet_length = struct.unpack('!BBH', packet[:4])

        if start_delimiter != START_DELIMITER:
            raise ValueError("Invalid start delimiter")

        payload_format = f'!{packet_length}sH'
        payload, checksum = struct.unpack(payload_format, packet[4:4 + packet_length + 2])

        calculated_checksum = calculate_checksum(payload)
        if checksum != calculated_checksum:
            raise ValueError("Checksum mismatch")

        if packet[-1] != END_DELIMITER:
            raise ValueError("Invalid end delimiter")

        return data_type_id, payload  # Return the data type ID and the payload

    except struct.error:
        raise ValueError("Invalid packet structure")

def create_packet(data_type_id, payload):
    """
    Creates a packet following the format:
    [Start Delimiter] [Data Type ID] [Packet Length] [Payload] [Checksum] [End Delimiter]
    """
    if len(payload) > 65535:
        raise ValueError("Payload is too large")

    packet_length = len(payload)
    checksum = calculate_checksum(payload)

    packet = struct.pack(f'!BBH{len(payload)}sH', START_DELIMITER, data_type_id, packet_length, payload, checksum)
    packet += struct.pack('B', END_DELIMITER)

    return packet

def display_packet_info(packet, data_label):
    """
    Displays the contents of the packet in a human-readable format along with additional explanation.
    """
    print(f"\n--- {data_label} ---")
    try:
        data_type_id, payload = parse_packet(packet)
        print(f"Packet Details for {data_label}:")
        print(f"  Start Delimiter: {hex(START_DELIMITER)}")
        print(f"  Data Type ID: {hex(data_type_id)}")
        print(f"  Payload Length: {len(payload)} bytes")
        print(f"  Payload: {payload}")
        print(f"  Checksum: {calculate_checksum(payload)}")
        print(f"  End Delimiter: {hex(END_DELIMITER)}")
    except ValueError as e:
        print(f"Error parsing packet: {e}")
