import typing as t


class LoadWorkBookOptions(t.TypedDict):
    read_only: bool = False,
    keep_vba: bool = False,
    data_only: bool = False,
    keep_links: bool = True,
    rich_text: bool = False


class IterRowsColsOptions(t.TypedDict):
    min_row: int | None
    max_row: int | None
    min_col: int | None
    max_col: int | None
    values_only: t.Literal[True]
