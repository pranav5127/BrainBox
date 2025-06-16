from google.adk.agents import Agent

from agents.evaluation_agent import evaluate_agent
from agents.presentation_agent import generate_presentation_from_topic

def create_presentation(topic: str) -> dict:
    return generate_presentation_from_topic(topic)

def evaluate_exam(file_path: str) -> dict:
    if file_path is None:
        file_path = "/home/pranav/PycharmProjects/PythonProject/adk_prototype/presentation_agent/pdfs/earth.txt"
    return evaluate_agent(file_path)

root_agent = Agent(
    name="weather_time_presentation_agent",
    model="gemini-2.0-flash",
    description="An agent that can generate presentation slides and evaluate exams.",
    tools=[create_presentation, evaluate_exam]
)
