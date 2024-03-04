import os
import json
import argparse
import requests
from loguru import logger
import time

def create_release_task(GITHUB_REPO: str, OWNER: str, TAG_NAME: str, TARGET_COMMITISH: str, NAME_RELEASE: str, BODY: str, DRAFT: str, PRERELEASE: str, GENERATE_NOTES: str ):
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f"Bearer {os.getenv('GITHUB_ACCESS_TOKEN')}",
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        "owner": OWNER,
        "name": GITHUB_REPO,
        "include_all_branches": False,
        "private": True

    }

data = {"tag_name":TAG_NAME,"target_commitish":TARGET_COMMITISH,"name":NAME_RELEASE,"body":BODY,"draft":DRAFT,"prerelease":PRERELEASE,"generate_release_notes":GENERATE_NOTES}'

response = requests.post('https://api.github.com/repos/OWNER/REPO/releases', headers=headers, data=data)
    try:
        response = requests.post(f"https://api.github.com/repos/{OWNER}/{GITHUB_REPO}/releases", headers=headers, data=json.dumps(data))
        response.raise_for_status()

        if response.status_code == 201:
            logger.info(f"{GITHUB_REPO} was created using {OWNER}")
        else:
            # error_message = f"Error in creating {GITHUB_REPO} using {TEMPLATE_REPO}. Response: {response.text}"
            logger.info(error_message)
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}") 

# def enable_branch_protection(GITHUB_REPO: str, OWNER: str):
#     headers = {
#         "Authorization": f"Bearer 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",
#         "Accept": "application/vnd.github.v3+json"
#     }

#     try:
#         response = requests.post(
#             f"https://api.github.com/repos/{OWNER}/{GITHUB_REPO}/branches/main/protection",
#             headers=headers,
#             json={
#                 "required_status_checks": None,
#                 "enforce_admins": True,
#                 "required_pull_request_reviews": {
#                     "dismiss_stale_reviews": True,
#                     "require_code_owner_reviews": True
#                 },
#                 "restrictions": None
#             }
#         )

#         response.raise_for_status()

#         if response.status_code == 200:
#             logger.info("Branch protection enabled for the main branch")
#         else:
#             logger.error(f"Failed to enable branch protection. Status code: {response.status_code}, Response: {response.json()}")

#     except requests.exceptions.RequestException as e:
#         logger.error(f"Failed to enable branch protection: {e}")      

def main():
    parser = argparse.ArgumentParser(description='GitHub Secrets Management Script')


    parser.add_argument('--repo-owner', help='GitHub repository owner', default="Shubhranshu-Pattanaik-Maersk")
    # parser.add_argument('--template-owner', help='Template repository owner', default="Maersk-Global")
    # parser.add_argument('--template-repo', help='GitHub template repository name', required=True)
    parser.add_argument('--repo-list', help='List of repositories separated by commas', required=True)
    parser.add_argument('--tn', help='tn', required=True)
    parser.add_argument('--tcs', help='List of repositories separated by commas', required=True)
    parser.add_argument('--nr', help='List of repositories separated by commas', required=True)
    parser.add_argument('--b', help='List of repositories separated by commas', required=True)
    parser.add_argument('--d', help='List of repositories separated by commas', required=True)
    parser.add_argument('--pr', help='List of repositories separated by commas', required=True)
    parser.add_argument('--gn', help='List of repositories separated by commas', required=True)

    args = parser.parse_args()    
    GITHUB_REPO_OWNER = args.repo_owner
    # GITHUB_TEMPLATE_OWNER = args.template_owner
    # GITHUB_TEMPLATE_REPO = args.template_repo
    REPO_LIST = args.repo_list.split(',')
    TAG_NAME = args.tn
    TARGET_COMMITISH = args.tcs
    NAME_RELEASE = args.nr
    BODY = args.b
    DRAFT = args.d
    PRERELEASE = args.pr
    GENERATE_NOTES = args.gn
                  

    for GITHUB_REPO in REPO_LIST:
        try:
            logger.info(f'Checking for repo {GITHUB_REPO}')            
            create_release_task(REPO_LIST,GITHUB_REPO_OWNER,TAG_NAME,TARGET_COMMITISH,NAME_RELEASE,BODY,DRAFT,PRERELEASE,GENERATE_NOTES)
            time.sleep(10)
            # enable_branch_protection(GITHUB_REPO, GITHUB_REPO_OWNER)
        except Exception as e:
            logger.error(f'Error checking repo {GITHUB_REPO}: {str(e)}')            

if __name__ == '__main__':
    main()
