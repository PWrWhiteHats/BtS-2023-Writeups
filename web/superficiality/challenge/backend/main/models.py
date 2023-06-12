from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    auth_key = models.UUIDField(null=True)
    current_jwt_signature = models.CharField(max_length=250, null=True)
    current_jwt_token = models.CharField(max_length=250, null=True)

    friends = models.ManyToManyField(
        'self',
        through='Friendship',
        through_fields=('user_1', 'user_2',)
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            self.profile
        except User.profile.RelatedObjectDoesNotExist:
            self.profile = Profile.objects.create(user=self)


class Friendship(models.Model):
    user_1 = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='friendships_1')
    user_2 = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='friendships_2')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="check_not_friend_with_self",
                check=~models.Q(user_1=models.F('user_2'))
            )
        ]


class Profile(models.Model):
    user = models.OneToOneField(to=User, related_name='profile', on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='posts')
    message = models.CharField(max_length=250)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='likes')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    message = models.CharField(max_length=250)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
