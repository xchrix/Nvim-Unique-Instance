# Launch one unique Neovim gui instance for every path

## 概述

该项目提供一个为每个工作区目录启动一个唯一的Nvim图形界面实例的方法。

* 当多次为同一个工作区启动Nvim窗口时，会在已有的窗口中执行打开文件和位置跳转指令，不会打开新的窗口。
* 当之前的窗口被复用时，该窗口将被唤起并聚焦于。（暂时仅支持`Windows Terminal`）
* 当打开不同工作区时，启动器会为每个不同的工作区启动不同的窗口。

## 依赖

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

## 安装

```bash
pyinstaller ./nvim_instance.py --nowindow
```

然后，调用`dist/`目录生成的`nvim_instance`可执行文件。

## 使用
```bash
<path_to_nvim_instance exec> [-h] --project PROJECT --file FILE [--line LINE] [--column COLUMN]

-h, --help            show this help message and exit
  --project PROJECT, -p PROJECT
                        project path, open same path will reuse previous window, necessary argument
  --file FILE, -f FILE  file name, necessary argument
  --line LINE, -l LINE  line number to jump to
  --column COLUMN, -c COLUMN
                        column number to jump to
```

## 原理

该启动器使用路径区分不同的工作区，为每个路径分配唯一的命名管道。管道的名称： `nvim_instance_<path_basename>_<sha512 hex value for path>`。
每次启动时，启动器先试图使用生成的管道名连接到已有的实例。连接成功则在已有实例中打开文件并跳转到指定位置。连接失败则新建一个实例，并重试。

## 测试

已经在`Windows 10`平台进行测试。

## 许可证

[MPL 2.0](https://mozilla.org/MPL/2.0/) （c） 2023 [Chrix](https://github.com/xchrix)