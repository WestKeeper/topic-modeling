from abc import abstractmethod

from components.pipeline.pipeline_module import PipelineModule


class Lemmatizer(PipelineModule):
    """"""
    @abstractmethod
    def lemmatize(self):
        """"""
        pass
