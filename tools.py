from llama_index.core.workflow import Context

# This tool is used by the agent in order to find relevant chunks of text based on the query.
async def retrieve_chunks(ctx: Context, query: str) -> str:
    """ Useful for retrieving relevant chunks from the document based on user questions. """
    state = await ctx.get("state")
    index = state.get("index")
    if not index:
        return "No index available."

    retriever = index.as_retriever()
    nodes = retriever.retrieve(query)
    chunks = "\n\n".join([n.get_content() for n in nodes])

    state["retrieved_chunks"] = chunks
    await ctx.set("state", state)
    return f"Retrieved relevant chunks:\n\n{chunks}"


# This tool is used by the agent in order to have access to the full text of the document.
async def summarize_document(ctx: Context) -> str:
    """Useful for storing the full parsed document in order to summarize it."""
    state = await ctx.get("state")
    full_text = state.get("parsed_text")

    if not full_text:
        return "Document is missing."

    state["summary_target_text"] = full_text
    await ctx.set("state", state)
    return "Full text loaded into state for summarization."


# This tool is used by the agent in order to record the final answer to the state.
async def record_answer(ctx: Context, answer: str) -> str:
    """ Records the assistant's final answer into state. """
    state = await ctx.get("state")
    if isinstance(answer, str) and answer.strip():
        state["answer"] = answer.strip()
        await ctx.set("state", state)
        return "Answer recorded."
    else:
        return "No answer provided."
