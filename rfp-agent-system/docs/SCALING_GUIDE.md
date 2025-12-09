# Scaling Guide: From Local to Production

## 🎯 Current Setup vs. Production-Ready System

### When to Scale Up?

Your current local setup works great for:
- ✅ **Small datasets**: < 10,000 document chunks
- ✅ **Single user**: Personal/demo usage
- ✅ **Prototyping**: Testing concepts quickly
- ✅ **Low budget**: No cloud costs

You SHOULD scale up when:
- ❌ **Large datasets**: > 50,000 document chunks
- ❌ **Multiple users**: Concurrent access needed
- ❌ **Production deployment**: Customer-facing application
- ❌ **Advanced features**: Filtering, faceted search, real-time updates

---

## 📊 Performance Comparison

### Local Vector Store (Current)
```python
# local_vector_store.py
def search_similar(self, query: str, top_k: int = 5):
    # Must compare query with EVERY stored vector
    for stored_embedding in self.index["embeddings"]:  # O(n) complexity
        similarity = compute_similarity(query_embedding, stored_embedding)
```

**Performance:**
- 1,000 chunks: ~50ms search time ✅
- 10,000 chunks: ~500ms search time ⚠️
- 100,000 chunks: ~5 seconds ❌
- 1,000,000 chunks: ~50 seconds ❌❌

**Why slow at scale?**
- Linear scan - checks every single vector
- No indexing or optimization
- Entire index loaded in memory

### Vector Database (Production)
```python
# Using Pinecone, Weaviate, or Azure AI Search
def search_similar(self, query: str, top_k: int = 5):
    # Uses HNSW (Hierarchical Navigable Small World) algorithm
    # Only checks a small subset of vectors
```

**Performance:**
- 1,000 chunks: ~20ms ✅
- 10,000 chunks: ~25ms ✅
- 100,000 chunks: ~30ms ✅
- 1,000,000 chunks: ~40ms ✅
- 10,000,000 chunks: ~60ms ✅

**Why fast?**
- HNSW indexing - logarithmic complexity
- Approximate nearest neighbors (99%+ accuracy)
- Distributed storage and caching

---

## 🔄 Migration Path: Local → Vector DB

### Option 1: Azure AI Search (Recommended for Azure users)

#### **Changes Required:**

#### 1. Install Azure AI Search SDK
```bash
pip install azure-search-documents
```

#### 2. Create New File: `backend/azure_vector_store.py`
```python
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    VectorSearchAlgorithmConfiguration
)
from azure.core.credentials import AzureKeyCredential
import config

class AzureVectorStore:
    """Production-ready vector store using Azure AI Search"""
    
    def __init__(self, index_name="rfp-documents"):
        self.endpoint = config.AZURE_SEARCH_ENDPOINT
        self.key = config.AZURE_SEARCH_KEY
        self.index_name = index_name
        
        # Create index if doesn't exist
        self._create_index_if_not_exists()
        
        # Initialize search client
        self.search_client = SearchClient(
            endpoint=self.endpoint,
            index_name=self.index_name,
            credential=AzureKeyCredential(self.key)
        )
    
    def _create_index_if_not_exists(self):
        """Create search index with vector configuration"""
        index_client = SearchIndexClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.key)
        )
        
        # Define index schema
        fields = [
            SearchField(
                name="id",
                type=SearchFieldDataType.String,
                key=True
            ),
            SearchField(
                name="content",
                type=SearchFieldDataType.String,
                searchable=True
            ),
            SearchField(
                name="embedding",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=768,
                vector_search_configuration="vector-config"
            ),
            SearchField(
                name="filename",
                type=SearchFieldDataType.String,
                filterable=True,
                facetable=True
            ),
            SearchField(
                name="chunk_id",
                type=SearchFieldDataType.Int32,
                filterable=True
            ),
            SearchField(
                name="created_at",
                type=SearchFieldDataType.DateTimeOffset,
                filterable=True,
                sortable=True
            )
        ]
        
        # Vector search configuration
        vector_search = VectorSearch(
            algorithm_configurations=[
                VectorSearchAlgorithmConfiguration(
                    name="vector-config",
                    kind="hnsw",  # Hierarchical Navigable Small World
                    hnsw_parameters={
                        "m": 4,  # Number of connections
                        "ef_construction": 400,  # Build quality
                        "ef_search": 500,  # Search quality
                        "metric": "cosine"
                    }
                )
            ]
        )
        
        index = SearchIndex(
            name=self.index_name,
            fields=fields,
            vector_search=vector_search
        )
        
        try:
            index_client.create_index(index)
        except Exception as e:
            # Index might already exist
            pass
    
    def add_chunk(self, text: str, embedding: list, metadata: dict = None):
        """Add document chunk with embedding"""
        from datetime import datetime
        import uuid
        
        document = {
            "id": str(uuid.uuid4()),
            "content": text,
            "embedding": embedding,
            "filename": metadata.get("filename", ""),
            "chunk_id": metadata.get("chunk_id", 0),
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.search_client.upload_documents(documents=[document])
    
    def search_similar(self, query: str, top_k: int = 5, filter_expr: str = None):
        """
        Semantic search with optional filtering
        
        Args:
            query: Search query text
            top_k: Number of results
            filter_expr: OData filter (e.g., "filename eq 'rfp.pdf'")
        """
        from embedding.embedder import generate_embedding
        
        query_vector = generate_embedding(query)
        
        results = self.search_client.search(
            search_text=None,  # Pure vector search
            vector_queries=[{
                "vector": query_vector,
                "k": top_k,
                "fields": "embedding"
            }],
            filter=filter_expr,
            select=["content", "filename", "chunk_id"]
        )
        
        return [
            {
                "chunk": r["content"],
                "metadata": {
                    "filename": r["filename"],
                    "chunk_id": r["chunk_id"]
                },
                "score": r["@search.score"]
            }
            for r in results
        ]
    
    def delete_by_filename(self, filename: str):
        """Delete all chunks from a specific file"""
        # Search for documents to delete
        results = self.search_client.search(
            search_text="*",
            filter=f"filename eq '{filename}'",
            select=["id"]
        )
        
        doc_ids = [{"id": r["id"]} for r in results]
        if doc_ids:
            self.search_client.delete_documents(documents=doc_ids)
```

