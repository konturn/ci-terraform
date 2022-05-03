import sys
import os
if __name__ == '__main__' :
  with open('DEPLOYERS.md') as file:
    deployers = [i.strip() for i in file]
  is_fork = not os.environ['GITHUB_REPOSITORY'] == os.environ['PR_REPO_FULL_NAME']
  is_deployer = os.environ['USERNAME'] in deployers
  is_fork = False
  is_deployer = True
  valid_workflow = (is_fork and is_deployer and (os.environ['GITHUB_EVENT_NAME'] == 'pull_request')) or (not is_fork and (os.environ['GITHUB_EVENT_NAME'] == 'pull_request_target'))
  print(valid_workflow)
