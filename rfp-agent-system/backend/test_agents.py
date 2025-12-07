from agents.business_process_agent import BusinessProcessAgent
from agents.gap_agent import GapAgent
from llm_client import local_llm
from memory.short_term_memory import ShortTermMemory

llm = local_llm

bp_agent = BusinessProcessAgent(llm, open("prompts/business_process.txt").read())
gap_agent = GapAgent(llm, open("prompts/gap.txt").read())

text = open("data/chunks/chunk_1.txt").read()

bp_output = bp_agent.extract(text)
gap_output = gap_agent.extract(text)

memory = ShortTermMemory()
memory.add("business_process", bp_output)
memory.add("gap_analysis", gap_output)

print("=== Business Process Analysis ===")
print(bp_output)
print("\n=== Gap Analysis ===")
print(gap_output)
print("\n=== Memory Store ===")
print(memory.get_all())
