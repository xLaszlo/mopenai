import asyncio
from enum import Enum

import typer
from loguru import logger
from pydantic import BaseModel


class Task(BaseModel):
    class Status(Enum):
        PENDING = 'pending'
        FINISHED = 'finished'

    id: int
    wait: int
    message: str
    status: Status = Status.PENDING


TASKS = [
    Task(id=0, wait=5, message="                        *** Hello World ***"),
    Task(id=1, wait=3, message="                        *** Here we go ***"),
    Task(id=2, wait=1, message="                        *** Learn Async ***"),
    Task(id=3, wait=10, message="                        *** Subscribe ***"),
    Task(id=4, wait=3, message="                        *** with feeling ***"),
    Task(id=5, wait=1, message="                        *** One more time ***"),
]


class AsyncWorker:
    def __init__(self):
        self.tasks = {}
        self.loop = asyncio.get_event_loop()
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(3)

    async def schedule(self, task: Task):
        async with self.lock:
            logger.info(f"Task scheduled: {task.id}")
            self.tasks[task.id] = task
        self.loop.create_task(self.run(task.id))

    async def run(self, task_id: int):
        logger.info(f'Task {task_id} started and waiting for the semaphore')
        async with self.semaphore:
            logger.info(f'Task {task_id} past the semaphore')
            async with self.lock:
                task = self.tasks[task_id]
            logger.info(f'Task {task_id} start waiting')
            await asyncio.sleep(task.wait)
            logger.info(f'Task {task_id} message: {task.message}')
            async with self.lock:
                task.status = Task.Status.FINISHED
        logger.info(f'Task {task_id} finished, semaphore released')

    async def is_finished(self):
        async with self.lock:
            finished = [task for task in self.tasks.values() if task.status == Task.Status.FINISHED]
            logger.info(f'Finished tasks: {[task.id for task in finished]}')
            return len(finished) == len(self.tasks)


async def main():
    logger.info('Processing start')
    async_worker = AsyncWorker()
    for task in TASKS:
        await async_worker.schedule(task)
    logger.info('Processing finished')
    while not await async_worker.is_finished():
        logger.info('Waiting for processing to finish')
        await asyncio.sleep(1)
    async with async_worker.lock:
        for task in TASKS:
            logger.info(f'Task {task.id} status: {task.status}')

    # await asyncio.gather(*[async_worker.run(task.id) for task in TASKS])


def typer_main():
    asyncio.run(main())


if __name__ == "__main__":
    typer.run(typer_main)
