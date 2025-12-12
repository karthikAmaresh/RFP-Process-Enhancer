"""
Azure AI Foundry Orchestrator - Uses Azure AI Agents API with file upload
Integrates with Azure AI Foundry project for advanced agent capabilities
"""
import os
from typing import Dict
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


class AzureFoundryOrchestrator:
    """Orchestrates all 12 RFP agents using Azure AI Foundry Agents API"""
    
    def __init__(self):
        """Initialize Azure AI Project Client with Default Credentials"""
        # Use DefaultAzureCredential - works with az login
        credential = DefaultAzureCredential()
        
        # Get connection details from env
        conn_str = os.getenv("PROJECT_CONNECTION_STRING")
        if not conn_str:
            raise ValueError("PROJECT_CONNECTION_STRING not set in .env file")
        
        # The connection string IS the endpoint for Azure AI Foundry
        # Format: https://rfp-process-enhancer-resource.services.ai.azure.com/api/projects/rfp-foundry
        # This is the full endpoint that should be used directly
        
        # Initialize Azure AI Project Client with the full connection string as endpoint
        self.project_client = AIProjectClient(
            credential=credential,
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group_name=os.getenv("AZURE_RESOURCE_GROUP", "rfp-process-enhancer"),
            project_name=os.getenv("AZURE_PROJECT_NAME", "rfp-foundry"),
            endpoint=conn_str  # Use full connection string as endpoint
        )
        
        # Model to use for agents
        self.model = os.getenv("AZURE_OPENAI_MODEL", "gpt-4o")
        
        # Agent configurations with specialized instructions
        self.agent_configs = {
            "introduction": {
                "name": "Introduction Agent",
                "instructions": """You are an expert RFP analyst specializing in executive summaries.
Your task: Extract and synthesize the problem statement and create a compelling executive summary.
Focus on: Business challenges, strategic objectives, high-level scope.
Format: Clear, concise executive summary with problem statement."""
            },
            "challenges": {
                "name": "Challenges Agent",
                "instructions": """You are an expert at identifying business challenges in RFPs.
Your task: Extract all business challenges, pain points, and problems the client is facing.
Focus on: Current issues, operational difficulties, strategic challenges.
Format: Numbered list of specific challenges with brief explanations."""
            },
            "pain_points": {
                "name": "Pain Points Agent",
                "instructions": """You are an expert at identifying user and operational pain points.
Your task: Extract specific pain points affecting users, staff, and operations.
Focus on: User frustrations, operational inefficiencies, system limitations.
Format: Categorized pain points by stakeholder type."""
            },
            "business_process": {
                "name": "Business Process Agent",
                "instructions": """You are an expert at analyzing business processes and workflows.
Your task: Map current business processes and identify workflow requirements.
Focus on: Process flows, workflow steps, integration points, automation needs.
Format: Structured process descriptions with key steps."""
            },
            "gap": {
                "name": "Gap Analysis Agent",
                "instructions": """You are an expert at gap analysis between current and desired states.
Your task: Identify gaps between current capabilities and desired outcomes.
Focus on: Technology gaps, capability gaps, process gaps, skill gaps.
Format: Clear gap statements with current vs. desired state."""
            },
            "personas": {
                "name": "Personas Agent",
                "instructions": """You are an expert at creating user personas and stakeholder profiles.
Your task: Identify and describe user personas, roles, and stakeholder groups.
Focus on: User types, roles, responsibilities, needs, technical proficiency.
Format: Detailed persona descriptions with characteristics."""
            },
            "constraints": {
                "name": "Constraints Agent",
                "instructions": """You are an expert at identifying project constraints and limitations.
Your task: Extract all constraints including technical, budget, timeline, regulatory.
Focus on: Technical limitations, compliance requirements, budget constraints, deadlines.
Format: Categorized constraints with impact assessment."""
            },
            "functional_requirements": {
                "name": "Functional Requirements Agent",
                "instructions": """You are an expert at extracting functional requirements from RFPs.
Your task: Identify all functional requirements and feature requests.
Focus on: System capabilities, user features, functionality, business rules.
Format: Numbered functional requirements with acceptance criteria."""
            },
            "nfr": {
                "name": "Non-Functional Requirements Agent",
                "instructions": """You are an expert at identifying non-functional requirements.
Your task: Extract NFRs including performance, security, scalability, usability.
Focus on: Performance metrics, security requirements, scalability needs, reliability.
Format: Categorized NFRs with measurable criteria."""
            },
            "architecture": {
                "name": "Architecture Agent",
                "instructions": """You are an expert solution architect analyzing technical requirements.
Your task: Identify architecture requirements, technical stack preferences, integration needs.
Focus on: System architecture, technology preferences, integration requirements, deployment.
Format: Architecture recommendations with technical justification."""
            },
            "assumptions": {
                "name": "Assumptions Agent",
                "instructions": """You are an expert at identifying implicit assumptions in RFPs.
Your task: Extract stated assumptions and identify implicit ones.
Focus on: Technical assumptions, business assumptions, resource assumptions.
Format: Numbered assumptions with rationale."""
            },
            "impact": {
                "name": "Impact Analysis Agent",
                "instructions": """You are an expert at analyzing business impact and change management.
Your task: Assess the impact of proposed changes on the organization.
Focus on: Organizational impact, change management needs, training requirements.
Format: Impact assessment with stakeholder considerations."""
            }
        }
        
        # Create vector store for RFP documents
        self.vector_store = None
        self.agents = {}  # Cache created agents
        self.thread = None  # Conversation thread
    
    def upload_rfp_document(self, file_path: str) -> str:
        """
        Upload RFP document and create vector store
        
        Args:
            file_path: Path to the RFP document
            
        Returns:
            Vector store ID
        """
        print(f"Uploading RFP document: {file_path}")
        
        # Upload file for agents using files.upload
        with open(file_path, 'rb') as f:
            file = self.project_client.agents.files.upload(file=f, purpose="assistants")
        print(f"✓ Uploaded file, ID: {file.id}")
        
        # Create vector store with the file using vector_stores.create
        self.vector_store = self.project_client.agents.vector_stores.create_and_poll(
            file_ids=[file.id],
            name="rfp-documents"
        )
        print(f"✓ Created vector store, ID: {self.vector_store.id}")
        
        return self.vector_store.id
    
    def create_agent(self, agent_type: str) -> str:
        """
        Create or retrieve cached agent
        
        Args:
            agent_type: Type of agent (introduction, challenges, etc.)
            
        Returns:
            Agent ID
        """
        # Return cached agent if exists
        if agent_type in self.agents:
            return self.agents[agent_type]
        
        config = self.agent_configs[agent_type]
        
        # Create agent with file search tool
        agent = self.project_client.agents.create_agent(
            model=self.model,
            name=config["name"],
            instructions=config["instructions"],
            tools=[{"type": "file_search"}],
            tool_resources={
                "file_search": {
                    "vector_store_ids": [self.vector_store.id]
                }
            }
        )
        
        # Cache agent
        self.agents[agent_type] = agent.id
        print(f"✓ Created {config['name']}, ID: {agent.id}")
        
        return agent.id
    
    def analyze_with_agent(self, agent_type: str, question: str) -> Dict:
        """
        Analyze RFP with specific agent
        
        Args:
            agent_type: Type of agent
            question: Question to ask the agent
            
        Returns:
            Dict with analysis result
        """
        try:
            # Create agent if not exists
            agent_id = self.create_agent(agent_type)
            
            # Create thread if not exists
            if not self.thread:
                self.thread = self.project_client.agents.threads.create()
            
            # Create message
            message = self.project_client.agents.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=question
            )
            
            # Run agent
            run = self.project_client.agents.create_and_process_run(
                thread_id=self.thread.id,
                agent_id=agent_id
            )
            
            if run.status == "failed":
                return {
                    "agent": self.agent_configs[agent_type]["name"],
                    "error": run.last_error,
                    "result": "",
                    "status": "error"
                }
            
            # Get response
            messages = self.project_client.agents.messages.list(thread_id=self.thread.id)
            result = messages.data[0].content[0].text.value
            
            return {
                "agent": self.agent_configs[agent_type]["name"],
                "result": result,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "agent": self.agent_configs[agent_type]["name"],
                "error": str(e),
                "result": "",
                "status": "error"
            }
    
    def run_all_agents(self, file_path: str) -> Dict[str, Dict]:
        """
        Run all 12 agents on the RFP document
        
        Args:
            file_path: Path to the RFP document
            
        Returns:
            Dict mapping agent type to result
        """
        # Upload document and create vector store
        self.upload_rfp_document(file_path)
        
        results = {}
        
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
            
            # Ask agent to analyze the RFP
            question = "Analyze the uploaded RFP document and provide your specialized analysis."
            result = self.analyze_with_agent(agent_type, question)
            results[agent_type] = result
        
        return results
    
    def cleanup(self):
        """Clean up resources"""
        try:
            # Delete agents
            for agent_id in self.agents.values():
                self.project_client.agents.delete_agent(agent_id)
            
            # Delete vector store
            if self.vector_store:
                self.project_client.agents.vector_stores.delete(self.vector_store.id)
            
            print("✓ Cleaned up resources")
        except Exception as e:
            print(f"⚠ Cleanup error: {e}")
