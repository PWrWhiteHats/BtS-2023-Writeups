class UserData {
  constructor(userid, userFullName, isJeff, isPrivate) {
    this.userid = userid;
    this.userFullName = userFullName;
    this.isJeff = isJeff;
    this.isPrivate = isPrivate;
  }
}

class ProfileData {
  constructor(userFullName, location, birthday, friends) {
    this.userFullName = userFullName;
    this.location = location;
    this.birthday = birthday;
    this.friends = friends || [];
  }
}

class CommentData {
  constructor(
    commentid,
    userid,
    message,
  ) {
    this.commentid = commentid;
    this.userid = userid;
    this.message = message;
  }
}

class PostData {
  constructor(
    postid,
    userid,
    message,
    comments = null,
    isFresh = false,
    isPublished = false,
    uuid = null,
  ) {
    this.postid = postid;
    this.userid = userid;
    this.message = message;
    this.comments = comments || [];
    this.isFresh = isFresh;
    this.isPublished = isPublished;
    this.uuid = uuid;
  }
}

export { CommentData, PostData, ProfileData, UserData };
