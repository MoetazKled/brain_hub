from app.agents.specialized.router_agent import RouterAgent
from app.agents.specialized.research_agent import ResearchAgent
from app.agents.specialized.code_agent import CodeAgent
from app.agents.specialized.summary_agent import SummaryAgent
from app.core.logger import logger


class MultiAgentOrchestrator:
    def __init__(self):
        self.router = RouterAgent()
        self.research_agent = ResearchAgent()
        self.code_agent = CodeAgent()
        self.summary_agent = SummaryAgent()

    def process(self, user_message: str, rag_context: dict = None) -> tuple:
        agent_type = self.router.route(user_message)

        logger.info(f"Using {agent_type} agent")

        if agent_type == "research":
            response = self.research_agent.process(user_message, rag_context)
        elif agent_type == "code":
            response = self.code_agent.process(user_message, rag_context)
        elif agent_type == "summary":
            response = self.summary_agent.process(user_message, rag_context)
        else:
            response = self.research_agent.process(user_message, rag_context)

        agents_used = ["router", agent_type]

        return response, agents_used