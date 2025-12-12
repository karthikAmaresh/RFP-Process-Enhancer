

from foundry_agent_manager import FoundryAgentManager
import os

PROMPT_FILES = [
    ("Introduction Agent", "introduction.txt"),
    ("Challenges Agent", "challenges.txt"),
    ("Pain Points Agent", "pain_points.txt"),
    ("Business Process Agent", "business_process.txt"),
    ("Gap Analysis Agent", "gap.txt"),
    ("Personas Agent", "persona.txt"),
    ("Constraints Agent", "constraints.txt"),
    ("Functional Requirements Agent", "functional_requirements.txt"),
    ("NFR Agent", "nfr.txt"),
    ("Architecture Agent", "architect.txt"),
    ("Assumptions Agent", "assumptions.txt"),
    ("Impact Agent", "impact.txt"),
]

PROMPT_DIR = os.path.join(os.path.dirname(__file__), "prompts")

def load_prompt(filename):
    path = os.path.join(PROMPT_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return f.read()

AGENT_DEFINITIONS = [
    {"name": name, "instructions": load_prompt(prompt_file)}
    for name, prompt_file in PROMPT_FILES
]

class FoundryOrchestrator:
    def __init__(self):
        self.manager = FoundryAgentManager()
        self.agent_objs = {}
        for agent_def in AGENT_DEFINITIONS:
            agent = self.manager.create_agent(
                name=agent_def["name"],
                instructions=agent_def["instructions"]
            )
            self.agent_objs[agent_def["name"]] = agent

    def run_all_agents(self, rfp_text):
        results = {}
        for agent_def in AGENT_DEFINITIONS:
            agent_name = agent_def["name"]
            agent = self.agent_objs[agent_name]
            thread = self.manager.create_thread()
            self.manager.send_message(thread.id, rfp_text)
            run = self.manager.run_agent(thread.id, agent.id)
            if run.status == "failed":
                results[agent_name] = f"Run failed: {run.last_error}"
            else:
                response = self.manager.get_agent_response(thread.id)
                results[agent_name] = response
            self.manager.delete_thread(thread.id)
        return results

    def cleanup(self):
        for agent in self.agent_objs.values():
            self.manager.delete_agent(agent.id)
