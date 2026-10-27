from models.schemas import AgentAction


_pending_action: AgentAction | None = None


def set_pending_action(action: AgentAction) -> None:
    global _pending_action
    _pending_action = action


def get_pending_action() -> AgentAction | None:
    return _pending_action


def clear_pending_action() -> None:
    global _pending_action
    _pending_action = None