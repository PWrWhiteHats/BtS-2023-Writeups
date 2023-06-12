To retrieve the hidden flag, a tool like steghide can be used to detect the existence of hidden data inside Marie Curie’s photo. Steghide will require a password in order to properly retrieve the hidden data.

The decrypted text should be: radioactivity
(Radioactivity being the main area of study associated to Marie Curie)

By using the aforementioned text above as the password to decrypt Marie Curie’s photo
using steghide, the following flag is found:

BtSCTF{M4r1e_Cur13_Skl0d0wsk4}


Example solution:

```
cewl -w wordlist -m 3 -d 1 https://en.wikipedia.org/wiki/Marie_Curie

stegseek file.jpg custom-wordlist
```