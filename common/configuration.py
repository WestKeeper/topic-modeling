"""This module includes the configuration classes for main script."""
from typing import Union
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml


def parse_config(config_file_path: Path) -> Dict[str, Any]:
    """Parses yaml configuration file.

    Args:
        config_file_path: A path to yaml config file.

    Returns:
        A dictionary containing parsed config values:
            key - config variable name, value - config variable value.
    """
    # Prepare yaml loader
    loader = yaml.FullLoader

    # Load config
    with open(config_file_path) as config:
        return yaml.load(config, Loader=loader)


class PackageDownloaderConfig:
    """Encapsulates package downloader configuration parameters."""
    def __init__(self, config_data: Dict[str, Any]):
        """Creates an instance of the class.

        Args:
            config_data: A dictionary containing configuration parameters.
        """
        pass


class DataLoaderConfig:
    """Encapsulates data downloader configuration parameters."""
    def __init__(self, config_data: Dict[str, Any]):
        """Creates an instance of the class.

        Args:
            config_data: A dictionary containing configuration parameters.
        """
        pass


class TokenizerConfig:
    """Encapsulates tokenizer configuration parameters."""
    def __init__(self, config_data: Dict[str, Any]):
        """Creates an instance of the class.

        Args:
            config_data: A dictionary containing configuration parameters.
        """
        pass


class LemmatizerConfig:
    """Encapsulates lemmatizer configuration parameters."""
    def __init__(self, config_data: Dict[str, Any]):
        """Creates an instance of the class.

        Args:
            config_data: A dictionary containing configuration parameters.
        """
        pass


class FilterConfig:
    """Encapsulates filter configuration parameters."""
    def __init__(self, config_data: Dict[str, Any]):
        """Creates an instance of the class.

        Args:
            config_data: A dictionary containing configuration parameters.
        """
        pass


class VocabularyBuilderConfig:
    """Encapsulates vocabulary builder configuration parameters."""
    def __init__(self, config_data: Dict[str, Any]):
        """Creates an instance of the class.

        Args:
            config_data: A dictionary containing configuration parameters.
        """
        pass


class TopicModelConfig:
    """Encapsulates topic model configuration parameters."""
    def __init__(self, config_data: Dict[str, Any]):
        """Creates an instance of the class.

        Args:
            config_data: A dictionary containing configuration parameters.
        """
        pass


class VisualizerConfig:
    """Encapsulates visualizer configuration parameters."""
    def __init__(self, config_data: Dict[str, Any]):
        """Creates an instance of the class.

        Args:
            config_data: A dictionary containing configuration parameters.
        """
        pass


class Configuration:
    """Encapsulates all configuration parameters."""
    def __init__(self,
                 config_file_path: Optional[str] = None,
                 config_dict: Optional[Dict[str, Any]] = None):
        """Creates an instance of the class.

        There are 2 possibilities to load configuration data:
            - from configuration file using a path;
            - from configuration dictionary.
        At least one of according attributes must be not None.
        If both attributes are not None, the configuration file is used.

        Args:
            config_file_path: A path to config file to load configuration data from.
            config_dict: A configuration dictionary to load configuration data from.
        """
        if config_file_path is not None:
            self._load_from_config(config_file_path)
        elif config_dict is not None:
            self._load_from_dict(config_dict)
        else:
            raise ValueError('At least one of config_path and config_dict must be not None.')

    def _load_data(self, data: Dict[str, Any]):
        """Loads configuration data from dictionary.

        Args:
            data: A configuration dictionary to load configuration data from.
        """
        self.lang = data['lang']

        self.package_downloader_config = PackageDownloaderConfig(data['package_downloader'])
        self.data_loader_config = DataLoaderConfig(data['data_loader'])
        self.tokenizer_config = TokenizerConfig(data['tokenizer'])
        self.lemmatizer_config = LemmatizerConfig(data['lemmatizer'])
        self.filter_config = FilterConfig(data['filter'])
        self.vocabulary_buider_config = VocabularyBuilderConfig(data['vocabulary_buider'])
        self.topic_model_config = TopicModelConfig(data['topic_model'])
        self.visualizer_config = VisualizerConfig(data['visualizer'])

    def _load_from_config(self, config_file_path: str):
        """Reads configuration file and form configuration dictionary.

        Args:
            config_path: A configuration dictionary to load configuration data from.
        """
        data = parse_config(config_file_path)
        self._load_data(data)

    def _load_from_dict(self, config_dict: Dict[str, Any]):
        """Redirects a configuration dictionary.

        Args:
            config_dict: A configuration dictionary to load configuration data from.
        """
        self._load_data(config_dict)
