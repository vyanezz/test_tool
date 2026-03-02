from datetime import datetime
from utils.colors import COLORS

class Logger:
    def __init__(self, enabled=True):
        self.enabled = enabled

    def log_api_call(self, endpoint, method=None, status="INFO"):
        if not self.enabled:
            return

        timestamp = datetime.now().strftime("%H:%M:%S")
        method_str = method.upper() if method else "ANY"
        color = COLORS.get(method_str, COLORS["ANY"])

        print(
            f"\033[90m[{timestamp}]\033[0m "
            f"\033[95m[{status}]\033[0m "
            f"{color}[{method_str}]{COLORS['RESET']} "
            f"{endpoint}"
        )
