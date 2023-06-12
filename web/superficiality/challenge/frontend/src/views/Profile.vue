<script>

import { mapStores} from 'pinia';

import ProfileHeader from '@/components/ProfileHeader.vue'
import ProfileNav from '@/components/ProfileNav.vue'
import ProfileTimeline from '@/components/ProfileTimeline.vue'
import ProfileAbout from '@/components/ProfileAbout.vue'
import ProfileFriends from '@/components/ProfileFriends.vue'

import {ProfileData, PostData, UserData} from '@/models'

import { useUserStore } from '@/stores/user'
import { useProfileStore } from '@/stores/profile'

import { getProfile, getUser } from '@/api/users'
import { fetchTimelinePosts, makeNewPost } from '@/api/posts'

export default {
  components: {
    ProfileHeader,
    ProfileNav,
    ProfileTimeline,
    ProfileAbout,
    ProfileFriends,
  },

  data() {
    return {
      isLoading: true,
      profile: null,
      posts: [],
      activeUser: null,
    }
  },

  computed: {
    ...mapStores(useUserStore),
    ...mapStores(useProfileStore),

    isProfile() {
      return this.$route.name === 'profile';
    },

    isAbout() {
      return this.$route.name === 'profile-about';
    },

    isFriends() {
      return this.$route.name === 'profile-friends';
    },

    activeUserId() {
      return this.$route.params.userId;
    },
  },

  methods: {
    loadProfile() {
      const userId = this.activeUserId;
      const token = this.userStore.token;

      let user = null;
      if (Object.hasOwn(this.profileStore.users, this.activeUserId)) {
        user = this.profileStore.users[this.activeUserId];
      }

      const handleTimelineSuccess = (data) => {
        this.posts = data.posts.map(post => new PostData(
          post.postid,
          post.userid,
          post.message,
          post.comments,
        ));

        for (const commentUser of data.users) {
            const newUser = new UserData(
              commentUser.userid,
              commentUser['full_name'],
              commentUser.isjeff,
            );
            this.profileStore.stashUser(commentUser.userid, newUser);
        }

        setTimeout(() => {
          this.isLoading = false;
        }, 0);
      };

      const launchTimelineFetch = () => {
        const timelineFetchPromise = fetchTimelinePosts(token, userId)
          .then(handleTimelineSuccess)
          .catch(error => {
            this.isLoading = false;
            console.error("Could not load timeline:", error);
          });
      };

      const handleProfileSuccess = (data) => {
        // profile data handling
        const newProfile = new ProfileData(
          data['full_name'],
          data.location,
          data.birthday,
          data.friends,
        );
        this.profileStore.stashProfile(userId, newProfile);
        this.profile = newProfile;


        // launch timeline loading
        launchTimelineFetch();
      }

      const launchProfileFetch = () => {
        getProfile(token, userId)
          .then(handleProfileSuccess)
          .catch(error => {
            this.isLoading = false;
            console.error("Could not load profile:", error);
          });
      }

      const launchUserFetch = (successCallback) => {
        getUser(token, userId)
          .then((data) => {
            const newUserData = new UserData(
              data.userid,
              data['full_name'],
              data.isjeff,
            );

            this.profileStore.stashUser(userId, newUserData);
            successCallback();
            this.activeUser = newUserData;
          })
          .catch(error => {
            console.error("Could not load user", error);

            if (error.response.status === 404) {
              this.$router.push({name: 'NotFound'});
            }
          });
      }

      const isProfileDownloaded = Object.hasOwn(
        this.profileStore.profiles,
        userId
      );

      const isUserDownloaded = Object.hasOwn(
        this.profileStore.users,
        userId,
      );

      if (isProfileDownloaded) {
        this.profile = this.profileStore.profiles[userId];
      }

      if (isUserDownloaded) {
        this.activeUser = this.profileStore.users[userId];
      }

      if (isUserDownloaded) {
        if (isProfileDownloaded) {
          launchTimelineFetch();
        } else {
          launchProfileFetch();
        }
      } else {
        if (isProfileDownloaded) {
          launchUserFetch(launchTimelineFetch);
        } else {
          launchUserFetch(launchProfileFetch);
        }
      }

    },  // loadProfile

    addNewPost(message) {
      const token = this.userStore.token;

      const newPostData = new PostData(
        null,
        this.activeUserId,
        message,
        null,
        true
      );
      this.posts.push(newPostData);

      makeNewPost(token, this.activeUserId, message)
        .then((data) => {
          newPostData.postid = data.postid;
          newPostData.isFresh = false;
          setTimeout(() => {
            this.posts.pop();
            this.posts.push(newPostData);
          }, 1000);
        })
        .catch((error) => {
          this.posts.pop();
          console.error("Could not create new message", error);
        });
    }
  },  // methods

  mounted() {
    this.loadProfile();
  },

  created() {
    this.$watch('$route.params.userId', (newVal, oldVal) => {
      if (newVal !== null && newVal !== undefined) {
        this.loadProfile();
      }
    })
  },
}
</script>

<template>
  <div class="my-5">
    <p v-if="isLoading">Loading ...</p>

    <div class="mb-5 rounded" v-if="!isLoading">

      <!-- profile strip, profile photo and name -->
      <ProfileHeader :profile="profile" :user="activeUser" v-if="profile != null & activeUser != null"/>

      <!-- nav tavs -->
      <ProfileNav
        :isProfile="isProfile"
        :isAbout="isAbout"
        :isFriends="isFriends"
      />
    </div>

    <ProfileTimeline v-if="isProfile & !isLoading & activeUser != null" :posts="posts" @newPost="addNewPost" ref="timeline" :user="activeUser"/>
    <ProfileAbout v-if="isAbout & !isLoading" :profile="profile" />
    <ProfileFriends v-if="isFriends & !isLoading" :profile="profile" />
  </div>
</template>
