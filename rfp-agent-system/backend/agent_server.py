"""
Generic FastAPI server for individual RFP agents.
Each agent runs as a microservice accepting text and returning analysis.
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import sys

# Import agent classes
from agents.introduction_agent import IntroductionAgent
from agents.business_process_agent import BusinessProcessAgent
from agents.gap_agent import GapAgent
from agents.persona_agent import PersonaAgent
from agents.pain_point_agent import PainPointsAgent
from agents.impact_agent import ImpactfulStatementsAgent
from agents.challenge_agent import ChallengesAgent
from agents.functional_requirements_agent import FunctionalRequirementsAgent
from agents.nfr_agent import NFRAgent
from agents.architect_agent import ArchitectAgent
from agents.constraints_agent import ConstraintsAgent
from agents.assumptions_agent import AssumptionsAgent
from llm_client import LLMClient
from memory.short_term_memory import ShortTermMemory

# Get agent type from environment variable
AGENT_TYPE = os.getenv("AGENT_TYPE", "introduction")

# Initialize FastAPI app
app = FastAPI(title=f"RFP {AGENT_TYPE.title()} Agent")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM client
try:
    llm_client = LLMClient()
    LLM = llm_client.generate
    print(f"✓ LLM client initialized, generate method: {type(LLM)}")
except Exception as e:
    print(f"ERROR initializing LLM client: {e}")
    import traceback
    traceback.print_exc()
    raise

# Load prompt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")

# Map agent types to classes and prompt files
AGENT_MAP = {
    "introduction": (IntroductionAgent, "introduction.txt"),
    "challenges": (ChallengesAgent, "challenges.txt"),
    "pain_points": (PainPointsAgent, "pain_points.txt"),
    "business_process": (BusinessProcessAgent, "business_process.txt"),
    "gap": (GapAgent, "gap.txt"),
    "personas": (PersonaAgent, "persona.txt"),
    "constraints": (ConstraintsAgent, "constraints.txt"),
    "functional_requirements": (FunctionalRequirementsAgent, "functional_requirements.txt"),
    "nfr": (NFRAgent, "nfr.txt"),
    "architecture": (ArchitectAgent, "architect.txt"),
    "assumptions": (AssumptionsAgent, "assumptions.txt"),
    "impact": (ImpactfulStatementsAgent, "impact.txt"),
}

# Initialize agent
if AGENT_TYPE not in AGENT_MAP:
    raise ValueError(f"Unknown agent type: {AGENT_TYPE}")

agent_class, prompt_file = AGENT_MAP[AGENT_TYPE]
with open(os.path.join(PROMPTS_DIR, prompt_file), "r") as f:
    prompt_text = f.read()

print(f"✓ Creating agent: {agent_class.__name__}")
print(f"✓ LLM type: {type(LLM)}, callable: {callable(LLM)}")
agent = agent_class(LLM, prompt_text)
print(f"✓ Agent created: {type(agent)}")
memory = ShortTermMemory()

# Request/Response models
class AnalysisRequest(BaseModel):
    text: str
    context: Dict[str, Any] = {}

class AnalysisResponse(BaseModel):
    agent: str
    result: str
    error: str = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": AGENT_TYPE,
        "service": f"RFP {AGENT_TYPE.title()} Agent"
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest):
    """
    Analyze RFP text using this agent.
    
    Args:
        request: AnalysisRequest with text and optional context
        
    Returns:
        AnalysisResponse with analysis result
    """
    try:
        # Store context in memory if provided
        for key, value in request.context.items():
            memory.add(key, value)
        
        # Run agent analysis
        print(f"  • Running {AGENT_TYPE} agent...")
        result = agent.extract(request.text)
        
        # Store result in memory
        memory.add(AGENT_TYPE, result)
        
        return AnalysisResponse(
            agent=AGENT_TYPE,
            result=result
        )
    except Exception as e:
        print(f"Error in {AGENT_TYPE} agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Kubernetes-style health check"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
