from abc import ABC
from abc import abstractmethod

from components.pipeline.pipeline_data_structure import PipelineDataStructure


class PipelineModule(ABC):
    """"""
    @abstractmethod
    def process(self, pipeline_data: PipelineDataStructure) -> PipelineDataStructure:
        """"""
        pass

