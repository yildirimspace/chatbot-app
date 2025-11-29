from crewai import Agent
from crew.llm import chatgpt_llm
from crew.tools import retrieve_context, retrieve_citations, summarize_text, extract_keywords

policy_analyst = Agent(
    role="Senior Policy Researcher",
    goal=(
        "Retrieve comprehensive evidence from the PDF report to answer user queries. "
        "Find relevant sections, statistics, timelines, risks, or policy descriptions as needed."
    ),
    backstory=(
        "You are a meticulous researcher for the Canada AI Strategy project. "
        "Your job is to find the ground truth in the 'Maple Protocol' PDF."
    ),
    llm=chatgpt_llm,
    tools=[retrieve_context],
    verbose=True,
    allow_delegation=False,
    max_iter=2,
)

domain_expert = Agent(
    role="Chief AI Strategy Architect",
    goal=(
        "Synthesize the researcher's findings into a natural, persuasive response that directly "
        "answers the user's question about the Maple Protocol and Canada's AI strategy."
    ),
    backstory=(
    "You are an AI strategy architect who advises governments and institutions on national AI ecosystems. "
    "You are familiar with the Maple Protocol (Canada's AI strategy proposal), but you only focus on Canada "
    "when the user asks about Canada or the Maple Protocol specifically."
    ),
    llm=chatgpt_llm,
    verbose=True,
    allow_delegation=False,
)
