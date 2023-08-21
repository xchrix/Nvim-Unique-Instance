# Launch one unique Neovim gui instance for every path

## Brief

This project provides a way to launch a unique instance of the Nvim GUI for each workspace directory.

* When the Nvim window is launched multiple times for the same workspace, the open file and location jump instructions are executed in the existing window, and no new window is opened.
* When different workspaces are opened, the launcher launches a different window for each different workspace.

## Dependency

#### [neovim-remote](https://github.com/mhinz/neovim-remote.git)
```bash
pip3 install neovim-remote
```

#### pyinstaller

```bash
pip install pyinstaller
# or
conda install -c conda-forge pyinstaller
```

## Installation

```bash
pyinstaller ./nvim_instance.py --nowindow
```

The `nvim_instance` executable is then generated in the `dist/` directory.

## Usage
```bash
<path_to_nvim_instance exec> [-h] [--exec EXEC] --project PROJECT --file FILE [--line LINE] [--column COLUMN]

-h, --help            show this help message and exit
  --exec EXEC, -e EXEC  Nvim gui command, use neovide by default
  --project PROJECT, -p PROJECT
                        project path, open same path will reuse previous window, necessary argument
  --file FILE, -f FILE  file name, necessary argument
  --line LINE, -l LINE  line number to jump to
  --column COLUMN, -c COLUMN
                        column number to jump to
```

## Principle

The initiator uses paths to distinguish between different workspaces and assigns each path a unique named pipe. Named of the Pipe: `nvim_instance_<path_basename>_<sha512 hex value for path>`.
At each startup, the initiator first attempts to connect to the existing instance using the generated pipe name. If the connection is successful, the file is opened in the existing instance and jumps to the specified location. If the connection fails, create a new instance and try again.

## Test

Tested on `Windows 10`.

## License

[MPL 2.0](https://mozilla.org/MPL/2.0/) （c） 2023 [Chrix](https://github.com/xchrix)