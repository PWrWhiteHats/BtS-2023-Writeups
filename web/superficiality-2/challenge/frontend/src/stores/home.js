import { defineStore } from "pinia";

import { PostData } from "@/models";

export const useHomeStore = defineStore("home", {
  state() {
    return {
      posts: [],
    };
  },

  actions: {
    addNewPost(message) {
      this.posts.push(new PostData(message));
    },

    replacePosts(posts) {
      this.posts = posts;
    },
  },
});
