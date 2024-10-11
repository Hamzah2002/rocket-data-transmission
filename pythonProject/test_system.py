import struct

START_DELIMITER = 0x7E  # A unique byte to mark the start of the packet
END_DELIMITER = 0x7F  # A unique byte to mark the end of the packet


def calculate_checksum(payload):
    """
    Calculates a simple checksum by summing all the bytes of the payload and returning the sum.
    """
    return sum(payload) & 0xFFFF  # Return checksum as 2-byte integer


def create_packet(data_type_id, payload):
    """
    Creates a packet according to the specified format.
    Packet structure:
    [Start Delimiter] [Data Type ID] [Packet Length] [Payload] [Checksum] [End Delimiter]
    """
    # Ensure payload is within reasonable length limits, adjust as necessary
    if len(payload) > 65535:
        raise ValueError("Payload is too large")  # Ensure it fits within 2 bytes for the length field

    packet_length = len(payload)  # 2-byte length of the payload
    checksum = calculate_checksum(payload)  # Calculate checksum for error detection

    # Pack the packet: Start, Data Type ID, Length, Payload, Checksum
    packet = struct.pack(
        f'!BBH{len(payload)}sH',  # Packet structure without the end delimiter
        START_DELIMITER,  # Start Delimiter (1 byte)
        data_type_id,  # Data Type ID (1 byte)
        packet_length,  # Packet Length (2 bytes)
        payload,  # Payload (variable length)
        checksum  # Checksum (2 bytes)
    )

    # Add the End Delimiter manually after packing
    packet += struct.pack('B', END_DELIMITER)

    return packet

# Example usage (using a dummy payload):
payload = b'\x01\x02\x03'  # Example payload
packet = create_packet(0x01, payload)
print(packet)  # This would give you the packet in byte format
