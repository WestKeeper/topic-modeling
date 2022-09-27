from abc import abstractmethod
from typing import List

from components.pipeline.pipeline_module import PipelineModule


class PackageDownloader(PipelineModule):
    """"""
    def __init__(self, packages: List[str]):
        """"""
        self._packages = packages

    @abstractmethod
    def download_packages(self):
        """"""
        pass
