<script>
import Post from '@/components/Post.vue'
import NewPost from '@/components/NewPost.vue'

export default {
  props: ['posts', 'user'],

  components: {
    Post,
    NewPost,
  },

  methods: {
    emitNewPost(message) {
      this.$emit('newPost', message);
    }
  }
}
</script>

<template>

  <div class="d-flex flex-column align-items-center justify-content-center">
    <!-- new post -->
    <NewPost @newPost="emitNewPost" :user="user"/>

    <!-- existing posts -->
    <div
      class="w-100 d-flex justify-content-center"
      v-for="post in posts.slice().reverse()"
      :key="post.postid"
      ref="posts"
    >
      <Post :post="post" />
    </div>
  </div>
</template>
