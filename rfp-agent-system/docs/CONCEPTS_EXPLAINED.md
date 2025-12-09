# Key Concepts & Implementation Details

## 📚 Core Concepts Explained with Files

---

## 1️⃣ Vector Embeddings (Semantic Search)

### **Concept:**
Converting text into numerical vectors (arrays of numbers) that capture semantic meaning. Similar texts have similar vectors, enabling "meaning-based" search instead of just keyword matching.

### **Files Involved:**

#### `backend/embedding/embedder.py`
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')

def generate_embedding(text: str) -> List[float]:
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()  # Returns 768 numbers
```

**What's happening:**
- Loads pre-trained neural network model (`all-mpnet-base-v2`)
- Model has learned semantic meaning from millions of texts
- Converts text → 768-dimensional vector (768 numbers between -1 and 1)
- Similar meanings = similar vector patterns

**Example:**
```
"car accident" → [0.23, -0.45, 0.12, ..., 0.67]  (768 numbers)
"vehicle crash" → [0.21, -0.43, 0.15, ..., 0.65]  (very similar!)
"pizza recipe" → [-0.78, 0.34, -0.23, ..., -0.12] (very different!)
```

**Why 768 dimensions?**
- Each dimension captures a different aspect of meaning
- More dimensions = more nuance captured
- 768 is a good balance between accuracy and speed

---

## 2️⃣ Cosine Similarity (Comparing Vectors)

### **Concept:**
Mathematical formula to measure how similar two vectors are. Tells us "how related" two pieces of text are.

### **Files Involved:**

#### `backend/embedding/embedder.py`
```python
def compute_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    # Convert to numpy arrays
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    
    # Calculate cosine similarity
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    similarity = dot_product / (norm1 * norm2)
    return float(similarity)
```

**The Math:**
```
similarity = (A · B) / (||A|| × ||B||)

Where:
- A · B = dot product (multiply corresponding numbers and sum)
- ||A|| = length of vector A
- ||B|| = length of vector B
```

**Result Range:**
- `1.0` = Identical meaning
- `0.8-0.9` = Very similar
- `0.5-0.7` = Somewhat related
- `0.0-0.4` = Not related
- `-1.0` = Opposite meaning

**Real Usage in Project:**
```python
query = "What are the technical requirements?"
query_embedding = generate_embedding(query)

for doc_embedding in stored_embeddings:
    score = compute_similarity(query_embedding, doc_embedding)
    if score > 0.7:  # Found relevant document!
        return document
```

---

## 3️⃣ Local Vector Store (No Database!)

### **Concept:**
Store embeddings in a simple JSON file instead of complex vector database. Good for small-scale projects.

### **Files Involved:**

#### `backend/local_vector_store.py`
```python
class LocalVectorStore:
    def __init__(self, storage_dir="data/embeddings"):
        self.index_file = os.path.join(storage_dir, "index.json")
        self.index = {
            "chunks": [],        # Original text pieces
            "embeddings": [],    # Their 768-dim vectors
            "metadata": []       # Info like filename, chunk_id
        }
```

**Storage Structure (`index.json`):**
```json
{
  "chunks": [
    "The system must handle 1000 users...",
    "Security requirements include..."
  ],
  "embeddings": [
    [0.23, -0.45, 0.12, ..., 0.67],
    [-0.12, 0.34, -0.56, ..., 0.23]
  ],
  "metadata": [
    {"filename": "rfp.pdf", "chunk_id": 1},
    {"filename": "rfp.pdf", "chunk_id": 2}
  ]
}
```

**Search Process:**
```python
def search_similar(self, query: str, top_k: int = 5):
    # 1. Convert query to vector
    query_embedding = generate_embedding(query)
    
    # 2. Compare with ALL stored vectors
    similarities = []
    for stored_embedding in self.index["embeddings"]:
        score = compute_similarity(query_embedding, stored_embedding)
        similarities.append(score)
    
    # 3. Sort and return best matches
    return top_5_results
```

**Pros vs. Database:**
- ✅ Simple - just a JSON file
- ✅ No setup - works immediately
- ✅ Fast for small datasets (<10K chunks)
- ❌ Slow for large datasets (must compare ALL vectors)
- ❌ No advanced features (filtering, updates)

---

## 4️⃣ Document Chunking (Text Splitting)

### **Concept:**
Breaking large documents into smaller pieces for processing. Large texts overwhelm LLMs, so we split them strategically.

### **Files Involved:**

#### `backend/document_processing/chunking.py`

**Method 1: Simple Chunking**
```python
def chunk_text(text: str, max_tokens: int = 500) -> List[str]:
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), max_tokens):
        chunk = " ".join(words[i:i+max_tokens])
        chunks.append(chunk)
    
    return chunks
