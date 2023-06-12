import { defineStore } from "pinia";

import { CommentData, PostData, UserData } from "@/models";

export const useProfileStore = defineStore("profile", {
  state() {
    return {
      profiles: {},
      users: {},
    };
  },

  actions: {
    stashProfile(userId, profileData) {
      this.profiles[userId] = profileData;
    },

    stashUser(userId, userData) {
      this.users[userId] = userData;
    },
  },
});
