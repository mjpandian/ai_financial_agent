import streamlit as st
import yfinance as yf
import pandas as pd
from langchain_ollama import OllamaLLM
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="Local AI Financial Analyst", 
    page_icon="📈", 
    layout="wide"
)

# --- App Title ---
st.title("📈 Local Financial Analyst")
st.markdown("Analyze stocks locally using **Ollama** models like **Gemma 3** and **DeepSeek-R1**.")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Settings")
    ticker = st.text_input("Enter Stock Ticker", value="NVDA").upper()
    model_name = st.selectbox(
        "Select Model", 
        ["gemma3:1b", "deepseek-r1:7b", "deepseek-r1:1.5b", "llama3.1"], 
        index=0
    )
    analyze_btn = st.button("Generate Analysis")
    
    st.divider()
    st.info(f"💡 **Tip:** Ensure Ollama is running and you have run `ollama pull {model_name}` in your terminal.")

# --- Helper Functions ---
def get_financial_data(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        
        # Fetch 1 month of history for the chart and data snippet
        hist = stock.history(period="1mo")
        
        if hist.empty:
            st.error("No data found for this ticker.")
            return None, None

        metrics = {
            "Name": info.get('longName', 'N/A'),
            "Price": info.get('currentPrice', 0.0),
            "Market Cap": info.get('marketCap', 0),
            "PE Ratio": info.get('trailingPE', 'N/A'),
            "52W High": info.get('fiftyTwoWeekHigh', 'N/A'),
            "52W Low": info.get('fiftyTwoWeekLow', 'N/A'),
            "Currency": info.get('currency', 'USD'),
            "History_Snippet": hist['Close'].tail(10).to_string()
        }
        return metrics, hist
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None, None

# --- Main App Logic ---
if analyze_btn:
    data, history = get_financial_data(ticker)
    
    if data:
        # 1. Visual Dashboard Section
        st.header(f"Financial Overview: {data['Name']} ({ticker})")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Price", f"{data['Price']} {data['Currency']}")
        col2.metric("Market Cap", f"{data['Market Cap']:,}")
        col3.metric("P/E Ratio", f"{data['PE Ratio']}")
        col4.metric("52W High", f"{data['52W High']}")

        # Display Historical Chart
        st.subheader("Price Trend (Last 30 Days)")
        st.line_chart(history['Close'])

        # 2. AI Analysis Section
        st.divider()
        st.subheader(f"🤖 AI Analysis ({model_name})")

        # Optimized Prompt Logic
        if "gemma" in model_name.lower():
            # Prompt optimized for Gemma's summarization style
            prompt = f"""
            You are a professional financial editor. Summarize the following data for {ticker} ({data['Name']}).
            
            KEY METRICS:
            - Price: {data['Price']} {data['Currency']}
            - P/E Ratio: {data['PE Ratio']}
            - 52W Range: {data['52W Low']} - {data['52W High']}
            
            RECENT PRICE HISTORY (Last 10 Days):
            {data['History_Snippet']}
            
            TASK:
            Provide a high-level Executive Summary using 'Bullet-Point' format.
            Address:
            1. Price Momentum: (Is it trending up or down based on history?)
            2. Valuation: (Is the P/E ratio attractive for this sector?)
            3. Outlook: (Neutral, Bullish, or Bearish?)
            Keep it professional, data-driven, and extremely concise.
            """
        else:
            # Prompt optimized for DeepSeek's reasoning/analytical style
            prompt = f"""
            You are a senior equity researcher. Perform a deep-dive analysis on {ticker} ({data['Name']}).
            
            DATA:
            {data}
            
            TASK:
            1. Analyze the current price relative to the 52-week high/low.
            2. Evaluate the volatility based on recent price history.
            3. Identify potential risks or opportunities for investors.
            Provide a detailed reasoning-based response.
            """

        # Execution with Streaming
        try:
            llm = OllamaLLM(model=model_name)
            
            with st.spinner(f"Requesting analysis from {model_name}..."):
                # Create a placeholder for the streaming text
                response_placeholder = st.empty()
                full_response = ""
                
                # Stream the output for a better user experience
                for chunk in llm.stream(prompt):
                    full_response += chunk
                    response_placeholder.markdown(full_response)
                    
        except Exception as e:
            st.error(f"Ollama Connection Error: {e}")
            st.warning("Make sure the Ollama server is running (check your taskbar or run 'ollama serve').")

else:
    st.info("👈 Enter a stock ticker in the sidebar and click 'Generate Analysis' to see the magic.")