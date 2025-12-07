# Agent for analyzing RFP problems
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


class PainPointsAgent:
    """
    Extract Pain Points: What problems need solving?
    """
    
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert at identifying pain points and problems in business systems."),
            ("user", """Analyze the following RFP content and extract all pain points and problems that need solving.

Focus on:
- Current system problems
- User complaints or difficulties
- Operational inefficiencies
- Technical issues
- Business challenges

RFP Content:
{content}

List and describe all identified pain points.""")
        ])
    
    def analyze(self, content: str) -> Dict[str, Any]:
        if not llm:
            return {
                "agent": "Pain Points",
                "responsibility": "What problems need solving?",
                "analysis": "Azure OpenAI not configured. Cannot perform analysis."
            }
        
        chain = self.prompt | llm
        response = chain.invoke({"content": content})
        
        return {
            "agent": "Pain Points",
            "responsibility": "What problems need solving?",
            "analysis": response.content
        }


class ImpactfulStatementsAgent:
    """
    Extract Impactful Statements: Budget, user count, compliance pressure
    """
    
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert at identifying critical business metrics and impactful statements in RFPs."),
            ("user", """Analyze the following RFP content and extract impactful statements related to:

- Budget constraints and financial information
- User count and scale requirements
- Compliance and regulatory pressures
- Critical business metrics
- Strategic priorities

RFP Content:
{content}

Extract and highlight all impactful statements with relevant numbers and context.""")
        ])
    
    def analyze(self, content: str) -> Dict[str, Any]:
        if not llm:
            return {
                "agent": "Impactful Statements",
                "responsibility": "Budget, user count, compliance pressure",
                "analysis": "Azure OpenAI not configured. Cannot perform analysis."
            }
        
        chain = self.prompt | llm
        response = chain.invoke({"content": content})
        
        return {
            "agent": "Impactful Statements",
            "responsibility": "Budget, user count, compliance pressure",
            "analysis": response.content
        }


class ChallengesAgent:
    """
    Extract Challenges of Current System: Performance, data issues, maintenance pain
    """
    
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert at analyzing technical and operational challenges in existing systems."),
            ("user", """Analyze the following RFP content and extract challenges with the current system.

Focus on:
- Performance issues (speed, scalability, reliability)
- Data problems (quality, integration, migration)
- Maintenance difficulties (cost, complexity, support)
- Technical debt
- System limitations

RFP Content:
{content}

Provide a detailed analysis of current system challenges.""")
        ])
    
    def analyze(self, content: str) -> Dict[str, Any]:
        if not llm:
            return {
                "agent": "Challenges",
                "responsibility": "Performance, data issues, maintenance pain",
                "analysis": "Azure OpenAI not configured. Cannot perform analysis."
            }
        
        chain = self.prompt | llm
        response = chain.invoke({"content": content})
        
        return {
            "agent": "Challenges",
            "responsibility": "Performance, data issues, maintenance pain",
            "analysis": response.content
        }