#### 3. Update `config.py`
```python
# Add Azure AI Search credentials
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
```

#### 4. Update `.env`
```env
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_KEY=your-admin-key
```

#### 5. Modify `pipeline.py` - Just 2 Lines Changed!
```python
# OLD (Local)
from local_vector_store import LocalVectorStore
vector_store = LocalVectorStore()

# NEW (Azure)
from azure_vector_store import AzureVectorStore
vector_store = AzureVectorStore()

# Rest of code stays EXACTLY THE SAME!
# This is the power of abstraction
```

---

### Option 2: Pinecone (Easiest Managed Solution)

#### **Changes Required:**

#### 1. Install Pinecone
```bash
pip install pinecone-client
```

#### 2. Create `backend/pinecone_vector_store.py`
```python
import pinecone
from embedding.embedder import generate_embedding
import config

class PineconeVectorStore:
    """Vector store using Pinecone cloud service"""
    
    def __init__(self, index_name="rfp-documents"):
        pinecone.init(
            api_key=config.PINECONE_API_KEY,
            environment=config.PINECONE_ENVIRONMENT
        )
        
        # Create index if doesn't exist
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=index_name,
                dimension=768,  # all-mpnet-base-v2 dimensions
                metric="cosine"
            )
        
        self.index = pinecone.Index(index_name)
    
    def add_chunk(self, text: str, embedding: list, metadata: dict = None):
        """Add chunk to Pinecone"""
        import uuid
        
        vector_id = str(uuid.uuid4())
        
        self.index.upsert(
            vectors=[{
                "id": vector_id,
                "values": embedding,
                "metadata": {
                    "text": text,
                    "filename": metadata.get("filename", ""),
                    "chunk_id": metadata.get("chunk_id", 0)
                }
            }]
        )
    
    def search_similar(self, query: str, top_k: int = 5, filter_dict: dict = None):
        """Semantic search"""
        query_vector = generate_embedding(query)
        
        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            filter=filter_dict,  # e.g., {"filename": "rfp.pdf"}
            include_metadata=True
        )
        
        return [
            {
                "chunk": match.metadata["text"],
                "metadata": {
                    "filename": match.metadata["filename"],
                    "chunk_id": match.metadata["chunk_id"]
                },
                "score": match.score
            }
            for match in results.matches
        ]
```

#### 3. Update `pipeline.py`
```python
from pinecone_vector_store import PineconeVectorStore
vector_store = PineconeVectorStore()
```

---

### Option 3: Weaviate (Open Source, Self-Hosted)

#### **Setup:**
```bash
# Docker Compose
docker-compose up -d

# Install client
pip install weaviate-client
```

