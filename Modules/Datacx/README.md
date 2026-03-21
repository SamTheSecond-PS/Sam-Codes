## datacx module

The module has **two items**:
-CSVcursor
-JSONcursor

Both help is usage of CSV and JSON files respectively

# Installation

```bash
pip install datacx
```

# usage

```Python
from datacx import JSONcursor # Or CSV, users wish

cs = JSONcursor("filename")
data = [{"key":"value"},
 {"key2":"value2"}]
cs.add_data(data) # Adds data to the file
cs.save() # saves data in the file
```
