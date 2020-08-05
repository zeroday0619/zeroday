import asyncio
from concurrent.futures import ThreadPoolExecutor


running_threads = 0
max_threads = 4


async def run_in_threadpool(function):
    global running_threads

    while running_threads >= max_threads:
        await asyncio.sleep(1)

    with ThreadPoolExecutor(max_workers=1) as thread_pool:
        running_threads = running_threads + 1

        loop = asyncio.get_event_loop()
        result = loop.run_in_executor(thread_pool, function)
        try:
            result = await result
        except Exception as e:
            raise e
        finally:
            running_threads = running_threads - 1
            thread_pool.shutdown(wait=True)
        return result
