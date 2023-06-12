# Textbook

The cryptosystem used in this challenge is [Paillier's](https://en.wikipedia.org/wiki/Paillier_cryptosystem) cryptosystem. The goal of the challenge was to decrypt the flag using `sign` and `verify` functions.

TO achieve that, first it should be noted that Paillier's cryptosystem has following partially homomorphic properties:

$$
D(E(m_1) * E(m_2) \mod n^2) = m_1 + m_2 \mod n
$$
$$
D(E(m_1)^m_2 \mod n^2 ) = m_2 * m_1 \mod n
$$

Now the encryption and decryption operations are defined as follows:

```python
def encrypt(m):
    r = getRandomRange(1, n)
    assert GCD(r, n) == 1
    mh = h(m)
    c = (pow(g, mh, n ** 2) * pow(r, n, n ** 2)) % (n ** 2)

    return c
```

```python
def decrypt(c):
    d = pow(c, phi, n ** 2)
    e = (d - 1) // n

    m = (e * mi) % n

    return m
```

We can easily see that the `sign` and `verify` functions are just slightly modified `decrypt` and `encrypt` functions correspondingly. The modification lies in additon of an additional `mask` parameter which is used for additonal RSA-like encryption of the flag:

```
flag_ct = encrypt(flag) ** mask % n**2
```

the `sign` function correlates to `decrypt` function in the following way:

```
#we are interested in s1
sign(m)[0] == decrypt(m * mask)
```

We observe that `verify` function recovers the message `m` from the signature, and we can implement our own `verify` function as it only uses the public key. Therefore by signing message `m = 1` we can recover the `mask` value as follows:


```
sign(1)[0] == decrypt(1 * mask) == decrypt(mask)
```

Mask recovery:

```
def verify_recover_m(s1, s2, pk):
    s1, s2 = sig
    n, g = pk
    mh = (h(m) * mask) % (n ** 2)
    
    m_prim = pow(g, s1, n ** 2) * pow(s2, n, n ** 2) % (n ** 2)

    return m_prim 

m = 1
sig = sign(m) 

mask = verify_m(sig[0], sig[1], pk)
```

Now knowing the mask, we can can observer that we can use `sign` to decrypt the flag by abusing homomorphic property:

```
D(flag_ct) == D(E(flag)^mask) = flag * mask % n
```

Because we only have access to `sign` function, we first have to multiply the `flag_ct` value by modular inversion of mask in `n ** 2`, and then to recover the flag, multiply the signature by the modular inversion of mask in $n$:

```
sign(flag_ct * mask^-1 % n ** 2) * mask^-1 % n = D(flag_ct * mask^-1 * mask % n ** 2) * mask^-1 % n = D(flag_ct) = D(E(flag)^mask) * mask^-1 % n = flag % n
```

and thats it!