# Superficiality - hack procedure

- open the dev console
- login in the website as kowalski
- post as yourself a message
- in the console notice a **POST** request to `/api/users/51/posts` with the
  header `Authorization: Bearer <jwt_token>`
- decode the payload of the JWT token with a base64 decoder
- notice that the payload is `{"userid": 51}`
- open a profile of another user and grab the user ID from the URL
  `/profile/<target_id>` (let's assume this will be our target user)
- change the payload to match the user id of the target user
  (`{"userid": <target_id>}`) and encode it as base64
- replace the payload part of the JWT token with the newly fabricated payload
- prepare a request client (either through a script or by using something like
  Postman)
- set a POST request to URL to `/api/users/<target_id>/posts` and the
  `Authorization` header with your new fabricated JWT token
- set the request body to `{'message': "I_HAVE_PWNED_THIS_PLATFORM"}`
- Send the request and get the flag from the response (under `winner_flag`)
