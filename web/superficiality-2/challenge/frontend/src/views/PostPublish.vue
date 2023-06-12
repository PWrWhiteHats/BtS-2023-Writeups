<script>

import {mapStores} from 'pinia'

import {PostData, UserData} from '@/models'
import Post from '@/components/Post.vue'

import {useUserStore} from '@/stores/user'
import {useProfileStore} from '@/stores/profile'
import {getPost, postPublish} from '@/api/posts'
import {getUser} from '@/api/users'

export default {

  components: {Post},

  data() {
    return {
      activePost: null,
      isLoading: true,
    }
  },

  computed: {
    ...mapStores(useUserStore, useProfileStore),

    activePostId() {
      return this.$route.params.postId;
    }
  },

  mounted() {
    const userId = this.userStore.userId;
    const token = this.userStore.token;

    const launchUserFetch = (targetUserId, successCallback) => {
      getUser(token, targetUserId)
        .then((data) => {
          const newUserData = new UserData(
            data.userid,
            data['full_name'],
            data.isjeff,
            data.isprivate,
          );

          this.profileStore.stashUser(targetUserId, newUserData);
          successCallback();
        })
        .catch(error => {
          console.error("Could not load user", error);
        });
    }

    const handlePostSuccess = (data) => {
        const postData = new PostData(
          data.postid,
          data.userid,
          data.message,
          [], // comments
          false, // isFresh
          data.ispublished,
          data.uuid,
        );

        launchUserFetch(postData.userid, () => {
            this.activePost = postData;
            this.isLoading = false;
        });


    };

    getPost(token, userId, this.activePostId)
      .then(handlePostSuccess)
      .catch(error => {
        console.error("Could not load post", error);
        this.isLoading = false;
      });
  },

  methods: {
    doPublish() {
      const token = this.userStore.token;

      postPublish(token, this.activePost.uuid)
        .then(data => {
          this.$router.push({
            name: 'profile',
            params: {userId: this.userStore.userId}
          });
        })
        .catch(error => {
          console.error("Could not publish post!", error);
        });
    }
  }
}

</script>


<template id="">

  <div v-if="isLoading" class="container container-fluid">
    <p>Loading ...</p>
  </div>

  <div v-else
    class="
      d-flex flex-column align-items-center
      container container-fluid
      border rounded-3 border-warning
      bg-dark-subtle my-5 p-4"
  >
    <div class="align-start borde">
      <p class="fs-5">Review post before publishing</p>
    </div>

    <Post
      v-if="!isLoading & (activePost !== null)"
      :post="activePost"
      no-publish-actions="true"
    />

    <button
      type="button" name="button"
      class="btn btn-danger"
      @click="doPublish"
    >Publish</button>
  </div>

</template>
