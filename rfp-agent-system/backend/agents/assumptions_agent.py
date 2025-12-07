from agents.base_agent import BaseAgent

class AssumptionsAgent(BaseAgent):
    """Assumptions and Dependencies Agent"""
    def extract(self, text):
        return self.run(text)
