import axios from "axios";

import { currentUserIdUrl, profileUrl, usersUrl, userUrl } from "@/urls";

export function getCurrentUser(token) {
  return new Promise((resolve, reject) => {
    const config = {
      headers: { "Authorization": `Bearer ${token}` },
    };
    axios.get(currentUserIdUrl(), config)
      .then((response) => {
        resolve(response.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}

export function getUser(token, userId) {
  return new Promise((resolve, reject) => {
    const config = {
      headers: { "Authorization": `Bearer ${token}` },
    };
    axios.get(userUrl(userId), config)
      .then((response) => {
        resolve(response.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}

export function getProfile(token, userId) {
  return new Promise((resolve, reject) => {
    const config = {
      headers: { "Authorization": `Bearer ${token}` },
    };
    axios.get(profileUrl(userId), config)
      .then((response) => resolve(response.data))
      .catch((error) => reject(error));
  });
}
