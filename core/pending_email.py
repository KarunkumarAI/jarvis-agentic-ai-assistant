from models.schemas import EmailRequest


_pending_email: EmailRequest | None = None


def set_pending_email(email: EmailRequest) -> None:
    global _pending_email
    _pending_email = email


def get_pending_email() -> EmailRequest | None:
    return _pending_email


def clear_pending_email() -> None:
    global _pending_email
    _pending_email = None