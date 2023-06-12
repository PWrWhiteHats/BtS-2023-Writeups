<script>

import { mapStores } from 'pinia'

import UserName from './UserName.vue'

import { useProfileStore } from '@/stores/profile'


export default {
  props: ['comment'],

  components: {UserName},

  computed: {
    ...mapStores(useProfileStore),

    profileUrl() {
      return this.$router.resolve(
        {name: 'profile', params: {userId: this.comment.userid}}
      ).fullPath;
    },

    commentUser() {
      return this.profileStore.users[this.comment.userid];
    },
  },

  methods: {
    navigateToProfile(userId) {
      return this.$router.push({name: 'profile', params: {userId}})
    }
  }
}
</script>

<template>
  <div class="bg-dark-subtle rounded-1 p-2 mb-2 d-flex">
    <div class="me-3">
      <i class="bi bi-person fs-2 py-1 px-2 border rounded-circle"></i>
    </div>

    <div class="d-flex flex-column justify-content-center">
      <a
        class="fw-bold"
        :class="{'link-underline-danger': commentUser.isPrivate}"
        :href="profileUrl"
        @click.prevent="navigateToProfile(comment.userid)"
      ><UserName :user="commentUser" /></a>
      <p class="mb-0">{{ comment.message }}</p>
    </div>
  </div>
</template>
