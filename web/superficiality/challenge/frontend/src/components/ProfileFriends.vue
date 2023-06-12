<script>

import { mapStores } from 'pinia'
import { useProfileStore } from '@/stores/profile'

import ProfilePhoto from './ProfilePhoto.vue'

import {UserData} from '@/models'

export default {
  props: ['profile'],
  components: {ProfilePhoto},
  computed: {
    ...mapStores(useProfileStore),
    friends() {
      return this.profile.friends.map(v => new UserData(v.userid, v['full_name']))
    },
  },

  methods: {
    friendUrl(friend) {
      return this.$router.resolve(
        {name: 'profile', params: {userId: friend.userid}}
      ).fullPath;
    },

    navigateToFriend(friend) {
      this.$router.push({name: 'profile', params: {userId: friend.userid}})
    }
  }
}
</script>

<template>
  <div class="col-12 bg-dark p-3 rounded-3">
    <div class="border-bottom mb-5">
      <h2>Friends</h2>
    </div>

    <div class="d-flex flex-wrap justify-content-center">
      <a
        class="
          friend-box
          text-white
          bg-secondary-subtle
          d-inline-flex flex-column justify-content-center align-items-center
          border rounded-3 p-3 m-2
          link-underline-dark
        "
        v-for="friend in friends"
        :href="friendUrl(friend)"
        @click.prevent="navigateToFriend(friend)"
      >
        <ProfilePhoto width=100 :user="friend" class="mb-4"/>
        <p>{{ friend.userFullName }}</p>
      </a>
    </div>

  </div>
</template>

<style scoped>
.friend-box {
  min-width: 20vmin;
}
</style>
