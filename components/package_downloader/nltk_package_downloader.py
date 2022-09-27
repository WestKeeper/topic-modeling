from typing import List

import nltk

from components.package_downloader.package_downloader import PackageDownloader
from components.pipeline.pipeline_data_structure import PipelineDataStructure


class NLTKPackageDownloader(PackageDownloader):
    """"""
    def __init__(self, packages: List[str]):
        """"""
        super.__init__(packages)

    def download_packages(self):
        """"""
        for package in self._packages:
            nltk.download(package)

    def process(self, pipeline_data: PipelineDataStructure) -> PipelineDataStructure:
        """"""
        self.download_packages()
        return pipeline_data
