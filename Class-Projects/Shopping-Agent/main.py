from agents import Agent, Runner
import asyncio



plant_agent = Agent(
    name="Plant Agent",
    instructions="""""",
)

medicine_agent = Agent(
    name= "Medicine Agent",
    instructions="""""",
)


parent_agent = Agent(
    name= "Parent Agent"
    instructions="""
    Your are a parent agen, Your task is to delegate user query to approriate agent.
    Delegate plant and flower related queries Any query other tahn plant and medicine """,
    handoffs=[plant_agent, medicine_agent]
)

aysnc def main():
    result = await Runner.run(
        plant_agent,
        "What is red-blod cells",
        run_config=config
    )