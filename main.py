from documents import load_all_documents
from rag import build_knowledge_base, ask_question

def main():
    print("=== AI Regulation Knowledge Base ===")
    print("Loading official regulatory documents...")
    
    # Load all documents
    documents = load_all_documents()
    print(f"Loaded {len(documents)} documents successfully.")
    
    # Build knowledge base
    collection, all_chunks, all_metadata = build_knowledge_base(documents)
    print("\nKnowledge base ready. You can now ask questions.\n")
    
    # Example questions
    test_questions = [
        "What AI systems are prohibited under the EU AI Act?",
        "What rights do individuals have under GDPR regarding AI decisions?",
        "What does the US Executive Order say about AI safety?",
        "How does CCPA protect California residents from automated decision making?",
        "What are the key principles of the UK AI Framework?"
    ]
    
    print("Running test questions...\n")
    print("=" * 60)
    
    for question in test_questions:
        answer, sources = ask_question(question, collection, all_chunks, all_metadata)
        print(f"\nQUESTION: {question}")
        print(f"\nANSWER: {answer}")
        print(f"\nSOURCES USED: {', '.join(set(sources))}")
        print("=" * 60)

if __name__ == "__main__":
    main()