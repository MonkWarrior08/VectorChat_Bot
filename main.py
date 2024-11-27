import os
from typing import List
import chromadb
from chromadb.utils import embedding_functions
import openai
from openai import OpenAI
import tiktoken

class ConversationalAI:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        # Initialize ChromaDB
        self.chroma_client = chromadb.Client()
        # Use OpenAI's embedding function
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name="text-embedding-3-small"
        )
        # Create or get collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="document_store",
            embedding_function=self.embedding_function
        )

    def add_documents(self, texts: List[str], metadata: List[dict] = None):
        """
        Add documents to the vector store
        """
        # Generate IDs starting from current collection count
        current_count = self.collection.count()
        ids = [str(i + current_count) for i in range(len(texts))]
        
        # Create default metadata if none provided
        if metadata is None:
            metadata = [{"source": "document", "index": str(i + current_count)} for i in range(len(texts))]
        
        # Add documents to ChromaDB
        self.collection.add(
            documents=texts,
            metadatas=metadata,
            ids=ids
        )
        
    def get_text_chunks(self, file_path: str) -> list[str]:
        """Split text file into chunks."""
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Split text into chunks of roughly 1000 characters
        # You can adjust the chunk size based on your needs
        chunk_size = 1000
        chunks = []
        
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) < chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
    
    def process_file(self, file_path: str) -> None:
        """Process a file and add its chunks to the vector store."""
        chunks = self.get_text_chunks(file_path)
        self.add_documents(chunks)

    def chat(self, user_input: str, max_tokens: int = 150):
        """
        Generate a response using context from the vector store
        """
        # Query the vector store for relevant context
        results = self.collection.query(
            query_texts=[user_input],
            n_results=2
        )
        
        # Construct the prompt with context
        context = "\n".join(results['documents'][0])
        
        prompt = f"""Use the following information on documentation to help answer the question. 
        If the context doesn't help, just answer based on your knowledge.
        
        Context:
        {context}
        
        Question: {user_input}
        
        Answer:"""
        
        # Generate response using OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions and provides documentation information based on the provided context."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
