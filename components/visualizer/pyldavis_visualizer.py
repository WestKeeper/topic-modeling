from typing import Dict, List, Tuple
import pyLDAvis
from gensim.models.ldamodel import LdaModel

from components.pipeline.pipeline_data_structure import PipelineDataStructure
from components.visualizer.visualizer import Visualizer


class PrimitiveVocabularyBuilder(Visualizer):
    """"""
    def __init__(self):
        """"""
        pass

    def visualize(
        self,
        lda_model: LdaModel,
        corpus: List[List[List[Tuple[int]]]],
        id2word: Dict[int, List[str]]
    ):
        """"""
        pyLDAvis.enable_notebook()
        pyLDAvis.gensim.prepare(lda_model, corpus, id2word)

    def process(self, pipeline_data: PipelineDataStructure) -> PipelineDataStructure:
        """"""
        topic_data = pipeline_data.topic_data
        topic_model = pipeline_data.topic_model
        filtered_by_freq_data = pipeline_data.filtered_by_freq_data
        # TODO(): filtered by freq data in not id2word. Needs to be resolved.
        self.visualize(topic_model, topic_data, filtered_by_freq_data)
        return pipeline_data

