from github import Github


class RepoCrawler(object):

    def __init__(self, github_token):
        self.github_client = Github(github_token)

    def get_repositories(self, organization):
        """Returns list of repository objects belonging to an organization"""
        org = self.github_client.get_organization(organization)
        return [repo for repo in org.get_repos()]

    def get_branches(self, repository):
        """Returns list of branch objects belonging to a repository"""
        repo = self.github_client.get_repo(repository)
        branches = [branch for branch in repo.get_branches()]
        return {'repo': repo, 'branches': branches}

    def get_repos_with_branches(self, organization):
        """Returns all repositories  with their branches in an organization"""
        repos = self.get_repositories(organization)
        return [self.get_branches(repo.full_name) for repo in repos]
