<script>

import { mapStores } from 'pinia'

import ProfilePhoto from './ProfilePhoto.vue'
import PostComment from './PostComment.vue'
import UserName from './UserName.vue'

import { useProfileStore } from '@/stores/profile'


export default {
  props: ['post', 'noPublishActions'],
  components: {ProfilePhoto, PostComment, UserName},

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

    publishUrl() {
      return this.$router.resolve(
        {name: 'publish-post', params: {postId: this.post.postid}}
      ).fullPath;
    }
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


    goToPublish() {
      this.$router.push({name: 'publish-post', params: {postId: this.post.postid}});
    },
  },
}

</script>

<template>

  <div
    class="col-12 col-md-8 bg-dark border rounded-3 p-3 mb-4"
    :class="{'border-warning': !post.isPublished & !noPublishActions}"
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
            :class="{'link-underline-danger': postUser.isPrivate}"
            @click.prevent="navigateToProfile(post.userid)"
          ><UserName :user="postUser" /></a><br/>
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
        :class="{
          'text-danger': isLiked,
          'disabled': !post.isPublished,
          'text-secondary': !post.isPublished,
        }"
        @click="post.isPublished ? toggleLike() : null"
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

    <div
      v-if="!post.isPublished & !noPublishActions"
      class="text-warning d-flex justify-content-between align-content-center"
    >
      <div class="d-flex flex-column justify-content-center">
        <span>Your post is not published</span>
      </div>

      <a
        class="btn btn-warning"
        :href="publishUrl"
        @click.prevent="goToPublish"
      >Go to publish overview</a>
    </div>

    <div v-if="post.isPublished" class="">
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
