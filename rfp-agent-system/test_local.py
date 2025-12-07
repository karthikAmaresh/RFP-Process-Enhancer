"""
Simple local test script - no Azure or MongoDB required
Tests core functionality: chunking, embedding, and basic operations
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_embedding():
    """Test embedding generation"""
    print("=" * 60)
    print("TEST 1: Embedding Generation")
    print("=" * 60)
    
    try:
        from document_processing.embedding import generate_embedding, get_model_info
        
        # Test single embedding
        text = "This is a test document for RFP processing"
        print(f"\nGenerating embedding for: '{text}'")
        
        embedding = generate_embedding(text)
        
        print(f"✅ Success!")
        print(f"   Embedding dimension: {len(embedding)}")
        print(f"   First 5 values: {embedding[:5]}")
        
        # Get model info
        info = get_model_info()
        print(f"\n📊 Model Info:")
        print(f"   Name: {info['model_name']}")
        print(f"   Dimension: {info['embedding_dimension']}")
        print(f"   Max sequence: {info['max_seq_length']}")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_chunking():
    """Test text chunking"""
    print("\n" + "=" * 60)
    print("TEST 2: Text Chunking")
    print("=" * 60)
    
    try:
        from document_processing.chunking import chunk_text
        
        # Create sample text
        text = "This is a sample sentence. " * 100
        print(f"\nSample text: {len(text.split())} words")
        
        # Test chunking
        chunks = chunk_text(text, max_tokens=50)
        
        print(f"✅ Success!")
        print(f"   Chunks created: {len(chunks)}")
        print(f"   First chunk ({len(chunks[0].split())} words): {chunks[0][:100]}...")
        print(f"   Last chunk ({len(chunks[-1].split())} words): {chunks[-1][:100]}...")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_process_rfp():
    """Test RFP processing (without storage)"""
    print("\n" + "=" * 60)
    print("TEST 3: RFP Processing Pipeline")
    print("=" * 60)
    
    try:
        from document_processing.chunking import chunk_text
        from document_processing.embedding import generate_embedding
        
        # Sample RFP text
        rfp_text = """
        Request for Proposal - Customer Management System
        
        Current System: The organization uses a legacy customer database 
        that was built 15 years ago. It has performance issues and lacks 
        modern features like cloud integration and mobile access.
        
        Business Process: Sales team enters customer data manually. 
        Customer service accesses records for support tickets. 
        Marketing team exports data for campaigns.
        
        Pain Points: System is slow, crashes frequently, no mobile access,
        difficult to generate reports, poor user interface.
        
        Requirements: Cloud-based solution, mobile responsive, automated 
        reporting, integration with existing email system, support for 
        1000+ concurrent users.
        
        Budget: $500,000 initial implementation, $100,000 annual maintenance.
        Timeline: Must be operational within 6 months.
        """
        
        print(f"\nProcessing sample RFP text...")
        print(f"Text length: {len(rfp_text)} characters")
        
        # Step 1: Chunk
        chunks = chunk_text(rfp_text, max_tokens=50)
        print(f"\n✅ Step 1: Chunking complete - {len(chunks)} chunks")
        
        # Step 2: Embed
        print(f"\n⏳ Step 2: Generating embeddings...")
        embeddings = []
        for i, chunk in enumerate(chunks):
            emb = generate_embedding(chunk)
            embeddings.append(emb)
            print(f"   Chunk {i+1}/{len(chunks)}: {len(emb)} dimensions")
        
        print(f"\n✅ Step 2: Embedding complete - {len(embeddings)} embeddings")
        
        # Step 3: Simulate storage (just count)
        print(f"\n✅ Step 3: Storage simulation")
        print(f"   Would store: {len(chunks)} chunks with embeddings")
        
        print(f"\n🎉 Full pipeline test successful!")
        print(f"   Total chunks: {len(chunks)}")
        print(f"   Total embeddings: {len(embeddings)}")
        print(f"   Embedding dimension: {len(embeddings[0])}")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_similarity():
    """Test similarity search (local, no DB)"""
    print("\n" + "=" * 60)
    print("TEST 4: Similarity Calculation")
    print("=" * 60)
    
    try:
        from document_processing.embedding import generate_embedding, compute_similarity
        
        # Test texts
        text1 = "What is the current business process?"
        text2 = "How does the business operate today?"
        text3 = "What is the project budget?"
        
        print(f"\nComparing texts:")
        print(f"  Text 1: {text1}")
        print(f"  Text 2: {text2}")
        print(f"  Text 3: {text3}")
        
        # Compute similarities
        sim_1_2 = compute_similarity(text1, text2)
        sim_1_3 = compute_similarity(text1, text3)
        
        print(f"\n✅ Results:")
        print(f"   Similarity (1-2): {sim_1_2:.4f} (similar topics)")
        print(f"   Similarity (1-3): {sim_1_3:.4f} (different topics)")
        
        if sim_1_2 > sim_1_3:
            print(f"\n✅ Semantic similarity working correctly!")
            print(f"   Similar questions are closer than different topics")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def main():
    print("\n" + "=" * 60)
    print("  LOCAL FUNCTIONALITY TEST")
    print("  No Azure or MongoDB required")
    print("=" * 60)
    
    results = {}
    
    # Run tests
    results['Embedding'] = test_embedding()
    results['Chunking'] = test_chunking()
    results['Pipeline'] = test_process_rfp()
    results['Similarity'] = test_similarity()
    
    # Summary
    print("\n" + "=" * 60)
    print("  TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {test}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Core functionality is working.")
        print("\nNext steps:")
        print("  1. Start the server: python backend/main.py")
        print("  2. Visit: http://localhost:8000/docs")
        print("  3. Try the API endpoints")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")


if __name__ == "__main__":
    main()
