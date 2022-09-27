from typing import Dict, List, Tuple

import pyLDAvis
from gensim.models.ldamodel import LdaModel


def visualize_lda(
    lda_model: LdaModel,
    corpus: List[List[List[Tuple[int]]]],
    id2word: Dict[int, List[str]]
):
    """"""
    pyLDAvis.enable_notebook()
    pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
