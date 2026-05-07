from mev_agentic_ai.agents.drl_agent import DRLAgent

class IntegratedDRLLLMAgent:
    def __init__(self) -> None:
        self.drl = DRLAgent()

    def act(self, observation: dict) -> dict:
        return self.drl.act(observation)
