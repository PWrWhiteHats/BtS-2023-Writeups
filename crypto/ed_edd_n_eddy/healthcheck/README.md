# Ed, Edd n Eddy

The goal of this challenge was to abuse weak verification algorhitm as defined in [RFC 8032](https://www.rfc-editor.org/rfc/rfc8032).

In order to do that, we need to realise that Edwards Curves are slighlty different than normal secure Elliptic Curves and the differnce that matters here is in the order of the curve. Namely, normal secure EC have order (number of elements of the curve) which is a prime number $q$. Edwards Curves have the property that the order of the curve is some prime number $q$ multiplied by a cofactor (4 for Ed448 and 8 for Ed25519):

$$
|EC| = q
$$
$$
|Ed448| = 4*q
$$
$$
|Ed25519| = 8*q
$$

Note: those $q$'s are obviously different numbers.

This results in a rather unexpected behaviour of a secure curve that the points on Edwards Curves can have different orders: some of the points will have order of the cofactor (or of a divisor of the cofactor), and some of the points will have order $q$. To remedy this, the base poing $B$ used to calculate every point in EdDSA signature scheme is of order $q$, and since this is a generator, every point that is used in this signature scheme also has order $q$. This means that the following verification equation works for every public key $A$ and ephemereal key $R$ constructed by mulltypling a scalar with base point $B$:

**Strong verification equation:**
$$
[s] * B == R + [k] * A
$$

It might be possible that the keys $A$ and $R$ have mixed order, i.e. they are constructed from a point $A^*$ of order $q$, and some point $P$ of different order (2, 4 or even 8 for Ed25519):

$$
A^{\text{mixed\_order}} = A^* + P^{2,4,8}
$$

For the rest of this writeup it will be assumed that we are working with Ed448 curve with a cofactor of 4, like in the challenge.

If the keys are constructed this way, the strong verification equation above will not hold even if valid secrets are used. This kind of construction is obviously invalid in the scheme, but for some reason RFC8032 defines alternative equation to make sure that mixed order keys work as well:

**Weak verification equation:**
$$
[4][s] * B == [4] * R + [4][k] * A
$$

by multiplying with the cofactor, we get rid of small order points (as multypling a point by their order/a multiple of their order results in the neutral element - $Point(0, 1)$) 

As we can see, both verifier in the challenge use explicitly use **strong verification**. The point of the challenge was to see that for OpenSSL implementation (`EddysPoint`) uses optimisation that transform the curve with an 4-isogeny $\phi$. This isogeny transforms the curve into a twisted Edwards Curve that has much better efficiency, but at the same time this transformation **gets rid of all points of order different than q** because the new curve has order $q$ instead of $4q$. Not going much into detail here (you can read about it in the [original paper](https://eprint.iacr.org/2014/027.pdf)) by applying the isogeny on a mixed order point $A^{\text{mixed\_order}}$ we are doing following calculations:

$$
\phi(A^{\text{mixed\_order}}) = \phi(A^* + P^{2,4}) = \phi(A^*) + \phi(P^{2,4}) = \phi(A^*)
$$

because $\phi( P^{2,4}) = Point(0,1)$ as $P^{2,4}$ lies in the kernel of the isogeny $\phi$

We see that the verification for `EddyVerifier` takes place on this new curve, as the dual (inverse) isogeny is never applied. This means that we can create such a mixed order ephemeral key $R$ that will verify for Eddy, and won't verify for Edd (as he uses strong verification and the low order point will not be factored out)

Knowing all of this, we can write a simple `sign` function, nearly excatly the same as in the RFC8032 with the addition of a point of order 2 --- $Point(0, -1)$. You can test order of this Point by doing following calculation using functions defined in this challenge:

$$
2 * Point(0, -1) = Point(0,1)
$$

The `sign` function will be then:

```python
def sign_maliciously(m, sk):
    r = H(str(sk) + m)
    B = Point(B_x, B_y)
    A = sk * B
    R = r * B + Point(0, -1) # here we add point of order 2
    k = H(str(R.x) + str(R.y) + str(A.x) + str(A.y) + m)
    S = (r + k * sk) % q
    return R, S
```

and by sending following signature back to the verifiers we can indeed see that it verifies for Eddy, while it doesn't verify for Edd.

This unexpected ambigiouty of the standard can create some potentially dangerous situations, where one signature will not verify for some verifiers, but it will for the others. In the context of a blockchain network, this might lead to chaos as some nodes will be mining unverified blocks.
