from datetime import datetime
from zoneinfo import ZoneInfo


class Agent:
    """
    Agent to provide current date/time information.
    """

    async def run(self, timezone: str = None, fmt: str = None):
        try:
            if timezone:
                now = datetime.now(ZoneInfo(timezone))
            else:
                now = datetime.now()
        except Exception as e:
            return f"Error: {str(e)}"

        if fmt:
            try:
                return now.strftime(fmt)
            except ValueError as e:
                return f"Error: {str(e)}"

        return now.isoformat()
