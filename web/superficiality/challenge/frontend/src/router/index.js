import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Login from "@/views/Login.vue";
import Profile from "@/views/Profile.vue";
import NotFound from "@/views/NotFound.vue";
import Winner from "@/views/Winner.vue";

import { useUserStore } from "@/stores/user";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/:pathMatch(.*)*",
      name: "NotFound",
      component: NotFound,
    },

    {
      path: "/",
      name: "home",
      component: Home,
    },

    {
      path: "/login/",
      name: "login",
      component: Login,
    },

    // profile posts
    {
      path: "/profile/:userId/",
      name: "profile",
      component: Profile,
    },

    // profile about
    {
      path: "/profile/:userId/about/",
      name: "profile-about",
      component: Profile,
    },

    // profile friends
    {
      path: "/profile/:userId/friends/",
      name: "profile-friends",
      component: Profile,
    },

    // profile friends
    {
      path: "/winner/:winnerFlag",
      name: "winner",
      component: Winner,
    },
  ],
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();

  if (!userStore.isAuthenticated && to.name !== "login") {
    next({ name: "login" });
  } else {
    next();
  }
});

export default router;
