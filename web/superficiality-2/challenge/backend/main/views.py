import json
import jwt
from http import HTTPStatus

from django.db import models
from django.conf import settings
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.http import require_http_methods

from main import forms as main_forms
from main.models import User, Post, Comment, Like


def check_jwt_authentication(view):

    def inner(request, *args, **kwargs):
        """

        """
        user = None

        if 'Authorization' in request.headers:
            AUTHORIZATION_VALUE = request.headers['Authorization']

            if 'Bearer' in AUTHORIZATION_VALUE:
                parts = AUTHORIZATION_VALUE.split(' ')

                if len(parts) == 2:
                    jwt_token = parts[1]
                    jwt_token.strip()

                    try:
                        target_user = User.objects.get(current_jwt_token=jwt_token)
                        payload = jwt.decode(jwt_token, str(target_user.auth_key), 'HS256')

                        if payload.get('userid') == target_user.id:
                            user = target_user

                    except User.DoesNotExist:
                        pass
                    except jwt.InvalidSignatureError:
                        pass
                    except jwt.InvalidTokenError:
                        pass

        if user is None:
            return JsonResponse({}, status=HTTPStatus.UNAUTHORIZED)
        else:
            request.user = user

        return view(request, *args, **kwargs)

    return inner


def check_userid_matches_request_user(maybe_view=None, *, exempt=[]):

    def decorator(view):
        """
        Part two of the vulnerability
        where the userid from the request is checked against
        the userid from the URL.

        Practically a modified JWT with the same user ID as in the URL
        will pass forever.
        """

        def inner(request, *args, **kwargs):
            # vulnerability part 2 right here
            # user id from URL is compared against the JWT base64 payload,
            # and no attempt to properly check the JWT is made

            assert 'userid' in kwargs

            if str(kwargs['userid']) == str(request.user.id) or (request.method in exempt):
                return view(request, *args, **kwargs)

            return JsonResponse({}, status=HTTPStatus.FORBIDDEN)

        return inner

    if maybe_view is None:
        return decorator

    return decorator(maybe_view)


def serialize_user_simple(user):
    return {
        'userid': user.pk,
        'full_name': user.full_name,
        'isjeff': user.username == "kowalski",
        'isprivate': user.is_private,
    }


def serialize_profile(user, profile):
    return {
        'location': profile.location,
        'birthday': profile.birth_date.isoformat() if profile.birth_date is not None else None,
        'full_name': user.full_name,
        'friends': [serialize_user_simple(friend) for friend in user.friends.all()]
    }


def serialize_post(post):
    return {
        'postid': post.id,
        'userid': post.user.pk,
        'message': post.message,
        'comments': [
            {
                'commentid': comment.pk,
                'userid': comment.user_id,
                'message': comment.message
            }
            for comment in post.comments.all()
        ],
        'ispublished': post.is_published,
        'uuid': post.uuid,
    }


def serialize_posts(posts):
    return [serialize_post(post) for post in posts]


@require_http_methods(['POST'])
def login(request):

    form = main_forms.LoginForm(json.loads(request.body))

    BAD_REQUEST = JsonResponse(
        {},
        status=HTTPStatus.BAD_REQUEST
    )

    if not form.is_valid():
        return BAD_REQUEST

    user = User.objects.filter(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password'],
    ).first()

    if user is None:
        return BAD_REQUEST

    return JsonResponse({
        'user_id': user.pk,
        'token': user.current_jwt_token,
    })


@require_http_methods(['OPTIONS', 'GET'])
@check_jwt_authentication
@check_userid_matches_request_user
def check_auth(request):
    """Doesn't do much, just used to check if the JWT still works"""
    return JsonResponse({})


@require_http_methods(['OPTIONS', 'GET'])
@check_jwt_authentication
def current_user(request):
    result = serialize_user_simple(request.user)
    return JsonResponse(result)


