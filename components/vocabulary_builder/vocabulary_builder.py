from abc import abstractmethod

from components.pipeline.pipeline_module import PipelineModule


class VocabularyBuilder(PipelineModule):
    """"""
    @abstractmethod
    def build_vocabulary(self):
        """"""
        pass
