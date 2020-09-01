from pydantic import BaseModel

from coding_report.api.github.models.base import BaseUser


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
