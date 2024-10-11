import socket
from generate_dummy_data import generate_binary_sensor_data, generate_binary_airbrake_status, generate_binary_pms_data

def send_packet(packet, host='localhost', port=12345):
    """Sends a packet to the ground station via a simulated network connection."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(packet, (host, port))  # Send the packet to the specified host and port
        print(f"Packet sent: {packet}")  # Print the packet that was sent for debugging purposes

# Simulating sending different types of data
if __name__ == '__main__':
    # Example of sending different types of generated binary data packets
    sensor_packet = generate_binary_sensor_data()  # Generate a binary packet for sensor data
    send_packet(sensor_packet)  # Send the sensor data packet

    airbrake_packet = generate_binary_airbrake_status()  # Generate a binary packet for airbrake status
    send_packet(airbrake_packet)  # Send the airbrake status packet

    pms_packet = generate_binary_pms_data()  # Generate a binary packet for power management data
    send_packet(pms_packet)  # Send the power management data packet
