To retrieve the hidden flag, a tool like steghide can be used to detect the existence of hidden data inside Marie Curie’s photo. Steghide will require a password in order to properly retrieve the hidden data, which will obviously need the provided text.

The provided text, albeit encrypted, does give out numerous hints in regard to the encryption method. The absence of symbols (.,_,-,=...etc) suggests that the cipher used may be poly-alphabetic.
Either by using dCode’s cipher identifier, or by using one of the most famous examples of poly-alphabetic encryption, the Vigenère cipher is detected. 

The decrypted text should be: radioactivity
(Radioactivity being the main area of study associated to Marie Curie)

By using the aforementioned text above as the password to decrypt Marie Curie’s photo
using steghide, the following flag is found:

BtSCTF{M4r1e_Cur13_Skl0d0wsk4}
