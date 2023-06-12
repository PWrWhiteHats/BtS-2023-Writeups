import random
import uuid
import logging
from collections import defaultdict
from django.core.management.base import BaseCommand

import jwt
from faker import Faker

from main.models import User, Post, Comment, Profile, Like

logger = logging.getLogger(__name__)
faker = Faker()


def make_posts(user):
    for i in range(random.randint(3, 10)):
        Post.objects.create(user=user, message=faker.paragraph(nb_sentences=random.randint(1, 5)))


class Command(BaseCommand):
    help = "Make me some data"

    def handle(self, *args, **options):
        logger.info("Generate some data for the social media platform")
        other_users = []

        NO_OF_USERS = 50

        logger.info(f"Making {NO_OF_USERS} users ...")
        # make random users
        for _ in range(NO_OF_USERS):
            new_user = User.objects.create(
                username=faker.pystr(),
                password=str(uuid.uuid4()),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
            )
            other_users.append(new_user)

            new_user.profile.location = faker.city()
            new_user.profile.birth_date = faker.date_object()
            new_user.profile.save()

            logger.info(f"Made user {new_user.full_name}")

        logger.info("Making JEFF ...")
        # make jeff
        jeff = User.objects.create(
            username="kowalski",
            password="12345",
            first_name="Jeff",
            last_name="Kowalski",

        )

        jeff.auth_key = uuid.uuid4()

        jeff_payload = {'userid': jeff.id}
        new_jwt_token = jwt.encode(jeff_payload, str(jeff.auth_key), 'HS256')
        signature = new_jwt_token.split('.')[2]
        jeff.current_jwt_signature = signature
        jeff.current_jwt_token = new_jwt_token

        jeff.save()

        jeff.profile.location = faker.city()
        jeff.profile.birth_date = faker.date_object()
        jeff.profile.save()

        logger.info("Made JEFF")

        # make friends
        logger.info("Making friends ...")
        for _ in range(NO_OF_USERS // 2):
            new_friend = random.sample(other_users, 1)[0]
            if jeff == new_friend:
                continue
            jeff.friends.add(new_friend)

        for target_user in other_users:
            logger.info(f"Making friends for {target_user.full_name}")
            for _ in range(NO_OF_USERS // 3):
                new_friend = random.sample(other_users, 1)[0]
                if new_friend == target_user:
                    continue
                target_user.friends.add(new_friend)

        all_users = other_users + [jeff]

        # make posts
        logger.info("Making posts ...")
        posts_by_user_id = defaultdict(list)

        for _ in range(3):
            post = Post.objects.create(user=jeff, message=faker.paragraph(nb_sentences=random.randint(1, 5)))
            logger.info(f"Post [{jeff.full_name}] : {post.message}")

        for _ in range(100):
            target_user = random.sample(all_users, 1)[0]
            post = Post.objects.create(user=target_user, message=faker.paragraph(nb_sentences=random.randint(1, 5)))
            posts_by_user_id[target_user.pk].append(post)  # make sure to keep a note of the post
            logger.info(f"Post [{target_user.full_name}] : {post.message}")

        # make comments
        logger.info("Making comments ...")
        for _ in range(100):
            users_pair = random.sample(all_users, 2)
            user_1 = users_pair[0]
            user_2 = users_pair[1]

            logger.info(f"Selected commenting pair {user_2.full_name} -> {user_1.full_name}")

            # retrieve all user's posts
            user_1_posts = posts_by_user_id[user_1.pk]

            # select a variable number of the user's posts
            posts_selection = random.sample(
                user_1_posts,
                random.randint(0, len(user_1_posts))
            )

            for post in posts_selection:
                new_comment = Comment.objects.create(
                    user=user_2,
                    post=post,
                    message=faker.paragraph(nb_sentences=random.randint(1, 2))
                )
                logger.info(f"Comment [on {post.id}] {new_comment.message}")