@require_http_methods(['OPTIONS', 'GET'])
@check_jwt_authentication
@check_userid_matches_request_user(exempt=['GET'])
def user(request, userid):
    try:
        user = User.objects.get(id=userid)
    except User.DoesNotExist:
        return JsonResponse({}, status=HTTPStatus.NOT_FOUND)
    return JsonResponse(serialize_user_simple(user))


@require_http_methods(['OPTIONS', 'GET', 'POST', 'PUT'])
@check_jwt_authentication
def profile(request, userid):
    user = User.objects.get(id=userid)

    try:
        profile = user.profile
    except User.profile.RelatedObjectDoesNotExist:
        return HttpResponseServerError()

    form = None
    if request.method in ['POST', 'PUT']:
        form = main_forms.ProfileForm(json.loads(request.body), instance=profile)
        form.user = user
        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

    if request.method == 'POST':
        if profile is not None:
            return JsonResponse(
                {'error': 'profile already exists'},
                status=HTTPStatus.BAD_REQUEST
            )
        else:
            profile = form.save()

    elif request.method == 'PUT':
        if profile is None:
            return JsonResponse(
                {'error': 'no profile available for update'},
                status=HTTPStatus.BAD_REQUEST
            )
        else:
            profile = form.save()

    return JsonResponse(serialize_profile(user, profile))


@require_http_methods(['OPTIONS', 'GET'])
@check_jwt_authentication
@check_userid_matches_request_user
def feed(request, userid):
    user = User.objects.get(id=userid)
    feed_users = User.objects.filter(
        models.Q(id=userid) | models.Q(id__in=user.friends.all().values_list('id', flat=True))
    )
    feed_posts = Post.objects.filter(user__in=feed_users, is_published=True).order_by('created_at')
    feed_posts = feed_posts.select_related('user').prefetch_related('comments')
    comments = Comment.objects.filter(post__in=feed_posts)

    involved_users = User.objects.filter(
        id__in=set(
            list(feed_posts.values_list('user_id', flat=True))
            + list(comments.values_list('user_id', flat=True))
        )
    )

    return JsonResponse({
        'users': [serialize_user_simple(user) for user in involved_users],
        'posts': serialize_posts(feed_posts),
    })


@require_http_methods(['OPTIONS', 'GET', 'POST'])
@check_jwt_authentication
def posts(request, userid):
    try:
        user = User.objects.get(id=userid)
    except User.DoesNotExist:
        raise JsonResponse({}, status=HTTPStatus.NOT_FOUND)

    if request.method == 'POST':
        form = main_forms.PostForm(json.loads(request.body))
        form.user = user

        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

        new_post = Post.objects.create(user=user, message=form.cleaned_data['message'])

        # !!!!
        # DELIBERATELY CHECKING THE USER ID TOO LATE - THIS IS PART 1 OF VULNERABILITY
        # PART 2 IS RETRIEVING THE POSTS FOR UUID WITHOUT
        # PART 3 IS PUBLISHING WITHOUT CHECKING THE USER

        if userid != request.user.id:
            return JsonResponse(
                # !!!!
                # taunt the hacker with some validation that the post was indeed created
                {'reason': "You don't have rights to see a new unpublished post"},
                status=HTTPStatus.UNAUTHORIZED
            )

        return JsonResponse(serialize_post(new_post))

    user_posts = Post.objects.filter(user=user)

    # !!!!!!!!!!!!
    # THIS IS WHERE THE HACKER WON'T BE ABLE TO GET VULNERABLE DATA
    # SO THE HACKER MUST LOOK SOMEWHERE ELSE LIKE /post
    # show only published posts to outside world
    if user != request.user:
        user_posts = user_posts.filter(is_published=True)

    comments = Comment.objects.filter(post__in=user_posts)

    involved_users = User.objects.filter(id__in=set(comments.values_list('user_id', flat=True)))

    return JsonResponse({
        'users': [serialize_user_simple(user) for user in involved_users],
        'posts': serialize_posts(user_posts),
    })


