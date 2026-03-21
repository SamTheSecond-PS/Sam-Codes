import csv
import os

'''Beginning of main class'''

class OnlyFileError(Exception):
    pass

class CSVcursor:
    def __init__(self, file):
        if os.path.exists(file):
            self.file = file
        else:
            raise OnlyFileError("Only files are allowed for CSVcursor class.")
        with open(self.file, newline="", encoding="utf-8") as f:
            self.data = []
            reader = csv.DictReader(f)
            for row in reader:
                self.data.append(row)

        self.position = 0
        self.selectedict = None
        self.selectelist = None

    def add_data(self, data) -> "CSVcursor":
        '''Adds a dictionary value to the csv file.'''
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict for add_data, got: {type(data).__name__}")
        self.data.append(data)
        return self

    def del_index(self, idx) -> "CSVcursor":
        '''It removes the value at a specific index.'''
        try:
            self.data.pop(idx)
        except IndexError:
            raise IndexError("Index out of range for del_index func.")

        return self
    
    def del_filter(self, condition_fn) -> "CSVcursor":
        '''Removes a value in the list/dict data by a lambda functions.'''
        if isinstance(self.data, list):
            self.data = [item for item in self.data if not condition_fn(item)]

        return self
    
    def mov_to_index(self, idx) -> "CSVcursor":
        '''If the data given is a list, moves to a specific index.'''
        if not isinstance(self.data, list):
            raise TypeError("mov_to_index only works for list data")
        if not isinstance(idx, int):
            raise ValueError(f"Expected int for idx, got {type(idx).__name__}")
        if not (0 <= idx < len(self.data)):
            raise IndexError(f"Index {idx} out of bounds of list of lenght {len(self.data)}")

        self.position = idx    
        return self
    
    def select_current(self, kv=False) -> "CSVcursor":
        '''Selects current index/key you're on.'''
        self.selectelist = self.data[self.position]
        return self
    
    def repl_curr_sel(self, new_data) -> "CSVcursor":
        '''Replaces the currently selected row with new_data.'''
        
        if self.selectelist is None:
            raise ValueError("No selection to replace. Call select_current() first.")
        
        if not isinstance(new_data, dict):
            raise ValueError(f"Expected dict for new_data, got {type(new_data).__name__}")
        

        self.data[self.position] = new_data
        self.selectelist = new_data
        
        return self


    def save(self):
        with open(self.file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.data[0].keys())
            writer.writeheader()
            writer.writerows(self.data)
    