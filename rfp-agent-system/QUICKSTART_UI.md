# RFP Process Enhancer UI - Quick Start

## 🚀 Running the Application

### Prerequisites
- Python 3.9+ with all backend dependencies installed
- Node.js 18+ with npm
- Ollama running with llama3 model
- Azure Document Intelligence configured (optional, can use local processing)

### Start Backend (Terminal 1)

```powershell
# From RFP-Process-Enhancer folder:
cd rfp-agent-system\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn api:app --reload --port 8000
```

✅ Backend running at: **http://localhost:8000**  
📚 API Docs at: **http://localhost:8000/docs**

### Start Frontend (Terminal 2)

```powershell
# From RFP-Process-Enhancer folder:
cd rfp-agent-system\ui
npm run dev
```

✅ Frontend running at: **http://localhost:5173**

## 📖 How to Use

1. Open `http://localhost:5173` in your browser
2. Drag & drop your RFP PDF or click to browse
3. Click "Process Document"
4. Wait for AI agents to analyze (progress shown in real-time)
5. View comprehensive analysis results

## 🎯 Features

- **Drag & Drop Upload** - Easy file upload interface
- **Real-time Progress** - See processing stages as they happen
- **10 AI Agents** - Comprehensive analysis from multiple perspectives
- **Beautiful Results** - Clean, readable output display
- **Modern UI** - Responsive design with Tailwind CSS

## 🔧 Troubleshooting

**Backend won't start?**
- Check if port 8000 is available
- Ensure all Python packages are installed: `pip install -r requirements.txt`
- Verify Ollama is running: `ollama list`

**Frontend won't start?**
- Check if port 5173 is available
- Run `npm install` if packages are missing
- Clear cache: `npm run dev -- --force`

**Processing fails?**
- Ensure PDF is not password-protected
- Check backend terminal for error messages
- Verify Azure credentials in `.env` (if using Azure)

## 📊 Processing Pipeline

```
Upload PDF → Extract Text → Chunk Document → Create Embeddings →
Run 10 AI Agents → Generate Knowledge Base → Display Results
```

## 🤖 AI Agents

1. **Business Process** - Identifies workflows and processes
2. **Gap Analysis** - Finds gaps and missing requirements
3. **Persona** - Defines user personas and stakeholders
4. **Pain Points** - Identifies customer pain points
5. **Impact** - Analyzes business impact
6. **Challenges** - Documents challenges and risks
7. **NFR** - Non-functional requirements
8. **Architecture** - Technical architecture recommendations
9. **Constraints** - System constraints and limitations
10. **Assumptions** - Key assumptions and dependencies
