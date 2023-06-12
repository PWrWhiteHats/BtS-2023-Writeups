# Gucamole

This challenge required implementting the so-called [forbidden attack](https://csrc.nist.gov/csrc/media/projects/block-cipher-techniques/documents/bcm/comments/800-38-series-drafts/gcm/joux_comments.pdf) for GCM AES mode of operation. The goal of the challenge is to modify the ciphertext and forge a valid MAC for it.

The only difference between GCM in this challenge in this challenge and normal GCM was the Galois field we are working in. For normal GCM it is $GF(2^{128})$ and here we are using $GF(3^{81})$. For the context of the attack, the only difference is that we no longer have only $\oplus$ operation defined as both addition and substraction.

First step in the forbidden attack is to create at least two messages with the same $IV$. Here we see that $IV$ for messages is generated deterministically using `md5` hash, so we can trivially create two different payloads that will hash to the same output. Here you can see two example payloads `coll1` and `coll2`. By sending those two payloads as the destination, we receive a set of 5 ciphertext pairs with the same $IV_i$. In any counter mode having two different messages with the same $IV$ already is a catastrophic failure, as we can trivially calculate $m_1 \oplus m_2$ (or in our case, $m_1 + m_2$ or $m_1 - m_2$), but here we are interested in recovering the $MAC$ key, which we can do by solving a polynomial.

**Please note that all arythmetic operations presented here are done in $GF(3^{81})$!** Functions that do that are defined in `guacamole.py` as `add`, `sub` and `mul`.

To recover the key, we need to realise that the $MAC$ is constructed as follows:

$TAG(m) = Enc(IV_i) + GHASH(H, \text{tag\_string})$

And the $GHASH(H, m)$ function is defined as recursively as follows:

```
GHASH(H, m):
Y_0 = 0
for(i in blocks(m)):
    Y_i = (block_i + Y_i-1) * H
return Y_i
```

where $H$ is the $MAC$ key.

We can rewrite this in a more analysis friendly way as:

$$
GHASH(H, m) = \sum_{i=0}^n block_i * H^i
$$

where $n$ is block length of $m$

We can see that this is just a polynomial with $H$ as the unknown. By having two messages with the same $IV_i$, we can isolate the result of $GHASH(H, \text{tag\_string})$:

$$
TAG(m^i_0) - TAG(m^i_1) = Enc(IV_i) + GHASH(H, \text{tag\_string\_0}) - (Enc(IV_i) + GHASH(H, \text{tag\_string\_1})) = GHASH(H, \text{tag\_string\_0}) - GHASH(H, \text{tag\_string\_1})
$$

Now, knowing the $GHASH$ equation we can write:

$$
TAG(m^i_0) - TAG(m^i_1) = GHASH(H, \text{tag\_string\_0}) - GHASH(H, \text{tag\_string\_1})
$$

$$
= \sum_{i=0}^{n0} block^0_i * H^i - \sum_{i=0}^{n1} block^1_i * H^i 
$$

$$
= \sum_{i=0}^{max(n0,n1)} (block^0_i - block^1_i) * H^i
$$

$$ 
 TAG(m^i_0) - TAG(m^i_1) - \sum_{i=0}^{max(n0,n1)} (block^0_i - block^1_i) * H^i = 0
$$

We can obviously recreate the `tag_string`, because all values used there are public:
```
tag_string = additional_data + zero_vector_v + ct + zero_vector_u + A_64_len
```

Now, we can solve this polynomial using for example `sage`:

```
gf = GF(3**81,modulus='primitive', name="x") # define Galois Field
x = gf.gens()[0] 
ff = PolynomialRing(gf, name="h") # define Polynomial Ring
h = ff.gens()[0] # h is the name of the variable

def GHASH(M):
    sum = 0
    for i, m in enumerate(M):
        sum = (sum + m) * h
    return sum

# transfrom all known values (tags and tag_strings) into
# numbers in GF(3^81)
t1 = gf.from_integer(int.from_bytes(message[2], 'big'))
t2 = gf.from_integer(int.from_bytes(message_prim[2], 'big'))

M = (gf.from_integer(x) for x in tag_string0)
M_prim = (gf.from_integer(x) for x in tag_string1)

# define the polynomial to solve
poly = t1 - t2 - (GHASH(M) - GHASH(M_prim))

# get roots
H = poly.roots()[0][0]
```

It should be noted that not every root is the solution. It can be clearly seen that the degree of this polynomial is equal to number of blocks in `tag_string`, which is equal to 4 in this challenge. This means that the root is only a candidate for they MAC key, but that's why there are 5 pairs of messages --- one of them should contain the real value of $H$. 

After recovering candidates for $H$, rest of the challenge is creating a modified flag ciphertext `flag_ct_prim` with additional data changed to 'You're mine.'. To do that, we need to first recover the value of keystream $Enc(IV)$. We can do it trivially as now we can reconstruct $GHASH(H, tag\_string\_flag)$.

$$
TAG(flag) = Enc(IV) + GHASH(H, \text{tag\_string\_flag})
$$
$$
Enc(IV) = TAG(flag) - GHASH(H, \text{tag\_string\_flag})
$$

Now construct new desired tag_string:

```
tag_string_new = "You're mine." + zero_vector_v + ct + zero_vector_u + A_64_len
```

And calculate the tag for it:
$$
TAG'(FLAG) = Enc(IV) + GHASH(H, \text{tag\_string\_new})
$$

Now you can just send new ciphertext and it will be verified. Congrats on the flag!

Please note that the code in `healthcheck,py` checks for valid `H` candidate before it tries to modify flag ciphertext. This step is not necessary.

Here's some pseudocode that does just that:

```
hsh_new = ghash(H, "You're mine." + zero_vector_v + ct + zero_vector_u + A_64_len)

for H in candidates:
    hsh_old = ghash(H, old_tag_sring)
    # Enc(IV)
    keystream = flag_tag - hsh_old
    # construct new tag
    tag_new = keystream + hsh_new

    verified = send_flag_ct_with_tag(tag_new)
    if verified:
        break;
```