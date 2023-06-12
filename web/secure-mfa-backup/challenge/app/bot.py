import asyncio
from os import getenv, path

from pyppeteer import launch

challenge_path = path.dirname(path.abspath(__file__))
with open(f"{challenge_path}/../flag") as file:
    FLAG = file.read()

default_wait_time = 10 if bool(getenv("DEBUG", False)) else int(getenv("SESSION_DURATION", 40))  # Run every 40 seconds


async def admin_task():
    await asyncio.sleep(1)
    cookie = {
        "name": "FLAG",
        "value": f"{FLAG}",
        "url": f"http://127.0.0.1:{getenv('PORT', 8080)}",
    }
    while True:
        print("## Bot opening browser")
        await asyncio.sleep(5)
        browser = await launch(
            headless=True,
            args=["--disable-gpu", "--no-sandbox"],
            ignoreHTTPSErrors=True,
            executablePath="/usr/bin/google-chrome",
            userDataDir="/home/user/",
            dumpio=True
        )
        page = await browser.newPage()
        await page.setCookie(cookie)
        await page.goto(f"http://127.0.0.1:{getenv('PORT', 8080)}/")
        await asyncio.sleep(default_wait_time)
        await browser.close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = loop.create_task(admin_task())
    try:
        loop.run_forever()
    except (KeyboardInterrupt, RuntimeError):
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
