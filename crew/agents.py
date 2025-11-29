from crewai import Agent
from crew.llm import chatgpt_llm
from crew.tools import retrieve_context, retrieve_citations, summarize_text, extract_keywords

policy_analyst = Agent(
    role="Senior Policy Researcher",
    goal=(
        "Retrieve comprehensive evidence from the Maple Protocol PDF to answer user queries. "
        "Find relevant sections, statistics, timelines, risks, and policy descriptions."
    ),
    backstory=(
        "You are a meticulous researcher for the Canada AI Strategy project. "
        "You excel at finding both quantitative indicators and qualitative details. "
        "You provide high-quality raw material for the Strategy Architect."
    ),
    llm=chatgpt_llm,
    tools=[retrieve_context],  # <-- only this for now
    verbose=True,
    allow_delegation=False,
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
