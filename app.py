import streamlit as st
import asyncio
import time
import nest_asyncio
from document_processor import save_uploaded_file, cleanup_file, parse_and_index_document
from agents import get_agent
from llama_index.core.workflow import Context
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

nest_asyncio.apply()
st.set_page_config(page_title="PDF AI", layout="centered")

# Initialize session state
for key in ["parsed_text", "index", "doc_loaded", "filename", "last_answer", "last_question", "agent", "session_id"]:
    if key not in st.session_state:
        st.session_state[key] = None

def main():
    st.title(":sparkles: PDF AI Assistant")
    st.markdown("Upload a PDF and ask questions using an agent powered by tools. :muscle:")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type="pdf",
        disabled=bool(st.session_state.get("doc_loaded", False))
    )


    if uploaded_file and not st.session_state["doc_loaded"]:
        st.toast("🔒 A document is loaded. Refresh the page to upload a new one.", icon="🔄")
        file_path = save_uploaded_file(uploaded_file)
        with st.spinner("📄 Parsing and indexing document..."):
            parsed_text, index = parse_and_index_document(file_path)
            cleanup_file(file_path)

            if parsed_text and index:
                st.session_state["parsed_text"] = parsed_text
                st.session_state["index"] = index
                st.session_state["doc_loaded"] = True
                st.session_state["filename"] = uploaded_file.name

                session_id = f"{uploaded_file.name}_{time.time()}"
                st.session_state["session_id"] = session_id

                agent = get_agent(session_id)
                st.session_state["agent"] = agent

                st.success("✅ Document parsed and indexed!")
            else:
                st.error("❌ Failed to parse the document.")

    if st.session_state["doc_loaded"]:
        with st.form("chat_form", clear_on_submit=True):
            query = st.text_input("🔍 Ask your question:")
            submitted = st.form_submit_button("Ask")

        if submitted and query:
            st.session_state["last_question"] = query
            st.session_state["last_answer"] = None
            with st.spinner("🤖 Thinking..."):
                try:
                    answer = asyncio.run(run_agent_workflow(query))
                    st.session_state["last_answer"] = answer
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        if st.session_state["last_answer"] and st.session_state["last_question"]:
            st.markdown(f"### 🧠 Assistant responds to :question: '{st.session_state['last_question']}'")
            st.divider()
            st.markdown(st.session_state["last_answer"])

async def run_agent_workflow(query):
    await asyncio.sleep(0.1)

    agent = st.session_state["agent"]
    context = Context(agent)
    await context.set("state", {
        "parsed_text": st.session_state["parsed_text"],
        "index": st.session_state["index"],
    })

    # Run the agent with the provided query
    await agent.run(query, ctx=context)

    state = await context.get("state")
    final_answer = state.get("answer", "").strip()

    return final_answer or "⚠️ The assistant could not generate a meaningful answer."

if __name__ == "__main__":
    main()
