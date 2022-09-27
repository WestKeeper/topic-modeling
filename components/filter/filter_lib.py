import re
from typing import List

from nltk.corpus import stopwords

from components.filter.constants import PUNCTUATION_PATTERN
from components.common.constants import LANG


def lowercase_matrix(text_matrix: List[List[str]]) -> List[List[str]]:
    """Lower case of matrix words.

    Args:
        text_matrix: A matrix with words of texts.

    Return:
        A matrix with words in a lowercase.
    """
    lowercased_matrix = []

    for text in text_matrix:
        text_list = []
        for token in text:
            text_list.append(token.lower())

        lowercased_matrix.append(text_list)

    return lowercased_matrix

def remove_stopwords(tokenized_matrix: List[List[str]]) -> List[List[str]]:
    """Removes stop words from a matrix.

    Args:
        tokenized_matrix: A matrix with words of texts.

    Return:
        A matrix without stop words.
    """
    stop_words = stopwords.words(LANG)

    indices_to_remove_dict = {}
    for sent_idx, tokenized_sent in enumerate(tokenized_matrix):
        for token_idx, token in enumerate(tokenized_sent):
            if token in stop_words:
                if sent_idx not in indices_to_remove_dict:
                    indices_to_remove_dict[sent_idx] = []
                indices_to_remove_dict[sent_idx].append(token)

    for sent_idx in indices_to_remove_dict:
        for token in indices_to_remove_dict[sent_idx]:
            del tokenized_matrix[sent_idx][tokenized_matrix[sent_idx].index(token)]
    return tokenized_matrix


def remove_punct(tokenized_matrix: List[List[str]]) -> List[List[str]]:
    """Removes punctuation words and digits and 1-symbol-words from a matrix.

    Args:
        tokenized_matrix: A matrix with words of texts.

    Return:
        A matrix without punctuation words.
    """
    indices_to_remove_dict = {}
    for sent_idx, tokenized_sent in enumerate(tokenized_matrix):
        for token_idx, token in enumerate(tokenized_sent):
            punc_patterns = re.findall(PUNCTUATION_PATTERN, token.strip().lower())
            if (len(punc_patterns) > 0 and punc_patterns[0] == token.strip().lower()) or \
                (token.isdigit()) or \
                    (len(token) == 1):
                if sent_idx not in indices_to_remove_dict:
                    indices_to_remove_dict[sent_idx] = []
                indices_to_remove_dict[sent_idx].append(token)

    for sent_idx in indices_to_remove_dict:
        for token in indices_to_remove_dict[sent_idx]:
            del tokenized_matrix[sent_idx][tokenized_matrix[sent_idx].index(token)]
    return tokenized_matrix


def remove_word_edge_punct(token: str) -> str:
    """"""
    init_token = token
    while True:
        punc_patterns = re.findall(PUNCTUATION_PATTERN, token[0])
        if len(punc_patterns) > 0:
            token = token[1:]
        else:
            break

    while True:
        punc_patterns = re.findall(PUNCTUATION_PATTERN, token[-1])
        if len(punc_patterns) > 0:
            token = token[:-1]
        else:
            break

    return token


def remove_words_edge_punct(text_matrix: List[List[str]]) -> List[List[str]]:
    """Lower case of matrix words.

    Args:
        text_matrix: A matrix with words of texts.

    Return:
        A matrix with words in a lowercase.
    """
    lowercased_matrix = []

    for text in text_matrix:
        text_list = []
        for token in text:
            text_list.append(remove_word_edge_punct(token))

        lowercased_matrix.append(text_list)

    return lowercased_matrix
