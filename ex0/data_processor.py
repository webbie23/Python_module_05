#!/usr/bin/python3

from abc import ABC, abstractmethod
from typing import Any
import inspect


class DataProcessor(ABC):
        

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if self.stored_data:
            oldest = (next(iter(self.stored_data)), self.stored_data.pop(next(iter(self.stored_data))))
        else:
            oldest = {}
        return (oldest)


class NumericProcessor(DataProcessor):
    def __init__(self):
        self.stored_data: dict[int, str] = {}
        self.last_key = 0
       
    def validate(self, data: Any) -> bool:
        if type(data) is not list:
            data = [data]
        for item in data:
            if (type(item) is not int) and (type(item) is not float) :
                return False
        return True    
        

    def ingest(self, data: float | int | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")  
        else:
            if type(data) is not list:
                    data = [data]
            for item in data:
                self.last_key += 1
                self.stored_data[self.last_key] = str(item)



# class TextProcessor(DataProcessor):
#     if type(data) is not list:
#     data = [data]
#     for item in data:
#         if (type(item) is not int) and (type(item) is not float) :
#             return False
#         return True


# def ingest(self, data: float | int | list[int | float]) -> None:
#     if not self.validate(data):
#         raise ValueError("Improper numeric data")
#     else:
#         if type(data) is not list:
#             data = [data]
#             if not self.stored_data.keys():
#                 max_key = 0
#             else:
#                 max_key = max(self.stored_data.keys())
#                 for item in data:
#                     max_key += 1
#                     self.stored_data[max_key] = item
        
#         pass


# class LogProcessor(DataProcessor):
    # def __init__(self, data):
    #     super().__init__(data)
    #     self.store_date: list[dict[str, str] | list[str, str]]

    # @abstractmethod
    # def validate(self, data: Any) -> bool:
    #     super().validate()
    #     pass

    # @abstractmethod
    # def ingest(self, data: dict[str, str] | list[str, str]) -> None:
        
    #     super().ingest()
    #     pass


def main():
    print("=== Code Nexus - Data Processor ===\n\n" \
            "Testing Numeric Processor...")
    print(NumericProcessor.__abstractmethods__)
    print(inspect.getsource(NumericProcessor))
    a= NumericProcessor()
    print(f"Trying to validate input '42' '{a.validate(42)}' :")

    print(f"Trying to validate input 'list' '{a.validate([67,79,10])}' :")
    a.ingest(42)
    a.ingest([67,79,10])
    print(a.stored_data)
    print(a.output())
    print(a.stored_data)
    print(a.output())
    print(a.stored_data)
    print(type(a.output()[1]))
    print(a.output())
    print(a.stored_data)
    print(a.output())
    print(a.stored_data)
    print(a.output())
    print(a.stored_data)
    a.ingest([1231,7321,12312])
    print(a.stored_data)
    print(a.output())
    print(a.stored_data)
    print(a.output())
    print(a.stored_data)




if __name__ == "__main__":
    main()