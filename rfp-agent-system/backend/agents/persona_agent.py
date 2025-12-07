from agents.base_agent import BaseAgent

class PersonaAgent(BaseAgent):
    def extract(self, text):
        return self.run(text)
