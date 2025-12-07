from ollama import Client
client = Client()

def local_llm(prompt):
    response = client.generate(model="llama3", prompt=prompt)
    return response['response']
