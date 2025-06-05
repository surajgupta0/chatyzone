# from langchain.vectorstores import Chroma
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_loaders import PyPDFLoader
# from langchain.schema import Document
# from langchain.chains import ConversationalRetrievalChain
# from langchain.prompts import PromptTemplate
# from langchain.memory import ConversationBufferMemory
# from google.generativeai import GenerativeModel
# from pathlib import Path
# import fitz  # PyMuPDF
# import hashlib
# import os

# # Configuration
# VECTOR_DIR = "./chatyzone"
# CHUNK_SIZE = 500
# CHUNK_OVERLAP = 100

# # Gemini LLM
# gemini_llm = GenerativeModel("gemini-pro")

# def hash_file(filepath: str):
#     """Return SHA-256 hash of a file for uniqueness."""
#     with open(filepath, "rb") as f:
#         return hashlib.sha256(f.read()).hexdigest()

# def convert_to_pdf(filepath: str) -> str:
#     """Convert any file to PDF using PyMuPDF and return new path."""
#     pdf_path = filepath
#     if not filepath.lower().endswith(".pdf"):
#         pdf_path = f"{Path(filepath).stem}.pdf"
#         doc = fitz.open(filepath)
#         doc.save(pdf_path)
    # return pdf_path

async def GenerateResponse(query: str, files_path: list, chat_history: list) -> str:
    try:
        return "Generating response..."  # Placeholder for actual response generation
        # Step 1: Setup Embedding & Vector Store
        embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        vectorstore = Chroma(persist_directory=VECTOR_DIR, embedding_function=embedding)

        added_hashes = set()
        for path in files_path:
            if not os.path.exists(path): continue

            pdf_path = convert_to_pdf(path)
            file_hash = hash_file(pdf_path)

            if file_hash in added_hashes or vectorstore.get(file_hash):  # Already indexed
                continue

            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
            split_docs = splitter.split_documents(documents)

            for doc in split_docs:
                doc.metadata["hash"] = file_hash

            vectorstore.add_documents(split_docs)
            added_hashes.add(file_hash)


        # Step 3: Prompt Setup
        prompt_template = """You are an intelligent assistant. Use the context and chat history to answer.

        Chat History:
        {chat_history}

        Question:
        {question}

        Answer:"""
        qa_prompt = PromptTemplate.from_template(prompt_template)

        # Step 4: LLM-based QA
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm                       = gemini_llm,
            retriever                 = retriever,
            return_source_documents   = True,
            combine_docs_chain_kwargs = {"prompt": qa_prompt}
        )

        result = qa_chain.invoke({"question": query,"context":retriever, "chat_history": chat_history})
        return result.get()("answer", "No answer found.")

    except Exception as e:
        print(f"[ERROR] GenerateResponse failed: {e}")
        return f"Error generating response: {str(e)}"
