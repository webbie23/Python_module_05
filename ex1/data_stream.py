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

class DataStream():
    def __init__(self):
        self.processors = []
        

    def register_processor(self, proc: DataProcessor) -> None:
        self.proc = proc()
        self.processors.append([self.proc, 0])


  

    def process_stream(self, stream: list[Any]) -> None:
        self.stream = stream
        for proccesor in self.processors:
            for item in self.stream:
                if proccesor[0].validate(item) == True:
                    proccesor[0].ingest(item)
                    stream.remove(item)
                    proccesor[1] += 1
            
                    
        
    def print_processors_stats(self) -> None:
        for proccesor in self.processors:
            print(f"{proccesor[0]}: total {proccesor[0].inde} items processed, remaining {len(proccesor[0].stored_data.values())} on processor")
            print (proccesor[0].stored_data.values())
        
        #{len(proccesor.stored_data.values())}
 
def main():


    test = DataStream()
    print (type(NumericProcessor))
    print (type(NumericProcessor()))
    #test.register_processor(NumericProcessor())



    # test.register_processor(TextProcessor())
    # data: Any = (['Hello world', [3.14, -1, 2.71], [{'log_level': 'WARNING', ' log_message': 'Telnet access! Use ssh instead'}, {'log_level': 'INFO', 'log_message': 'User wil is connected'}], 42, ['Hi', 'five']])
    # test.process_stream(data)
    # test.print_processors_stats()




    # proc_num = DataStream()
    # print("=== Code Nexus - Data Stream ===\n\nInitialize Data Stream...\n== DataStream statistics ==\nNo processor found, no data\n\nRegistering Numeric Processor\n\nSend first batch of data on stream: ", data)
    # proc_num.register_processor(NumericProcessor())
    # proc_num.register_processor(LogProcessor())
    # proc_num.register_processor(TextProcessor())
    # print(proc_num.processors)
    # proc_num.process_stream(data)
    # proc_num.print_processors_stats()
    



    # try:
    #     proc_num.process_stream(data)
    # except ValueError as e:

    # proc_num.print_processors_stats()
    # proc_num.process_stream(data)
    # proc_num.print_processors_stats()
    # print("\nRegistering other data processors\nSend the same batch again\n== DataStream statistics ==")
    # proc_txt = DataStream()
    # proc_txt.register_processor(TextProcessor())
    # proc_log = DataStream()
    # proc_log.register_processor(LogProcessor())
    # proc_num.
    
    


    

















if __name__ == "__main__":
    main()
