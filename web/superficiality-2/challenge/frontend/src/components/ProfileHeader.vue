<script>
import SampleHeaderPhoto from './SampleHeaderPhoto.vue'
import ProfilePhoto from './ProfilePhoto.vue'

import { mapStores } from 'pinia'
import { useProfileStore } from '@/stores/profile'

export default {
  props: ['profile', 'user'],
  components: {
    SampleHeaderPhoto,
    ProfilePhoto,
  },
  computed: {
    ...mapStores(useProfileStore),
  }
}
</script>

<template>
  <div class="profile-header-background-strip rounded-top">
    <!-- <SampleHeaderPhoto /> -->
  </div>
  <div class="profile-presentation bg-dark p-3 d-flex">

    <div class="">
      <ProfilePhoto width=150 :user="user"/>
    </div>

    <div class="d-flex flex-fill flex-column justify-content-center px-3">
      <h1>{{ profile.userFullName }}</h1>
      <span>{{ profile.friends.length }} friends</span>
    </div>
  </div>
</template>

<style scoped>

</style>
