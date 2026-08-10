from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self, data):
        self.data = data
        self.store_data:str = ['yes']

    @abstractmethod
    def validate(self, data: Any) -> bool:
        
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass
    

    def output(self) -> tuple[int, str]:
        return (self.store_data)


class NumericProcessor(DataProcessor):
    def __init__(self, data):
        super().__init__(data)

    def validate(self) -> bool:
        try:
            int(self.data)
        except ValueError:
            try:
                float(self.data)
            except ValueError:
                return(False)
        self.store_data.append(str(self.data))
        return(True)

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
    a = NumericProcessor("hello")
    print(f"Trying to validate input '42'", a.validate()  )
    #a= NumericProcessor("Hello")
    #print(f"Trying to validate input '{a.validate()}' :")
    print (a.store_data)
    
    






if __name__ == "__main__":
    main()