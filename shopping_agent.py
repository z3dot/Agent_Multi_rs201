from crewai import Agent, Task, Crew
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from typing import List, Dict
import json

# Initialize the LLM pipeline
llama_pipeline = pipeline(
    "text-generation",
    model="nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
    device_map="auto"
)

llama_llm = HuggingFacePipeline(pipeline=llama_pipeline)

class ShoppingRequest:
    def __init__(self, items: List[Dict], budget: float):
        self.items = items
        self.budget = budget
        self.total_cost = 0.0
        self.status = "pending"

class ShoppingSystem:
    def __init__(self):
        # Create specialized agents
        self.product_researcher = Agent(
            role='Product Researcher',
            goal='Find the best products matching customer requirements',
            backstory='Expert at product research and price comparison',
            verbose=True,
            allow_delegation=False,
            llm=llama_llm
        )

        self.shopping_agent = Agent(
            role='Shopping Agent',
            goal='Process shopping requests and manage purchases',
            backstory='Experienced in handling customer orders and payment processing',
            verbose=True,
            allow_delegation=True,
            llm=llama_llm
        )

        self.payment_processor = Agent(
            role='Payment Processor',
            goal='Handle payment transactions securely',
            backstory='Specialized in secure payment processing and verification',
            verbose=True,
            allow_delegation=False,
            llm=llama_llm
        )

    def process_shopping_request(self, request: ShoppingRequest) -> Dict:
        # Create tasks for the shopping workflow
        research_task = Task(
            description=f'Research products: {json.dumps(request.items)}',
            agent=self.product_researcher
        )

        shopping_task = Task(
            description=f'Process shopping order within budget: ${request.budget}',
            agent=self.shopping_agent
        )

        payment_task = Task(
            description='Process payment and verify transaction',
            agent=self.payment_processor
        )

        # Create and execute the crew
        shopping_crew = Crew(
            agents=[self.product_researcher, self.shopping_agent, self.payment_processor],
            tasks=[research_task, shopping_task, payment_task],
            verbose=2
        )

        result = shopping_crew.kickoff()
        return {
            "status": "completed",
            "result": result
        }

# Example usage
if __name__ == "__main__":
    # Create a sample shopping request
    sample_request = ShoppingRequest(
        items=[
            {"name": "laptop", "specifications": "16GB RAM, 512GB SSD"},
            {"name": "headphones", "specifications": "wireless, noise-cancelling"}
        ],
        budget=2000.0
    )

    # Initialize and run the shopping system
    shopping_system = ShoppingSystem()
    result = shopping_system.process_shopping_request(sample_request)
    print(result)