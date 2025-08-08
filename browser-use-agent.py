import asyncio
from dotenv import load_dotenv
from browser_use.llm import ChatGoogle
from browser_use import Agent, BrowserSession

load_dotenv()


async def main():
    llm = ChatGoogle(model="gemini-2.0-flash")

    browser_session = BrowserSession(
        headless=False,
        keep_alive=True,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
        ],
    )

    agent = Agent(
        task="Go to google.com and search for 'browser automation'",
        llm=llm,
        browser_session=browser_session,
    )

    try:
        await browser_session.start()  # 브라우저 세션 시작
        print("🚀 Starting browser-use agent...")
        result = await agent.run(max_steps=10)
        print("✅ Task completed!")
        print(f"Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await browser_session.close()  # 브라우저 완전 종료


if __name__ == "__main__":
    asyncio.run(main())
