import os
import abc


class BaseSerializer(abc.ABC):
    def __init__(self, data_dir, file_name, settings=None):
        """
        :param data_dir: normally ~/.football_client
        :param file_name: name without extension, e.g., leagues
        :param settings: dict
        """
        self.data_dir = data_dir
        self.settings = settings or {}
        self.serialized_file = os.path.join(self.data_dir, f"{file_name}.{self.get_extension()}")

    @staticmethod
    def get_extension():
        """
        Get the file extension for the serialized data format (e.g., "json", "tsv")
        """
        raise NotImplementedError('get_extension() must be implemented in the derived class')

    @abc.abstractmethod
    def write(self, data):
        """
        Serialize data to the specified format
        """
        raise NotImplementedError('write() must be implemented in the derived class')

    @abc.abstractmethod
    def read(self):
        """
        Read serialized data from the specified format
        :return: dict
        """
        raise NotImplementedError('read() must be implemented in the derived class')
