import socket
import threading
import time
from generate_dummy_data import (
    generate_binary_sensor_data, generate_binary_airbrake_status,
    generate_binary_pms_data, generate_binary_fc_data, generate_binary_video_data
)
from packet import display_packet_info
#edit number 1
# Create a lock object to synchronize print statements
print_lock = threading.Lock()  # This ensures that only one thread prints at a time to avoid mixed-up output

# Function to send data using TCP for reliable transmission
def send_tcp_packet(packet, host='localhost', port=12345):
    """
    Sends a packet to the ground station via a TCP connection.
    TCP is reliable and ensures that data is delivered without errors.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))  # Establish a TCP connection to the host and port
        sock.sendall(packet)  # Send the entire packet over TCP
        with print_lock:
            print("\n--- Sending TCP Packet ---")
            display_packet_info(packet, "Sent TCP Packet")  # Display packet details
            print("--------------------------\n")


# Function to send data using UDP for faster transmission (like video data)
def send_udp_packet(packet, host='localhost', port=54321):
    """
    Sends a packet to the ground station via a UDP connection.
    UDP is faster but less reliable, making it good for video streaming.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(packet, (host, port))  # Send the packet using UDP
        with print_lock:
            print("\n--- Sending UDP Packet ---")
            display_packet_info(packet, "Sent UDP Packet")  # Display packet details what
            print("--------------------------\n")


# Function to receive TCP packets (sensor/control data)
def receive_tcp_data(host='localhost', port=12345):
    """
    Receives TCP packets and processes them.
    This function listens for incoming TCP connections and processes the packets received.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((host, port))  # Bind to the host and port to start listening for incoming connections
        server_sock.listen(1)  # Start listening for incoming TCP connections
        print(f"\nListening for TCP connections on {host}:{port}...\n")

        while True:
            conn, addr = server_sock.accept()  # Accept a new TCP connection from a client
            with conn:
                packet = conn.recv(1024)  # Receive up to 1024 bytes of data from the connection
                with print_lock:
                    print(f"\n--- Received TCP Packet from {addr} ---")
                    display_packet_info(packet, "Received TCP Packet")  # Display the packet details
                    print("------------------------------\n")


# Function to receive UDP packets (video data)
def receive_udp_data(host='localhost', port=54321):
    """
    Receives UDP packets and processes them.
    This function listens for incoming UDP packets and processes them.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((host, port))  # Bind to the host and port to start listening for UDP packets
        print(f"\nListening for UDP packets on {host}:{port}...\n")

        while True:
            packet, addr = sock.recvfrom(1024)  # Receive up to 1024 bytes of data from a UDP packet
            with print_lock:
                print(f"\n--- Received UDP Packet from {addr} ---")
                display_packet_info(packet, "Received UDP Packet")  # Display the packet details
                print("------------------------------\n")


# Function to run the simulation
def run_simulation():
    """
    Simulates sending and receiving TCP and UDP packets.
    This function starts the receivers and sends various data packets (sensor, control, video).
    """
    # Start threads to receive both TCP and UDP data
    tcp_receiver_thread = threading.Thread(target=receive_tcp_data)  # Thread to receive TCP data
    udp_receiver_thread = threading.Thread(target=receive_udp_data)  # Thread to receive UDP data

    tcp_receiver_thread.daemon = True  # Daemon threads will stop when the main program exits
    udp_receiver_thread.daemon = True

    tcp_receiver_thread.start()  # Start the TCP receiver thread
    udp_receiver_thread.start()  # Start the UDP receiver thread

    time.sleep(1)  # Give the receiver threads time to start before sending packets

    # Simulate sending different types of data
    for _ in range(3):  # Repeat the loop 3 times to send multiple sets of data packets
        # Sending sensor data over TCP
        sensor_packet, _ = generate_binary_sensor_data()  # Generate a sensor data packet
        send_tcp_packet(sensor_packet)  # Send the sensor data over TCP

        # Sending airbrake status over TCP
        airbrake_packet, _ = generate_binary_airbrake_status()  # Generate airbrake status data
        send_tcp_packet(airbrake_packet)  # Send the airbrake status over TCP

        # Sending power management data over TCP
        pms_packet, _ = generate_binary_pms_data()  # Generate power management system (PMS) data
        send_tcp_packet(pms_packet)  # Send the PMS data over TCP

        # Sending flight controller data over TCP
        fc_packet, _ = generate_binary_fc_data()  # Generate flight controller data
        send_tcp_packet(fc_packet)  # Send the flight controller data over TCP

        # Sending video data over UDP
        video_packet, _ = generate_binary_video_data()  # Generate video data
        send_udp_packet(video_packet)  # Send the video data over UDP

        time.sleep(3)  # Small delay between sending sets of data to simulate real-time communication


# The program starts here
if __name__ == '__main__':
    run_simulation()  # Start the simulation when the script is executed
