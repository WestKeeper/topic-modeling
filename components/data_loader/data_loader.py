from abc import abstractmethod
from pathlib import Path
from typing import List, Tuple

from components.pipeline.pipeline_module import PipelineModule


class DataLoader(PipelineModule):
    """"""
    @abstractmethod
    def load_file(self, path: Path) -> str:
        """"""
        pass

    @abstractmethod
    def load_files(self, paths: List[Path]) -> List[str]:
        """"""
        pass

    @abstractmethod
    def load_files_by_dir(self, path: str) -> Tuple[List[str], List[str]]:
        """"""
        pass
