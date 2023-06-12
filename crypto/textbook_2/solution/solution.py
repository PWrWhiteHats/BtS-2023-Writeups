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

def handle_pow(r):
    print(r.recvuntil(b'python3 '))
    print(r.recvuntil(b' solve '))
    challenge = r.recvline().decode('ascii').strip()
    p = pwnlib.tubes.process.process(['kctf_bypass_pow', challenge])
    solution = p.readall().strip()
    r.sendline(solution)
    print(r.recvuntil(b'Correct\n'))

def h(s: bytes) -> int:
    return int.from_bytes(s, 'big')

def int_to_bytes(n: int) -> bytes:
    return n.to_bytes(n.bit_length() // 8 + 1, 'big', signed=True)

def verify(m, sig, pk):
    s1, s2 = sig
    n, g = pk
    mh = m
    
    m_prim = pow(g, s1, n ** 2) * pow(s2, n, n ** 2) % (n ** 2)
    return m_prim

def sign(m):
    r.sendline(b"1")
    (r.recvuntil(b'>'))
    r.sendline(m.hex().encode())
    (r.recvuntil(b's1 = '))
    s1 = int(r.recvline().decode())
    r.recvuntil(b's2 = ')
    s2 = int(r.recvline().decode())
    r.recvuntil(b'>')
    return s1, s2

def encrypt(m):
    r.sendline(b"3")
    (r.recvuntil(b'>'))
    r.sendline(m.hex().encode())
    (r.recvuntil(b'c = '))
    c = int.from_bytes(bytes.fromhex(r.recvline().decode()), 'big') 
    r.recvuntil(b'>')
    return c

# try few times, its easier than
# figureing out the proper algebra :P
for i in range(10):
    r = remote('127.0.0.1', 4455)

    #print(r.recvuntil('== proof-of-work: '))
    #if r.recvline().startswith(b'enabled'):
    #    handle_pow(r)

    #r.recvuntil(b'n = ')
    #print(r.recvline())

    r.recvuntil(b'flag = ')
    flag_enc = bytes.fromhex((r.recvline().decode()))

    (r.recvuntil(b'>'))

    # its paillier cryptosystem, additively homomorphic - all
    # you have to do is figure out algebra knowing that: 
    # sign === decryption
    # verify === encryption
    # Dec(E(m1) * E(m2) mod n **2) == m1 + m2 mod n
    # Dec(E(m1)^m2 mod n **2 ) == m2 * m1 mod n

    # mask2 = E(y, unknown)
    # Dec(1 * mask2) = y
    y = sign((1).to_bytes(1, 'big'))
    # print(verify(b'xd', (y[0], y[1]), (n, g)))
    y = y[0]

    # Dec(E(flag)^mask1 * mask2) = 
    # Dec(E(flag)^mask1 * Enc(y)) = flag * mask1 + y
    # flag * mask1 = Dec(E(flag)^mask1 * Enc(y)) - y % n
    flag_mask1 = (sign((flag_enc))[0] - y)

    # Enc(1)^mask1
    m = (1).to_bytes(1, 'big', signed=True)
    enc_mask1 = encrypt(m)

    # Dec(Enc(m)^mask1 * Enc(y)) = 1 * mask1 + y
    mask1_mod_n = (sign(int_to_bytes(enc_mask1))[0] - y) 
    m = (-1).to_bytes(1, 'big', signed=True)
    neg_enc_mask1 = encrypt(m)

    # Dec(Enc(m)^mask1 * Enc(y)) = -1 * mask1 + y
    neg_mask1_mod_n = (sign(int_to_bytes(neg_enc_mask1))[0] - y) 

    # n recovery
    # mask + (-mask) % n = 0 % n === n or 0 or -n in this case
    # try some times until we get something solvable
    decoded = None

    n = mask1_mod_n + neg_mask1_mod_n

    if n == 0:
        print("n == 0")
        r.sendline(b"4")
        r.close()
        continue

    if n < 0:
        n = -n
    try:
        #print(n)
        mask1 = mask1_mod_n % n
        #print(mask1)
        flag = (pow(mask1, -1, n) * (flag_mask1 % n)) % n
        print(int_to_bytes(flag))
        decoded = int_to_bytes(flag).decode()
        print(decoded)
        break
    except:
        r.sendline(b"4")
        r.close()
        continue

if not decoded:
    raise Exception("Failed to recover flag")

r.sendline(b"4")

exit(0)
