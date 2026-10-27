from models.schemas import AgentAction, PermissionResult, RiskLevel


HIGH_RISK_ACTIONS = {
    "delete_file",
    "delete_folder",
    "send_email",
    "send_message",
    "install_software",
    "run_terminal_command",
    "execute_executable",
    "make_purchase",
    "change_system_settings",
    "delete_email",
}


MEDIUM_RISK_ACTIONS = {
    "download_file",
    "edit_document",
    "move_file",
    "create_calendar_event",
    "fill_form",
}


def classify_risk(action: str) -> RiskLevel:
    action = action.lower().strip()

    if action in HIGH_RISK_ACTIONS:
        return RiskLevel.HIGH

    if action in MEDIUM_RISK_ACTIONS:
        return RiskLevel.MEDIUM

    return RiskLevel.LOW


def apply_risk_policy(agent_action: AgentAction) -> AgentAction:
    agent_action.risk_level = classify_risk(
        agent_action.action
    )
    return agent_action


def needs_confirmation(
    agent_action: AgentAction,
) -> bool:
    return agent_action.risk_level == RiskLevel.HIGH


def evaluate_permission(
    agent_action: AgentAction,
) -> PermissionResult:

    checked_action = apply_risk_policy(agent_action)

    if checked_action.risk_level == RiskLevel.HIGH:
        return PermissionResult(
            allowed=False,
            confirmation_required=True,
            message="User confirmation required.",
        )

    return PermissionResult(
        allowed=True,
        confirmation_required=False,
        message="Action allowed.",
    )