```

**What's happening:**
```
Original: "The system shall provide authentication. Users must login..."
         (5000 words)

Split into chunks of 500 words:
Chunk 1: "The system shall provide authentication. Users must..."
Chunk 2: "...login with credentials. The database shall store..."
Chunk 3: "...encrypted passwords. Security requirements include..."
```

**Method 2: Overlapping Chunks**
```python
def chunk_text_with_overlap(text: str, chunk_size: int = 700, overlap: int = 100):
    # Move 600 words forward each time (700 - 100 overlap)
    # Last 100 words of chunk N = first 100 words of chunk N+1
```

**Why Overlap?**
```
Without Overlap:
Chunk 1: "The user shall login with..." [ends]
Chunk 2: [starts] "...password and username"
❌ Lost context between chunks!

With Overlap:
Chunk 1: "The user shall login with password and username"
Chunk 2: "password and username. The system validates..."
✅ Context preserved!
```

**Real Usage:**
```python
# In pipeline.py
text = extract_text_from_pdf(file_path)  # 50,000 words
chunks = chunk_text(text, max_tokens=500)  # 100 chunks
# Each chunk processed separately by AI agents
```

---

## 5️⃣ Azure Document Intelligence (OCR + Text Extraction)

### **Concept:**
Cloud service that extracts text from PDFs, including scanned images (OCR = Optical Character Recognition).

### **Files Involved:**

#### `backend/document_processing/extract_text.py`
```python
from azure.ai.formrecognizer import DocumentAnalysisClient

def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    client = DocumentAnalysisClient(
        endpoint=config.FORM_RECOGNIZER_ENDPOINT,
        credential=AzureKeyCredential(config.FORM_RECOGNIZER_KEY)
    )
    
    # Send PDF to Azure
    poller = client.begin_analyze_document("prebuilt-read", file_bytes)
    result = poller.result()
    
    # Extract text from result
    full_text = "\n".join([
        line.content 
        for page in result.pages 
        for line in page.lines
    ])
    
    return full_text
```

**What Azure Does:**
1. **Receives PDF** (as bytes/binary data)
2. **Detects pages, layout, text regions**
3. **OCR for images** (if PDF contains scanned images)
4. **Extracts tables, forms** (preserves structure)
5. **Returns structured data** (pages → lines → words)

**Why Use Azure vs. Simple PDF Parser?**
```
Simple Parser (PyPDF2):
- Can't read scanned images ❌
- Misses tables ❌
- Poor formatting ❌
- Free ✅

Azure Document Intelligence:
- OCR for scanned docs ✅
- Table extraction ✅
- Layout preservation ✅
- Costs money (~$1.50 per 1000 pages) ❌
```

**Real Example:**
```
Input: Scanned RFP (image-based PDF)
Azure extracts: "The system shall provide real-time monitoring..."

Without OCR: [Binary gibberish, no text]
```

---

## 6️⃣ Multi-Agent System (Specialized AI Workers)

### **Concept:**
Instead of one AI doing everything, have multiple specialized AIs (agents) each expert in one task. Like a team where everyone has a role.

### **Files Involved:**

#### `backend/agents/base_agent.py`
```python
class BaseAgent(ABC):
    def __init__(self, llm: Callable, prompt_template: str):
        self.llm = llm  # Language model
        self.prompt_template = prompt_template  # Instructions
    
    @abstractmethod
    def extract(self, text: str) -> Any:
        """Each agent implements this differently"""
        pass
    
    def run(self, text: str) -> str:
        prompt = self.prompt_template.replace("{{input}}", text)
        response = self.llm(prompt)
        return response
```

#### `backend/agents/nfr_agent.py` (Example)
```python
class NFRAgent(BaseAgent):
    def extract(self, text: str) -> str:
        return self.run(text)
```

**The Team Structure:**
```
orchestrator.py (Manager)
    ├─ BusinessProcessAgent ("Find workflows")
    ├─ GapAgent ("Find missing requirements")
    ├─ PersonaAgent ("Identify users")
    ├─ PainPointsAgent ("Find problems")
    ├─ ImpactAgent ("Measure impact")
    ├─ ChallengesAgent ("List challenges")
    ├─ NFRAgent ("Extract non-functional requirements")
    ├─ ArchitectAgent ("Design architecture")
    ├─ ConstraintsAgent ("Find constraints")
    └─ AssumptionsAgent ("Document assumptions")
