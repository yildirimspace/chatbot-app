from crewai import Task
from crew.agents import policy_analyst, domain_expert

# ==============================================================================
# 1. SYSTEM RULES
# ==============================================================================
SYSTEM_RULES = (
    "You MUST answer strictly using the provided information from the documents."
    "If a claim is not in the context, say you don't know. Be concise, neutral, and structured."
    "Do not create unnecessary bullet-point summaries unless the context explicitly requires it."
    "Write in clear paragraphs: Explanation + Evidence + Implications + Summary."
    "Summarizing the overall effect in ≤25 words."
)

# # ==============================================================================
# # 2. PROJECT CONTEXT
# # ==============================================================================
# PROJECT_CONTEXT = """
# MAPLE PROTOCOL FACT SHEET:
# 1. The project is motivated by the rapid global acceleration of national AI strategies, as governments seek to scale AI adoption while managing governance, trust, and societal risks. 
# 2. It situates Canada as a country with world-class AI research and a legacy in responsible AI, but facing a competitiveness challenge that requires a more coordinated, future-ready federal strategy. 
# 3. Methodologically, it applies a two-step design: (i) a cross-country feature-importance analysis using AI ecosystem metrics for 193 countries, and (ii) benchmarking Canada against the top 
# 4. AI-policy leaders to identify best practices in governance, risk management, compute infrastructure, public-sector adoption, industrial incentives, and workforce development. 
# 5. The intended output is an evidence-informed set of recommendations for the federal Government of Canada, with explicit scope limits that exclude provincial/municipal policies and private-sector strategies except where used for contextual benchmarking.  
# """

# ==============================================================================
# 3. DOMAIN DIRECTIVES
# ==============================================================================
DOMAIN_DIRECTIVES = {
    "general": ("Focus on Canada's position relative to global leaders (US, UK) and the overall strategy."),
    "policy": ("Emphasize the 'Implementation Roadmap', government levers, regulation, and funding."),
    "research": ("Emphasize sovereign models, compute capacity, and the 'Brain Drain' of talent."),
    "product": ("Emphasize the commercialization gap, startup ecosystem, and venture capital."),
    "manufacturing": ("Emphasize AI adoption in real sectors (energy, health) and productivity gains."),
}

# ==============================================================================
# 4. TASK DEFINITIONS (Hardened)
# ==============================================================================

# Task 1: Retrieval (The Hunter)
task_gather = Task(
    description=(
        "You are the Senior Policy Researcher. The user asked: '{query}'\n\n"
        "**YOUR JOB:**\n"
        "Find the most relevant evidence in the report to answer this question.\n\n"
        
        "**STRICT EXECUTION RULES:**\n"
        "1. You are permitted to use **ONLY ONE** tool call per turn.\n"
        "2. Do NOT try to use `retrieve_context` and `retrieve_citations` at the same time.\n"
        "3. Use `retrieve_context` FIRST. Wait for the result. Then stop.\n\n"
        "4. Use tool `summarize_text` on the raw text to produce a mini-summary.\n"
        "5. Use tool `extract_keywords` on the raw text to produce 8–12 keywords.\n"
        
        "**CORRECT FORMAT:**\n"
        "Action: retrieve_context\n"
        "Action Input: {'query': '...your search query...'}\n"
    ),
    expected_output="A summary of the retrieved context and key facts.",
    agent=policy_analyst,
)

# Task 2: Strategy Answer (The Architect)
task_answer = Task(
    description=(
        f"{SYSTEM_RULES}\n\n"
        # "**BACKGROUND FACTS:**\n"
        # f"{PROJECT_CONTEXT}\n\n"
        "**DIRECTIVE:**\n"
        "{domain_directive}\n\n"
        "**INSTRUCTION:**\n"
        "Use the researcher's output AND the Background Facts to write a grounded answer."
        "Include an 'Implications' section. Avoid claims not present in the cited context or facts."
        "END with the required bold 'Summary' sentence."
    ),
    expected_output=(
        "A concise, cited answer with sections 'Explanation', 'Evidence', 'Implications',"
        "and a final bold 'Summary' sentence."
    ),
    agent=domain_expert,
    context=[task_gather],
)