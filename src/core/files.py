from dataclasses import InitVar, dataclass, field
from pathlib import Path


@dataclass(slots=True)
class File:
    path_input: InitVar[str | Path]
    path: Path = field(init=False)
    content: bytes = field(init=False)
    encoding: str = "utf-8"
    _is_changed = False

    def __post_init__(self, path_input: str | Path):
        self.path = self._validate_path(path_input)
        self.content = self.read_content()

    @staticmethod
    def _validate_path(path: Path | str) -> Path:
        if isinstance(path, str):
            path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File {path} does not exist")
        if not path.is_file():
            raise FileNotFoundError(f"{path} is not a file")
        return path

    def read_content(self):
        with self.path.open("rb") as f:
            return f.read()

    @property
    def extension(self) -> str:
        return self.path.suffix

    @property
    def default_inverted_path(self) -> Path:
        return self.path.with_suffix("_inverted")
