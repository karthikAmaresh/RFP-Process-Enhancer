from agents.base_agent import BaseAgent

class ArchitectAgent(BaseAgent):
    """Architecture Requirements Agent"""
    def extract(self, text):
        return self.run(text)
