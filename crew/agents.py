from crewai import Agent
from crew.llm import chatgpt_llm
from crew.tools import (
    retrieve_context,
    retrieve_citations,
    summarize_text,
    extract_keywords,
)

# The Policy Researcher
policy_analyst = Agent(
    role="Senior Policy Researcher",
    
    goal=(
        "Retrieve comprehensive evidence from the PDF report to answer user queries."
        "Find relevant sections, statistics, timelines, risks, or policy descriptions as needed."
    ),
    
    backstory=(
        "You are a meticulous researcher for the Canada AI Strategy project."
        "Your job is to find the ground truth in the 'Maple Protocol' PDF."
        "While you love data (z-scores, budgets, Top 10 rankings), you are also skilled at"
        "finding qualitative details like implementation phases, risk factors, and strategic justifications."
        "You provide the raw material that the Strategy Architect needs."
    ),
    llm=chatgpt_llm,
    #tools=[retrieve_context, retrieve_citations],
    tools=[retrieve_context, retrieve_citations, summarize_text, extract_keywords],
    verbose=True,
    allow_delegation=False
)

# AI Strategy Architect
domain_expert = Agent(
    role="Chief AI Strategy Architect",
    
    goal=(
        "Synthesize the researcher's findings into a natural, persuasive response."
        "Explain the 'Maple Protocol' strategy in a way that directly answers the user's specific question."
    ),
    
    backstory=(
        "You are the architect of the 'Maple Protocol' and a strategic advisor."
        "You are realistic but ambitious about Canada's future in AI."
        "You understand the gap between Canada's strong government policy and its weak commercial ecosystem."
        "Your goal is to explain the solution clearly and engagingly, without sounding like a robot."
        "You take the raw evidence and turn it into a compelling narrative."
    ),
    llm=chatgpt_llm,
    verbose=True,
    allow_delegation=False
)