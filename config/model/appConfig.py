from dataclasses import dataclass, field


@dataclass(kw_only=True)
class AppConfig:
    timezone: str
    timestampFormat: str
    imageWidth: int
    imageHeight: int
    collectors: list[str] = field(default_factory=list, init=True)
    destinationFolder: str