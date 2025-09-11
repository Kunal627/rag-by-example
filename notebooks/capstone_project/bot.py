import gradio as gr
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.llms import Ollama
import torch

# -----------------------------
# Configs and other setup
# -----------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
EMBED_MODEL = "intfloat/e5-base-v2"
CHAT_MODEL = "llama3"
INDEX_DIR = "./data/vector_store/faiss_index"

embeddings = HuggingFaceBgeEmbeddings(
        model_name=EMBED_MODEL, encode_kwargs={"normalize_embeddings": True}
    )

vectorstore = FAISS.load_local(
    INDEX_DIR, embeddings, allow_dangerous_deserialization=True
)

# -----------------------------
# Setup LLM (local Ollama model)
# -----------------------------
llm = Ollama(model=CHAT_MODEL)

# -----------------------------
# Retrieval with similarity scores
# -----------------------------
def retrieve_with_similarity(query, top_k=5):
    """Retrieve docs from FAISS with similarity scores, return chunks with scores."""
    retrieved_with_scores = vectorstore.similarity_search_with_score(query, k=top_k)
    if not retrieved_with_scores:
        return [], []

    chunks = [
        {"content": doc.page_content, "metadata": doc.metadata, "similarity_score": float(score)}
        for doc, score in retrieved_with_scores
    ]
    return retrieved_with_scores, chunks

# -----------------------------
# Query function (FAISS only)
# -----------------------------
def chat_with_faiss(query, user_prompt, top_k=5):
    retrieved_with_scores, retrieved_chunks = retrieve_with_similarity(query, top_k=top_k)

    # Build context for LLM
    context = "\n\n".join([doc.page_content for doc, _ in retrieved_with_scores])
    final_prompt = f"Answer the query {query} with given Context:\n{context}\n\nUser Prompt:\n{user_prompt}\n\nAnswer:"

    answer = llm(
        final_prompt,
        temperature=0.02,
        max_tokens=1000,
        top_p=0.95
    )

    # Sources
    sources = []
    for doc, score in retrieved_with_scores:
        meta = doc.metadata
        page = meta.get("page_num", "N/A")
        sources.append(f"- Page {page} | Similarity Score: {score:.4f}")

    sources_text = "\n".join(sources) if sources else "No sources found."

    full_answer = f"**Answer:**\n{answer}\n\n**Sources:**\n{sources_text}"

    return full_answer, retrieved_chunks

# -----------------------------
# Gradio UI
# -----------------------------
with gr.Blocks() as demo:
    gr.Markdown("## 💬 My Chef")

    chatbot = gr.Chatbot()
    query_box = gr.Textbox(placeholder="Enter your query for retrieval", label="Query")
    prompt_box = gr.Textbox(placeholder="Enter your prompt for generation", label="Prompt")
    top_k_slider = gr.Slider(1, 15, value=5, step=1, label="Retrieve top K from FAISS")
    clear = gr.Button("Clear")

    retrieved_chunks_md = gr.JSON(label="Retrieved Chunks (with similarity scores)")
    answer_box = gr.Markdown(label="Answer")

    def user_query(query_message, prompt_message, chat_history, top_k):
        answer, retrieved_chunks = chat_with_faiss(query_message, prompt_message, top_k=top_k)
        chat_history.append((f"Q: {query_message}\nPrompt: {prompt_message}", answer))
        return "", "", chat_history, retrieved_chunks, answer

    query_box.submit(
        user_query,
        [query_box, prompt_box, chatbot, top_k_slider],
        [query_box, prompt_box, chatbot, retrieved_chunks_md, answer_box]
    )
    prompt_box.submit(
        user_query,
        [query_box, prompt_box, chatbot, top_k_slider],
        [query_box, prompt_box, chatbot, retrieved_chunks_md]
    )
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch(server_name="0.0.0.0", server_port=7860, share=False, pwa=True)