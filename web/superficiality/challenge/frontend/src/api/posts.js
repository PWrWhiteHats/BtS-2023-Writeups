import axios from "axios";

import { feedPostsUrl, postsUrl } from "@/urls";

export function fetchFeedPosts(token, userId) {
  return new Promise((resolve, reject) => {
    const config = {
      headers: { "Authorization": `Bearer ${token}` },
    };
    axios.get(feedPostsUrl(userId), config)
      .then((response) => {
        resolve(response.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}

export function fetchTimelinePosts(token, userId) {
  return new Promise((resolve, reject) => {
    const config = {
      headers: { "Authorization": `Bearer ${token}` },
    };
    axios.get(postsUrl(userId), config)
      .then((response) => {
        resolve(response.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}

export function makeNewPost(token, userId, message) {
  return new Promise((resolve, reject) => {
    const config = {
      headers: { "Authorization": `Bearer ${token}` },
    };

    const payload = {
      "message": message,
    };

    axios.post(postsUrl(userId), payload, config)
      .then((response) => {
        resolve(response.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}
