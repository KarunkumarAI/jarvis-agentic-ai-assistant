from agent.router import execute_action
from core.pending_action import (
    clear_pending_action,
    get_pending_action,
)


def confirm_pending_action() -> str:
    action = get_pending_action()

    if action is None:
        return "There is no pending action."

    try:
        result = execute_action(action)
        clear_pending_action()
        return result

    except Exception as error:
        clear_pending_action()
        return f"Action failed: {error}"


def cancel_pending_action() -> str:
    action = get_pending_action()

    if action is None:
        return "There is no pending action."

    clear_pending_action()

    return "Action cancelled."