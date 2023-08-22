#!/usr/bin/env python

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import os
import sys
import time
import re
import hashlib
import argparse

if __name__ == '__main__':
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        PIPE_DIR = r"\\.\\pipe\\nvim\\"
    elif sys.platform == 'linux':
        PIPE_DIR = r"/tmp/nvim/"

    parser = argparse.ArgumentParser(description="Nvim Instance management, launch one unique Nvim GUI for one path")
    # parser.add_argument('--exec', '-e', help='Nvim gui command, use neovide by default', default="neovide")
    parser.add_argument('--project', '-p',
                        help='project path, open same path will reuse previous window, necessary argument',
                        required=True)
    parser.add_argument('--file', '-f', help='file name, necessary argument', required=True)
    parser.add_argument('--line', '-l', help='line number to jump to', default=0)
    parser.add_argument('--column', '-c', help='column number to jump to', default=0)
    args = parser.parse_args()

    # command = args.exec

    # project = os.path.abspath('..')  # 测试切换目录指令是否正常工作
    # project = os.getcwd()
    project = os.path.abspath(args.project)

    print("project: " + project)
    base = os.path.basename(project)
    if len(base) == 0:
        # print("null")
        base = "root"
    if len(base) > 128:
        base = base[0:128]
    # print(base)
    hasher = hashlib.sha512()
    hasher.update(project.encode('utf-8'))
    instance_name = "nvim_instance_" + base + "_" + hasher.hexdigest()
    print(instance_name)
    # PIPE_NAME = r"\\.\pipe\nvim_godot\home"
    PIPE_NAME = PIPE_DIR + instance_name

    line = args.line
    col = args.column
    file_name = os.path.abspath(args.file)
    # print("file: " + file_name)
    # print("(" + str(line) + ", " + str(col) + ")")

    i = 0
    while True:
        ret: int = os.system("nvr --nostart -s --servername " + PIPE_NAME
                             + " -c \"cd  " + re.escape(project) + "  \" "
                             + " -c \"call cursor( " + str(line) + " , " + str(col) + " )  \" "
                             + " --remote " + file_name)

        if ret == 0:
            print("ok")
            break
        else:
            print("fail to exec command")

        if i >= 30:
            print("retry too many times, fail")
            quit(-1)

        if i ==0:
            # ret: int = os.system(command + " -- --listen " + PIPE_NAME)
            ret: int = os.system("wt nt nvim --listen " + PIPE_NAME + " ")
            # ret: int = os.system("neovide -- --listen " + PIPE_NAME)
            if ret != 0:
                print("can not create a new nvim instance")
            else:
                print("create a new nvim instance")
            time.sleep(0.1)
        i += 1

