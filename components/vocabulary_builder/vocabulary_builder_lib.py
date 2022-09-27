import collections


def build_vocabulary(tokenized_texts, max_size=1000000, max_doc_freq=1, min_count=5, pad_word=None):
    word_counts = collections.defaultdict(int)
    doc_n = 0
    for txt in tokenized_texts:
        doc_n += 1
        unique_text_tokens = set(txt)
        for token in unique_text_tokens:
            word_counts[token] += 1

    word_count = {word: cnt for word, cnt in word_counts.items() if cnt >= min_count and cnt / doc_n <= max_doc_freq}

    return word_count


def filter_by_freq(tokenized_texts, max_size=1000000, max_doc_freq=1, min_count=5, pad_word=None):
    word_counts = collections.defaultdict(int)
    doc_n = 0
    for txt in tokenized_texts:
        doc_n += 1
        unique_text_tokens = set(txt)
        for token in unique_text_tokens:
            word_counts[token] += 1

    word_count = word_counts

    indices_to_remove_dict = {}
    for sent_idx, tokenized_sent in enumerate(tokenized_texts):
        for token_idx, token in enumerate(tokenized_sent):
            if word_count[token] < min_count or word_count[token] / doc_n > max_doc_freq:
                if sent_idx not in indices_to_remove_dict:
                    indices_to_remove_dict[sent_idx] = []
                indices_to_remove_dict[sent_idx].append(token)

    for sent_idx in indices_to_remove_dict:
        for token in indices_to_remove_dict[sent_idx]:
            del tokenized_texts[sent_idx][tokenized_texts[sent_idx].index(token)]

    return tokenized_texts
