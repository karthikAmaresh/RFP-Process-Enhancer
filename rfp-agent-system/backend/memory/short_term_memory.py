class ShortTermMemory:
    def __init__(self):
        self.store = {}

    def add(self, agent_name, output):
        self.store[agent_name] = output

    def get_all(self):
        return self.store
