from crewai import Task
from crew.agents import policy_analyst, domain_expert

# ==============================================================================
# 1. SYSTEM RULES
# ==============================================================================
SYSTEM_RULES = (
    "You MUST answer strictly using the provided information from the documents. "
    "If a claim is not in the context, say you don't know. Be concise, neutral, and structured. "
    "Do not create unnecessary bullet-point summaries unless the context explicitly requires it. "
    "Write in clear paragraphs that (i) explain the answer, (ii) reference supporting evidence, "
    "(iii) discuss implications, and (iv) end with a short summary. "
    "Summarize the overall effect in ≤25 words. "
)


DOMAIN_DIRECTIVES = {
    "general": (
    "Explain the answer at the global level. "
    "Only discuss Canada if the user explicitly mentions Canada or the Maple Protocol."
    ),
    "policy": (
    "Emphasize implementation roadmaps, government levers, regulation, and funding. "
    "If the user mentions a specific country, focus on that country; otherwise stay general."
    ),
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
        "You are the Senior Policy Researcher for the Maple Protocol report.\n\n"
        "The user asked: '{query}'. Your job is to retrieve the most relevant text "
        "from the Maple Protocol PDF.\n\n"
        "You have access to ONE tool: `retrieve_context`.\n"
        "Its schema is:\n"
        "- Name: retrieve_context\n"
        "- Argument: query (string)\n\n"
        "You MUST follow this exact interaction pattern with tools:\n\n"
        "Thought: <brief reasoning about what you will do>\n"
        "Action: retrieve_context\n"
        "Action Input: {{'query': '<short natural-language search query>'}}\n"
        "Observation: <tool output>\n\n"
        "IMPORTANT:\n"
        "- The Action Input MUST be a dictionary with a single key 'query'.\n"
        "- The value of 'query' MUST be a plain string (not another dictionary, "
        "not an object with 'description' or 'metadata').\n"
        "- Do NOT put 'description' or 'metadata' or any other keys in Action Input.\n\n"
        "After you see the Observation, think about what it contains and then finish with:\n\n"
        "Thought: I now can give a great answer\n"
        "Final Answer: <1–2 paragraph description of the retrieved context and key facts>\n"
    ),
    expected_output=(
        "1–2 paragraphs describing what was retrieved from the Maple Protocol and the "
        "key facts relevant to the user's question."
    ),
    agent=policy_analyst,
)


# Task 2: Strategy Answer (The Architect)
task_answer = Task(
    description=(
    f"{SYSTEM_RULES}\n\n"
    "STYLE:\n"
    "- Answer naturally, like ChatGPT: clear, friendly, and easy to read.\n"
    "- Use 2–5 paragraphs unless the question asks for phases, steps, pillars, or timelines.\n"
    "- If the question includes words like 'outline', 'phases', 'roadmap', '0–60 months', "
    "'steps', or 'pillars', you SHOULD use a clean numbered list.\n"
    "- Each numbered item should have 1–3 sentences. Start with a short intro paragraph, "
    "then the list, then one small closing paragraph.\n"
    "- Do NOT use visible section labels like 'Explanation', 'Evidence', or 'Implications'. "
    "Blend these elements into normal paragraphs.\n\n"
    "DIRECTIVE:\n"
    "{domain_directive}\n\n"
    "INSTRUCTION:\n"
    "Use the Policy Researcher's retrieved context to answer the question using only information "
    "that appears in the context or background facts. In the body of the answer: \n"
    "- Give a clear answer in normal prose.\n"
    "- Refer to supporting evidence or numbers from the retrieved context.\n"
    "- Briefly note what it means for national AI strategy or the relevant country. "
    "If no country is mentioned, discuss the global implications.\n"
    "- If the question is about phases, pillars, steps, or a roadmap, present the items as a numbered list.\n\n"
    "END the entire response with ONE bold summary sentence (≤25 words).\n"
    "If the user does NOT mention a specific country, answer in general global terms and "
    "do NOT default to Canada. Use Canada only as an example if clearly helpful.\n"
    "If the user explicitly mentions Canada or the Maple Protocol, then you may focus on Canada.\n"
    "If something is not in the context, say you don't know."
    ),
    expected_output=(
        "A natural answer (paragraphs plus a numbered list when appropriate) that covers explanation, "
        "evidence, and implications, ending with one bold summary sentence."
    ),
    agent=domain_expert,
    context=[task_gather],
)



