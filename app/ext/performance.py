import asyncio
from concurrent.futures import ThreadPoolExecutor


async def run_in_threadpool(function):
    max_threads = 4
    running_threads = 0

    while running_threads >= max_threads:
        await asyncio.sleep(0.00001)

    with ThreadPoolExecutor(max_workers=4) as thread_pool:
        running_threads = running_threads + 1

        loop = asyncio.get_event_loop()
        result = loop.run_in_executor(thread_pool, function)
        try:
            result = await result
        except Exception as e:
            raise e
        finally:
            running_threads -= 1
            thread_pool.shutdown(wait=True)
        return result
