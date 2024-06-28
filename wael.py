import streamlit as st
import serial
import time
import atexit

# Function to initialize the Arduino board
def initialize_board(port):
    try:
        arduino = serial.Serial(port, 9600)
        time.sleep(2)  # Wait for Arduino to initialize
        st.session_state['board_initialized'] = True
        st.session_state['arduino'] = arduino
        st.success(f'Arduino connected on port {port}')
    except serial.SerialException as e:
        st.error(f'Could not open {port}: {e}')
    except Exception as e:
        st.error(f'An unexpected error occurred: {e}')

# Streamlit App
st.title(' T83 NYS conference')

# Input fields for port and pin
port = st.text_input('Enter the Arduino port (e.g., COM3 or /dev/ttyACM0):', value='COM3')
pin = st.number_input('Enter the Arduino pin number to control:', min_value=0, max_value=13, value=13)

# Initialize board button
if st.button('Initialize Arduino'):
    initialize_board(port)

# Check if the board is initialized
if 'board_initialized' in st.session_state and st.session_state['board_initialized']:
    arduino = st.session_state['arduino']
    
    if st.button('Turn On LED'):
        st.write('Turning on the LED...')
        arduino.write(f'{pin},HIGH\n'.encode())
        time.sleep(1)  # Keep the LED on for 1 second
        st.write('LED is now on.')

    if st.button('Turn Off LED'):
        st.write('Turning off the LED...')
        arduino.write(f'{pin},LOW\n'.encode())
        st.write('LED is now off.')

# Ensure proper shutdown of the Arduino board
def cleanup():
    if 'arduino' in st.session_state:
        st.session_state['arduino'].close()

atexit.register(cleanup)
