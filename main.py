import streamlit as st
import yfinance as yf
import pandas as pd
from langchain_ollama import OllamaLLM
from datetime import datetime

# --- TRACING SETUP (MUST BE AT THE TOP) ---
import phoenix as px
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor

if "tracing_initialized" not in st.session_state:
    # 1. Start the local Phoenix server
    px.launch_app() 
    # 2. Register the local tracer provider
    tracer_provider = register(project_name="local-financial-analyst")
    # 3. Instrument LangChain to use this provider
    LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
    st.session_state.tracing_initialized = True

# --- Page Config ---
st.set_page_config(page_title="Offline AI Analyst", page_icon="📈", layout="wide")

# --- UI Header ---
st.title("📈 Private Local Financial Analyst")
st.markdown(f"**Tracing Dashboard:** [http://localhost:6006](http://localhost:6006)")

# --- Sidebar ---
with st.sidebar:
    st.header("Configuration")
    ticker = st.text_input("Enter Stock Ticker", value="NVDA").upper()
    model_name = st.selectbox(
        "Select Model", 
        ["gemma3:1b", "deepseek-r1:7b", "deepseek-r1:1.5b", "llama3.1"], 
        index=0
    )
    analyze_btn = st.button("Generate Analysis")
    st.info(f"Using local model: {model_name}")

# --- Data Fetching ---
def get_financial_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        hist = stock.history(period="1mo")
        
        metrics = {
            "Name": info.get('longName', 'N/A'),
            "Price": info.get('currentPrice', 0.0),
            "PE": info.get('trailingPE', 'N/A'),
            "52W_High": info.get('fiftyTwoWeekHigh', 'N/A'),
            "History": hist['Close'].tail(5).to_string()
        }
        return metrics, hist
    except Exception as e:
        st.error(f"Data Error: {e}")
        return None, None

# --- Main App Execution ---
if analyze_btn:
    data, history = get_financial_data(ticker)
    
    if data:
        # Visuals
        col1, col2, col3 = st.columns(3)
        col1.metric("Stock", data["Name"])
        col2.metric("Current Price", f"${data['Price']}")
        col3.metric("P/E Ratio", data["PE"])
        st.line_chart(history['Close'])
        
        st.divider()
        st.subheader("🤖 AI Analysis")

        # Prompt
        prompt = f"""
        Summarize the financial health of {ticker} based on:
        Price: {data['Price']}
        P/E: {data['PE']}
        Recent Trend: {data['History']}
        Provide a concise bullish or bearish outlook.
        """

        # Model Execution (Automatically captured by Phoenix)
        try:
            llm = OllamaLLM(model=model_name)
            response_container = st.empty()
            full_text = ""
            
            # Streaming works with tracing
            for chunk in llm.stream(prompt):
                full_text += chunk
                response_container.markdown(full_text)
                
            st.success("Analysis complete. Trace sent to Local Phoenix.")
        except Exception as e:
            st.error(f"Model Error: {e}. Is Ollama running?")