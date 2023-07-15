from abc import ABC, abstractmethod
from model.columnData import ColumnData


class AbstractBaseCollector(ABC):
    @abstractmethod
    def get_data(self) -> ColumnData:
        pass