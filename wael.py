import streamlit as st
import time
import atexit

# Mock Serial class for cloud deployment
class MockSerial:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate

    def write(self, command):
        st.write(f"Mock command to {self.port}: {command}")

    def close(self):
        st.write(f"Closing mock connection to {self.port}")

# Function to initialize the Arduino board
def initialize_board(port):
    try:
        if st.secrets["environment"] == "cloud":
            arduino = MockSerial(port, 9600)
        else:
            import serial
            arduino = serial.Serial(port, 9600)
            time.sleep(2)  # Wait for Arduino to initialize
        
        st.session_state['board_initialized'] = True
        st.session_state['arduino'] = arduino
        st.success(f'Arduino connected on port {port}')
    except Exception as e:
        st.error(f'Could not open {port}: {e}')

# Streamlit App
st.title('Arduino Control with Streamlit')

# Input fields for port and pin
port = st.text_input('Enter the Arduino port (e.g., COM3 or /dev/ttyACM0):', value='COM3')

# Initialize board button
if st.button('Initialize Arduino'):
    initialize_board(port)

# Check if the board is initialized
if 'board_initialized' in st.session_state and st.session_state['board_initialized']:
    arduino = st.session_state['arduino']
    
    if st.button('Turn On LED with 10-minute Delay'):
        st.write('Scheduling LED to turn on after 10 minutes...')
        arduino.write('TURN_ON\n'.encode())
        st.write('LED will turn on in 10 minutes.')

    if st.button('Turn Off LED with 10-minute Delay'):
        st.write('Scheduling LED to turn off after 10 minutes...')
        arduino.write('TURN_OFF\n'.encode())
        st.write('LED will turn off in 10 minutes.')

# Ensure proper shutdown of the Arduino board
def cleanup():
    if 'arduino' in st.session_state:
        st.session_state['arduino'].close()

atexit.register(cleanup)
