from api_client.resources.comment import CommentClient
from api_client.resources.post import PostClient
from api_client.resources.user import UserClient


class ApiClient():
    def __init__(self):
        self._posts = None
        self._comments = None
        self._users = None

    @property
    def posts(self):
        if self._posts is None:
            self._posts = PostClient()
        return self._posts

    @property
    def comments(self):
        if self._comments is None:
            self._comments = CommentClient()
        return self._comments

    @property
    def users(self):
        if self._users is None:
            self._users = UserClient()
        return self._users
