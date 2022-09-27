from enum import Enum
from typing import Any, Dict
from dataclasses import dataclass


class PipelineDataStructureKey(Enum):
    """"""
    LOADED_DATA = 'loaded_data'
    TOKENIZED_DATA = 'tokenized_data'
    LEMMATIZED_DATA = 'lemmatized_data'
    FILTERED_DATA = 'filtered_data'
    VOCABULARY_DATA = 'vocabulary_data'
    TOPIC_DATA = 'topic_data'

@dataclass
class PipelineDataStructure:
    """"""
    loaded_data: Dict[str, Any]
    tokenized_data: Dict[str, Any]
    lemmatized_data: Dict[str, Any]
    filtered_data: Dict[str, Any]
    vocabulary_data: Dict[str, Any]
    filtered_by_freq_data: Dict[str, Any]
    topic_data: Dict[str, Any]
    topic_model: Any

