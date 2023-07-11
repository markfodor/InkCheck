from dataclasses import dataclass, field

@dataclass(kw_only=True)
class ColumnData:
    title: str
    is_list: bool
    text: str = field(default=None, init=False)
    items: list[str] = field(default_factory=list, init=False)