import socket
from packet import parse_packet  # Import the parsing function from packet.py


def receive_packet(host='localhost', port=12345):
    """Receives packets and parses them."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((host, port))  # Bind to the specified host and port
        print(f"Listening on {host}:{port}...")

        while True:
            # Receive a packet (up to 1024 bytes) and get the sender's address
            packet, addr = sock.recvfrom(1024)
            try:
                # Parse the packet using the parse_packet function
                data_type_id, payload = parse_packet(packet)

                # Print the received data type ID and payload
                print(f"Received packet from {addr}: Data Type ID {data_type_id}, Payload {payload}")
            except ValueError as e:
                # Handle errors such as invalid packet structure or checksum mismatch
                print(f"Error: {e}")


if __name__ == '__main__':
    receive_packet()  # Start the packet receiver
