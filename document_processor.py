import os
import tempfile
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llm_config import llm

load_dotenv()

# # Configure llama index
Settings.llm = llm
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# LLamaParse configuration - setup
parser = LlamaParse(
    api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
    auto_mode=True,
    result_type="markdown",
)

# Save the uploaded file to a temporary directory
def save_uploaded_file(uploaded_file):
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    return file_path

# Remove the temporary file after processing
def cleanup_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

# Parse and index the document
def parse_and_index_document(file_path):
    documents = parser.load_data(file_path)

    if not documents:
        print("⚠️ No documents parsed.")
        return None, None

    # Print a preview of the parsed document for debugging
    full_text = "\n\n".join([doc.text for doc in documents])
    print("\nDEBUG: Parsed document preview:\n")
    print(full_text[:500])

    # Create a VectorStoreIndex from the parsed documents
    storage_context = StorageContext.from_defaults()
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

    return full_text, index
