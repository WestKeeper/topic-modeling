from typing import Dict, List
from components.pipeline.pipeline_data_structure import PipelineDataStructure

from gensim import corpora
from gensim.models import CoherenceModel
from gensim.models.ldamodel import LdaModel

from components.topic_model.topic_model import TopicModel


class LDAModel(TopicModel):
    """"""
    def __init__(self, filtered_matrix: List[List[str]]):
        """"""
        super.__init__()
        id2word, corpora = self._prepare_data(filtered_matrix)
        self._model = self._create_model(id2word, corpora)

    def _prepare_data(self, filtered_matrix: List[List[str]]) -> List[List[str]]:
        """"""
        id2word = corpora.Dictionary(filtered_matrix)
        corpus = [id2word.doc2bow(text) for text in filtered_matrix]

        return id2word, corpus

    def _create_model(self, id2word, corpus) -> LdaModel:
        """"""
        lda_model = LdaModel(corpus=corpus,
                             id2word=id2word,
                             num_topics=20,
                             random_state=100,
                             update_every=1,
                             chunksize=100,
                             passes=10,
                             alpha='auto',
                             per_word_topics=True)

        return lda_model

    def get_perplexity(self, corpus) -> float:
        """"""
        perplexity = self._model.log_perprlexity(corpus)
        return perplexity

    def get_coherence(self, filtered_matrix, id2word, corpus, coherence_method='u_mass') -> float:
        """"""
        coherence_model_lda = CoherenceModel(
            model=self._model, texts=filtered_matrix, dictionary=id2word,
            corpus=corpus, coherence=coherence_method)
        coherence = coherence_model_lda.get_coherence()
        return coherence

    def get_metrics(self, filtered_matrix, id2word, corpus) -> Dict[str: float]:
        """"""
        perplexity = self.get_perplexity(corpus)
        coherence = self.get_coherence(filtered_matrix, id2word, corpus)

        return {
            'perplexity': perplexity,
            'coherence': coherence
        }

    def print_topics(self):
        """"""
        self._model.print_topics()

    def process(self, pipeline_data: PipelineDataStructure) -> PipelineDataStructure:
        topic_data = self._get_metrics(pipeline_data.filtered_data)
        pipeline_data.topic_data = topic_data
        return pipeline_data
