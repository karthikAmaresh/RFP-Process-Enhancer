"""
Azure OpenAI Orchestrator - Runs all 12 agents using Azure OpenAI directly
Replaces Container Apps with direct Azure OpenAI calls
"""
import os
from typing import Dict
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


class AzureOpenAIOrchestrator:
    """Orchestrates all 12 RFP agents using Azure OpenAI"""
    
    def __init__(self):
        """Initialize Azure OpenAI client"""
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT4", "gpt-4o")
        
        # Agent configurations with specialized prompts
        self.agents = {
            "introduction": {
                "name": "Introduction Agent",
                "system_prompt": """You are an expert RFP analyst specializing in executive summaries.
Your task: Extract and synthesize the problem statement and create a compelling executive summary.
Focus on: Business challenges, strategic objectives, high-level scope.
Format: Clear, concise executive summary with problem statement."""
            },
            "challenges": {
                "name": "Challenges Agent",
                "system_prompt": """You are an expert at identifying business challenges in RFPs.
Your task: Extract all business challenges, pain points, and problems the client is facing.
Focus on: Current issues, operational difficulties, strategic challenges.
Format: Numbered list of specific challenges with brief explanations."""
            },
            "pain_points": {
                "name": "Pain Points Agent",
                "system_prompt": """You are an expert at identifying user and operational pain points.
Your task: Extract specific pain points affecting users, staff, and operations.
Focus on: User frustrations, operational inefficiencies, system limitations.
Format: Categorized pain points by stakeholder type."""
            },
            "business_process": {
                "name": "Business Process Agent",
                "system_prompt": """You are an expert at analyzing business processes and workflows.
Your task: Map current business processes and identify workflow requirements.
Focus on: Process flows, workflow steps, integration points, automation needs.
Format: Structured process descriptions with key steps."""
            },
            "gap": {
                "name": "Gap Analysis Agent",
                "system_prompt": """You are an expert at gap analysis between current and desired states.
Your task: Identify gaps between current capabilities and desired outcomes.
Focus on: Technology gaps, capability gaps, process gaps, skill gaps.
Format: Clear gap statements with current vs. desired state."""
            },
            "personas": {
                "name": "Personas Agent",
                "system_prompt": """You are an expert at creating user personas and stakeholder profiles.
Your task: Identify and describe user personas, roles, and stakeholder groups.
Focus on: User types, roles, responsibilities, needs, technical proficiency.
Format: Detailed persona descriptions with characteristics."""
            },
            "constraints": {
                "name": "Constraints Agent",
                "system_prompt": """You are an expert at identifying project constraints and limitations.
Your task: Extract all constraints including technical, budget, timeline, regulatory.
Focus on: Technical limitations, compliance requirements, budget constraints, deadlines.
Format: Categorized constraints with impact assessment."""
            },
            "functional_requirements": {
                "name": "Functional Requirements Agent",
                "system_prompt": """You are an expert at extracting functional requirements from RFPs.
Your task: Identify all functional requirements and feature requests.
Focus on: System capabilities, user features, functionality, business rules.
Format: Numbered functional requirements with acceptance criteria."""
            },
            "nfr": {
                "name": "Non-Functional Requirements Agent",
                "system_prompt": """You are an expert at identifying non-functional requirements.
Your task: Extract NFRs including performance, security, scalability, usability.
Focus on: Performance metrics, security requirements, scalability needs, reliability.
Format: Categorized NFRs with measurable criteria."""
            },
            "architecture": {
                "name": "Architecture Agent",
                "system_prompt": """You are an expert solution architect analyzing technical requirements.
Your task: Identify architecture requirements, technical stack preferences, integration needs.
Focus on: System architecture, technology preferences, integration requirements, deployment.
Format: Architecture recommendations with technical justification."""
            },
            "assumptions": {
                "name": "Assumptions Agent",
                "system_prompt": """You are an expert at identifying implicit assumptions in RFPs.
Your task: Extract stated assumptions and identify implicit ones.
Focus on: Technical assumptions, business assumptions, resource assumptions.
Format: Numbered assumptions with rationale."""
            },
            "impact": {
                "name": "Impact Analysis Agent",
                "system_prompt": """You are an expert at analyzing business impact and change management.
Your task: Assess the impact of proposed changes on the organization.
Focus on: Organizational impact, change management needs, training requirements.
Format: Impact assessment with stakeholder considerations."""
            }
        }
    
    def analyze_with_agent(self, agent_type: str, rfp_text: str, context: Dict = None) -> Dict:
        """
        Analyze RFP text with a specific agent using Azure OpenAI
        
        Args:
            agent_type: Type of agent (introduction, challenges, etc.)
            rfp_text: The RFP text to analyze
            context: Optional context from previous agents
            
        Returns:
            Dict with analysis result
        """
        if agent_type not in self.agents:
            return {"error": f"Unknown agent type: {agent_type}", "result": ""}
        
        agent_config = self.agents[agent_type]
        
        try:
            # Build user message with context if available
            user_message = f"RFP Document:\n\n{rfp_text}"
            if context:
                user_message += f"\n\nContext from previous analysis:\n{str(context)}"
            
            # Call Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": agent_config["system_prompt"]},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            result = response.choices[0].message.content
            
            return {
                "agent": agent_config["name"],
                "result": result,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "agent": agent_config["name"],
                "error": str(e),
                "result": "",
                "status": "error"
            }
    
    def run_all_agents(self, rfp_text: str) -> Dict[str, Dict]:
        """
        Run all 12 agents sequentially on the RFP text
        
        Args:
            rfp_text: The RFP document text
            
        Returns:
            Dict mapping agent type to result
        """
        results = {}
        context = {}
        
        agent_order = [
            "introduction",
            "challenges", 
            "pain_points",
            "business_process",
            "gap",
            "personas",
            "constraints",
            "functional_requirements",
            "nfr",
            "architecture",
            "assumptions",
            "impact"
        ]
        
        for agent_type in agent_order:
            print(f"  • Running {agent_type} agent...")
            result = self.analyze_with_agent(agent_type, rfp_text, context)
            results[agent_type] = result
            
            # Add successful results to context for next agents
            if result.get("status") == "success":
                context[agent_type] = result["result"][:500]  # Keep context manageable
        
        return results
