#!/usr/bin/env python3

from pwn import *

addr = "localhost"
port = 1337
p = remote(addr, port)

for i in range(420):
    print("i:", i)
    A = p.readline().decode("utf-8")[7:-2].split(", ")
    for i in range(len(A)):
        A[i] = A[i][1:-1]

    B = p.readline().decode("utf-8")[6:-2].split(", ")
    for i in range(len(B)):
        B[i] = B[i][1:-1]

    pos = 0
    for i in range(len(A)):
        if A[i] in B:
            pos = i
            break

    out = A[pos]
    for i in range(8):
        out += " " + A[17 + pos * 8 + i]

    p.readuntil("Send PSI to Alice: ")
    p.writeline(out)
    p.readuntil("Send PSI to Bob: ")
    p.writeline(out)
print(p.readline())
print()
p.close()
