import axios from "axios";

import { feedPostsUrl, postsUrl, postUrl, publishPostUrl } from "@/urls";

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

export function getPost(token, userId, postId) {
  return new Promise((resolve, reject) => {
    const config = {
      headers: { "Authorization": `Bearer ${token}` },
    };
    axios.get(postUrl(userId, postId), config)
      .then((response) => {
        resolve(response.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}

export function postPublish(token, postUuid) {
  return new Promise((resolve, reject) => {
    const config = {
      headers: { "Authorization": `Bearer ${token}` },
    };
    axios.post(publishPostUrl(postUuid), {}, config)
      .then((response) => {
        resolve(response.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}
