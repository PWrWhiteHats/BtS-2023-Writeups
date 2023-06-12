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

r = remote('127.0.0.1', 80)

#print(r.recvuntil('== proof-of-work: '))
#if r.recvline().startswith(b'enabled'):
#    handle_pow(r)

def int_to_bytes(n: int) -> bytes:
    return n.to_bytes(n.bit_length() // 8 + 1, 'big')

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


r.recvuntil(b'n = ')
n = int(r.recvline().decode())

r.recvuntil(b'g = ')
g = int(r.recvline().decode())

r.recvuntil(b'flag = ')
flag_enc = bytes.fromhex((r.recvline().decode()))

(r.recvuntil(b'>'))

mask_enc = sign((1).to_bytes(1, 'big'))
mask = verify(b'xd', mask_enc, (n, g))

# its paillier cryptosystem, additively homomorphic - all
# you have to do is figure out algebra knowing that: 
# sign === decryption
# verify === encryption
# Dec(E(m1) * E(m2) mod n **2) == m1 + m2 mod n
# Dec(E(m1)^m2 mod n **2 ) == m2 * m1 mod n

flag = int_to_bytes(((sign(flag_enc)[0] - (sign(int_to_bytes(mask))[0]) * pow(2, -1, n)) * pow(mask, -1, n )) % (n))
print(flag.decode())

r.sendline(b"3")

exit(0)
