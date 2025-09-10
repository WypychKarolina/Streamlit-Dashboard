# 📈 Live Stock Streaming Dashboard

A real-time dashboard for fetching and visualizing **stock market data** from Yahoo! Finance.  
The project consists of two parts:
- **Server** – fetches stock data, calculates a moving average, and streams it via a socket.
- **Client (Dashboard)** – a Streamlit app that receives the data and displays it in real-time.

---

## 🛠️ Technologies Used
- streamlit  
- socket  
- streamlit-autorefresh  
- threading  
- queue  
- yfinance  

---

## 🚀 How to Run

### Start the server
```bash
python server.py
```
###Start the client (dashboard)
```bash
streamlit run client.py
