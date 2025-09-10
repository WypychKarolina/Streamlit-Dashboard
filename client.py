import streamlit as st
from streamlit_autorefresh import st_autorefresh
import socket
import threading
import queue

st.set_page_config(page_title="Live Stock Dashboard", layout="wide")
st.title("📈 Live Stock Price & Moving Average")
st_autorefresh(interval=5000, limit=None, key="datarefresh")

# Initialize session state
if "received_data" not in st.session_state:
    st.session_state.received_data = []
if "socket_thread_started" not in st.session_state:
    st.session_state.socket_thread_started = False

# Create a thread-safe queue
if "data_queue" not in st.session_state:
    st.session_state.data_queue = queue.Queue()

def read_from_socket(host: str, port: int, q: queue.Queue):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"[THREAD] Connected to socket at {host}:{port}")
            while True:
                data = s.recv(1024).decode("utf-8") #bytes to string
                if data:
                    for line in data.strip().splitlines():
                        print(f"[THREAD] Received: {line}")
                        q.put(line)  # push to queue
    except Exception as e:
        print(f"[THREAD] Socket error: {e}")

# Start thread
if not st.session_state.socket_thread_started:
    thread = threading.Thread(
        target=read_from_socket,
        args=("localhost", 9999, st.session_state.data_queue)
    )
    thread.daemon = True
    thread.start()
    st.session_state.socket_thread_started = True

# Pull from queue to received_data
while not st.session_state.data_queue.empty():
    line = st.session_state.data_queue.get()
    st.session_state.received_data.append(line)
    if len(st.session_state.received_data) > 20:
        st.session_state.received_data.pop(0)

# Display in UI
st.markdown("### Latest Prices")
if st.session_state.received_data:
    st.table([line.split(",") for line in st.session_state.received_data])
else:
    st.write("Waiting for data...")
