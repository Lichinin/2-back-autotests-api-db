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
