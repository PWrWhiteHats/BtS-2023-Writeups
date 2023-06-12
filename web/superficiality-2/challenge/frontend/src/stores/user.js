import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";

export const useUserStore = defineStore("user", {
  state() {
    return {
      isAuthenticated: useLocalStorage("vanity/auth/isAuthenticated", false),
      userId: useLocalStorage("vanity/auth/userid", null),
      token: useLocalStorage("vanity/auth/token", null),
    };
  },

  actions: {
    persistToken(token) {
      this.token = token;
    },

    persistUserId(userId) {
      this.userId = userId;
    },

    clear() {
      this.isAuthenticated = false;
      this.token = null;
      this.userId = null;
    },
  },
});
