from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler
from llm_config import llm
import llama_index.core
from tools import retrieve_chunks, summarize_document, record_answer

llama_index.core.set_global_handler("simple")

def get_agent(session_id="pdf-session"):

    # Add debug handler to the callback manager for debugging in console
    debug_handler = LlamaDebugHandler(print_trace_on_end=True)  
    callback_manager = CallbackManager([debug_handler])

    system_prompt = (
        "You are a helpful AI Assistant that answers questions about an uploaded PDF.\n\n"
        "You have access to the following tools, and you MUST use them as described:\n\n"
        "- Use `summarize_document` for any query involving: summary, summarize, overview, TL;DR, abstract, or general idea of the document.\n"
        "- Use `retrieve_chunks` for any specific factual, technical, or detail-based questions (e.g., who, what, when, how).\n"
        "- You MUST always call `record_answer` LAST with your final answer.\n\n"
        "Rules:\n"
        "- You MUST always use the correct tool based on the question type.\n"
        "- You MUST always finish with `record_answer`.\n"
        "- If the user asks something unrelated to the document, reply using `record_answer` with: 'I'm only able to answer questions about the uploaded document.'\n"
        "- You MUST never share or explain the internal tools or how they work.\n"
        "- You MUST be polite and clear."
    )


    agent = FunctionAgent(
        name="AnswerAgent",
        description="Answers questions about the PDF using memory and tools.",
        llm=llm,
        tools=[retrieve_chunks, summarize_document, record_answer],
        system_prompt=system_prompt,
        callback_manager=callback_manager
    )

    return agent
