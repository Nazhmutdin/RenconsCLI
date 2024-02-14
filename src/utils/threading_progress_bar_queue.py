import typing
from queue import Queue
from src.utils.progress_bar import init_progress_bar


class ThreadProgressBarQueue(Queue):

    def init_progress_bar(self, desc: str = "[blue]Parsing...") -> None:
        self.progress_bar = init_progress_bar(desc)
        self.progress_bar.start()
        self.task = self.progress_bar.add_task(desc, total=self.qsize(), )


    def get(self, block: bool = True, timeout: float | None = None) -> typing.Any:
        self.progress_bar.update(self.task, advance=1)
        return super().get(block, timeout)
