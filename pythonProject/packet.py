import struct  # Used to pack and unpack binary data

# Constants for start and end delimiters that mark the boundaries of a packet
START_DELIMITER = 0x7E  # Marks the beginning of the packet (1 byte)
END_DELIMITER = 0x7F  # Marks the end of the packet (1 byte)

def calculate_checksum(payload):
    """
    Calculates a simple checksum by summing all the bytes of the payload and returning the sum.
    The result is limited to 2 bytes using '& 0xFFFF' to ensure the value is always within
    the range of 0 to 65535 (the size of two bytes).
    """
    return sum(payload) & 0xFFFF  # Sum all bytes in the payload, restricted to 2 bytes

def parse_packet(packet):
    """
    Parses a packet and checks that the packet is valid by looking at the start delimiter,
    checking the checksum, and ensuring the end delimiter is correct.
    If successful, it returns the data type ID and the payload.
    Raises ValueError if the packet structure is invalid or if the checksum doesn't match.
    """
    try:
        # First, unpack the first 4 bytes of the packet:
        # '!BBH' means:
        # '!' = use network (big-endian) byte order
        # 'B' = 1 byte for the start delimiter
        # 'B' = 1 byte for the data type ID
        # 'H' = 2 bytes for the payload length
        start_delimiter, data_type_id, packet_length = struct.unpack('!BBH', packet[:4])

        # Check if the start delimiter is valid (should match the START_DELIMITER constant)
        if start_delimiter != START_DELIMITER:
            raise ValueError("Invalid start delimiter")

        # Create a format string for unpacking the payload and the checksum
        # 's' means string (or bytes in this case), 'H' is for 2 bytes of checksum
        payload_format = f'!{packet_length}sH'
        payload, checksum = struct.unpack(payload_format, packet[4:4 + packet_length + 2])

        # Calculate what the checksum should be and compare it with the received one
        calculated_checksum = calculate_checksum(payload)
        if checksum != calculated_checksum:
            raise ValueError("Checksum mismatch")  # Raise an error if checksums don't match

        # Ensure the packet ends with the correct end delimiter
        if packet[-1] != END_DELIMITER:
            raise ValueError("Invalid end delimiter")

        # If everything is valid, return the data type ID and the payload
        return data_type_id, payload

    except struct.error:
        # Raise an error if there was an issue unpacking the packet (wrong structure)
        raise ValueError("Invalid packet structure")

def create_packet(data_type_id, payload):
    """
    Creates a packet following the format:
    [Start Delimiter] [Data Type ID] [Packet Length] [Payload] [Checksum] [End Delimiter]
    - Start Delimiter: 1 byte
    - Data Type ID: 1 byte (indicates what kind of data is being sent)
    - Payload Length: 2 bytes (the size of the payload in bytes)
    - Payload: The actual data being sent
    - Checksum: 2 bytes (used for verifying the integrity of the payload)
    - End Delimiter: 1 byte
    """
    # Ensure the payload is not too large (the packet length can only hold 2 bytes)
    if len(payload) > 65535:  # 65535 is the maximum value for 2 bytes
        raise ValueError("Payload is too large")

    # Calculate the length of the payload (2 bytes)
    packet_length = len(payload)

    # Calculate the checksum for the payload
    checksum = calculate_checksum(payload)

    # Pack the fields together into a single packet:
    # '!BBH' = Start Delimiter (1 byte), Data Type ID (1 byte), Payload Length (2 bytes)
    # 's' = Payload (variable length), 'H' = Checksum (2 bytes)
    packet = struct.pack(f'!BBH{len(payload)}sH', START_DELIMITER, data_type_id, packet_length, payload, checksum)

    # Add the End Delimiter manually to the end of the packet
    packet += struct.pack('B', END_DELIMITER)

    return packet  # Return the fully formed packet (as a bytes object)

def display_packet_info(packet, data_label):
    """
    Displays the contents of a packet in a human-readable format, showing the different parts
    of the packet (start delimiter, data type ID, payload, checksum, end delimiter).
    If the packet structure is invalid, it prints an error message.
    """
    print(f"\n--- {data_label} ---")  # Label the output with the type of packet being shown
    try:
        # Parse the packet to extract its components (data type ID and payload)
        data_type_id, payload = parse_packet(packet)

        # Print out each part of the packet
        print(f"Packet Details for {data_label}:")
        print(f"  Start Delimiter: {hex(START_DELIMITER)} (Marks the beginning of the packet)")
        print(f"  Data Type ID: {hex(data_type_id)} (Indicates the type of data being sent)")
        print(f"  Payload Length: {len(payload)} bytes (Length of the data in the packet)")
        print(f"  Payload: {payload} (The actual data)")
        print(f"  Checksum: {calculate_checksum(payload)} (Used for verifying integrity)")
        print(f"  End Delimiter: {hex(END_DELIMITER)} (Marks the end of the packet)")
    except ValueError as e:
        # If there's an issue parsing the packet, print an error message
        print(f"Error parsing packet: {e}")
