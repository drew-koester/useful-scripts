import requests
from termcolor import colored
from datetime import datetime

global DEBUG
DEBUG = False
global date
date = datetime.utcnow()

repos = ["kb-service", "provider-service", "shift-service", "steadymd-consult-rs-agent", "steadymd-service-client",
        "subscriber-referral-coordination", "chat-suggestion-beta", "content-search", "data-science-connector",
        "ds-service", "dx-search", "model-training", "otc-search-beta",
        "detekt-custom-backend-rules", "flow-flows", "flow-storage", "patient-contact", "agent-recordstore-client",
        "jwt-manager", "surescripts-admin-service","rte-service",
        "record-store", "rs-cognito-sync-agent", "rs-payment-method-agent", "cov-rs-agent", "patient-subscription-service",
        "medication-service", "health-data-outbound-service", "rs-price-agent", "allergy-intolerance-rs-agent", 
        "medical-billing-service", "pubsub", "auth-service", "pharmacy-service", "prescription-service",
        "provider-ums", "eligibility-service", "lab-results-ingestion", "external-sso",
        "insurance-service", "dts-service", "mirth", "account-management-service",
        "steadymd-service-client", "solv-service-client", "solv-appt-service"]
# repos = ["record-store"]
repos.sort()

def get_open_pull_requests(owner, repo, token):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=open"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Repo: {repo}")
        print(f"Error: Unable to fetch pull requests. Status code: {response.status_code}")
        return None

#defining the function for subtracting 
def get_difference(startdate, enddate):
    diff = enddate - startdate
    return diff.days

def display_date(passed_date):
    difference = date - datetime.strptime(passed_date, "%Y-%m-%dT%H:%M:%SZ")
    if(difference.days <= 3):
        color = 'white'
    elif(difference.days <= 7):
        color = 'yellow'
    else: 
        color = 'red'
    print(colored("  Create: " + passed_date +' ('+ f'{difference.days}' + " ago)", color))


def display_pull_requests(pull_requests, repo):
    print(colored(repo, 'white', attrs=['bold']))
    if pull_requests:
        for pr in pull_requests:
            # print(pr)
            ok = True
            if pr['draft'] == True:
                ok = False
            if "NEMO-" in pr['title']:
                ok = False
            if "ORCA-" in pr['title']:
                ok = False
            if "SEAL-" in pr['title']:
                ok = False
            if "CI-" in pr['title']:
                ok = False
            for label in pr['labels']:
                if label['name'] == "WIP":
                    ok = False

            if ok == True:
                print("  Title: " + colored(pr['title'], 'white', attrs=['bold']))
                print(f"  URL: {pr['html_url']}")
                print(f"  Author: {pr['user']['login']}")
                display_date(pr['created_at'])

                print("  ------")
            else:
                if DEBUG:
                    print(f"   SKIP: {pr['title']}")


if __name__ == "__main__":
    owner = "rafastealth"
    token = "create-your-own"

    for repo in repos:
        pull_requests = get_open_pull_requests(owner, repo, token)
        display_pull_requests(pull_requests, repo)