def handle_new_post_for_challenge(new_post, result):
    # kowalski must post as someone else
    if new_post.user.username == "kowalski":
        return

    # you have to post a specific message to win
    if new_post.message != "I_SEE_EVERYTHING":
        return

    # the targeted user must be private
    if not new_post.user.is_private:
        return

    flag = settings.WINNER_FLAG
    result['winner_flag'] = flag


@require_http_methods(["OPTIONS", "POST"])
@check_jwt_authentication
def publish_post(request, post_uuid):
    """
    !!!!!!!!!!!!
    NOTICE THIS DOES NOT CHECK THE USER
    the vulnerability consists in the fact that
    we wrote code, and naively assuming that we won't get here because the user does not have the UUID for this

    !!!!!!!!!!!!
    """
    try:
        post = Post.objects.filter(is_published=False).get(uuid=post_uuid)
        post.is_published = True
        post.save()
    except ValueError:
        return JsonResponse({}, status=HTTPStatus.BAD_REQUEST)
    except Post.DoesNotExist:
        return JsonResponse(
            {'reason': "Post does not exist or was already published"},
            status=HTTPStatus.BAD_REQUEST
        )

    result = {}
    handle_new_post_for_challenge(post, result)

    return JsonResponse(result, status=HTTPStatus.ACCEPTED)


# !!!!!!!!!!!!
# DELIBERATLY NOT CHECKING FOR USER ID
@require_http_methods(['OPTIONS', 'GET', 'DELETE'])
@check_jwt_authentication
def post(request, userid, postid):
    post = None

    # !!!!!!!!!!!!
    # DELIBERATELY NOT FILTERING BY is_published
    # can happen in real situations leaving endpoint not protected enough
    try:
        post = Post.objects.get(id=postid)
    except Post.DoesNotExist:
        return JsonResponse(
            {'errors': [f"post with id {postid} does not exist"]},
            status=HTTPStatus.NOT_FOUND
        )

    if request.method == 'DELETE':
        post.delete()
        return JsonResponse({}, status=HTTPStatus.ACCEPTED)

    return JsonResponse(serialize_post(post))


@require_http_methods(['OPTIONS', 'POST'])
@check_jwt_authentication
@check_userid_matches_request_user
def comments(request, userid, postid):
    """
    Only for creating comments
    """
    user = User.objects.get(id=userid)

    try:
        Post.objects.get(id=postid)
    except Post.DoesNotExist:
        return JsonResponse(
            {'errors': [f"post with id {postid} does not exist"]},
            status=HTTPStatus.NOT_FOUND
        )

    form = main_forms.CommentForm(json.loads(request.body))
    form.user = user

    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

    comment = form.save()

    return JsonResponse({'commentid': comment.id, 'message': comment.message})


@require_http_methods(['OPTIONS', 'POST', 'DELETE'])
@check_jwt_authentication
@check_userid_matches_request_user
def like(request, userid, postid):
    try:
        user = User.objects.get(id=userid)
    except User.DoesNotExist:
        return JsonResponse({}, status=HTTPStatus.NOT_FOUND)

    try:
        post = Post.objects.get(id=postid)
    except Post.DoesNotExist:
        return JsonResponse(
            {'errors': [f"post with id {postid} does not exist"]},
            status=HTTPStatus.NOT_FOUND
        )

    if request.method == "POST":
        Like.objects.create(user=user, post=post)
        return JsonResponse({}, status=HTTPStatus.CREATED)

    elif request.method == "DELETE":
        try:
            like = Like.objects.filter(post_id=postid, user_id=userid)
            like.delete()
        except Like.DoesNotExist:
            return JsonResponse({}, status=HTTPStatus.BAD_REQUEST)

    return JsonResponse({}, status=HTTPStatus.METHOD_NOT_ALLOWED)
