from typing import List

from nltk.tokenize import word_tokenize

from components.pipeline.pipeline_module import PipelineModule
from components.pipeline.pipeline_data_structure import PipelineDataStructure


class Tokenizer(PipelineModule):
    """"""
    def __init__(self, lang: str = 'russian'):
        """"""
        self._lang = lang

    def tokenize(self, text_list: List[str]) -> List[List[str]]:
        """Tokenizes a list of texts.

        Args:
            text_matrix: A matrix with words of texts.

        Return:
            A matrix with tokenized texts.
        """
        tokenized_matrix = []

        for text in text_list:
            tokenized_matrix.append(word_tokenize(text, language=self._lang))

        return tokenized_matrix

    def process(self, pipeline_data: PipelineDataStructure) -> PipelineDataStructure:
        """"""
        loaded_data = pipeline_data.loaded_data
        pipeline_data.tokenized_data = self.tokenize(loaded_data)
        return pipeline_data
