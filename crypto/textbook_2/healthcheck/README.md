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

We can easily see that the `sign` and `verify` functions are just slightly modified `decrypt` and `encrypt` functions correspondingly. The modification lies in additon of additional `mask1` and `mask2` parameters which are used for additonal RSA-like encryption of the flag:

```
flag_ct = encrypt(flag) ** mask1 % n**2
```

and for the `sign` function.

the `sign` function correlates to `decrypt` function in the following way:

```
#we are interested in s1
sign(c)[0] == D(c * mask2)
```

To recover the flag it is necessary to learn the value of `n`. To to that, we can observe the following:

we can rewrite 
```
mask2 = E(x)
``` 
for some unknown `x` and 
```
c = E(m)
``` 
for some `m`. Then:
```
sign(c) = D(E(m) * E(x)) = m + x mod N
```
Knowing that, we can sign `m=1` to recover the `x` value:

```
sign(1) = D(1 * mask2) = D(1 * E(x)) = D(E(x)) = x mod N
```
now we have a real decryption function to use, defined as:
```
# it doesn't matter that the result can be negative
Dec(c) = sign(c) - x = m
``` 
because 
```
sign(c) = m + x
```

Now we can ask the server to encrypt `m=1` and get:

```
ct1 = E(1)^mask1
```

By decrypting it using `sign` function and `x` value, we get:

```
Dec(E(1)^mask1) = 1 * mask1 mod n
```

By doing the same for `m=-1` we get:

```
ct2 = E(-1)^mask1
```

and by decrypting it:

```
Dec(E(-1)^mask1) = -1 * mask1 mod n = -mask1 mod n
```
Having both `-mask1 mod n` and `mask1 mod n` it is easy enough to recover n, because in 1/3 times `mask1 + (-mask1) = n` (other options are = 0 and = -n). In case of `mask1 + (-mask1) = 0` the algorhitm can be rerun.

Rest of the solution is very similiar to Textbook 1:

We know the value of `mask1`, so we can do the following:

```
flag = (sign(flag_ct) - x mod n) * mask1^-1 mod n 
``` 
because:
```
D(E(flag)^mask1)* mask1^-1 mod n = flag * mask1 * mask1^-1 mod n = flag mod n
```