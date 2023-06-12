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
from sage.all_cmdline import *
from guacamole import *
import math

def handle_pow(r):
    print(r.recvuntil(b'python3 '))
    print(r.recvuntil(b' solve '))
    challenge = r.recvline().decode('ascii').strip()
    p = pwnlib.tubes.process.process(['kctf_bypass_pow', challenge])
    solution = p.readall().strip()
    r.sendline(solution)
    print(r.recvuntil(b'Correct\n'))

r = remote('crypto-guacamole.ch3.bts.wh.edu.pl', 1337)

#print(r.recvuntil('== proof-of-work: '))
#if r.recvline().startswith(b'enabled'):
#    handle_pow(r)

with open("coll1", "rb") as f:
    msg1 = f.read()

with open("coll2", "rb") as f:
    msg2 = f.read()

r.recvuntil(b"flag ct = ")
flag_ct = bytes.fromhex(r.recvline().decode())
r.recvuntil(b"flag iv = ")
flag_iv = bytes.fromhex(r.recvline().decode())
r.recvuntil(b"flag t = ")
flag_tag = bytes.fromhex(r.recvline().decode())

candidates = []

for i in range(1):
    (r.recvuntil(b">"))
    r.sendline(b"1")
    (r.recvuntil(b">"))
    r.sendline((msg1 + i.to_bytes(2, 'big')).hex().encode())

    msgs_1 = []
    for j in range(5):
        r.recvuntil(b"ct = ")
        ct = bytes.fromhex(r.recvline().decode())
        r.recvuntil(b"iv = ")
        iv = bytes.fromhex(r.recvline().decode())
        r.recvuntil(b"t = ")
        t = bytes.fromhex(r.recvline().decode())
        msgs_1.append((ct, iv, t))

    r.recvuntil(b">")
    r.sendline(b"1")
    (r.recvuntil(b">"))
    r.sendline((msg2 + i.to_bytes(2, 'big')).hex().encode())

    msgs_2 = []
    for j in range(5):
        (r.recvuntil(b"ct = ").decode())
        ct = bytes.fromhex(r.recvline().decode())
        r.recvuntil(b"iv = ")
        iv = bytes.fromhex(r.recvline().decode())
        r.recvuntil(b"t = ")
        t = bytes.fromhex(r.recvline().decode())
        msgs_2.append((ct, iv, t))

    gf = GF(3**81,modulus='primitive', name="x")
    x = gf.gens()[0] 
    ff = PolynomialRing(gf, name="h")
    h = ff.gens()[0]

    def h_m(M):
        sum = 0
        for i, m in enumerate(M):
            sum = (sum + m) * h
        return sum

    for i in range(5):
        message = msgs_1[i]
        message_prim = msgs_2[i]

        X_blocks = [[], []]
        for i, ct in enumerate([message[0], message_prim[0]]):
            ct_len, A_len = len(ct) * 8, len(b"handshake") * 8
            u = 128 * math.ceil(ct_len / 128) - ct_len
            v = 128 * math.ceil(A_len / 128) - A_len

            zero_vector_v = b'\x00' * (v // 8)
            zero_vector_u = b'\x00' * (u // 8)
            A_64_len = int.to_bytes(A_len, 8, 'big')
            ct_64_len = int.to_bytes(ct_len, 8, 'big')

            X_str = b"handshake" + zero_vector_v + ct + zero_vector_u + A_64_len + ct_64_len
            
            m = len(X_str) // 16
            X_blocks[i] = [int.from_bytes(X_str[i*16:(i+1)*16], 'big') for i in range(m)]

        M = X_blocks[0]
        M_prim = X_blocks[1]
        t1 = gf.from_integer(int.from_bytes(message[2], 'big'))
        t2 = gf.from_integer(int.from_bytes(message_prim[2], 'big'))

        M = (gf.from_integer(x) for x in M)
        M_prim = (gf.from_integer(x) for x in M_prim)

        poly = t1 - t2 - (h_m(M) - h_m(M_prim))
        candidates += [root.to_integer() for root, n in poly.roots()]

print(r.recvuntil(b">"))
candidates = set([int(x).to_bytes(17, 'big') for x in candidates])
print(candidates)

for candidate in candidates:
    # get a random message
    ct, iv, tag = msgs_1[0]
    ct_len, A_len = len(ct) * 8, len(b"testy test !!!") * 8
    u = 128 * math.ceil(ct_len / 128) - ct_len
    v = 128 * math.ceil(A_len / 128) - A_len

    zero_vector_v = b'\x00' * (v // 8)
    zero_vector_u = b'\x00' * (u // 8)
    A_64_len = int.to_bytes(A_len, 8, 'big')
    ct_64_len = int.to_bytes(ct_len, 8, 'big')

    X_str = b"testy test !!!" + zero_vector_v + ct + zero_vector_u + A_64_len + ct_64_len

    hsh = ghash(candidate, X_str)

    ct_len, A_len = len(ct) * 8, len(b"handshake") * 8
    u = 128 * math.ceil(ct_len / 128) - ct_len
    v = 128 * math.ceil(A_len / 128) - A_len

    zero_vector_v = b'\x00' * (v // 8)
    zero_vector_u = b'\x00' * (u // 8)
    A_64_len = int.to_bytes(A_len, 8, 'big')
    ct_64_len = int.to_bytes(ct_len, 8, 'big')

    X_str = b"handshake" + zero_vector_v + ct + zero_vector_u + A_64_len + ct_64_len

    hsh_old = ghash(candidate, X_str)

    keystream = sub(int.from_bytes(tag, 'big'), int.from_bytes(hsh_old, 'big'))

    tag_new = add(int.from_bytes(hsh, 'big'), keystream).to_bytes(17, 'big')

    r.sendline(b"2")
    (r.recvuntil(b"ct:\n(hex)>"))
    r.sendline(ct.hex().encode())
    (r.recvuntil(b"add. data:\n(hex)>"))
    r.sendline((b"testy test !!!").hex().encode())
    (r.recvuntil(b"iv:\n(hex)>"))
    r.sendline(iv.hex().encode())
    (r.recvuntil(b"tag:\n(hex)>"))
    r.sendline(tag_new.hex().encode())
    test = (r.recvline().decode()).strip()
    (r.recvline().decode())
    r.recvuntil(b">")
    if test != "Decryption error":
        print("Candidate selected")
        H = candidate
        break

# forgery time
print("H", int.from_bytes(H, 'big'))


ct_len, A_len = len(flag_ct) * 8, len(b"You're mine.") * 8
u = 128 * math.ceil(ct_len / 128) - ct_len
v = 128 * math.ceil(A_len / 128) - A_len

zero_vector_v = b'\x00' * (v // 8)
zero_vector_u = b'\x00' * (u // 8)
A_64_len = int.to_bytes(A_len, 8, 'big')
ct_64_len = int.to_bytes(ct_len, 8, 'big')

X_str = b"You're mine." + zero_vector_v + flag_ct + zero_vector_u + A_64_len + ct_64_len

hsh = ghash(H, X_str)

ct_len, A_len = len(flag_ct) * 8, len(b"flag") * 8
u = 128 * math.ceil(ct_len / 128) - ct_len
v = 128 * math.ceil(A_len / 128) - A_len

zero_vector_v = b'\x00' * (v // 8)
zero_vector_u = b'\x00' * (u // 8)
A_64_len = int.to_bytes(A_len, 8, 'big')
ct_64_len = int.to_bytes(ct_len, 8, 'big')

X_str = b"flag" + zero_vector_v + flag_ct + zero_vector_u + A_64_len + ct_64_len

hsh_old = ghash(H, X_str)

keystream = sub(int.from_bytes(flag_tag, 'big'), int.from_bytes(hsh_old, 'big'))

tag_new = add(int.from_bytes(hsh, 'big'), keystream).to_bytes(17, 'big')

r.sendline(b"2")
print(r.recvuntil(b"ct:\n(hex)>"))
r.sendline(flag_ct.hex().encode())
print(r.recvuntil(b"add. data:\n(hex)>"))
r.sendline((b"You're mine.").hex().encode())
print(r.recvuntil(b"iv:\n(hex)>"))
r.sendline(flag_iv.hex().encode())
print(r.recvuntil(b"tag:\n(hex)>"))
r.sendline(tag_new.hex().encode())
test = (r.recvline().decode()).strip()
print(test)
print(r.recvuntil(b">"))

r.sendline(b"3")

if not test.startswith("flag"):
    raise Exception("Error") 