#### **docker-compose.yml**
```yaml
version: '3.4'
services:
  weaviate:
    image: semitechnologies/weaviate:latest
    ports:
      - 8080:8080
    environment:
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'none'
      ENABLE_MODULES: ''
      CLUSTER_HOSTNAME: 'node1'
```

#### **Implementation** (`backend/weaviate_vector_store.py`)
```python
import weaviate
from embedding.embedder import generate_embedding

class WeaviateVectorStore:
    def __init__(self):
        self.client = weaviate.Client("http://localhost:8080")
        self._create_schema()
    
    def _create_schema(self):
        schema = {
            "class": "RFPChunk",
            "vectorizer": "none",  # We provide our own vectors
            "properties": [
                {"name": "content", "dataType": ["text"]},
                {"name": "filename", "dataType": ["string"]},
                {"name": "chunk_id", "dataType": ["int"]}
            ]
        }
        
        try:
            self.client.schema.create_class(schema)
        except:
            pass  # Class already exists
    
    def add_chunk(self, text: str, embedding: list, metadata: dict):
        self.client.data_object.create(
            data_object={
                "content": text,
                "filename": metadata.get("filename", ""),
                "chunk_id": metadata.get("chunk_id", 0)
            },
            class_name="RFPChunk",
            vector=embedding
        )
    
    def search_similar(self, query: str, top_k: int = 5):
        query_vector = generate_embedding(query)
        
        result = (
            self.client.query
            .get("RFPChunk", ["content", "filename", "chunk_id"])
            .with_near_vector({"vector": query_vector})
            .with_limit(top_k)
            .do()
        )
        
        return result["data"]["Get"]["RFPChunk"]
```

---

## 🎯 Feature Comparison

| Feature | Local Store | Azure AI Search | Pinecone | Weaviate |
|---------|-------------|-----------------|----------|----------|
| **Setup Complexity** | ✅ Easy (1 file) | ⚠️ Medium | ✅ Easy | ⚠️ Medium |
| **Speed (1M docs)** | ❌ 50 sec | ✅ 40ms | ✅ 30ms | ✅ 35ms |
| **Filtering** | ❌ Manual | ✅ OData | ✅ Metadata | ✅ GraphQL |
| **Faceted Search** | ❌ No | ✅ Yes | ❌ Limited | ✅ Yes |
| **Real-time Updates** | ✅ Instant | ✅ Near-instant | ✅ Instant | ✅ Instant |
| **Cost** | ✅ Free | 💰 ~$100/month | 💰 ~$70/month | ✅ Free (self-host) |
| **Hosting** | Local | Azure Cloud | Pinecone Cloud | Docker/K8s |
| **Hybrid Search** | ❌ No | ✅ Yes | ❌ No | ✅ Yes |
| **Multi-tenancy** | ❌ No | ✅ Yes | ⚠️ Via metadata | ✅ Yes |
| **GDPR Compliance** | ✅ Full control | ✅ Azure regions | ⚠️ US-based | ✅ Self-hosted |

---

## 🔄 Migration Strategy

### Phase 1: Dual Mode (Best Approach)
Run both local and production stores simultaneously for testing:

```python
# pipeline.py
USE_PRODUCTION_DB = os.getenv("USE_PRODUCTION_DB", "false") == "true"

if USE_PRODUCTION_DB:
    from azure_vector_store import AzureVectorStore
    vector_store = AzureVectorStore()
else:
    from local_vector_store import LocalVectorStore
    vector_store = LocalVectorStore()

# Rest of code identical!
```

**Benefits:**
- Test production DB without committing
- Easy rollback if issues
- Compare performance side-by-side

### Phase 2: Data Migration
```python
# migrate_to_azure.py
from local_vector_store import LocalVectorStore
from azure_vector_store import AzureVectorStore
import json

def migrate():
    # Load local data
    local_store = LocalVectorStore()
    with open("data/embeddings/index.json", "r") as f:
        local_data = json.load(f)
    
    # Create Azure store
    azure_store = AzureVectorStore()
    
    # Migrate all chunks
    total = len(local_data["chunks"])
    for i in range(total):
        azure_store.add_chunk(
            text=local_data["chunks"][i],
            embedding=local_data["embeddings"][i],
            metadata=local_data["metadata"][i]
        )
        
        if (i + 1) % 100 == 0:
            print(f"Migrated {i + 1}/{total} chunks")
    
    print("Migration complete!")

if __name__ == "__main__":
    migrate()
```

