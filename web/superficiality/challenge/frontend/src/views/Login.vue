<script>

import { mapStores } from 'pinia'

import { useUserStore } from '@/stores/user'
import { useAppStore } from '@/stores/app'
import { doLogin } from '@/api/authentication'

export default {
  computed: {
    ...mapStores(useUserStore),
    ...mapStores(useAppStore),
  },

  data() {
    return {
      inProgress: false,
      badCredentials: false,
    }
  },

  methods: {
    login() {
      this.inProgress = true;
      this.badCredentials = false;

      const username = this.$refs.username.value;
      const password = this.$refs.password.value;

      doLogin(username, password).then((data) => {
        this.$router.push({name: 'home'});
        this.userStore.persistToken(data.token);
        this.userStore.persistUserId(data['user_id']);
        this.userStore.isAuthenticated = true;
        this.inProgress = false;

      }).catch(error => {
        if (error.response.status === 400) {
          this.badCredentials = true;
        }
        this.inProgress = false;
      });
    },
  }
}
</script>

<template>
  <div class="m-0 vh-100 vw-100 d-flex flex-column justify-content-center align-items-center">

    <div class="text-danger fs-1 mb-5">
      <h1>❉ Vanity book</h1>
    </div>

    <div class="" v-if="inProgress">
      <p>Authenticating ...</p>
    </div>

    <div class="login-form" v-else>
      <div class="">
        <div class="mb-3">
          <label class="mb-2" for="username">Username</label>
          <input
            class="form-control" type="text" name="username"
            ref="username"
            @keydown.enter="login()"
          >
        </div>

        <div class="mb-4">
          <label class="mb-2" for="password">Password</label>
          <input
            class="form-control" type="password" name="password"
            ref="password"
            @keydown.enter="login()"
          >
        </div>

        <div class="d-flex justify-content-end">
          <button
            class="btn btn-danger"
            type="button"
            name="button"
            @click="login"
          >Login</button>
        </div>
      </div>

      <div class="text-end mt-3" v-if="badCredentials">
        <p>Bad credentials, please try again with right ones!</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-form {
  width: 40vw;
}
</style>
