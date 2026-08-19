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
        if len(self.stored_data) == 0:
            return (0, '')
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
            for item in test_data:
                a, b = item.values()
                self.stored_data[self.new_key] = a + ": " + b
                self.new_key += 1


class DataStream():
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.proc = proc
        self.processors.append(self.proc)

    def process_stream(self, stream: list[Any]) -> None:
        self.stream = stream
        if len(stream) == 0:
            return
        for proccesor in self.processors:
            for item in self.stream:
                if proccesor.validate(item) is True:
                    proccesor.ingest(item)
                    stream.remove(item)
        if len(self.stream) != 0:
            for item in stream:
                print("DataStream error - "
                      "Can't process element in stream:", item)
        return

    def print_processors_stats(self) -> None:
        print("\n== DataStream statistics ==")
        if len(self.processors) == 0:
            print("No processor found, no data")
        for proccesor in self.processors:
            proc_data = proccesor.stored_data
            proc_name = str(proccesor).split('.')[1].split(' ')[0]
            print(
                f"{proc_name}: total {list(proc_data.keys())[-1]+1}"
                f" items processed, "
                f"remaining {len(proc_data.values())} on processor")


def main() -> None:
    data: Any = (['Hello world', [3.14, -1, 2.71],
                  [{'log_level': 'WARNING', ' log_message':
                      'Telnet access! Use ssh instead'},
                   {'log_level': 'INFO', 'log_message':
                       'User wil is connected'}], 42, ['Hi', 'five']])
    print("=== Code Nexus - Data Stream ===\n\nInitialize Data Stream")
    data_stream = DataStream()
    data_stream.print_processors_stats()
    print("\nRegistering Numeric Processor\n\nSend first batch "
          "of data on stream: ", data)
    data_stream = DataStream()
    num_proc = NumericProcessor()
    data_stream.register_processor(num_proc)
    data_stream.process_stream(data.copy())
    data_stream.print_processors_stats()
    print("\nRegistering other data processors\nSend the same batch again\n")
    text_proc = TextProcessor()
    log_proc = LogProcessor()
    data_stream.register_processor(text_proc)
    data_stream.register_processor(log_proc)
    data_stream.process_stream(data.copy())
    data_stream.print_processors_stats()
    print("\nConsume some elements from the data processors:"
          "Numeric 3, Text 2, Log 1")
    num_proc.output()
    num_proc.output()
    num_proc.output()
    text_proc.output()
    text_proc.output()
    log_proc.output()
    data_stream.print_processors_stats()


if __name__ == "__main__":
    main()
