import os
from memory.short_term_memory import ShortTermMemory
from agents.business_process_agent import BusinessProcessAgent
from agents.gap_agent import GapAgent
from agents.persona_agent import PersonaAgent
from agents.pain_point_agent import PainPointsAgent
from agents.impact_agent import ImpactfulStatementsAgent
from agents.challenge_agent import ChallengesAgent
from agents.nfr_agent import NFRAgent
from agents.architect_agent import ArchitectAgent
from agents.constraints_agent import ConstraintsAgent
from agents.assumptions_agent import AssumptionsAgent
from llm_client import local_llm

llm = local_llm

# Get the directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")

def run_all_agents(text):
    """
    Run all RFP analysis agents on the given text
    
    Args:
        text: RFP document text or chunk
        
    Returns:
        dict: All agent outputs stored in memory
    """
    memory = ShortTermMemory()

    agents = {
        "business_process": BusinessProcessAgent(llm, open(os.path.join(PROMPTS_DIR, "business_process.txt")).read()),
        "gap": GapAgent(llm, open(os.path.join(PROMPTS_DIR, "gap.txt")).read()),
        "personas": PersonaAgent(llm, open(os.path.join(PROMPTS_DIR, "persona.txt")).read()),
        "pain_points": PainPointsAgent(llm, open(os.path.join(PROMPTS_DIR, "pain_points.txt")).read()),
        "impact": ImpactfulStatementsAgent(llm, open(os.path.join(PROMPTS_DIR, "impact.txt")).read()),
        "challenges": ChallengesAgent(llm, open(os.path.join(PROMPTS_DIR, "challenges.txt")).read()),
        "nfr": NFRAgent(llm, open(os.path.join(PROMPTS_DIR, "nfr.txt")).read()),
        "architecture": ArchitectAgent(llm, open(os.path.join(PROMPTS_DIR, "architect.txt")).read()),
        "constraints": ConstraintsAgent(llm, open(os.path.join(PROMPTS_DIR, "constraints.txt")).read()),
        "assumptions": AssumptionsAgent(llm, open(os.path.join(PROMPTS_DIR, "assumptions.txt")).read()),
    }

    for name, agent in agents.items():
        print(f"Running {name} agent...")
        output = agent.extract(text)
        memory.add(name, output)

    return memory.get_all()


def save_to_kb(memory_output):
    with open("kb.md", "w") as f:
        for key, value in memory_output.items():
            f.write(f"## {key.upper()}\n")
            f.write(value + "\n\n")


if __name__ == "__main__":
    # Test with sample text
    text = open("data/chunks/chunk_1.txt").read()
    results = run_all_agents(text)
    
    print("=== All Agent Results ===")
    for agent_name, output in results.items():
        print(f"\n--- {agent_name.upper()} ---")
        print(output)
    
    # Save to knowledge base
    save_to_kb(results)
    print("\n✓ Results saved to kb.md")
