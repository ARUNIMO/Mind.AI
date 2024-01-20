import streamlit as st
import socket
import threading

# Function to handle receiving messages
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            st.write(message)
        except Exception as e:
            st.error(f"Error receiving message: {e}")
            break

# Function to handle sending messages
def send_message(client_socket, message):
    try:
        client_socket.send(message.encode('utf-8'))
    except Exception as e:
        st.error(f"Error sending message: {e}")

# Main Streamlit app
def main():
    st.title("Chat Application")

    # Input for user's name
    user_name = st.text_input("Enter your name:", key="user_name")

    # Connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('localhost', 12345))
    except Exception as e:
        st.error(f"Error connecting to server: {e}")
        return

    # Send the user's name to the server
    client.send(user_name.encode('utf-8'))

    # Start a thread for receiving messages
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    # Text input for sending messages
    message_input = st.text_input("Type your message:")
    if st.button("Send"):
        if message_input:
            send_message(client, f'{user_name}: {message_input}')

if __name__ == "__main__":
    main()
