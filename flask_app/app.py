import torch
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from config import *

from huggingface_hub import login


from flask import Flask, redirect, url_for, request, jsonify


# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'RAG pipeline for quantum notes is up and running!'

def login_hugging_face():
    login(hugging_face_token)
    return "login done"

# Load the model
def load_gemma_model():
    model_name = "google/gemma-2b-it"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"  # Gemma needs left padding for batched generation

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",       # or omit this if issues arise
        device_map=None           # Don't use device_map on CPU

    )


    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        top_p=1.0,
        do_sample=False       # Disable sampling; forces greedy decoding

    )

    return pipe


def loade_vector_store(path="./chroma_bge_768"):
    embedding_fn = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5"
    )

    vectorstore = Chroma(
        client=chromadb.PersistentClient(path="./chroma_bge_768"),
        collection_name="qnotes_docs",
        embedding_function=embedding_fn
    )

    return vectorstore



import sys, os, pathlib
sys.path.insert(0, os.path.abspath("./src"))        # points to ./src relative to the notebook

from src.quantum_router import pick_quantum_template


def retriever(user_query, pipe, vectorstore, k = 7):

    # Use your vectorstore to get context
    retrieved_docs = vectorstore.similarity_search(user_query, k=k)

    retrieved_context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    template_fn = pick_quantum_template(user_query)

    prompt = template_fn(retrieved_context, user_query)

    output = pipe(prompt)[0]['generated_text']

    answer = output.split("Answer (structured and accurate):")[-1].strip()
    context = output.split("Context:")[-1].strip().split("Question:")[0].strip()
    question = output.split("Question:")[-1].strip().split("Answer (structured and accurate):")[0].strip()
    
    result = {
        "question": question,
        "context": retrieved_context,
        "answer": answer
    }

    return result


@app.route('/ask', methods=['POST'])
def run():
    if request.is_json:
        try:
            data = request.get_json()
            # Process the json data here
            user_query = data['prompt']
            pipe = load_gemma_model()
            vectorstore = loade_vector_store(path="./chroma_bge_768")
            result = retriever(user_query, pipe, vectorstore, k = 7)

    
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)