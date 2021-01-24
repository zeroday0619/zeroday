import asyncio
import multiprocessing
from concurrent.futures import ThreadPoolExecutor




async def run_in_threadpool(function):
    max_threads = 4
    running_threads = 0
    

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


class CancellablePool:
    def __init__(self, max_workers=3):
        self._free = {self._new_pool() for _ in range(max_workers)}
        self._working = set()
        self._change = asyncio.Event()

    def _new_pool(self):
        return multiprocessing.Pool(1)

    async def apply(self, fn, *args):
        """
        Like multiprocessing.Pool.apply_async, but:
         * is an asyncio coroutine
         * terminates the process if cancelled
        """
        while not self._free:
            await self._change.wait()
            self._change.clear()
        pool = usable_pool = self._free.pop()
        self._working.add(pool)

        loop = asyncio.get_event_loop()
        fut = loop.create_future()
        def _on_done(obj):
            loop.call_soon_threadsafe(fut.set_result, obj)
        def _on_err(err):
            loop.call_soon_threadsafe(fut.set_exception, err)
        pool.apply_async(fn, args, callback=_on_done, error_callback=_on_err)

        try:
            return await fut
        except asyncio.CancelledError:
            pool.terminate()
            usable_pool = self._new_pool()
        finally:
            self._working.remove(pool)
            self._free.add(usable_pool)
            self._change.set()

    def shutdown(self):
        for p in self._working | self._free:
            p.terminate()
        self._free.clear()