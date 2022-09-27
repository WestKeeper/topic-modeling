from abc import abstractmethod
from typing import Dict

from components.pipeline.pipeline_module import PipelineModule


class TopicModel(PipelineModule):
    """"""
    @abstractmethod
    def get_metrics() -> Dict[str: float]:
        """Gets a list of metrics and returns a dict name-val."""
        pass
