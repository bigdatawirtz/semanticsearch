import uuid
import gradio as gr
import chromadb
from chromadb.utils import embedding_functions
import json
import requests

# -----------------------------
# 1. Initialize ChromaDB
# -----------------------------

client = chromadb.EphemeralClient()
#client = chromadb.PersistentClient(path="./chroma_db") # Uncomment for persistent storage

embedding_fn = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="documents",
    embedding_function=embedding_fn
)

# -----------------------------
# 2. Function: upload json files
# -----------------------------
def upload_text(files):
    """
    files: list of uploaded json file paths from Gradio
    """
    if not files:
        return "No files uploaded."

    added = []
    errors = []

    # Ensure list
    if not isinstance(files, (list, tuple)):
        files = [files]

    for f in files:
        try:
            # f is a path string, open normally
            with open(f, "r", encoding="utf-8") as fh:
                content = fh.read()

            if not content.strip():
                errors.append(f"{f} is empty")
                continue

            # Validate JSON content
            try:
                json_data = json.loads(content)
            except json.JSONDecodeError as e:
                errors.append(f"{f}: Invalid JSON format - {e}")
                continue


            # Generate a unique ID
            doc_id = str(uuid.uuid4())

            # Metadata: filename (just basename)
            import os
            metadata = {"filename": os.path.basename(f)}

            # Add to Chroma in-memory collection
            collection.add(
                ids=[doc_id],
                documents=[content],
                metadatas=[metadata]
            )

            added.append(doc_id)

        except Exception as e:
            errors.append(f"{f}: failed ({e})")

    msg_parts = []
    if added:
        msg_parts.append(f"✅ Successfully uploaded {len(added)} file(s):")
        msg_parts.extend([f"  • {item}" for item in added])
        msg_parts.append(f"\n📊 Total documents in memory: {collection.count()}")
    if errors:
        msg_parts.append(f"\n❌ Errors ({len(errors)} file(s) failed):")
        msg_parts.extend([f"  • {error}" for error in errors])

    return "\n".join(msg_parts) if msg_parts else "No files processed."



# -----------------------------
# 3. Function: query the database
# -----------------------------
def ask_question(question):
    if not question.strip():
        return "Please enter a question."

    results = collection.query(
        query_texts=[question],
        n_results=1
    )

    if not results["documents"]:
        return "No documents found."

    best_doc = results["documents"][0][0]
    metadata = results["metadatas"][0][0]

    return f"📄 **Best matching document** (from: {metadata.get('filename')})\n\n```\n{best_doc}\n```"



# -----------------------------
# 4. Ollama request function
# -----------------------------


def ask_ollama(question):
    # Step 1: Find the most relevant document from Chroma
    results = collection.query(query_texts=[question], n_results=1)
    if not results["documents"]:
        return "No documents found to use as context."

    best_doc = results["documents"][0][0]
    filename = results["metadatas"][0][0].get("filename")

    # Step 2: Build the prompt
    prompt = f"""
You are an assistant. Use the following document as context.

=== DOCUMENT ({filename}) ===
{best_doc}
=== END DOCUMENT ===

User question: {question}

Provide a clear and helpful answer based ONLY on the document.
"""

    # Step 3: Send to Ollama
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.3",        # Change to your Ollama model name
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        return f"Error calling Ollama: {response.text}"

    return response.json()["response"]



# -----------------------------
# 4. Gradio Interface
# -----------------------------

with gr.Blocks(title="ChromaDB Text Search") as demo:

    gr.Markdown("# 📚 ChromaDB Semantic Text Search App")
    gr.Markdown("Upload Json files and query them using semantic search.")

    with gr.Tab("Upload"):
        text_upload = gr.File(file_count="multiple", file_types=[".json"])
        upload_btn = gr.Button("Upload Json Files")
        upload_output = gr.Textbox(label="Status", lines=6)
        upload_btn.click(upload_text, inputs=[text_upload], outputs=[upload_output])

    with gr.Tab("Search"):
        question_box = gr.Textbox(label="Ask a question")

        ask_btn = gr.Button("Search Best Document")
        search_output = gr.Markdown()
        ask_btn.click(ask_question, inputs=[question_box], outputs=[search_output])
    
        ollama_btn = gr.Button("Ask LLM (Ollama)")
        ollama_output = gr.Markdown()
        ollama_btn.click(ask_ollama, inputs=[question_box], outputs=[ollama_output])        

demo.launch()
