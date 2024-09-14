from __future__ import annotations

# Standard Library Imports
import asyncio as aio
import inspect
import threading
import typing

from typing import Dict, Tuple

AnyCallable = typing.Callable[..., typing.Any]
AnyException = typing.Union[Exception, typing.Type[Exception]]
AnyCoroutine = typing.Coroutine[typing.Any, typing.Any, typing.Any]

__all__ = ("AsyncIOPool",)

WorkerPoolInfo = Dict[
    str,
    typing.Optional[
        typing.Union[
            int,
            bool,
            Tuple[int, ...],
            aio.AbstractEventLoop,
        ]
    ],
]


class AsyncIOPool:
    loop: aio.AbstractEventLoop
    loop_runner: threading.Thread
    singleton: typing.Optional["AsyncIOPool"] = None

    def __new__(cls, *args: typing.Any, **kwargs: typing.Any) -> "AsyncIOPool":

        if not isinstance(cls.singleton, cls):
            cls.singleton = super(AsyncIOPool, cls).__new__(cls)

        return cls.singleton

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:

        try:
            aio.get_running_loop()
            raise SystemError("There is already a running event loop in this thread!")
        except RuntimeError:
            pass

        kwargs.update(
            threads=False,
            forking_enable=False,
        )

        self.limit = 1
        self.loop = aio.new_event_loop()

        self.loop_runner = threading.Thread(
            target=self.loop.run_forever,
            name="job-worker-async-loop",
            daemon=True,
        )

        self.loop_runner.start()

        aio.set_event_loop(self.loop)

    def run(
            self,
            task_function: AnyCallable | AnyCoroutine,
            *args: typing.Any,
            **kwargs: typing.Any,
    ) -> typing.Any:
        if inspect.iscoroutinefunction(task_function):
            task_function = task_function(*args, **kwargs)

        if callable(task_function) and not bool(
                inspect.iscoroutine(task_function) or aio.isfuture(task_function)
        ):
            task_function = aio.to_thread(
                task_function,
                *args,
                **kwargs,
            )
        if not inspect.isawaitable(task_function):
            return task_function
        try:
            result: aio.Future = aio.run_coroutine_threadsafe(
                task_function,
                self.loop,
            )
        except TypeError:
            return task_function

        # Once the our future has been awaited, it will either
        # have raised an exception or returned a result. If it
        # raised an exception, propagate it back to the caller
        error = result.exception()
        if error:
            raise error
        return self.run(result.result())

    @classmethod
    def run_in_pool(
            cls,
            task_function: AnyCallable | AnyCoroutine,
            *args: typing.Any,
            **kwargs: typing.Any,
    ) -> typing.Any:
        """Run the supplied tasks in the pool's thread-bound async loop."""
        worker_pool = cls.singleton
        if not worker_pool:
            worker_pool = cls()

        return worker_pool.run(
            task_function,
            *args,
            **kwargs,
        )

    async def shutdown(self) -> None:
        """Shut down the worker pool."""
        if self.loop.is_running():
            self.loop.stop()
            await self.loop.shutdown_asyncgens()
        closer = getattr(
            self.loop,
            "aclose",
            None,
        )
        if not self.loop.is_closed() and callable(closer):
            await closer()

    def join(self) -> None:
        """Join the loop-runner thread."""
        self.loop_runner.join()
