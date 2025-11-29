from crewai import Crew
from crew.tasks import task_gather, task_answer, DOMAIN_DIRECTIVES

def kickoff_query(query: str, domain_directive: str):
    crew = Crew(
        agents=[task_gather.agent, task_answer.agent],
        tasks=[task_gather, task_answer],
        verbose=True,
    )
    return crew.kickoff(inputs={
        "query": query,
        "domain_directive": domain_directive,
    })

if __name__ == "__main__":
    q = "What specific policy levers does the strategy propose to improve Canada's AI compute infrastructure?"
    directive = DOMAIN_DIRECTIVES["general"]      # use the 'general' directive text
    ans = kickoff_query(q, directive)
    print("\n=== FINAL ANSWER ===\n")
    print(ans)
