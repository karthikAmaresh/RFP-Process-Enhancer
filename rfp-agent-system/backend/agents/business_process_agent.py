from agents.base_agent import BaseAgent

class BusinessProcessAgent(BaseAgent):
    def extract(self, text):
        return self.run(text)
