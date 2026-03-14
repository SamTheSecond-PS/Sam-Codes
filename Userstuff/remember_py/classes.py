from abc import ABC, abstractmethod

class InvalidOperationError(Exception):
    pass

class Stream(ABC):
    def __init__(self):
        self.opeened = False

    def open(self):
        if self.opened:
            raise InvalidOperationError("Stream is already opened.")
        self.opened = True
    
    def close(self):
        if not self.opened:
            raise InvalidOperationError("Stream is already closed.")
        self.opened = False

    @abstractmethod
    def read(self):
        pass

        
class FileStream(Stream):
    def read(self):
        print("reading data")

class NetworkStream(Stream):
    def read(self):
        print("Reading data from a network")

class MemoryStream(Stream):
    def read(self):
        print("Reading data from memory stream.")

stream = MemoryStream()
stream.open()

________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________ # type: ignore



