import os
import re
import yaml
import argparse
from github import Github
from dotenv import load_dotenv

load_dotenv()

def replace_env_vars(match):
    return os.environ.get(match.group(1), match.group(0))


def load_config(config_path):
    with open(config_path, 'r') as config_file:
        content = config_file.read()
        content = re.sub(r'\$\{(.+?)\}', replace_env_vars, content)
        return yaml.safe_load(content)

config = load_config('config.yml')

ACCESS_TOKEN = config['access_token']
OWNER = config['repo']['org']
REPO_NAMES = config['repo']['names']
BRANCH = config['release']['branch']

g = Github(base_url="https://github.com/api/v3", login_or_token=ACCESS_TOKEN)


def create_tagged_release(repo_name, repo_tag):
    repo = g.get_repo(f"{OWNER}/{repo_name}")
    branch = repo.get_branch(BRANCH)

    if repo.get_tags() is not None:
        for tag in repo.get_tags():
            if tag.name == repo_tag:
                print(f"Tag {repo_tag} already exists.")
                return

    release_name = f"Version {repo_tag}"
    commit = repo.get_commit(branch.commit.sha)
    repo.create_git_release(repo_tag, release_name, "Release notes for " + release_name, target_commitish=commit.sha,
                            draft=False, prerelease=False)

    print(f"Created a new tagged release: {repo_tag} - {release_name}")


def parse_args():
    parser = argparse.ArgumentParser(description="Create a new tagged release for a GitHub repository.")
    parser.add_argument("--tag", required=True, help="The tag for the new release (e.g., v1.0.0).")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    for i in REPO_NAMES:
        create_tagged_release(i, args.tag)
