from models.schemas import AgentAction
from tools.browser import (
    close_browser,
    google_search,
    go_back,
    open_website,
    scroll_down,
    youtube_search,
)
from tools.desktop import open_application


def execute_action(agent_action: AgentAction) -> str:
    action = agent_action.action
    target = agent_action.target

    if action == "open_application":
        return open_application(target or "")

    if action == "open_website":
        return open_website(target or "")

    if action == "google_search":
        return google_search(target or "")

    if action == "youtube_search":
        return youtube_search(target or "")

    if action == "scroll_down":
        return scroll_down()

    if action == "go_back":
        return go_back()

    if action == "close_browser":
        close_browser()
        return "Browser closed."

    return f"Unsupported action: {action}"