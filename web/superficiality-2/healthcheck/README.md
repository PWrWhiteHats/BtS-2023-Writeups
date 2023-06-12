# Superficiality 2 - hack procedure

- open the dev console
- login in the website as kowalski
- post as yourself a message
- notice that the new message is unpublished and there is an intermediary step
  for publishing the post
- publish the post
- examine the dev console and notice some requests
  - POST to `/api/users/51/posts`
  - GET to `/api/users/51/post/<some_id>`
  - POST to `/api/publish-post/<some_uuid>`
- copy the `Authorization` header
- prepare a request client (either through a script or by using something like
  Postman)
- in the browser open the profile of a private user (visible and clearly marked
  as private in `Home` or in `Profile -> Friends`) and copy the ID of their
  profile from `/profile/<target_id>` (let's assume this is our target user)
- set a POST request to `/api/users/<target_id>/posts` with the previously
  copied `Authorization` header
- in the request body write `{"message": "I_SEE_EVERYTHING"}`
- send the request
- notice the response payload
  `{'reason': "You don't have rights to see a new unpublished post"}` which
  means the post was persisted to the database (somehow) but we still can't see
  the serialized body (particularly for obtaining the publishing UUID)
- prepare a GET request to `/api/users/51/post/<some_id>` with the previously
  copied `Authorization` header
  - make a few requests with different IDs like (1, 50, 100, 500)
  - notice that you have access to all the posts of all the users due to some
    flaw in filtering
  - notice the body of the successful responses
    ```
    {
      ...,
      'userid': <some_user_id>,
      'uuid': <post_uuid>,
      ...
    }
    ```
  - notice there are also 404's if you are trying a way too large post id
  - try to get the last post by trying multiple requests -> you know it is the
    last post if the post ID after it yields a 404 error
  - copy the post UUID from the response payload
- prepare a POST request to `/api/publish-post/<copied_post_uuid>` with the
  previously copied `Authorization` header
- send the request and obtain the flag from the response payload (under
  `winner_flag`)
