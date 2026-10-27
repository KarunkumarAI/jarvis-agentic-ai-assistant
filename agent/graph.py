from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agent.planner import plan_action
from agent.router import execute_action
from core.permissions import evaluate_permission
from models.schemas import AgentAction
from core.pending_action import set_pending_action
from core.pending_action import set_pending_action

MAX_RETRIES = 1


class AgentState(TypedDict):
    user_request: str
    action: AgentAction | None
    result: str
    retries: int


def planner_node(state: AgentState) -> dict:
    action = plan_action(state["user_request"])
    return {"action": action}


def permission_node(state: AgentState) -> dict:
    action = state["action"]

    if action is None:
        return {
            "result": "No valid action was created."
        }

    permission = evaluate_permission(action)

    if permission.confirmation_required:
        set_pending_action(action)

        return {
            "result": (
                f"CONFIRMATION_REQUIRED: "
                f"{action.action} "
                f"{action.target or ''}"
            )
        }

    return {"result": ""}


def execute_node(state: AgentState) -> dict:
    action = state["action"]

    if action is None:
        return {"result": "No action available."}

    try:
        return {"result": execute_action(action)}

    except Exception as error:
        return {"result": f"ERROR: {error}"}


def retry_node(state: AgentState) -> dict:
    return {
        "retries": state["retries"] + 1,
        "result": "",
    }


def after_permission(state: AgentState) -> str:
    return "finish" if state["result"] else "execute"


def after_execute(state: AgentState) -> str:
    if not state["result"].startswith("ERROR:"):
        return "finish"

    if state["retries"] >= MAX_RETRIES:
        return "finish"

    return "retry"


def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("permission", permission_node)
    graph.add_node("execute", execute_node)
    graph.add_node("retry", retry_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "permission")

    graph.add_conditional_edges(
        "permission",
        after_permission,
        {
            "execute": "execute",
            "finish": END,
        },
    )

    graph.add_conditional_edges(
        "execute",
        after_execute,
        {
            "retry": "retry",
            "finish": END,
        },
    )

    graph.add_edge("retry", "planner")

    return graph.compile()


jarvis_agent = build_agent()


def run_agent(user_request: str) -> str:
    result = jarvis_agent.invoke(
        {
            "user_request": user_request,
            "action": None,
            "result": "",
            "retries": 0,
        }
    )

    return result["result"]