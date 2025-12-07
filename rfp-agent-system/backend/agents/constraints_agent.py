from agents.base_agent import BaseAgent

class ConstraintsAgent(BaseAgent):
    """Constraints and Limitations Agent"""
    def extract(self, text):
        return self.run(text)
