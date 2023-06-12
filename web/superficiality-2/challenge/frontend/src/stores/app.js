import { defineStore } from "pinia";

export const useAppStore = defineStore("app", {
  state() {
    return {
      isLoading: true,
    };
  },

  actions: {
    unload() {
      this.isLoading = false;
    },
  },
});
