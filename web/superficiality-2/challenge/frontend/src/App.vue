<script>
import { mapStores } from 'pinia'

import { RouterView } from 'vue-router';

import NavigationTab from './components/NavigationTab.vue';

import { useUserStore } from '@/stores/user'
import { useAppStore } from '@/stores/app'
import { useProfileStore } from '@/stores/profile'
import { getCurrentUser } from '@/api/users'

import { UserData } from '@/models'

export default {
  components: {
    NavigationTab,
  },

  computed: {
  ...mapStores(useUserStore),
  ...mapStores(useAppStore),
  ...mapStores(useProfileStore),

    isHome() {
      return this.$route.name === 'home';
    },

    isProfile() {
      return (
        this.$route.name === 'profile' |
        this.$route.name === 'profile-about' |
        this.$route.name === 'profile-friends'
      );
    },
  },

  mounted() {
      const userId = this.userStore.userId;
      const token = this.userStore.token;
      if (token === null) {
        setTimeout(this.appStore.unload, 500);
      } else {
        getCurrentUser(token)
          .then(data => {
            const userData = new UserData(data.userid, data['full_name'], data.isjeff, data.isprivate);
            this.profileStore.stashUser(userId, userData)
            setTimeout(this.appStore.unload, 500);
          })
          .catch(error => {
            console.log("can't get current user", error);
            if (error.response.status === 401) {
              this.userStore.clear()
            }
            setTimeout(this.appStore.unload, 500);
          });
      };
  },
}

</script>

<template>
  <div
    class="
      d-flex flex-column justify-content-center align-items-center
      fs-1 vh-100 vw-100
    "
    v-if="appStore.isLoading"
  >
    <div class="
      text-danger
      d-flex justify-content-center align-items-center
    " style="height: 100pt">
      <span class="loading-piece me-3">❉</span>
      <h1 class="d-inline-block mb-0 p-0">Vanity book</h1>
    </div>
  </div>

  <header v-if="!appStore.isLoading">
    <nav
      class="navbar navbar-expand-lg bg-dark"
      v-if="userStore.isAuthenticated"
    >
      <div class="container-fluid fs-2 text">

        <!-- brand -->
        <a
          class="navbar-brand text-danger"
          style="cursor: pointer"
          @click="$router.push({name: 'home'})"
        >❉ Vanity book</a>

        <!-- hamburger -->
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- actual menu -->
        <div
          class="collapse navbar-collapse"
            id="navbarSupportedContent">
          <ul
            class="
              nav navbar-nav
              justify-content-center
              me-auto mb-2 mb-lg-0
              flex-fill
            ">

            <!-- home link -->
            <NavigationTab
              :toLink="{name: 'home'}"
              :is-active="isHome"
              icon="bi-house" />

            <!-- profile link -->
            <NavigationTab
              :toLink="{name: 'profile', params: {userId: userStore.userId}}"
              :is-active="isProfile"
              icon="bi-person" />
          </ul>
        </div>

        <div class="fs-6 px-3">
          <span class="text-secondary font-monospace">Made by N3m3X1s</span>
        </div>
      </div>
    </nav>
  </header>

  <main
    v-if="!appStore.isLoading"
    :class="{'container': userStore.isAuthenticated,'container-fluid': userStore.isAuthenticated}"
  >
    <RouterView />
  </main>
</template>

<style scoped>
.logout {
  cursor: pointer;

  &:hover {
    background-color: var(--bs-secondary-bg) !important;
  }
}

@keyframes spin {
  from {
    rotate: none;
  }

  to {
    rotate: 360deg;
  }
}

.loading-piece {
  font-size: 60pt;
  display: inline-block;
  animation-name: spin;
  animation-duration: 3s;
  animation-iteration-count: infinite;
  animation-timing-function: linear;

}
</style>
