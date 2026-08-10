from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self, data):
        self.data = self.validate(data)
    pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        pass


class NumericProcessor(DataProcessor):
    def __init__(self, data):
        super().__init__(data)
        self.store_data: list[float | int | list[int] | list[float]]

    @abstractmethod
    def validate(self, data: Any) -> bool:
        super().validate()
        try:
            int(data)
        except TypeError:
            try:
                float(data)
            except TypeError:
                return(False)
        self.store_data.append(data)

    @abstractmethod
    def ingest(self, data: float | int | list[int] | list[float]) -> None:
        super().ingest()
        pass


class TextProcessor(DataProcessor):
    def __init__(self, data):
        super().__init__(data)
        self.store_date: list[str | list[str]]

    @abstractmethod
    def validate(self, data: Any) -> bool:
        super().validate()
        pass

    @abstractmethod
    def ingest(self, data: str | list[str]) -> None:
        super().ingest()
        
        pass


class LogProcessor(DataProcessor):
    def __init__(self, data):
        super().__init__(data)
        self.store_date: list[dict[str, str] | list[str, str]]

    @abstractmethod
    def validate(self, data: Any) -> bool:
        super().validate()
        pass

    @abstractmethod
    def ingest(self, data: dict[str, str] | list[str, str]) -> None:
        
        super().ingest()
        pass


def main():
    print("=== Code Nexus - Data Processor ===\n\n" \
            "Testing Numeric Processor...")
    input_data: Any = [42, "Hello"]
    for item in input_data:
        print("Trying to validate input '{item}' :", NumericProcessor.validate(item))






if __name__ == "__main__":
    main()