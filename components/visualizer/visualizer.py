from abc import abstractmethod
from typing import Dict

from components.pipeline.pipeline_module import PipelineModule


class Visualizer(PipelineModule):
    """"""
    @abstractmethod
    def visualize() -> Dict[str: float]:
        """"""
        pass
