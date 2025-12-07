# Agent for generating RFP summaries
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import Dict, Any, List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Initialize Azure OpenAI (optional)
llm = None
if config.AZURE_OPENAI_ENDPOINT and config.AZURE_OPENAI_API_KEY and config.AZURE_OPENAI_DEPLOYMENT:
    try:
        llm = AzureChatOpenAI(
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            api_key=config.AZURE_OPENAI_API_KEY,
            deployment_name=config.AZURE_OPENAI_DEPLOYMENT,
            api_version="2024-02-15-preview",
            temperature=0.3
        )
    except Exception as e:
        print(f"Warning: Could not initialize Azure OpenAI client: {e}")


class BusinessProcessAgent:
    """
    Extract Business Process: Understand what the system does today
    """
    
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert business analyst specializing in understanding existing business processes and systems."),
            ("user", """Analyze the following RFP content and extract information about the current business process.

Focus on:
- What the current system does
- Key functionalities and workflows
- Business operations and activities
- Current system capabilities

RFP Content:
{content}

Provide a structured analysis of the current business process.""")
        ])
    
    def analyze(self, content: str) -> Dict[str, Any]:
        if not llm:
            return {
                "agent": "Business Process",
                "responsibility": "Understand what the system does today",
                "analysis": "Azure OpenAI not configured. Cannot perform analysis."
            }
            
        chain = self.prompt | llm
        response = chain.invoke({"content": content})
        
        return {
            "agent": "Business Process",
            "responsibility": "Understand what the system does today",
            "analysis": response.content
        }


class GapAnalysisAgent:
    """
    Extract Gap between Current & Proposed: Identify missing pieces / improvement areas
    """
    
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert in gap analysis, identifying differences between current state and desired future state."),
            ("user", """Analyze the following RFP content to identify gaps between current and proposed solutions.

Focus on:
- Missing capabilities in current system
- Proposed improvements or new features
- Areas requiring enhancement
- Functionality gaps

RFP Content:
{content}

Provide a detailed gap analysis.""")
        ])
    
    def analyze(self, content: str) -> Dict[str, Any]:
        if not llm:
            return {
                "agent": "Gap Analysis",
                "responsibility": "Identify missing pieces / improvement areas",
                "analysis": "Azure OpenAI not configured. Cannot perform analysis."
            }
            
        chain = self.prompt | llm
        response = chain.invoke({"content": content})
        
        return {
            "agent": "Gap Analysis",
            "responsibility": "Identify missing pieces / improvement areas",
            "analysis": response.content
        }
