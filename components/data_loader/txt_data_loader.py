from pathlib import Path
from typing import List, Tuple

from components.data_loader.data_loader import DataLoader


class TXTDataLoader(DataLoader):
    """"""
    def __init__(self, text_file_regex: str = '**/*.txt', encoding: str = 'utf-8'):
        """"""
        self._encoding = encoding
        self._text_file_regex = text_file_regex

    def load_file(self, path: Path) -> str:
        """Loads text from txt file.

        Args:
            path: A path to a txt file.

        Return:
            A txt in a string.
        """
        text = ''
        with open(path, 'r', encoding=self._encoding) as fin:
            text = ''.join(fin)
        return text

    def load_files(self, paths: List[Path]) -> List[str]:
        """Loads a sample of texts in a list.

        Args:
            paths: A list of paths to files to be loaded.

        Return:
            A list with loaded texts.
        """
        texts = []
        for path in paths:
            text = self.load_file(path)
            texts.append(text)
        return texts

    def load_files_by_dir(self, path: str) -> Tuple[List[str], List[str]]:
        """"""
        paths = sorted(Path(path).glob(self._text_file_regex))
        texts = self.load_files(paths)
        return texts, paths
