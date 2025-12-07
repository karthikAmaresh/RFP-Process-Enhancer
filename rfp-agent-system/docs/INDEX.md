# Documentation Index

Quick reference to all project documentation.

## 📖 Core Documentation

### [README.md](../README.md)
**Main project overview** - Features, quick start, and basic usage

### [SETUP.md](SETUP.md)
**Complete setup guide** - Step-by-step installation and configuration

### [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
**Project architecture** - File structure and component organization

### [ARCHITECTURE.md](ARCHITECTURE.md)
**Technical design** - System architecture and design decisions

---

## 🚀 Getting Started

**New users start here:**
1. Read [README.md](../README.md) for overview
2. Follow [SETUP.md](SETUP.md) for installation
3. Process your first document
4. View results in `backend/kb.md`

---

## 📁 File Organization

```
rfp-agent-system/
├── README.md                  # Main documentation
├── docs/
│   ├── INDEX.md              # This file
│   ├── SETUP.md              # Setup instructions
│   ├── PROJECT_STRUCTURE.md  # File structure
│   └── ARCHITECTURE.md       # Technical design
├── backend/
│   ├── agents/               # 10 AI agents
│   ├── prompts/              # Prompt templates
│   ├── pipeline.py           # Main script
│   └── verify_setup.py       # Setup verification
├── kb.md                     # Generated output
└── *.pdf                     # Input documents
```

---

## 🔍 Quick Reference

### Process a Document
```bash
python backend/pipeline.py --file "document.pdf"
```

### Verify Setup
```bash
cd backend
python verify_setup.py
```

### View Results
Check `backend/kb.md` for analysis from all 10 agents

---

## 📝 What's in Each Doc

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **README** | Project overview | First time viewing project |
| **SETUP** | Installation guide | Setting up the system |
| **PROJECT_STRUCTURE** | File organization | Understanding codebase |
| **ARCHITECTURE** | Technical design | Development/customization |

---

## 💡 Common Tasks

### First Time Setup
→ Read: [SETUP.md](SETUP.md)

### Understanding the Code
→ Read: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

### Adding New Features
→ Read: [ARCHITECTURE.md](ARCHITECTURE.md)

### Troubleshooting
→ Check: [SETUP.md](SETUP.md) → Troubleshooting section

---

## 🎯 The 10 AI Agents

All agents are documented in [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md):
1. Business Process
2. Gap Analysis
3. Personas
4. Pain Points
5. Impact Assessment
6. Challenges
7. Non-Functional Requirements
8. Solution Architecture
9. Constraints
10. Assumptions

---

**Need help?** Start with [SETUP.md](SETUP.md) troubleshooting section.
