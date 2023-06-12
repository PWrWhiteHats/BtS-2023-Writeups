# Typhon by Ernikus
## Walkthrough

1. The .ZIP file is password-protected.
Among the files, there is a file named `!   cGVybXV0NSxuby1kdXBs`. Remove the "!   " (not necessary), and then decode the rest using CyberChief (base64 decoding). We obtain the message: `permut5,no-dupl`, which means "permutation of 5 words with no duplicates".

2. The above message refers to what we need to do with the remaining files in the .ZIP file - there are 50 empty files with strange names. The password is a combination of 5 of these files. We need to break it using a brute-force method. A permutation of 5 out of 50 without repetitions gives us a total of `254 251 200` possible combinations. Assuming that the average computer performs `1 million operations per second`, it will take `about 5 minutes` to crack it. I suggest preparing a dictionary (which can be over 6 GB in size!) and starting a brute-force attack with the dictionary to break the password for the .ZIP file.

You can use the script [permutations.py](files/permutations.py). For example, use `python3 permutations.py nebula.zip`.

**Correct combination: `n45Ap - zqFlr - Frept - nEpvy - 505sN`
`n45ApzqFlrFreptnEpvy505sN`**

3. Once you have the password, the flag is hidden in the file named `!   cGVybXV0NSxuby1kdXBs`:

`QnRTQ1RGe1RIM19GNExMXzBGXzBMWU1QVTV9`

Decode this using base64.

This is the flag.