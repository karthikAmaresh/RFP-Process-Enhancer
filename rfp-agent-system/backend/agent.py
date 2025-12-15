import os
from pathlib import Path
import re
from openai import AzureOpenAI
import json
from mcp.server.fastmcp import FastMCP
import inspect

# Initialize FastMCP server
mcp = FastMCP("Context Reader Agent")

# Global variable to store parsed context
context_sections = {}

# Global variable to store memory
memory_content = ""
memory_file_path = Path(__file__).parent / "data/memory/" / "memory.md"

def parse_markdown(file_path):
    """Parse markdown file into sections based on headings."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = {}
    current_section = None
    current_content = []
    
    for line in content.split('\n'):
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = heading_match.group(2).strip()
            current_content = []
        else:
            current_content.append(line)
    
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections

@mcp.tool()
def get_section_content(section_name: str) -> str:
    """
    Get the content from a specific section in the context document.
    
    Args:
        section_name: The name of the section to retrieve
    
    Returns:
        The content of the requested section
    """
    for key, value in context_sections.items():
        if key.lower() == section_name.lower():
            return value
    
    available = ', '.join(context_sections.keys())
    return f"Section '{section_name}' not found. Available sections: {available}"

@mcp.tool()
def list_sections() -> list:
    """
    List all available sections in the context document.
    
    Returns:
        A list of all section names
    """
    return list(context_sections.keys())

@mcp.tool()
def search_in_context(query: str) -> dict:
    """
    Search for specific information across all sections in the context.
    
    Args:
        query: The search query to find in the context
    
    Returns:
        A dictionary with section names as keys and matching content as values
    """
    results = {}
    query_lower = query.lower()
    
    for section, content in context_sections.items():
        if query_lower in content.lower():
            results[section] = content
    
    if not results:
        return {"message": f"No results found for '{query}'"}
    
    return results

@mcp.tool()
def get_memory() -> str:
    """
    Retrieve all stored memories from previous interactions.
    
    Returns:
        The complete memory content showing past experiences and learned facts
    """
    global memory_content
    if not memory_content or memory_content.strip() == "":
        return "No memories stored yet."
    return memory_content

@mcp.tool()
def record_memory(category: str, content: str) -> str:
    """
    Record a new memory or fact learned from the current interaction.
    
    Args:
        category: The category of the memory (e.g., 'User Preferences', 'Common Questions', 'Clarifications', 'Insights')
        content: The memory content to record
    
    Returns:
        Confirmation message
    """
    global memory_content, memory_file_path
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create memory entry
    memory_entry = f"\n### {category}\n**Recorded:** {timestamp}\n{content}\n"
    
    # Append to memory content
    memory_content += memory_entry
    
    # Write to file
    if memory_file_path and os.path.exists(os.path.dirname(memory_file_path)):
        with open(memory_file_path, 'a', encoding='utf-8') as f:
            f.write(memory_entry)
    
    return f"Memory recorded successfully under category '{category}'"

class ContextAgent:
    def __init__(self, context_file_path, memory_file="data/memory/memory.md", azure_endpoint=None, api_key=None, api_version="2024-08-01-preview", deployment_name=None):
        """Initialize the agent with a context file, memory file, and Azure OpenAI credentials."""
        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=api_key or os.getenv("AZURE_OPENAI_KEY"),
            api_version=api_version
        )
        self.deployment_name = deployment_name or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
        
        global context_sections, memory_content, memory_file_path
        context_sections = parse_markdown(context_file_path)
        
        # Load memory
        memory_file_path = memory_file
        if os.path.exists(memory_file_path):
            with open(memory_file_path, 'r', encoding='utf-8') as f:
                memory_content = f.read()
        else:
            # Create memory directory and file if it doesn't exist
            os.makedirs(os.path.dirname(memory_file_path), exist_ok=True)
            memory_content = "# Agent Memory\n\nThis file stores learned experiences and facts from past interactions.\n"
            with open(memory_file_path, 'w', encoding='utf-8') as f:
                f.write(memory_content)
        
        # Get MCP tools in OpenAI format (sync version)
        self.tools = self._convert_mcp_tools_to_openai_sync()
    
    def _convert_mcp_tools_to_openai_sync(self):
        """Convert FastMCP tools to OpenAI function format (synchronous)."""
        tools = []
        # Get the MCP tool functions directly
        tool_functions = {
            'get_section_content': get_section_content,
            'list_sections': list_sections,
            'search_in_context': search_in_context,
            'get_memory': get_memory,
            'record_memory': record_memory
        }
        
        for tool_name, tool_func in tool_functions.items():
            # Extract function signature and docstring
            sig = inspect.signature(tool_func)
            doc = inspect.getdoc(tool_func) or ""
            
            # Parse parameters
            parameters = {
                "type": "object",
                "properties": {},
                "required": []
            }
            
            for param_name, param in sig.parameters.items():
                param_type = "string"  # Default type
                
                # Try to get type from annotation
                if param.annotation != inspect.Parameter.empty:
                    if param.annotation == str:
                        param_type = "string"
                    elif param.annotation == int:
                        param_type = "integer"
                    elif param.annotation == bool:
                        param_type = "boolean"
                    elif "list" in str(param.annotation):
                        param_type = "array"
                    elif "dict" in str(param.annotation):
                        param_type = "object"
                
                parameters["properties"][param_name] = {
                    "type": param_type,
                    "description": f"Parameter: {param_name}"
                }
                
                # Add to required if no default value
                if param.default == inspect.Parameter.empty:
                    parameters["required"].append(param_name)
            
            tools.append({
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": doc.split('\n')[0] if doc else f"Tool: {tool_name}",
                    "parameters": parameters
                }
            })
        
        return tools
    
    def _execute_mcp_tool(self, function_name, arguments):
        """Execute an MCP tool."""
        # Get the MCP tool functions directly
        tool_functions = {
            'get_section_content': get_section_content,
            'list_sections': list_sections,
            'search_in_context': search_in_context,
            'get_memory': get_memory,
            'record_memory': record_memory
        }
        
        if function_name in tool_functions:
            tool_func = tool_functions[function_name]
            print(f"Executing MCP tool: {function_name} with arguments: {arguments}")
            try:
                result = tool_func(**arguments)
                return result
            except Exception as e:
                return f"Error executing {function_name}: {str(e)}"
        else:
            return f"Unknown function: {function_name}"
    
    def chat(self, user_question, history=None) -> str:
        """Main chat function that uses GPT-4o with MCP tools."""
        messages = [
            {
                "role": "system",
                "content": """
                You are a helpful assistant that answers questions based on a context document.
                # Tools:
                    get_section_content
                    list_sections
                    search_in_context
                    get_memory
                    record_memory
                # Instructions:
                    You can use the provided tools to retrieve information from the context.
                    You also have access to memory of past interactions. 
                    When you didn't get any information, use the available tools to retrieve information from the context and memory to answer user questions accurately.
                    Record important facts, user preferences, common questions, and insights in memory to improve your responses over time.
                    Always check memory at the start of conversations to provide personalized and context-aware responses.
                """
            }
        ]
        
        # Append conversation history if provided
        if history:
            for message in history:
                messages.append(message)
        
        # Add current user question
        messages.append({
            "role": "user",
            "content": user_question + ". Think step-by-step and use the tools when necessary and derive the answer based on the available information."
        })
        
        # First API call
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        messages.append(response_message)
        
        # Handle tool calls
        while response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"\n🔧 Calling MCP tool: {function_name}")
                print(f"   Arguments: {function_args}")
                
                # Execute MCP tool
                function_response = self._execute_mcp_tool(function_name, function_args)
                
                print(f"   Result: {str(function_response)[:100]}...")
                
                # Add function response to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(function_response) if isinstance(function_response, (dict, list)) else str(function_response)
                })
            
            # Get next response
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            messages.append(response_message)
        
        return response_message.content


# Example usage
if __name__ == "__main__":
    # Create a sample context file
    os.makedirs("context", exist_ok=True)
    
    # Initialize agent
    print("Initializing Context Agent with FastMCP tools...")
    agent = ContextAgent("context/kb.md")
    
    # Example questions
    questions = [
        "What products does the company offer?",
        "How can I contact the company?",
        "Tell me about the team",
        "What are the pricing details?"
    ]
    
    for question in questions:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}")
        answer = agent.chat(question)
        print(f"\nAnswer: {answer}\n")