import random
from packet import create_packet


def generate_binary_sensor_data():
    """
    Simulates sensor data as a binary string.
    For example, temperature could be represented as binary data.
    """
    # Simulate a random sensor reading between 15.0 and 25.0 (e.g., temperature in Celsius)
    sensor_value = random.uniform(15.0, 25.0)

    # Convert the sensor value into an integer and then to a 32-bit binary string.
    # We multiply by 100 to avoid dealing with floating-point numbers in binary.
    sensor_binary = format(int(sensor_value * 100), '032b')

    # Convert the 32-bit binary string into 4 bytes using the 'int.to_bytes' method.
    payload = int(sensor_binary, 2).to_bytes(4, byteorder='big')

    # Create a packet using the create_packet function. The data type ID for sensor data is 0x01.
    return create_packet(0x01, payload), f"Sensor Data (Temperature: {sensor_value:.2f} °C)"


def generate_binary_airbrake_status():
    """
    Simulates airbrake status as a binary string.
    Airbrake status is represented as a percentage (0-100), which can be converted to binary.
    """
    # Simulate airbrake status as a random percentage (0-100)
    airbrake_status = random.randint(0, 100)

    # Convert the percentage to an 8-bit binary string (since it's a small number)
    airbrake_binary = format(airbrake_status, '08b')

    # Convert the 8-bit binary string to 1 byte
    payload = int(airbrake_binary, 2).to_bytes(1, byteorder='big')

    # Create a packet with data type ID 0x02 (Airbrake Status)
    return create_packet(0x02, payload), f"Airbrake Status (Deployed: {airbrake_status}%)"


def generate_binary_pms_data():
    """
    Simulates power management system (PMS) data as binary.
    Battery voltage is represented as a 16-bit value in binary.
    """
    # Simulate battery voltage in millivolts (between 3000 and 4200 mV)
    voltage = random.randint(3000, 4200)

    # Convert the voltage to a 16-bit binary string
    voltage_binary = format(voltage, '016b')

    # Convert the 16-bit binary string to 2 bytes
    payload = int(voltage_binary, 2).to_bytes(2, byteorder='big')

    # Create a packet with data type ID 0x03 (PMS Data)
    return create_packet(0x03, payload), f"PMS Data (Battery Voltage: {voltage} mV)"


def generate_binary_fc_data():
    """
    Simulates flight controller data as binary.
    Altitude and velocity are represented as 32-bit binary values.
    """
    # Simulate altitude (0 to 10,000 meters)
    altitude = random.uniform(0, 10000)

    # Simulate velocity (0 to 300 meters/second)
    velocity = random.uniform(0, 300)

    # Convert altitude and velocity to 32-bit binary strings, scaling the values by 100 for precision
    altitude_binary = format(int(altitude * 100), '032b')
    velocity_binary = format(int(velocity * 100), '032b')

    # Convert both 32-bit binary strings to bytes and concatenate them to form the payload
    payload = (int(altitude_binary, 2).to_bytes(4, byteorder='big') +
               int(velocity_binary, 2).to_bytes(4, byteorder='big'))

    # Create a packet with data type ID 0x04 (Flight Controller Data)
    return create_packet(0x04, payload), f"Flight Controller Data (Altitude: {altitude:.2f} m, Velocity: {velocity:.2f} m/s)"


def generate_binary_video_data():
    """
    Simulates video data as binary.
    Video data could be represented as a sequence of binary bits (dummy video frame).
    """
    # Generate 10 random bytes of video data, each byte is represented as an 8-bit binary value
    video_binary = ''.join(format(random.randint(0, 255), '08b') for _ in range(10))

    # Convert the binary string to 10 bytes
    payload = int(video_binary, 2).to_bytes(10, byteorder='big')

    # Create a packet with data type ID 0x05 (Video Data)
    return create_packet(0x05, payload), "Video Data (Dummy 10-byte video frame)"
