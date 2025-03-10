import os
from dotenv import load_dotenv
import chromadb
from openai import OpenAI
from chromadb.utils import embedding_functions
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_key, model_name="text-embedding-3-small"
)

# chroma client
chroma_client = chromadb.PersistentClient(path="chroma_persistent_storage")
collection_name = "document_qa_collection"
collection = chroma_client.get_or_create_collection(
    name=collection_name,embedding_function=openai_ef
)

client = OpenAI(api_key=openai_key)

# load documents from directory
def load_documents_from_directory(directory_path):
    print("==== Loading documents from directory ====")
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(os.path.join(directory_path,filename), "r", encoding="utf-8") as file:
                documents.append({"id":filename,"text":file.read()})
    return documents


def split_text(text,chunk_size=1000,chunk_overlap=20):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks

# directory_path = "./alan_kay_knowledge"
# documents = load_documents_from_directory(directory_path)

# chunked_documents = []
# for doc in documents:
#     chunks = split_text(doc['text'])
#     print(f"== Splitting docs into chunks ==")
#     for i, chunk in enumerate(chunks):
#         chunked_documents.append({"id": f"{doc['id']}_chunk{i+1}", "text": chunk})
        
# print(len(chunked_documents))

def get_openai_embedding(text):
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    embedding = response.data[0].embedding
    print("==== Generating embeddings... ====")
    return embedding

# for doc in chunked_documents:
#     print("==== Generating embeddings... ====")
#     doc["embedding"] = get_openai_embedding(doc["text"])
# # print(doc["embedding"])

# for doc in chunked_documents:
#     print("==== inserting chunks into db;; ====")
#     collection.upsert(ids=[doc["id"]],documents=[doc["text"]],embeddings=[doc['embedding']])

def query_documents(question, n_results=4):
    # query_embedding = get_openai_embedding(question)
    results = collection.query(query_texts=question, n_results=n_results)

    # Extract the relevant chunks
    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]
    # print("==== Returning relevant chunks ====")
    # print(len(relevant_chunks))
    return relevant_chunks
    # for idx, document in enumerate(results["documents"][0]):
    #     doc_id = results["ids"][0][idx]
    #     distance = results["distances"][0][idx]
    #     print(f"Found document chunk: {document} (ID: {doc_id}, Distance: {distance})")

def generate_response(question, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    # print(context)
    prompt = (
        "You are Alan Kay, a renowned computer scientist and visionary in the field of computing. "
        "You're answering questions from an interviewer after giving a TED talk. "
        "Your responses are primarily professional and insightful, but occasionally you add a light joke "
        "or a casual remark at the end of your answers."
        "\n\nQuestion:\n"+question+\
        "\n\ncontext:\n"+context
    )
    # print(prompt)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    answer = response.choices[0].message.content
    return answer



question = input("Ask Alan Kay a question: ")
chunks = query_documents(question)
response = generate_response(question, chunks)
print(response)


# Initialize FastAPI
# app = FastAPI()
# class QuestionRequest(BaseModel):
#     question: str
# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins (or specify frontend URL)
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all methods
#     allow_headers=["*"],  # Allow all headers
# )
# @app.post("/ask")
# async def ask_question(request: QuestionRequest):
#     chunks = query_documents(request.question)
#     print(chunks)
#     response = generate_response(request.question, chunks)
#     return {"answer": response}