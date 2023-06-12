let SERVER = `${window.location.origin}/api`;

if (import.meta.env.DEV) {
  SERVER = "http://localhost:8000";
}

// authentication
const loginUrl = () => `${SERVER}/login`;
const checkAuthUrl = () => `${SERVER}/check-auth`;

// user info
const currentUserIdUrl = () => `${SERVER}/current-user`;
const usersUrl = () => `${SERVER}/users`;
const userUrl = (userId) => `${usersUrl()}/${userId}`;
const profileUrl = (userId) => `${userUrl(userId)}/profile`;

// posts
const feedPostsUrl = (userId) => `${userUrl(userId)}/feed`;
const postsUrl = (userId) => `${userUrl(userId)}/posts`;
const postUrl = (userId, postId) => `${postsUrl(userId)}/${postId}`;

const commentsUrl = (userId, postId) => `${postUrl(userId, postId)}/comments`;

const likeUrl = (userId, postId) => `${postUrl(userId, postId)}/like`;

export {
  checkAuthUrl,
  commentsUrl,
  currentUserIdUrl,
  feedPostsUrl,
  likeUrl,
  loginUrl,
  postsUrl,
  postUrl,
  profileUrl,
  usersUrl,
  userUrl,
};
