from google.adk.agents import Agent

from agents.presentation_agent import generate_presentation_from_topic


def create_presentation(topic: str) -> dict:
    return generate_presentation_from_topic(topic)

root_agent = Agent(
    name="weather_time_presentation_agent",
    model="gemini-2.0-flash",
    description="An agent that can generate presentation slides.",
    tools=[create_presentation]
)
