from rich.progress import Progress, BarColumn, TaskProgressColumn, MofNCompleteColumn, TimeElapsedColumn, TimeRemainingColumn


progress_columns = (
    BarColumn(), 
    TaskProgressColumn(),
    "[blue]processed: ",
    MofNCompleteColumn(),
    TimeElapsedColumn(),
    "[blue]remaining: ",
    TimeRemainingColumn()
)


def init_progress_bar(description: str) -> Progress:
    return Progress(description, *progress_columns)