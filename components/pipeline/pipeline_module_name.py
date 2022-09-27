from enum import Enum


class PipelineModuleName(Enum):
    PACKAGE_LOADER = 'package_downloader'
    DATA_LOADER = 'data_loader'
    TOKENIZER = 'tokenizer'
    LEMMATIZER = 'lemmatizer'
    FILTER = 'filter'
    VOCABULARY_BUILDER = 'vocabulary_buider'
    TOPIC_MODEL = 'topic_model'
    VISUALIZER = 'visualizer'
