import os
import anthropic
from chromadb import Client
from chromadb.config import Settings
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
import chromadb

# Initialize
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def build_knowledge_base(documents):
    print("Building knowledge base from real documents...")
    chroma_client = chromadb.EphemeralClient()
    collection = chroma_client.create_collection("ai_regulations")
    
    all_chunks = []
    all_ids = []
    all_metadata = []
    
    for doc_name, doc_text in documents.items():
        print(f"Processing {doc_name}...")
        chunks = chunk_text(doc_text)
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_ids.append(f"{doc_name}_{i}")
            all_metadata.append({"source": doc_name})
    
    print(f"Total chunks created: {len(all_chunks)}")
    
    # Add to ChromaDB in batches
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        batch_chunks = all_chunks[i:i + batch_size]
        batch_ids = all_ids[i:i + batch_size]
        batch_metadata = all_metadata[i:i + batch_size]
        embeddings = embedding_model.encode(batch_chunks).tolist()
        collection.add(
            documents=batch_chunks,
            embeddings=embeddings,
            ids=batch_ids,
            metadatas=batch_metadata
        )
    
    return collection, all_chunks, all_metadata

def hybrid_search(query, collection, all_chunks, all_metadata, top_k=5):
    # Vector search
    query_embedding = embedding_model.encode([query]).tolist()
    vector_results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    
    # BM25 keyword search
    tokenized_chunks = [chunk.split() for chunk in all_chunks]
    bm25 = BM25Okapi(tokenized_chunks)
    bm25_scores = bm25.get_scores(query.split())
    top_bm25_indices = sorted(range(len(bm25_scores)), 
                               key=lambda i: bm25_scores[i], reverse=True)[:top_k]
    
    # Combine results
    combined_chunks = []
    combined_sources = []
    seen = set()
    
    for doc, metadata in zip(vector_results['documents'][0], 
                              vector_results['metadatas'][0]):
        if doc not in seen:
            combined_chunks.append(doc)
            combined_sources.append(metadata['source'])
            seen.add(doc)
    
    for idx in top_bm25_indices:
        chunk = all_chunks[idx]
        if chunk not in seen:
            combined_chunks.append(chunk)
            combined_sources.append(all_metadata[idx]['source'])
            seen.add(chunk)
    
    return combined_chunks[:top_k], combined_sources[:top_k]

def ask_question(query, collection, all_chunks, all_metadata):
    print(f"\nSearching for: {query}")
    chunks, sources = hybrid_search(query, collection, all_chunks, all_metadata)
    
    context = ""
    for i, (chunk, source) in enumerate(zip(chunks, sources)):
        context += f"\n[Source: {source}]\n{chunk}\n"
    
    prompt = f"""You are an AI regulation expert. Answer the question based strictly on the provided context from official regulatory documents. Always cite which regulation your answer comes from.

Context:
{context}

Question: {query}

Provide a clear, accurate answer with specific citations to the source documents."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text, sources