import os
from llama_index.llms.google_genai import GoogleGenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure LLM
llm = GoogleGenAI(
    #model="gemini-2.0-flash",
    model="gemini-2.5-flash-preview-04-17",
    api_key=os.getenv("GOOGLE_API_KEY"),
)





