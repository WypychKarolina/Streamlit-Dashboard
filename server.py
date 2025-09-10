import yfinance as yf
import socket
import time
from statistics import mean

HOST = "localhost"
PORT = 9999
SYMBOL = "AAPL"
MOVING_AVG_WINDOW = 5
FETCH_INTERVAL_SECONDS = 20 # how often to fetch data (in seconds)

def get_latest_price():
    """
    Downloads the latest stock closing price for the given symbol.
    """
    data = yf.download(tickers=SYMBOL, period="1d", interval="1m") #data from one day, 1 minute interval
    if data.empty:
        raise ValueError("No data fetched for symbol: {}".format(SYMBOL))
    return data['Close']['AAPL'].values[-1] #last closing price

def start_socket_server():
    """
    Starts a TCP socket server that sends stock price and moving average data.
    """
    print(f"Starting socket server on {HOST}:{PORT}...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a TCP socket
    server_socket.bind((HOST, PORT)) # bind to the host and port
    server_socket.listen(1) # listen for 1 incoming connection
    print("Waiting for a client to connect...")

    client_socket, address = server_socket.accept() # accept the connection
    print(f"Client connected from {address}")

    price_history = []
    
    try:
        while True:
            try:
                price = get_latest_price()
                print('price', price)
                price_history.append(price)
                print('price_history', price_history)
                if len(price_history) > MOVING_AVG_WINDOW:
                    price_history.pop(0)
                moving_avg = mean(price_history)

                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                message = f"{timestamp}, PRICE: {price:.2f}, MA_{MOVING_AVG_WINDOW}: {moving_avg:.2f}\n"
                print(f"Sending: {message.strip()}")
                client_socket.send(message.encode('utf-8'))

            except Exception as e:
                print(f"Error fetching or sending data: {e}")

            time.sleep(FETCH_INTERVAL_SECONDS) # wait before fetching the next price

    except KeyboardInterrupt:
        print("Shutting down server.") #by pressing Ctrl+C
    finally:
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    start_socket_server()
    #print(get_latest_price())
