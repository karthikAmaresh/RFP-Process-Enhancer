# Complete RFP Processing Pipeline
# Uses: Azure Blob Storage, Azure Document Intelligence, Azure OpenAI (GPT-4o)

import os
import sys
from dotenv import load_dotenv
from document_processing.extract_text import extract_text_from_blob, extract_text_from_pdf
from document_processing.chunking import chunk_text
from embedding.embedder import generate_embedding
from orchestrator_http import run_all_agents, save_to_kb

# Load Container App URLs
load_dotenv('.env.agents')

async def process_rfp_document(blob_name: str = None, file_path: str = None):
    """
    Complete pipeline to process RFP document
    
    Args:
        blob_name: Name of blob in Azure Storage (if using Blob Storage)
        file_path: Local file path (if not using Blob Storage)
        
    Returns:
        dict: Analysis results from all agents
    """
    print("=" * 60)
    print("RFP PROCESSING PIPELINE")
    print("=" * 60)
    
    # Step 1: Extract text from document
    print("\n[1/5] Extracting text from document...")
    if blob_name:
        try:
            text = extract_text_from_blob(blob_name)
            print(f"✓ Extracted text from blob: {blob_name}")
        except Exception as e:
            print(f"✗ Error extracting from blob: {e}")
            print("Falling back to local file if provided...")
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            else:
                raise
    elif file_path:
        # For PDF files, read bytes and process directly (no blob upload needed)
        if file_path.lower().endswith('.pdf'):
            try:
                print(f"Reading PDF file...")
                with open(file_path, 'rb') as f:
                    file_bytes = f.read()
                
                print(f"Extracting text from PDF using Azure Document Intelligence...")
                from document_processing.extract_text import extract_text_from_pdf_bytes
                text = extract_text_from_pdf_bytes(file_bytes)
                print(f"✓ Extracted text from PDF: {file_path}")
            except Exception as e:
                print(f"✗ PDF extraction failed: {e}")
                raise
        else:
            # Plain text file
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            print(f"✓ Loaded text from: {file_path}")
    else:
        raise ValueError("Either blob_name or file_path must be provided")
    
    print(f"Document length: {len(text)} characters")
    
    # Step 2: Chunk the text
    print("\n[2/5] Chunking text...")
    chunks = chunk_text(text, max_tokens=500)
    print(f"✓ Created {len(chunks)} chunks")
    
    # Save chunks to data/chunks directory
    chunks_dir = "data/chunks"
    os.makedirs(chunks_dir, exist_ok=True)
    for i, chunk in enumerate(chunks):
        with open(f"{chunks_dir}/chunk_{i+1}.txt", 'w', encoding='utf-8') as f:
            f.write(chunk)
    print(f"✓ Saved chunks to {chunks_dir}/")
    
    # Step 3: Generate embeddings and store locally
    print("\n[3/5] Generating embeddings and storing locally...")
    from local_vector_store import LocalVectorStore
    
    vector_store = LocalVectorStore()
    embeddings = []
    
    filename = blob_name or os.path.basename(file_path) if file_path else "unknown"
    
    for i, chunk in enumerate(chunks):
        emb = generate_embedding(chunk)
        embeddings.append(emb)
        
        # Store in local vector store (no database needed!)
        vector_store.add_chunk(
            text=chunk,
            embedding=emb,
            metadata={"filename": filename, "chunk_id": i + 1}
        )
        
        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(chunks)} chunks")
    
    stats = vector_store.get_stats()
    print(f"✓ Generated {len(embeddings)} embeddings (768-dim)")
    print(f"✓ Stored in local vector store: {stats['total_chunks']} chunks")
    
    # Step 4: Run all agents on first chunk (or combined text)
    print("\n[4/5] Running AI agents for analysis...")
    # Use first chunk for demo, or combine chunks for full analysis
    analysis_text = chunks[0] if len(chunks) > 0 else text[:5000]
    results = await run_all_agents(analysis_text)
    print(f"✓ Completed analysis with {len(results)} agents")
    
    # Step 5: Results ready (don't auto-save to file)
    print("\n[5/5] Analysis complete - results ready")
    print("✓ Results available via API (kb.md not auto-generated)")
    
    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)
    
    return results


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process RFP documents')
    parser.add_argument('--blob', help='Azure Blob name')
    parser.add_argument('--file', help='Local file path')
    
    args = parser.parse_args()
    
    if not args.blob and not args.file:
        print("Usage:")
        print("  python pipeline.py --blob <blob_name>")
        print("  python pipeline.py --file <file_path>")
        print("\nExample with local file:")
        print("  python pipeline.py --file sample_rfp.txt")
        return
    
    try:
        results = process_rfp_document(blob_name=args.blob, file_path=args.file)
        
        print("\n--- SUMMARY ---")
        for agent_name in results.keys():
            print(f"  - {agent_name}")
        
    except Exception as e:
        print(f"\n✗ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
