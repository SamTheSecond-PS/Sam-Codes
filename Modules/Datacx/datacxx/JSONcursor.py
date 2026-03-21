import json
import os

'''Beginning of main class'''

class OnlyFileError(Exception):
    pass

class JSONcursor:
    def __init__(self, file):
        if os.path.exists(file):
            self.file = file
        else:
            raise OnlyFileError("Only file objects are allowed for JSONcursor class.")
        with open(self.file, "r") as f:
            try:
                self.data = json.load(f)
            except json.JSONDecodeError:
                self.data = []

        self.position = 0
        self.selectedict = None
        self.selectelist = None

    def add_data(self, data) -> "JSONcursor":
        '''Adds the data given to the list/dict in memory 
        which is to be saved to the file later'''
        if isinstance(self.data, list):
            self.data.append(data)

        elif isinstance(self.data, dict)  and isinstance(data, dict):
            self.data.update(data)
        else:
            self.data = [self.data, data] if self.data is not None else [data]

        return self
    
    def remove_index(self, idx) -> "JSONcursor":
        '''If the data inside the class if a list, it removes 
        the value at a specific index.'''
        try:
            self.data.pop(idx)
        except IndexError:
            raise IndexError("Index out of range for remove_index func.")

        return self

    def remove_filter(self, condition_fn) -> "JSONcursor":
        '''Removes a value in the list/dict data by a lambda functions.'''
        if isinstance(self.data, list):
            self.data = [item for item in self.data if not condition_fn(item)]

        elif isinstance(self.data, dict):
            self.data = {k:v for k, v in self.data.items() if not condition_fn(k, v)}

        return self

    def mov_to_index(self, idx) -> "JSONcursor":
        '''If the data given is a list, moves to a specific index.'''
        if not isinstance(self.data, list):
            raise TypeError("mov_to_index only works for list data")
        if not isinstance(idx, int):
            raise ValueError(f"Expected int for idx, got {type(idx).__name__}")
        if not (0 <= idx < len(self.data)):
            raise IndexError(f"Index {idx} out of bounds of list of lenght {len(self.data)}")

        self.position = idx    
        return self
        
    def has_key(self, key) -> bool:
        '''Checks if the data, list or dict, has a specific key.'''
        if isinstance(self.data, dict):
            return key in self.data
        elif isinstance(self.data, list):
            return any(isinstance(d, dict) and key in d for d in self.data)
        
        return False

    def select_current(self, kv=False) -> "JSONcursor":
        '''Selects current index/key you're on.'''
        self.selectelist = self.data[self.position]
        if kv:
            self.selectedict = {k: v for k, v in self.selectelist.items()}
        return self

    def select_index(self, idx) -> "JSONcursor":
        if not isinstance(idx, int):
            raise ValueError(f"Expetcted int for select_index, got: {type(idx).__name__}")
        if not isinstance(self.data, list):
            raise TypeError("select_index only works for list data.")
        if not (0 <= idx < len(self.data)):
            raise IndexError(f"value {idx} out of bounds.")
        
        self.selectelist = self.data[idx]
        return self
    
    def select_dict(self, key):
        if not isinstance(self.data, dict):
            return TypeError("select_key only works for dict type data.")
        if not self.has_key(key):
            return KeyError(f"Key {key} does not exist.")
        
        self.selecdict = {f"{key}":f"{self.data[f"{key}"]}"}
        return self

    def save(self) -> "JSONcursor":
        '''Saves all the changes to the file.'''
        with open(self.file, 'w') as f:
            json.dump(self.data, f, indent=2)
        
        return self
    
    def repl_curr_sel(self, new_data) -> "JSONcursor":
        '''Replaces the currently selected item in data with new_data.'''

        if self.selectelist is None and self.selectedict is None:
            raise ValueError("No selection to replace. Call select_current() or select_dict() first.")

        if isinstance(self.data, list):
            self.data[self.position] = new_data
            self.selectelist = new_data

        elif isinstance(self.data, dict):
            if not isinstance(self.selectedict, dict):
                raise ValueError("selectedict must be a dict to replace a dict entry.")
            key = next(iter(self.selectedict.keys()))
            self.data[key] = new_data
            self.selectedict = {key: new_data}

        else:
            raise TypeError("Unsupported data type in self.data for replacement.")

        return self
        
    
    @property
    def selected_list(self):
        return self.selectelist
    
    @property
    def selected_dict(self):
        return self.selectedict
    
    @property
    def pos(self):
        return self.position
    

