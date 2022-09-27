from abc import abstractmethod

from components.pipeline.pipeline_module import PipelineModule


class Tokenizer(PipelineModule):
    """"""
    @abstractmethod
    def tokenize(self):
        """"""
        pass
