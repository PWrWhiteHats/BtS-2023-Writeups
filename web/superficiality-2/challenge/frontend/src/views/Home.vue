<script>

import { mapStores } from 'pinia'

import Post from '@/components/Post.vue'

import { useHomeStore } from '@/stores/home'
import { useUserStore } from '@/stores/user'
import { useProfileStore } from '@/stores/profile'

import { fetchFeedPosts } from "@/api/posts";

import { PostData, CommentData, UserData } from '@/models';

export default {
  components: {
    Post,
  },

  data() {
    return {
      somethingWentWrong: false,
      isLoading: true,
    };
  },

  computed: {
    ...mapStores(useHomeStore),
    ...mapStores(useUserStore),
    ...mapStores(useProfileStore),

    noPosts() {
      return this.homeStore.posts.length === 0;
    }
  },

  mounted() {
    const token = this.userStore.token;
    const userId = this.userStore.userId;

    fetchFeedPosts(token, userId)
      .then((posts) => {

        // handle the feed posts storage
        const newPostsData = posts.posts.map(
          (post) =>
            new PostData(
              post.postid,
              post.userid,
              post.message,
              post.comments.map(
                comment => new CommentData(
                  comment.commentid,
                  comment.userid,
                  comment.message,
                )
              ),
              false,
              post.ispublished,
              post.uuid,
            ),
        );

        this.homeStore.replacePosts(newPostsData);

        // stash profiles
        for (const postUser of posts.users) {

            const newProfile = new UserData(
              postUser.userid,
              postUser['full_name'],
              postUser.isjeff,
              postUser.isprivate,
            );
            this.profileStore.stashUser(postUser.userid, newProfile);
        }

        this.isLoading = false;
      })
      .catch(error => {
        this.somethingWentWrong = true;
        console.error("problem with fetching feed", error);
      });
  }

}
</script>

<template>
  <div class="d-flex flex-column align-items-center mt-5">
    <Post v-for="post in homeStore.posts.slice().reverse()" :post="post" />
  </div>
  <div v-if="noPosts & !isLoading">
    <p>No posts !</p>
  </div>
  <div v-if="isLoading">
    <p>Loading ...</p>
  </div>
</template>

<style scoped>

</style>