# Test later
# task_gather = Task(
#     description=(
#         "You are the Senior Policy Researcher for the Maple Protocol report.\n\n"
#         "The user asked: '{query}'. Your job is to retrieve the most relevant text "
#         "from the Maple Protocol PDF and then summarize it.\n\n"

#         "You have access to ONE tool: `retrieve_context`.\n"
#         "Its schema is:\n"
#         "- Name: retrieve_context\n"
#         "- Argument: query (string)\n\n"

#         "TOOL USAGE RULES (VERY IMPORTANT):\n"
#         "- You may call `retrieve_context` AT MOST ONCE for this task.\n"
#         "- If you have already called `retrieve_context` once, you MUST NOT call it again, "
#         "even if the tool output suggests trying something else.\n"
#         "- If you cannot get useful output from the tool, you must still write a Final Answer "
#         "that honestly describes the problem.\n\n"

#         "When you decide to use the tool, you MUST follow this exact interaction pattern:\n\n"
#         "Thought: <brief reasoning about what you will do>\n"
#         "Action: retrieve_context\n"
#         "Action Input: {\"query\": \"<short natural-language search query>\"}\n"
#         "Observation: <tool output>\n\n"

#         "IMPORTANT FORMAT DETAILS:\n"
#         "- The Action Input MUST be a JSON object with double quotes, like: {\"query\": \"...\"}.\n"
#         "- Do NOT use single quotes.\n"
#         "- Do NOT include any other keys such as 'description' or 'metadata'.\n\n"

#         "AFTER TOOL CALL (OR IF YOU CHOOSE NOT TO CALL IT):\n"
#         "- Once you have either (a) one Observation from `retrieve_context` or (b) decided not to use it,\n"
#         "  you MUST stop using tools and finish the task.\n\n"
#         "Then respond in this format:\n\n"
#         "Thought: I now can give a great answer\n"
#         "Final Answer: <1–2 paragraphs describing the retrieved context and key facts relevant to the user's question. "
#         "If the tool failed or returned no useful data, clearly state that and explain what, if anything, you could infer.>\n"
#     ),
#     expected_output=(
#         "1–2 paragraphs describing what was retrieved from the Maple Protocol and the "
#         "key facts relevant to the user's question (or an honest explanation if retrieval failed)."
#     ),
#     agent=policy_analyst,
# )

# task_answer = Task(
#     description=(
#         f"{SYSTEM_RULES}\n\n"
#         "STYLE:\n"
#         "- Answer like a helpful AI assistant: natural, clear, and friendly but still professional.\n"
#         "- Use 2–5 short paragraphs. It should read as one flowing answer, not a form.\n"
#         "- You may use a short list only when it genuinely clarifies timelines, phases, or pillars.\n"
#         "- Do NOT label sections as 'Explanation', 'Evidence', or 'Implications'. Just weave those "
#         "elements into the narrative.\n\n"
#         "DIRECTIVE:\n"
#         "{domain_directive}\n\n"
#         "INSTRUCTION:\n"
#         "Using the Policy Researcher's output and any Background Facts provided, write a grounded answer "
#         "to the user's question. In the body of the answer you should:\n"
#         "- First, directly answer the question in plain language.\n"
#         "- Refer to specific facts, numbers, or passages from the retrieved context as supporting evidence.\n"
#         "- Briefly discuss what this means for Canada's AI strategy in the relevant domain.\n\n"
#         "Then END the response with a single bold sentence (≤25 words) that summarizes the overall takeaway.\n"
#         "Do not invent facts outside the retrieved context; if something is unknown, say so explicitly."
#     ),
#     expected_output=(
#         "A natural, multi-paragraph answer that covers explanation, evidence, and implications, "
#         "ending with one bold summary sentence."
#     ),
#     agent=domain_expert,
#     context=[task_gather],
# )