<script>
import { RouterLink } from 'vue-router'

import ProfileNavItem from '@/components/ProfileNavItem.vue'

export default {
  components: {
    RouterLink,
    ProfileNavItem,
  },
  props: ['isProfile', 'isAbout', 'isFriends'],
}
</script>

<template id="">
  <nav class="nav bg-dark border-top fs-5 p-3 rounded-bottom">
    <ProfileNavItem
      title="Posts"
      to-tab="profile"
      :is-active="isProfile" />

    <ProfileNavItem
      title="About"
      to-tab="profile-about"
      :is-active="isAbout" />

    <ProfileNavItem
      title="Friends"
      to-tab="profile-friends"
      :is-active="isFriends" />
  </nav>
</template>

<style scoped>
  .nav-item {
    cursor: pointer;
  }
</style>
