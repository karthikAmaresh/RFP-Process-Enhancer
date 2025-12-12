import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Use your Foundry project URL
def get_foundry_project_client():
    credential = DefaultAzureCredential()
    project_url = os.getenv("FOUNDRY_PROJECT_URL", "https://rfp-process-enhancer-resource.services.ai.azure.com/api/projects/rfp-foundry")
    return AIProjectClient(endpoint=project_url, credential=credential)

class FoundryAgentManager:
    def __init__(self):
        self.client = get_foundry_project_client()
        self.agents = {}

    def create_agent(self, name, instructions, model="gpt-4o", tools=None, tool_resources=None):
        agent = self.client.agents.create_agent(
            model=model,
            name=name,
            instructions=instructions,
            tools=tools or [],
            tool_resources=tool_resources or None,
        )
        self.agents[name] = agent
        return agent

    def create_thread(self):
        return self.client.agents.create_thread()

    def send_message(self, thread_id, user_input, attachments=None):
        return self.client.agents.create_message(
            thread_id=thread_id,
            role="user",
            content=user_input,
            attachments=attachments or []
        )

    def run_agent(self, thread_id, agent_id):
        run = self.client.agents.create_and_process_run(thread_id=thread_id, agent_id=agent_id)
        return run

    def get_agent_response(self, thread_id):
        messages = self.client.agents.list_messages(thread_id=thread_id)
        for msg in messages.data:
            if msg.role == "assistant":
                return msg.content[0].text.value
        return None

    def delete_agent(self, agent_id):
        self.client.agents.delete_agent(agent_id)

    def delete_thread(self, thread_id):
        self.client.agents.delete_thread(thread_id)
