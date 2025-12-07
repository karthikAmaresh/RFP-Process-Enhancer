from agents.base_agent import BaseAgent

class NFRAgent(BaseAgent):
    """Non-Functional Requirements Agent"""
    def extract(self, text):
        return self.run(text)
