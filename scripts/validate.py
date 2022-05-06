import sys
import os
from github import Github


def check_is_verified(token, repository, ref):
    client = Github(login_or_token=token)
    repo = client.get_repo(repository)
    latest_commit = repo.get_commit(ref)
    return latest_commit.commit.raw_data["verification"]["verified"]


def validate(
    token,
    github_repository,
    working_repository,
    pr_branch_name,
    github_event_name,
    committer_email,
):
    is_verified = check_is_verified(token, working_repository, pr_branch_name)
    is_fork = not github_repository == working_repository
    is_deployer = committer_email in deployers
    is_pull_request_event = github_event_name == "pull_request"
    is_pull_request_target_event = github_event_name == "pull_request_target"

    valid_workflow = is_verified and (
        (is_fork and is_deployer and is_pull_request_target_event)
        or (not is_fork and is_pull_request_event)
    )
    return valid_workflow


if __name__ == "__main__":
    deployer_path = os.environ["GITHUB_WORKSPACE"] + "/DEPLOYERS.md"
    with open(deployer_path) as file:
        deployers = [i.strip() for i in file]

    token = os.environ["GITHUB_TOKEN"]
    github_repository = os.environ["GITHUB_REPOSITORY"]
    working_repository = os.environ["PR_REPO_FULL_NAME"]
    pr_branch_name = os.environ["GITHUB_HEAD_REF"]
    github_event_name = os.environ["GITHUB_EVENT_NAME"]
    committer_email = os.environ["EMAIL"]

    valid_workflow = validate(
        token,
        github_repository,
        working_repository,
        pr_branch_name,
        github_event_name,
        committer_email,
    )

    print(valid_workflow)