```

**How It Works:**

#### `backend/orchestrator.py`
```python
def run_all_agents(text: str) -> dict:
    memory = ShortTermMemory()
    
    agents = {
        "nfr": NFRAgent(LLM, open("prompts/nfr.txt").read()),
        "architecture": ArchitectAgent(LLM, open("prompts/architect.txt").read()),
        # ... 8 more agents
    }
    
    # Run each agent
    for name, agent in agents.items():
        print(f"Running {name} agent...")
        output = agent.extract(text)  # AI analysis
        memory.add(name, output)      # Store result
    
    return memory.get_all()
```

**Agent Specialization Example:**

**NFR Agent Prompt** (`prompts/nfr.txt`):
```
You are an expert in Non-Functional Requirements.
Analyze this RFP and extract:
- Performance requirements (response time, throughput)
- Security requirements
- Scalability needs
- Availability/uptime requirements
...
```

**Architecture Agent Prompt** (`prompts/architect.txt`):
```
You are a software architect.
Based on this RFP, recommend:
- System architecture (microservices, monolith, etc.)
- Technology stack
- Database design
- Integration patterns
...
```

**Why This Works:**
- Each agent focuses on ONE thing → better quality
- Specialized prompts → more accurate results
- Easy to add/remove agents
- Parallel processing possible (future optimization)

---

## 7️⃣ Prompt Engineering (Instructing AI)

### **Concept:**
Carefully crafted instructions that tell the LLM exactly what to do and how to format output.

### **Files Involved:**

#### `backend/prompts/nfr.txt` (Example)
```
You are an expert system analyst specializing in Non-Functional Requirements (NFRs).

Your task: Analyze the RFP document and extract ALL non-functional requirements.

Categories to identify:
1. Performance (response time, throughput, load)
2. Security (authentication, authorization, encryption)
3. Scalability (user growth, data volume)
4. Availability (uptime, disaster recovery)
5. Maintainability (code quality, documentation)
6. Usability (user experience, accessibility)

Output Format:
# Non-Functional Requirements

## Performance Requirements
- [Requirement 1]
- [Requirement 2]

## Security Requirements
- [Requirement 1]
...

Input RFP:
{{input}}
```

**Prompt Components:**

1. **Role Definition**
   ```
   "You are an expert system analyst..."
   ```
   → Sets context for LLM behavior

2. **Task Description**
   ```
   "Your task: Analyze the RFP document and extract..."
   ```
   → Clear objective

3. **Structured Instructions**
   ```
   "Categories to identify: 1. Performance 2. Security..."
   ```
   → Break down complex task

4. **Output Format**
   ```
   "Output Format: # Non-Functional Requirements..."
   ```
   → Ensures consistent structure

5. **Input Placeholder**
   ```
   "{{input}}"
   ```
   → Where document text goes

**Why This Matters:**
```
Bad Prompt:
"Find requirements in this document"
→ Vague, inconsistent output

Good Prompt (like ours):
"You are an expert... Extract these specific categories... 
Format as markdown with these sections..."
→ Specific, structured, repeatable
```

---

## 8️⃣ LLM Integration (Local Ollama)

### **Concept:**
Running Large Language Models (like ChatGPT) on your own computer instead of paying for API calls.

### **Files Involved:**

#### `backend/llm_client.py`
```python
from ollama import Client

client = Client()  # Connects to local Ollama server

def local_llm(prompt: str, model: str = "llama3") -> str:
    response = client.generate(model=model, prompt=prompt)
    return response['response']
```

**How It Works:**
```
1. Ollama runs as background service (like a mini web server)
2. Stores LLM models locally (~4.7 GB for llama3)
3. Python code sends text to Ollama
4. Ollama runs inference (AI thinking)
5. Returns generated text
```

**Process Flow:**
```python
# Agent wants to analyze text
agent.run("Extract requirements from: The system shall...")

# Goes through llm_client.py
local_llm("You are an expert... Extract requirements from: The system shall...")

