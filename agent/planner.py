from core.llm import get_llm
from core.permissions import apply_risk_policy
from models.schemas import AgentAction


def plan_action(user_request: str) -> AgentAction:
    llm = get_llm().with_structured_output(AgentAction)

    action = llm.invoke(
        f"""
        You are the planner for JARVIS.

        Available tools:

        desktop:
        - open_application

        browser:
        - open_website
        - google_search
        - youtube_search
        - youtube_play
        - scroll_down
        - go_back
        - close_browser

        User request:
        {user_request}

        Choose exactly one appropriate tool and action.

        Examples:

        Open Chrome
        tool = desktop
        action = open_application
        target = chrome

        Search Google for LangGraph tutorials
        tool = browser
        action = google_search
        target = LangGraph tutorials

        Search YouTube for Python tutorials
        tool = browser
        action = youtube_search
        target = Python tutorials

        Play Shape of You by Ed Sheeran on YouTube
        tool = browser
        action = youtube_play
        target = Ed Sheeran Shape of You official music video

        Open YouTube and play Believer by Imagine Dragons
        tool = browser
        action = youtube_play
        target = Imagine Dragons Believer official music video
        """
    )

    return apply_risk_policy(action)