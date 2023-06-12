import axios from "axios";

import { loginUrl } from "@/urls";

export function doLogin(username, password) {
  return new Promise((resolve, reject) => {
    const payload = { username, password };

    axios.post(loginUrl(), payload)
      .then((response) => {
        resolve(response.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}
