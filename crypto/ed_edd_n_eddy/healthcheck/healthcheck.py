#!/usr/bin/env python3
from pwn import remote
from hashlib import sha512
from dataclasses import dataclass


q = 2 ** 446 - 0x8335dc163bb124b65129c96fde933d8d723a70aadc873d6d54a7bb0d
p = 2 ** 448 - 2 ** 224 - 1
B_x = (224580040295924300187604334099896036246789641632564134246125461686950415467406032909029192869357953282578032075146446173674602635247710)
B_y = (298819210078481492676017930443930673437544040154080242095928241372331506189835876003536878655418784733982303233503462500531545062832660)
d = (-39081) % p

def H(message: str) -> bytes:
    return int.from_bytes(sha512(message.encode()).digest(), 'big') % q

@dataclass
class Point():
    x:      int
    y:      int

    def _point_add(self, P, Q):
        if (Q == P):
            return self._point_double(P)

        A = 1
        B = (A ** 2) % p
        C = (P.x * Q.x) % p
        D = (P.y * Q.y) % p
        E = (d * C * D) % p
        F = (B - E) % p
        G = (B + E) % p

        H = ((P.x + P.y) * (Q.x + Q.y)) % p

        X = (A * F * (H - C - D)) % p
        Y = (A * G * (D - C)) % p
        Z = (F * G) % p

        x = (X * pow(Z, -1, p)) % p
        y = (Y * pow(Z, -1, p)) % p

        return self.__class__(x, y)


    def _point_double(self, P):
        B = pow((P.x + P.y), 2, p)
        C = pow(P.x, 2, p)
        D = pow(P.y, 2, p)
        E = (C + D)  % p

        H = 1
        J = (E - 2 * H) % p

        X = ((B - E) * J) % p
        Y = (E * (C - D)) % p
        Z = (E * J) % p

        x = (X * pow(Z, -1, p)) % p
        y = (Y * pow(Z, -1, p)) % p

        return self.__class__(x, y)

    def _point_multiply(self, x, P):
        Q = Point(0, 1)  # Neutral element
        while x > 0:
            if x & 1:
                Q = Q + P
            P = P + P
            x >>= 1

        return Q

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __neg__(self):
        return self.__class__(self.x, -self.y)

    def __add__(self, other):
        return self._point_add(self, other)

    def __mul__(self, other: int):
        return self._point_multiply(other, self)

    def __rmul__(self, other: int):
        return self._point_multiply(other, self)

def handle_pow(r):
    print(r.recvuntil(b'python3 '))
    print(r.recvuntil(b' solve '))
    challenge = r.recvline().decode('ascii').strip()
    p = pwnlib.tubes.process.process(['kctf_bypass_pow', challenge])
    solution = p.readall().strip()
    r.sendline(solution)
    print(r.recvuntil(b'Correct\n'))

r = remote('127.0.0.1', 1337)

#print(r.recvuntil('== proof-of-work: '))
#if r.recvline().startswith(b'enabled'):
#    handle_pow(r)

# basically what is happening is that
# even though both Ed448 implementations
# use 'strong' verification (aka cofactorless),
# the optimizations made by applying 4-isogeny
# make it so the EddysPoint implementation
# implicitly uses verification with cofactors.
#
# it means that adding any point of order (2, 4) to
# to the challenge R (or to the public key!)
# will result in the following:
#   1. EddPoint implementation will reject the signature,
#   because it uses strong verification
#   2. EddyPoint implementation will validate the signature,
#   because event though the verification formula is the 'strong'
#   verification formula, the points of order (2, 4) are 'factored out'
#   by the isogeny:
#   φ_a(R) = [n]φ_a(R_org) + [m]φ_a((0, -1)) = [n]φ_a(R_org)
#   because (0, -1) is in the kernel of isogeny.

def sign_maliciously(m, sk):
    r = H(str(sk) + m)
    B = Point(B_x, B_y)
    A = sk * B
    R = r * B + Point(0, -1)
    k = H(str(R.x) + str(R.y) + str(A.x) + str(A.y) + m)
    S = (r + k * sk) % q
    return R, S

#print(r.recv_raw(numb=4096))
(r.recvuntil(b'message to sign: '))
m = r.recvline().decode().strip()
print(m)
(r.recvuntil(b'signing key: '))
sk = int(r.recvline().decode())
print(sk)
(r.recvuntil(b'>'))

r.sendline(b"yeah")

print(r.recvuntil(b'>'))
r.sendline(m.encode())

R, S = sign_maliciously(m, sk)
print(R, S)

(r.recvuntil(b'>').decode())
r.sendline(str(R.x).encode())
(r.recvuntil(b'>'))
r.sendline(str(R.y).encode())
(r.recvuntil(b'>'))
r.sendline(str(S).encode())

print(r.recvuntil(b'VERIFICATION').decode())
print(r.recvline().decode())
print(r.recvuntil(b'VERIFICATION').decode())
print(r.recvline().decode())
print(r.recvuntil(b'BtSCTF{').decode())
print(r.recvuntil(b'}').decode())

exit(0)
