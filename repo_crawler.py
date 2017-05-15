import base64
from github import Github


class RepoCrawler(object):

    def __init__(self, github_token):
        self.github_client = Github(github_token)

    def get_user(self):
        """Returns user object"""
        return self.github_client.get_user()

    def get_repository(self, repository):
        """Returns repo object of repository"""
        repos = self.github_client.get_user().get_repos()
        return next((repo for repo in repos if repo.name == repository), None)

    def get_repositories(self, organization):
        """Returns list of repository objects belonging to an organization"""
        return self.github_client.get_organization(organization).get_repos()

    def get_branches(self, repository):
        """Returns list of branch objects belonging to a repository"""
        repo = self.github_client.get_repo(repository)
        branches = [branch for branch in repo.get_branches()]
        return {'repo': repo, 'branches': branches}

    def get_repos_with_branches(self, organization):
        """Returns all repositories  with their branches in an organization"""
        repos = self.get_repositories(organization)
        return [self.get_branches(repo.full_name) for repo in repos]

    def get_repository_contents(self, repository):
        """Return array of content objects in a repository"""
        return self.get_repository(repository).get_contents('.')

    def get_files(self, repository):
        """Return array of files in a repository root"""
        return [content for content in self.get_repository_contents(
            repository) if content.type == 'file']

    def get_file_content(self, repository, file):
        """Return decoded file content for a file in a repository"""
        file = self.get_repository(repository).get_file_contents(file)
        return base64.b64decode(file.content).decode('utf-8')
