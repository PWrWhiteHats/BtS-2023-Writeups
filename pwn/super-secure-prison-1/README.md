# Super secure prison 1

Prison's Warden asked me to create a management software for them. 
I made this yesterday and I hope nobody finds bugs there...

> Can you read the flag?

## Solution

```
from os import spawnvp, P_WAIT
print(spawnvp(P_WAIT, 'cat', ['cat', 'flag']))
STOP
```