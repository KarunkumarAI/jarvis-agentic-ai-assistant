import subprocess
from pathlib import Path


HOME = Path.home()

APP_REGISTRY = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "file explorer": ["explorer.exe"],
    "edge": ["msedge.exe"],
    "chrome": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ],
    "vscode": [
        HOME / "AppData/Local/Programs/Microsoft VS Code/Code.exe",
    ],
}

ALIASES = {
    "vs code": "vscode",
    "code": "vscode",
    "explorer": "file explorer",
    "google chrome": "chrome",
}


def open_application(app_name: str) -> str:
    name = app_name.lower().strip()
    name = ALIASES.get(name, name)

    if name not in APP_REGISTRY:
        return f"Application '{app_name}' is not registered."

    for command in APP_REGISTRY[name]:
        path = Path(command)

        if path.exists() or not path.is_absolute():
            try:
                subprocess.Popen([str(command)])
                return f"{app_name.title()} opened successfully."

            except FileNotFoundError:
                continue

    return f"{app_name.title()} is registered, but its executable was not found."