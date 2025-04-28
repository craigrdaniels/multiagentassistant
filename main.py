from dotenv import load_dotenv
import asyncio

load_dotenv()

import sys
from src.core.main import Core


async def main():
    aura = Core()
    if len(sys.argv) < 2:
        print("Usage: main <module>")
        return
    module = sys.argv[1]
    result = await aura.run_agent(module)


if __name__ == "__main__":
    asyncio.run(main())
