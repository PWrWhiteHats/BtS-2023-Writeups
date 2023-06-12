# Solution

After decompiling binary to C we see, that most of code is totally useless. It generates random variable r. Then it prints out every character of flag xored with r and increment r.

Binary takes 32 characters from file `flag`, but we don't know how long flag is. We can try to assume that it is shorter than 32, Which means we will know value of 0 xor (r+32). Than we can unxor every previous character and get some result. It will be flag, shorter than 32.

Example script in python in is [healthcheck.py](healthcheck.py)