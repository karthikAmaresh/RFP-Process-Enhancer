"""
Test script to validate the RFP processing pipeline
"""
import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health_check():
    print_section("1. Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        result = response.json()
        print(json.dumps(result, indent=2))
        
        # Check if all services are healthy
        services = result.get("services", {})
        issues = [k for k, v in services.items() if "error" in str(v).lower()]
        
        if issues:
            print(f"\n⚠️  Warning: Issues detected in: {', '.join(issues)}")
        else:
            print("\n✅ All services healthy!")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_pipeline_validation():
    print_section("2. Pipeline Validation")
    try:
        response = requests.post(f"{BASE_URL}/validate-pipeline")
        result = response.json()
        print(json.dumps(result, indent=2))
        
        status = result.get("overall_status")
        if status == "success":
            print(f"\n✅ Pipeline validation passed: {result.get('summary')}")
            return True
        else:
            print(f"\n❌ Pipeline validation failed: {result.get('summary')}")
            return False
    except Exception as e:
        print(f"❌ Pipeline validation failed: {e}")
        return False

def test_upload(file_path=None):
    print_section("3. Upload & Process Document")
    
    if not file_path:
        print("⏭️  Skipping upload test (no file provided)")
        print("   To test: python test_pipeline.py path/to/your/rfp.pdf")
        return None
    
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        return None
    
    try:
        print(f"Uploading: {file_path}")
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        result = response.json()
        print(json.dumps(result, indent=2))
        
        if response.status_code == 200:
            print(f"\n✅ Upload successful!")
            print(f"   Filename: {result.get('filename')}")
            print(f"   Chunks: {result.get('chunks')}")
            print(f"   Text length: {result.get('text_length')} characters")
            return result.get('filename')
        else:
            print(f"\n❌ Upload failed: {result}")
            return None
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None

def test_search(query="system requirements"):
    print_section("4. Search Indexed Content")
    try:
        print(f"Searching for: '{query}'")
        response = requests.get(
            f"{BASE_URL}/search",
            params={"query": query, "top_k": 3}
        )
        result = response.json()
        
        print(f"\nResults count: {result.get('results_count')}")
        
        for i, item in enumerate(result.get('results', [])[:3], 1):
            print(f"\n--- Result {i} ---")
            print(f"File: {item.get('fileName')}")
            print(f"Chunk: {item.get('chunk')}")
            print(f"Score: {item.get('score', 0):.4f}")
            print(f"Content preview: {item.get('content', '')[:150]}...")
        
        if result.get('results_count', 0) > 0:
            print(f"\n✅ Search successful!")
            return True
        else:
            print(f"\n⚠️  No results found (may need to upload documents first)")
            return False
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return False

def test_analysis(filename):
    print_section("5. Agent Analysis")
    
    if not filename:
        print("⏭️  Skipping analysis test (no file uploaded)")
        return False
    
    try:
        print(f"Analyzing: {filename}")
        print("⏳ This may take 10-15 seconds...")
        
        response = requests.post(f"{BASE_URL}/analyze/{filename}")
        result = response.json()
        
        if response.status_code == 200:
            analysis = result.get('analysis', {})
            agents = analysis.get('agents_analysis', [])
            
            print(f"\n✅ Analysis complete!")
            print(f"   Agents run: {len(agents)}")
            
            for agent in agents:
                print(f"\n--- {agent.get('agent')} ---")
                print(f"Responsibility: {agent.get('responsibility')}")
                if 'error' in agent:
                    print(f"❌ Error: {agent.get('error')}")
                else:
                    analysis_text = agent.get('analysis', '')
                    print(f"Analysis preview: {analysis_text[:200]}...")
            
            return True
        else:
            print(f"\n❌ Analysis failed: {result}")
            return False
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

def main():
    import sys
    
    print("\n" + "="*60)
    print("  RFP PIPELINE VALIDATION TEST")
    print("="*60)
    
    start_time = time.time()
    results = {}
    
    # Get file path if provided
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Run tests
    results['health'] = test_health_check()
    results['validation'] = test_pipeline_validation()
    
    uploaded_filename = test_upload(file_path)
    results['upload'] = uploaded_filename is not None
    
    results['search'] = test_search()
    results['analysis'] = test_analysis(uploaded_filename)
    
    # Summary
    print_section("SUMMARY")
    elapsed = time.time() - start_time
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    print(f"Time Elapsed: {elapsed:.2f} seconds\n")
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {test.capitalize()}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