# Ollama receives prompt
# LLaMA 3 model processes it (takes 2-3 min)
# Returns: "Requirements: 1. System must provide... 2. Users can..."
```

**Local vs. Cloud LLM:**

| Aspect | Local (Ollama) | Cloud (OpenAI API) |
|--------|----------------|-------------------|
| **Cost** | Free | $0.002 per 1K tokens |
| **Privacy** | Complete | Data sent to servers |
| **Speed** | Slower (CPU/GPU dependent) | Faster (powerful servers) |
| **Setup** | Download model (4.7 GB) | Get API key |
| **Offline** | ✅ Works offline | ❌ Needs internet |

**Our Choice:** Local Ollama because:
- No API costs (important for testing)
- Complete data privacy (RFPs often confidential)
- Good enough quality for our use case

---

## 9️⃣ Short-Term Memory (State Management)

### **Concept:**
Temporary storage to hold data while processing. Like RAM in a computer - fast but temporary.

### **Files Involved:**

#### `backend/memory/short_term_memory.py`
```python
class ShortTermMemory:
    def __init__(self):
        self.memory = {}  # Simple dictionary
    
    def add(self, key: str, value: Any):
        self.memory[key] = value
    
    def get(self, key: str) -> Any:
        return self.memory.get(key)
    
    def get_all(self) -> dict:
        return self.memory
    
    def clear(self):
        self.memory = {}
```

**Usage in Pipeline:**
```python
# orchestrator.py
memory = ShortTermMemory()

# Agent 1 runs
result1 = business_process_agent.extract(text)
memory.add("business_process", result1)

# Agent 2 runs
result2 = gap_agent.extract(text)
memory.add("gap_analysis", result2)

# ... 8 more agents

# Finally, save all results
all_results = memory.get_all()
save_to_kb(all_results)  # Write to kb.md file
```

**Why Not Just a Dict?**
- Abstraction: Can change implementation later (e.g., add to database)
- Clear interface: `add()`, `get()`, `clear()`
- Easy to extend: Add features like `get_recent()`, `search()`

**Real Example:**
```python
Memory State During Processing:
{
  "business_process": "## Business Processes\n1. User registration...",
  "gap_analysis": "## Gaps\n1. Missing authentication...",
  "personas": "## User Personas\n1. Admin - manages system..."
  # ... more agents add their results
}

After All Agents Complete:
→ Save to kb.md
→ Clear memory for next document
```

---

## 🔟 RESTful API (Frontend-Backend Communication)

### **Concept:**
Web API that follows REST principles - using HTTP methods (GET, POST) to communicate between frontend and backend.

### **Files Involved:**

#### `backend/api.py`
```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/api/process")
async def process_document(file: UploadFile = File(...)):
    # 1. Receive uploaded file
    content = await file.read()
    
    # 2. Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    
    # 3. Process through pipeline
    process_rfp_document(file_path=tmp_path)
    
    # 4. Read results
    kb_content = open("kb.md").read()
    
    # 5. Return to frontend
    return {"success": True, "output": kb_content}
```

#### `ui/src/App.jsx`
```javascript
const handleUpload = async () => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await fetch('http://localhost:8000/api/process', {
        method: 'POST',
        body: formData
    })
    
    const data = await response.json()
    setResult(data.output)  // Display in UI
}
```

**REST Principles Used:**

1. **Resource-Based URLs**
   ```
   /api/process    → Process a document
   /api/kb         → Get knowledge base
   ```

2. **HTTP Methods with Meaning**
   ```
   POST /api/process  → Create/process new document
   GET /api/kb        → Retrieve existing data
   ```

3. **Stateless**
   - Each request independent
   - No session tracking needed

4. **JSON Responses**
   ```json
   {
     "success": true,
     "message": "Processed document.pdf",
     "output": "# Analysis\n..."
   }
   ```

**CORS (Cross-Origin Resource Sharing):**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Why needed:** Browser security blocks requests from one domain (localhost:5173) to another (localhost:8000) unless explicitly allowed.

---

## 1️⃣1️⃣ Async/Await (Non-Blocking Operations)

### **Concept:**
Code that doesn't wait/block while doing slow operations (like file uploads). Allows server to handle multiple requests simultaneously.

### **Files Involved:**

#### `backend/api.py`
```python
@app.post("/api/process")
async def process_document(file: UploadFile = File(...)):
    content = await file.read()  # Doesn't block server!
    # ... rest of processing
```

**How It Works:**

**Synchronous (Blocking):**
```python
def process(file):
    content = file.read()  # Wait here (10 seconds)
    # Server frozen, can't handle other requests!
    process_content(content)
```

**Asynchronous (Non-Blocking):**
```python
async def process(file):
    content = await file.read()  # Start reading, but...
    # Server can handle other requests while reading!
    await process_content(content)
