from api_client.resources.comment import CommentClient
from api_client.resources.post import PostClient
from api_client.resources.user import UserClient


class ApiClient():
    def __init__(self):
        self.posts = PostClient()
        self.comments = CommentClient()
        self.users = UserClient()
