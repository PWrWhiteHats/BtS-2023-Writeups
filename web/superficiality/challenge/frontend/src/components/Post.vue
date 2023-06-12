<script>

import { mapStores } from 'pinia'

import ProfilePhoto from './ProfilePhoto.vue'
import PostComment from './PostComment.vue'

import { useProfileStore } from '@/stores/profile'


export default {
  props: ['post'],
  components: {ProfilePhoto, PostComment},

  data() {
    return {
      isLiked: false,
      commentsEnabled: false,
      likesCount: 123,
    };
  },

  computed: {
    ...mapStores(useProfileStore),

    profileUrl() {
      return this.$router.resolve(
        {name: 'profile', params: {userId: this.post.userid}}
      ).fullPath;
    },

    postUser() {
      return this.profileStore.users[this.post.userid];
    },
  },

  methods: {
    toggleLike() {
      this.isLiked = !this.isLiked;
      if (this.isLiked) {
        this.likesCount += 1;
      } else {
        this.likesCount -= 1;
      }
    },

    toggleComments() {
      this.commentsEnabled = !this.commentsEnabled;
    },

    hasComments() {
      return this.post.comments.length > 0;
    },

    navigateToProfile(userId) {
      return this.$router.push({name: 'profile', params: {userId}})
    },
  },
}

</script>

<template>
  <div
    class="col-12 col-md-8 bg-dark border rounded-3 p-3 mb-4"
    :class="{'border-warning': post.isFresh}"
  >
    <!-- top side -->
    <div class="d-flex border-bottom mb-4">

      <!-- some icon -->
      <div class="p-3">
        <ProfilePhoto :user="postUser" />
      </div>

      <div class="d-flex flex-column justify-content-center">
        <!-- name -->
        <div class="">
          <a
            class="fs-5"
            :href="profileUrl"
            @click.prevent="navigateToProfile(post.userid)"
          >{{ postUser.userFullName }}</a><br/>
        </div>

        <!-- timestamp -->
        <div class="">
          <span class="text-secondary">2d</span>
        </div>
      </div>
    </div>

    <!-- content -->
    <div class="pb-4 mb-2 border-bottom">
        {{ post.message }}
    </div>

    <!-- reactions -->
    <div class="d-flex justify-content-center align-items-center mb-2">

      <!-- like button -->
      <div
        class="
          post-action rounded-1
          flex-fill d-flex justify-content-center
        "
        :class="{'text-danger': isLiked}"
        @click="toggleLike"
      >
        <i class="bi bi-hand-thumbs-up fs-3"></i>
      </div>

      <!-- comments button -->
      <div
        class="
          post-action rounded-1
          flex-fill d-flex justify-content-center
        "
        :class="{
          'text-danger': commentsEnabled,
          'disabled': !hasComments(),
          'text-secondary': !hasComments(),
        }"
        @click="hasComments() ? toggleComments() : null"
      >
        <i class="bi bi-chat-dots fs-3" :disabled="!hasComments()"></i>
      </div>
    </div>

    <div class="">
      <p class="fs-6 text-secondary"><strong>{{ likesCount }}</strong> liked your post</p>
    </div>

    <!-- actions like/comment -->
    <div v-show="commentsEnabled">
      <PostComment
        :comment="comment"
        v-for="comment in post.comments"
      />
    </div>

    <!-- comments -->

  </div>
</template>

<style scoped>
  .post-action {
    cursor: pointer;

    &:hover {
      background-color: #555;
    }

    &.disabled {
      cursor: default;

      &:hover {
        background-color: initial;
      }
    }
  }
</style>