```

**Visual Example:**
```
Synchronous:
Request 1: ████████████ (12 sec) → Done
Request 2:                         ████████████ (12 sec) → Done
Total: 24 seconds

Asynchronous:
Request 1: ████████████ (12 sec) → Done
Request 2: ████████████ (12 sec) → Done
Total: 12 seconds (both processed simultaneously!)
```

**In Our Project:**
- File uploads are async (reading PDF bytes)
- API responds immediately while processing in background
- UI shows loading state during processing

---

## 1️⃣2️⃣ Pipeline Architecture (Sequential Processing)

### **Concept:**
Data flows through multiple stages, each transforming it. Like an assembly line - each station does one job.

### **Files Involved:**

#### `backend/pipeline.py`
```python
def process_rfp_document(file_path: str):
    # Stage 1: Extract
    text = extract_text_from_pdf_bytes(file_bytes)
    
    # Stage 2: Chunk
    chunks = chunk_text(text, max_tokens=500)
    
    # Stage 3: Embed
    embeddings = [generate_embedding(chunk) for chunk in chunks]
    
    # Stage 4: Store
    vector_store.add_chunks(chunks, embeddings)
    
    # Stage 5: Analyze
    results = run_all_agents(chunks[0])
    
    # Stage 6: Save
    save_to_kb(results)
```

**Pipeline Visualization:**
```
PDF File (Input)
    ↓
[Extract Text] → Plain text string
    ↓
[Chunk Text] → List of text pieces
    ↓
[Generate Embeddings] → List of vectors
    ↓
[Store Vectors] → Saved in JSON
    ↓
[Run Agents] → Analysis results
    ↓
[Save KB] → kb.md file
    ↓
Knowledge Base (Output)
```

**Benefits:**
- **Clear flow:** Easy to understand what happens when
- **Modularity:** Change one stage without affecting others
- **Testability:** Test each stage independently
- **Error handling:** Know exactly where failures occur

---

## 📊 How Everything Connects

```
USER UPLOADS PDF
       ↓
[React UI - App.jsx]
  - Drag & drop
  - FormData with file
       ↓
[FastAPI - api.py]
  - Receives upload
  - Saves temp file
       ↓
[Pipeline - pipeline.py]
       ↓
   ┌───┴───┐
   ↓       ↓
[Azure Doc Intelligence]  [Chunking]
extract_text.py          chunking.py
   ↓                        ↓
  Text                   Chunks
       ↓
[Embedder - embedder.py]
  - Sentence Transformers
  - Generate 768-dim vectors
       ↓
[Vector Store - local_vector_store.py]
  - Save to JSON
  - Enable semantic search
       ↓
[Orchestrator - orchestrator.py]
  - Loads 10 agents
  - Each agent has specific prompt
       ↓
[Agents - agents/*.py]
  - BaseAgent pattern
  - Each extracts specific info
       ↓
[LLM Client - llm_client.py]
  - Sends prompts to Ollama
  - Gets AI responses
       ↓
[Memory - short_term_memory.py]
  - Collects all agent outputs
       ↓
[Save KB - orchestrator.py]
  - Write kb.md file
       ↓
[API Response - api.py]
  - Return KB content as JSON
       ↓
[React UI - App.jsx]
  - Display results
       ↓
USER SEES ANALYSIS
```

---

## 🎯 Summary: Concept → File Mapping

| Concept | Primary Files | Purpose |
|---------|---------------|---------|
| **Vector Embeddings** | `embedding/embedder.py` | Convert text to 768 numbers |
| **Cosine Similarity** | `embedding/embedder.py` | Compare vector similarity |
| **Vector Storage** | `local_vector_store.py` | Store embeddings in JSON |
| **Document Chunking** | `document_processing/chunking.py` | Split large texts |
| **OCR/Text Extraction** | `document_processing/extract_text.py` | Extract from PDFs |
| **Multi-Agent System** | `agents/*.py`, `orchestrator.py` | Specialized AI workers |
| **Prompt Engineering** | `prompts/*.txt` | Instruct LLMs effectively |
| **Local LLM** | `llm_client.py` | Run AI locally (Ollama) |
| **Memory Management** | `memory/short_term_memory.py` | Temporary data storage |
| **REST API** | `api.py` | Frontend-backend communication |
| **Async Processing** | `api.py` | Non-blocking operations |
| **Pipeline** | `pipeline.py` | Sequential processing stages |

Each concept has a clear purpose and implementation. Understanding these building blocks helps you explain how the entire system works! 🚀
