### Project structure:
```
folder_sync/
│
├── logs/
├── src/
│   ├── test/
│   │   ├── replica/
│   │   └── source/
│   │   
│   ├── settings.ini
│   ├── sync.py
│   └── utils.py
│
├── Makefile
├── README.md
└── requirements.txt
```

**src/sync.py**:
- Contains the main logic of the program.

**src/utils.py**:
- This module contains helper functions, such as the function of creating an address if it does not exist, etc.

**src/settings.ini**:
- This file contains the default settings for the program.

**src/test/replica | source**:
- These directories are used for testing purposes.


### Libraries used:
- argparse
- os
- shutil
- argparse
- asyncio
- filecmp
- hashlib
- inspect
- logging
- sys
- colorlog
- configparser

___
### How to run the program:
In **src/settings.ini** you can change the default settings of the program (in this case logging level).


There is **Makefile** in the root directory of the project. You can run the program by running the following command:

```bash
make help # To see the help message
```
```bash
make install # To install Venv and dependencies
```
```bash
make run # To run the program with default arguments
```
```bash
make run_sync # To run the program with default arguments
```

**Arguments:**
- `--sync`: To enable automatically sync the source and replica directories. (default is True)
- `--interval`: The interval in seconds to check for changes in the source directory. (default is 1s)
- `--log`: The path to the log file. (default is logs/{generated_timestamp}.log)
- `--replica`: The path to the replica directory. (default is "src/test/replica")
- `--source`: The path to the source directory. (default is "src/test/source")
- `--help`: To see the help message.

```bash
python3 src/sync.py -sync --interval 1 --log logs/mylog.log --replica /path/to/replica --source /path/to/source
```
___
## Author
[Martin Fencl](https://github.com/Howardzi-nn) | [martin@martinfencl.eu](mailto:martin@martinfencl.eu)
