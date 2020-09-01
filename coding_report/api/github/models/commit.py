from typing import Optional

from pydantic import BaseModel


class BaseUser(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: Optional[str]
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool


class CommitAuthor(BaseModel):
    name: str
    email: str
    date: str


class Committer(BaseModel):
    name: str
    email: str
    date: str


class Tree(BaseModel):
    url: str
    sha: str


class Verification(BaseModel):
    verified: bool
    reason: str


class CommitDetail(BaseModel):
    url: str
    author: CommitAuthor
    committer: Committer
    message: str
    tree: Tree
    comment_count: int
    verification: Verification


class CommitAuthorDetail(BaseUser):
    pass


class CommitterDetail(BaseUser):
    pass


class Commit(BaseModel):
    url: str
    sha: str
    node_id: str
    html_url: str
    comments_url: str
    commit: CommitDetail
    author: CommitAuthorDetail
    committer: CommitterDetail
