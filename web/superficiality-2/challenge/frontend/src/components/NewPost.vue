<script>
import { mapStores } from 'pinia'

import ProfilePhoto from '@/components/ProfilePhoto.vue'

import { useProfileStore } from '@/stores/profile'
import { useHomeStore } from '@/stores/home'

export default {
  props: ['user'],
  components: {
    ProfilePhoto,
  },

  data() {
    return {
      newMessageValue: '',
    }
  },

  computed: {
    ...mapStores(useProfileStore, useHomeStore),
  },

  methods: {
    sendMessage() {
      if (this.newMessageValue === '') return;
      this.$emit('newPost', this.newMessageValue);
      this.newMessageValue = '';
    }
  },
}
</script>

<template>
  <div class="col-12 col-md-8 bg-body-tertiary border border-secondary rounded-3 p-3 mb-4">

    <div class="">
      <p class="mb-3">What's on your mind today?</p>
    </div>

    <div class="mb-3 d-flex justify-content-center">
      <ProfilePhoto width=55 class="me-3 border border-light" :user="user" />
      <div class="flex-fill d-flex flex-column justify-content-center">
        <input
          type="text"
          placeholder="write something ..."
          class="form-control bg-secondary-subtle d-block"
          v-model="newMessageValue"
          @keydown.enter="sendMessage()"
        >
      </div>
    </div>

    <div class="d-flex justify-content-center">
      <button
        type="button"
        name="button"
        class="btn btn-outline-danger"
        @click="sendMessage()"
      >Send</button>
    </div>
  </div>
</template>
