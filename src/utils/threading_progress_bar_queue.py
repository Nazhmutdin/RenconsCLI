import typing
from queue import Queue
from src.utils.progress_bar import init_progress_bar


class ThreadProgressBarQueue(Queue):

    def init_progress_bar(self) -> None:
        self.progress_bar = init_progress_bar("[blue]Parsing...")
        self.progress_bar.start()
        self.task = self.progress_bar.add_task("[blue]Parsing...", total=self.qsize(), )


    def get(self, block: bool = True, timeout: float | None = None) -> typing.Any:
        self.progress_bar.update(self.task, advance=1)
        return super().get(block, timeout)
