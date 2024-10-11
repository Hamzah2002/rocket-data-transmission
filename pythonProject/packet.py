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
        # Unpack fixed fields: Start Delimiter (1 byte), Data Type ID (1 byte), Payload Length (2 bytes)
        start_delimiter, data_type_id, packet_length = struct.unpack('!BBH', packet[:4])

        # Check that start delimiter is correct
        if start_delimiter != START_DELIMITER:
            raise ValueError("Invalid start delimiter")

        # Extract payload based on the packet length
        payload_format = f'!{packet_length}sH'  # Payload length and checksum
        payload, checksum = struct.unpack(payload_format, packet[4: 4 + packet_length + 2])

        # Verify the checksum
        calculated_checksum = calculate_checksum(payload)
        if checksum != calculated_checksum:
            raise ValueError("Checksum mismatch")

        # Check that the packet ends with the correct end delimiter
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

    # Check if the payload is too large (since the length field can only hold 2 bytes)
    if len(payload) > 65535:  # Maximum value for 2-byte length is 65535
        raise ValueError("Payload is too large")  # Raise an error if the payload is too big

    # Get the length of the payload in bytes (2-byte value)
    packet_length = len(payload)

    # Calculate checksum for error detection: this will be used to verify data integrity
    checksum = calculate_checksum(payload)

    # Pack the packet fields together:
    # '!BBH{len(payload)}sH' means:
    # - '!' indicates network byte order (big-endian)
    # - 'B' is for 1 byte (Start Delimiter)
    # - 'B' is for 1 byte (Data Type ID)
    # - 'H' is for 2 bytes (Packet Length)
    # - '{len(payload)}s' is for the payload (of dynamic size)
    # - 'H' is for 2 bytes (Checksum)
    packet = struct.pack(
        f'!BBH{len(payload)}sH',  # Defines the packet format
        START_DELIMITER,  # Start delimiter, 1 byte
        data_type_id,  # Data Type ID, 1 byte
        packet_length,  # Payload length, 2 bytes
        payload,  # Payload data (variable length)
        checksum  # Checksum (for error detection), 2 bytes
    )

    # Add the End Delimiter manually after packing the rest of the packet
    packet += struct.pack('B', END_DELIMITER)  # End delimiter, 1 byte

    return packet  # Return the complete packet as a bytes object

# Example usage (using a dummy payload):
payload = b'\x01\x02\x03'  # Example payload (3 bytes of data)
packet = create_packet(0x01, payload)  # Create a packet with Data Type ID 0x01
print(packet)  # This would give you the packet in byte format