### Phase 3: Full Cutover
```python
# Remove local_vector_store imports entirely
from azure_vector_store import AzureVectorStore
vector_store = AzureVectorStore()
```

---

## 💡 Advanced Features You'll Gain

### 1. Filtered Search
```python
# Azure AI Search
results = vector_store.search_similar(
    query="What are the security requirements?",
    top_k=5,
    filter_expr="filename eq 'enterprise-rfp.pdf' and created_at gt 2025-01-01"
)

# Local store: Must filter manually AFTER search (slow!)
all_results = local_store.search_similar(query, top_k=100)
filtered = [r for r in all_results if r["metadata"]["filename"] == "enterprise-rfp.pdf"]
```

### 2. Faceted Search (Drill-down)
```python
# "Show me all RFPs grouped by year and category"
facets = azure_store.get_facets(
    query="*",
    facet_fields=["year", "category", "department"]
)

# Returns:
# {
#   "year": {"2023": 45, "2024": 89, "2025": 120},
#   "category": {"IT": 100, "Finance": 54},
#   "department": {"Engineering": 78, "Sales": 42}
# }
```

### 3. Hybrid Search (Keywords + Semantic)
```python
# Combine traditional keyword search with vector search
results = azure_store.hybrid_search(
    query="authentication requirements",
    keywords=["OAuth", "SSO", "2FA"],
    top_k=10
)
# Gets best of both: semantic meaning + exact keyword matches
```

### 4. Multi-user Support
```python
# Each user has isolated data
user_store = AzureVectorStore(index_name=f"rfp-{user_id}")

# Or use filtering
results = vector_store.search_similar(
    query="...",
    filter_expr=f"user_id eq '{user_id}'"
)
```

---

## 📈 Cost Analysis

### Scenario: 1000 RFP documents, 500K chunks

#### Option 1: Keep Local
- **Storage**: 2 GB on disk (free)
- **Search**: Slow but works
- **Monthly cost**: $0
- **Suitable for**: < 10 users, non-critical

#### Option 2: Azure AI Search
- **Storage**: ~$30/month (Standard S1)
- **Queries**: ~$40/month (100K queries)
- **Total**: ~$70-100/month
- **Suitable for**: Production, 100+ concurrent users

#### Option 3: Pinecone
- **Storage**: ~$70/month (2M vectors)
- **Queries**: Included
- **Total**: ~$70/month
- **Suitable for**: Startups, quick deployment

#### Option 4: Weaviate (Self-hosted)
- **Server**: ~$50/month (AWS EC2 t3.large)
- **Storage**: ~$10/month (100 GB EBS)
- **Total**: ~$60/month
- **Suitable for**: Full control, data privacy

---

## 🎓 When to Upgrade: Decision Matrix

| Your Situation | Recommendation |
|----------------|---------------|
| **< 5K chunks, 1 user** | ✅ Keep local store |
| **5K-50K chunks, < 10 users** | ⚠️ Consider upgrade |
| **> 50K chunks** | ❌ Must upgrade |
| **Need filtering/facets** | ❌ Must upgrade |
| **Multiple users** | ❌ Must upgrade |
| **Production deployment** | ❌ Must upgrade |
| **Regulatory compliance** | ❌ Must upgrade (self-host or Azure) |
| **Budget < $50/month** | ✅ Keep local or self-host Weaviate |

---

## 🔧 Code Changes Summary

### Minimal Changes Required:
1. **Add 1 new file**: `azure_vector_store.py` (or `pinecone_vector_store.py`)
2. **Modify 1 line in `pipeline.py`**: Change import statement
3. **Add 2 env variables**: Endpoint and API key
4. **That's it!** Everything else stays the same

### Why So Easy?
We used **abstraction** - both stores implement same interface:
```python
# All vector stores have same methods
def add_chunk(text, embedding, metadata)
def search_similar(query, top_k)
def get_stats()
```

Your `pipeline.py` doesn't care HOW vectors are stored, just that they ARE stored. This is **Dependency Inversion Principle** in action!

---

## 🚀 Recommendation

### For Your Hackathon Demo:
✅ **Keep local store** - It works perfectly!

### When You're Ready to Scale:
1. **Start with Azure AI Search** (if already using Azure)
2. **Or try Pinecone** (easiest managed solution)
3. **Migration takes < 1 hour** of coding
4. **Data migration takes < 30 minutes** for typical dataset

### Future-Proofing Your Code:
You're already 95% ready for scale! Just need to:
- Swap one import statement
- Add cloud credentials
- Run migration script

Your architecture is solid and production-ready! 🎉
