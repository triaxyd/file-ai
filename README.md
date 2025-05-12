# This guide will help you set up and run the PDF AI.
## Prerequisites
    
    Python 3.9–3.13

    pip installed

    Google Gemini API key: https://aistudio.google.com/app/apikey

    LlamaCloud API key: https://cloud.llamaindex.ai/

## Setup
1. **Clone the repository**
<pre> git clone https://github.com/triaxyd/file-ai.git </pre>

2. **Create a virtual environment**
<pre>
python -m venv venv
source venv/bin/activate
</pre>

3. **Create a .env file**
<pre>
GOOGLE_API_KEY=your-google-api-key
LLAMA_CLOUD_API_KEY=your-llama-cloud-api-key
</pre>

4. **Install dependencies**
<pre>
pip install -r requirements.txt
</pre>

5. **Run the application**
<pre>
streamlit run app.py
</pre>


## Project Structure
```
file-ai/    
├── .env    # API keys (must be created)
├── venv/   # Virtual environment directory
├── requirements.txt    # Python dependencies
├── README.md   # README file
├── .gitignore  # Git ignore file
├── agents.py   # Agent setup
├── document_processor.py   # Utility to parse and index uploaded PDFs
├── llm_config.py   # LLM configuration
├── tools.py    # Tools for agents 
└── app.py  # Streamlit app main file
```