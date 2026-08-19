#!/usr/bin/python3

from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.stored_data: Any = {}
        self.new_key: int = 0
        self.valid_value: Any = []

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        oldest: tuple[int, str]
        if self.stored_data:
            oldest = (next(iter(self.stored_data)),
                      self.stored_data.pop(next(iter(self.stored_data))))

        return (oldest)


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        self.stored_data: dict[int, str] = {}
        self.new_key = 0
        self.valid_value: list[int | float] = []

    def validate(self, data: int | float | list[int | float]) -> bool:
        validate_data: list[int | float]
        if not isinstance(data, list):
            validate_data = [data]
        else:
            validate_data = data
        for item in validate_data:
            if (type(item) is not int) and (type(item) is not float):
                return False
        self.valid_value = validate_data
        return True

    def ingest(self, data: list[int | float] | int | float) -> None:
        test_data: list[int | float]
        if not isinstance(data, list):
            test_data = [data]
        else:
            test_data = data
        if not test_data == self.valid_value:
            raise ValueError("Improper numeric data")
        else:
            for item in test_data:
                self.stored_data[self.new_key] = str(item)
                self.new_key += 1


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        self.stored_data: dict[int, str] = {}
        self.new_key = 0
        self.valid_value: list[str] = []

    def validate(self, data: Any) -> bool:
        validate_data: list[str]
        if not isinstance(data, list):
            validate_data = [data]
        else:
            validate_data = data
        for item in validate_data:
            if not isinstance(item, str):
                return False
        self.valid_value = validate_data
        return True

    def ingest(self, data: str | list[str]) -> None:
        test_data: list[str]
        if not isinstance(data, list):
            test_data = [data]
        else:
            test_data = data
        if not test_data == self.valid_value:
            raise ValueError("Improper string data")
        else:
            for item in test_data:
                self.stored_data[self.new_key] = item
                self.new_key += 1


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        self.stored_data: dict[int, str] = {}
        self.new_key = 0
        self.valid_value: list[dict[str, str]] = []

    def validate(self, data: Any) -> bool:
        validate_data: list[dict[str, str]]
        if not isinstance(data, list):
            validate_data = [data]
        else:
            validate_data = data
        for item in validate_data:
            if not isinstance(item, dict):
                return False
            else:
                if len(item) != 2:
                    return False
                for k, v in item.items():
                    if not (isinstance(k, str) and isinstance(v, str)):
                        return False, k, v
        self.valid_value = validate_data
        return True

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        test_data: list[dict[str, str]]
        if not isinstance(data, list):
            test_data = [data]
        else:
            test_data = data
        if not test_data == self.valid_value:
            raise ValueError("Improper dictionary data")
        else:
            print("test_data: ", test_data)
            for item in test_data:
                a, b = item.values()
                self.stored_data[self.new_key] = a + ": " + b
                self.new_key += 1


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n\n"
          "Testing Numeric Processor...")
    proc_test = NumericProcessor()
    print(f" Trying to validate input '42': {proc_test.validate(42)}")
    print(
        f" Trying to validate input 'hello'  : {proc_test.validate("hello")}")
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        proc_test.ingest("foo")
    except ValueError as e:
        print(" Got exception:", e)
    print(" Processing data: [1, 2, 3, 4, 5]")
    proc_test.validate([-1, 2, 3, 4, 5])
    proc_test.ingest([-1, 2, 3, 4, 5])
    print(" Extracting 3 values...")
    n = proc_test.output()
    print(f" Numeric value {n[0]} :{n[1]}")
    n = proc_test.output()
    print(f" Numeric value {n[0]} :{n[1]}")
    n = proc_test.output()
    print(f" Numeric value {n[0]} :{n[1]}")
    print("\nTesting Text Processor...")
    text_test = TextProcessor()
    print(" Trying to validate input '42': ", text_test.validate(42))
    print(" Processing data: ['Hello', 'Nexus', 'World']")
    text_test.validate(['Hello', 'Nexus', 'World'])
    text_test.ingest(['Hello', 'Nexus', 'World'])
    print(" Extracting 1 value...")
    t = text_test.output()
    print(f" Text value {t[0]} :{t[1]}")
    print("\nTesting Log Processor...")
    log_test = LogProcessor()
    print(" Trying to validate input 'Hello' : ",
          log_test.validate("Hello"))
    log_test_list = [{'log_level': 'NOTICE',
                      'log_message': 'Connection to server'},
                     {'log_level': 'ERROR',
                      'log_message': 'Unauthorized access!!'}]
    print(f" Processing data: {log_test_list}")
    log_test.validate(log_test_list)
    log_test.ingest(log_test_list)
    print(" Extracting 2 values...")
    test_log: tuple[int, str] = log_test.output()
    print(f" Numeric value {test_log[0]}: {test_log[1]}")
    test_log = log_test.output()
    print(f" Numeric value {test_log[0]}: {test_log[1]}")


if __name__ == "__main__":
    main()
