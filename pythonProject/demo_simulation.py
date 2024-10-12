import socket
import time
from generate_dummy_data import (
    generate_binary_sensor_data, generate_binary_airbrake_status,
    generate_binary_pms_data, generate_binary_fc_data, generate_binary_video_data
)
from packet import display_packet_info
import sys
import threading

# Create a lock object to synchronize print statements
print_lock = threading.Lock()  # This ensures that only one thread prints at a time to avoid mixed-up output

def send_packet(packet, host='localhost', port=12345):
    """
    Sends a packet to the ground station via a simulated network connection.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Create a UDP socket and send the packet to the specified host and port
        sock.sendto(packet, (host, port))

        # Lock the print statements so that only one thread prints at a time
        with print_lock:
            sys.stdout.flush()  # Ensure that any previous output is fully printed before starting new print
            print("\n--- Sending Packet ---")
            display_packet_info(packet, "Sent Packet")  # Display details about the sent packet
            print("----------------------\n")
            sys.stdout.flush()  # Flush output to ensure no overlap with other threads

def receive_packet(host='localhost', port=12345):
    """
    Receives packets sent to the specified port, simulates a ground station receiving data.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Bind the socket to the given host and port to listen for incoming packets
        sock.bind((host, port))
        print(f"\nListening on {host}:{port}...\n")  # Notify that the program is listening for packets

        while True:
            # Receive a packet (max size 1024 bytes) and get the address of the sender
            packet, addr = sock.recvfrom(1024)

            # Lock print output so only one thread prints at a time
            with print_lock:
                print(f"\n--- Received Packet from {addr} ---")  # Show where the packet came from
                display_packet_info(packet, "Received Packet")  # Display details of the received packet
                print("------------------------------\n")
                sys.stdout.flush()  # Ensure that all output is printed immediately

def run_simulation():
    """
    Simulates the full process of generating, sending, and receiving packets.
    """
    # Start a separate thread to receive packets (like a simulated ground station)
    receiver_thread = threading.Thread(target=receive_packet)
    receiver_thread.daemon = True  # This ensures the thread stops when the main program exits
    receiver_thread.start()  # Start the receiver thread

    time.sleep(1)  # Give the receiver thread a little time to start before sending packets

    # Simulate sending different types of data packets a few times
    for _ in range(3):  # Run the loop 3 times to show multiple sets of data packets being sent
        sensor_packet, sensor_label = generate_binary_sensor_data()  # Generate sensor data packet
        send_packet(sensor_packet)  # Send the sensor data packet
        time.sleep(1)  # Delay to allow clear printing of the previous packet

        airbrake_packet, airbrake_label = generate_binary_airbrake_status()  # Generate airbrake status packet
        send_packet(airbrake_packet)  # Send the airbrake status packet
        time.sleep(1)  # Delay to prevent print overlap

        pms_packet, pms_label = generate_binary_pms_data()  # Generate power management system packet
        send_packet(pms_packet)  # Send the power management system packet
        time.sleep(1)  # Ensure output clarity

        fc_packet, fc_label = generate_binary_fc_data()  # Generate flight controller data packet
        send_packet(fc_packet)  # Send the flight controller data packet
        time.sleep(1)  # Space out the packet printing

        video_packet, video_label = generate_binary_video_data()  # Generate video data packet
        send_packet(video_packet)  # Send the video data packet
        time.sleep(3)  # Slightly longer delay to simulate real-time transmission

if __name__ == '__main__':
    run_simulation()  # Start the simulation when the script is executed
