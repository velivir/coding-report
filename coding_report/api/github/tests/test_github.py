from coding_report.api.github.github import fetch_commits, fetch_repo_info
from coding_report.api.github.models.commit import Commit
from coding_report.api.github.models.repository import Repository


def test_fetch_repo_info(settings):
    github_login, github_token = settings
    repo = Repository(
        **fetch_repo_info(
            github_login=github_login,
            github_api_token=github_token,
            owner='octocat',
            repo_name='Hello-World',
        )
    )
    assert repo.name == 'Hello-World'
    assert repo.full_name == 'octocat/Hello-World'
    assert repo.created_at == '2011-01-26T19:01:12Z'


def test_fetch_commits(settings):
    github_login, github_token = settings
    commit = Commit(
        **fetch_commits(
            github_login=github_login,
            github_api_token=github_token,
            owner='octocat',
            repo_name='Hello-World',
        )[0]
    )
    assert commit.author.login == 'octocat'
