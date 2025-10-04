#!/usr/bin/env python3
"""
Test script to verify the real RAG pipeline is working
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ai_imports():
    """Test if AI libraries can be imported"""
    try:
        from sentence_transformers import SentenceTransformer
        import chromadb
        from chromadb.config import Settings
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
        print("✅ All AI libraries imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_embedding_model():
    """Test embedding model loading"""
    try:
        from sentence_transformers import SentenceTransformer
        print("Loading embedding model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        test_text = "This is a test sentence"
        embedding = model.encode(test_text)
        print(f"✅ Embedding model working - embedding shape: {embedding.shape}")
        return True
    except Exception as e:
        print(f"❌ Embedding model error: {e}")
        return False

def test_chromadb():
    """Test ChromaDB functionality"""
    try:
        import chromadb
        from chromadb.config import Settings
        
        print("Testing ChromaDB...")
        client = chromadb.PersistentClient(path="./test_chroma_db")
        
        # Create test collection
        collection = client.create_collection("test_collection")
        
        # Add test documents
        collection.add(
            documents=["This is a test document"],
            metadatas=[{"source": "test"}],
            ids=["doc1"]
        )
        
        # Query test
        results = collection.query(
            query_texts=["test document"],
            n_results=1
        )
        
        print(f"✅ ChromaDB working - found {len(results['documents'][0])} documents")
        return True
    except Exception as e:
        print(f"❌ ChromaDB error: {e}")
        return False

def test_streamlit_dashboard():
    """Test if Streamlit dashboard can be imported"""
    try:
        # Import the dashboard components
        from streamlit_dashboard import RealRAGPipeline
        print("✅ Streamlit dashboard components imported successfully")
        return True
    except Exception as e:
        print(f"❌ Dashboard import error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Real RAG Pipeline Components")
    print("=" * 50)
    
    tests = [
        ("AI Imports", test_ai_imports),
        ("Embedding Model", test_embedding_model),
        ("ChromaDB", test_chromadb),
        ("Streamlit Dashboard", test_streamlit_dashboard)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Real RAG pipeline is ready!")
        print("\n🚀 You can now run: streamlit run streamlit_dashboard.py")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
