from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel


class GuidModel(BaseModel):
    rendered: str


class TitleModel(BaseModel):
    rendered: str


class MetaModel(BaseModel):
    footnotes: str


class ContentModel(BaseModel):
    rendered: str
    protected: bool


class PostModel(BaseModel):
    id: int
    date: datetime
    date_gmt: datetime
    guid: GuidModel
    modified: datetime
    modified_gmt: datetime
    slug: str
    status: str
    type: str
    link: str
    title: TitleModel
    content: ContentModel
    author: int
    featured_media: int
    comment_status: str
    ping_status: str
    sticky: bool
    template: str
    format: str
    meta: MetaModel
    categories: List[int]
    tags: List[str]
    class_list: List[str]
    _links: Dict[str, List[Dict]]


class DeletePostModel(BaseModel):
    deleted: bool
    previous: PostModel


class CommentModel(BaseModel):
    id: int
    post: int
    parent: int
    author: int
    author_name: str
    author_url: str
    date: datetime
    date_gmt: datetime
    content: Dict[str, str]
    link: str
    status: str
    type: str
    author_avatar_urls: Dict
    meta: List
    _links: Dict[str, List[Dict]]


class DeleteCommentModel(BaseModel):
    deleted: bool
    previous: CommentModel


class UserGetModel(BaseModel):
    id: int
    name: str
    url: str
    description: str
    link: str
    slug: str
    avatar_urls: Dict[str, str]
    meta: List
    _links: Dict[str, List[Dict]]


class UserPostModel(BaseModel):
    id: int
    username: str
    name: str
    first_name: str
    last_name: str
    email: str
    url: str
    description: str
    link: str
    locale: str
    nickname: str
    slug: str
    roles: List[str]
    registered_date: datetime
    capabilities: Dict[str, bool]
    extra_capabilities: Dict[str, bool]
    avatar_urls: Dict[str, str]
    meta: Dict[str, List]
    _links: Dict[str, List[Dict]]


class DeleteUserModel(BaseModel):
    deleted: bool
    previous: UserPostModel
