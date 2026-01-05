# Private Local Financial Analyst

A local AI-powered financial analysis tool built with Streamlit, utilizing Ollama models for intelligent stock analysis without relying on external APIs. Includes integrated tracing with Phoenix for monitoring AI model performance.

## Functionality

The Private Local Financial Analyst allows users to analyze stock performance by entering a stock ticker symbol. It provides:

- **Real-time Financial Data**: Fetches current stock metrics including price, market cap, P/E ratio, and 52-week high/low from Yahoo Finance.
- **Historical Price Charts**: Displays a 30-day price trend line chart.
- **AI-Powered Analysis**: Generates professional financial analysis using local Ollama models (Gemma3, DeepSeek-R1, Llama3.1).
- **Model Selection**: Choose between different Ollama models optimized for summarization or deep analysis.
- **Streaming Responses**: Real-time streaming of AI analysis for better user experience.
- **Integrated Tracing**: Automatic tracing of AI model interactions using Phoenix for performance monitoring and debugging.

Key features include executive summaries, price momentum analysis, valuation insights, and investment outlook assessments. All AI interactions are traced locally for privacy and analysis.

## Design

The application follows a clean, user-friendly design with:

- **Sidebar Configuration**: Easy input for stock ticker and model selection.
- **Responsive Layout**: Wide layout with metric cards and charts.
- **Error Handling**: Graceful handling of data fetching errors and Ollama connection issues.
- **Progressive Disclosure**: Analysis only appears after user interaction.
- **Visual Feedback**: Spinners and placeholders during AI processing.
- **Tracing Dashboard**: Link to local Phoenix dashboard for monitoring AI performance.

The UI is built with Streamlit components, ensuring accessibility and simplicity.

## Implementation

### Architecture

- **Frontend**: Streamlit web app for user interface.
- **Data Source**: Yahoo Finance API via `yfinance` library.
- **AI Engine**: Local Ollama models integrated through LangChain's `OllamaLLM`.
- **Tracing**: Phoenix with OpenInference instrumentation for LangChain tracing.
- **Data Processing**: Pandas for data manipulation and visualization.

### Key Components

1. **Data Fetching**: `get_financial_data()` function retrieves stock info and history.
2. **Prompt Engineering**: Model-specific prompts optimized for different AI capabilities (Gemma for concise summaries, DeepSeek for detailed reasoning).
3. **Streaming Output**: Real-time text streaming for AI responses.
4. **Tracing Integration**: Automatic capture of model interactions for analysis and debugging.
5. **Error Management**: Try-except blocks for robust error handling.

### Dependencies

- `streamlit`: Web app framework
- `yfinance`: Financial data API
- `pandas`: Data manipulation
- `langchain-ollama`: Ollama integration for LangChain
- `arize-phoenix`: Local tracing server
- `openinference-instrumentation-langchain`: LangChain tracing instrumentation

### Model Optimization

- **Gemma3**: Used for bullet-point executive summaries focusing on key metrics.
- **DeepSeek-R1**: Employed for in-depth analysis with reasoning and risk assessment.
- **Fallback Models**: Llama3.1 for general analysis.

## How to Run

### Prerequisites

1. **Python 3.12+**: Ensure Python is installed.
2. **Ollama**: Install Ollama from [ollama.ai](https://ollama.ai) and have it running.
3. **Models**: Pull required models:
   ```bash
   ollama pull gemma3:1b
   ollama pull deepseek-r1:7b
   ollama pull deepseek-r1:1.5b
   ollama pull llama3.1
   ```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-financial-agent.git
   cd ai-financial-agent
   ```

2. Install dependencies using uv (recommended):
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Ensure Ollama is running in the background.

2. Run the app:
   ```bash
   uv run streamlit run main.py
   ```

   Or with pip:
   ```bash
   streamlit run main.py
   ```

3. Open the provided local URL in your browser (typically http://localhost:8501).

4. Enter a stock ticker (e.g., NVDA) in the sidebar, select a model, and click "Generate Analysis".

5. Monitor AI performance via the tracing dashboard at http://localhost:6006.

### Troubleshooting

- **Ollama Connection Error**: Ensure Ollama is running (`ollama serve`) and the selected model is pulled.
- **No Data Found**: Verify the stock ticker is correct and available on Yahoo Finance.
- **Tracing Issues**: Phoenix should launch automatically; check http://localhost:6006 for the dashboard.
- **Import Errors**: Confirm all dependencies are installed.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.