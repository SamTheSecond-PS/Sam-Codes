import asyncio as ai

async def main(n):
    print(f"start {n + n}")
    await ai.sleep(1)
    print(f"end {n + n}")

async def gather():
    await ai.gather(
        main(1),
        main(2),
        main('a')
    )

ai.run(gather())

