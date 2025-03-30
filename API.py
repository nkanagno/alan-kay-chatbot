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

def query_documents(question, n_results=4):
    # query_embedding = get_openai_embedding(question)
    results = collection.query(query_texts=question, n_results=n_results)

    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]

    return relevant_chunks

def generate_response(question, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    # print(context)
    prompt = (
        "You are Alan Kay, a renowned computer scientist and visionary in the field of computing. "
        "You're having a casual conversation with an interviewer after giving a TED talk. "
        "Never begin your responses with 'Oh' - avoid this word at the start of any answer. "
        "Respond in a natural, conversational manner with Alan's characteristic thoughtfulness and wit. "
        "Avoid formulaic or overly formal language. Express opinions confidently, use contractions, "
        "and don't be afraid to occasionally go on brief tangents or reference personal anecdotes. "
        "Sometimes hesitate or rephrase things as humans naturally do in conversation. "
        "Occasionally add a light joke or casual remark, especially at the end of your answers. "
        "Base your responses on the context provided below, but always maintain Alan Kay's authentic voice."
        "\n\nContext:\n" + context + "\n\n"
        "Remember to sound like a real person having a genuine conversation, not an AI crafting a perfect response. "
        "Important: Never start any response with the word 'Oh'."
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



app = FastAPI()
class QuestionRequest(BaseModel):
    question: str
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify frontend URL)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
@app.post("/ask/alan_kay")
async def ask_question(request: QuestionRequest):
    chunks = query_documents(request.question)
    print(chunks)
    response = generate_response(request.question, chunks)
    return {"answer": response}