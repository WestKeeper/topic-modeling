from typing import List

import pymorphy2

from components.pipeline.pipeline_data_structure import PipelineDataStructure


class Pymorphy2Lemmatizer(Lemmatizer):
    """"""
    def __init__(self, lang: str = 'ru'):
        """"""
        self._lang = lang

    def lemmatize(self, tokenized_matrix: List[List[str]]) -> List[List[str]]:
        """Lemmatizes matrix texts via pymorphy2.

        Args:
            tokenized_matrix: A matrix with words of texts.

        Return:
            A matrix with lemmatized words.
        """
        morph = pymorphy2.MorphAnalyzer(self._lang)

        lemmatized_matrix = []
        for sent_idx, tokenized_sent in enumerate(tokenized_matrix):
            lemmatized_matrix.append([])
            for token_idx, token in enumerate(tokenized_sent):
                lemmatized_matrix[sent_idx].append(morph.parse(token)[0].normal_form)

        return lemmatized_matrix

    def process(self, pipeline_data: PipelineDataStructure) -> PipelineDataStructure:
        """"""
        tokenized_data = pipeline_data.tokenized_data
        pipeline_data.lemmatized_data = self.lemmatize(tokenized_data)
        return pipeline_data
