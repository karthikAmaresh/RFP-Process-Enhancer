from agents.base_agent import BaseAgent

class GapAgent(BaseAgent):
    def extract(self, text):
        return self.run(text)
