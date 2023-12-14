import requests
from requests.auth import HTTPBasicAuth
from jenkinsapi.jenkins import Jenkins
import datetime
from termcolor import colored

# this could come from https://github.com/rafastealth/terraform-meta/blob/main/services/service_map.json instead
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
# repos = ["kb-service"]
repos.sort()

def get_jenkins_build_status(auth, jenkins_url, job_name):
    # url = f"{jenkins_url}/job/{job_name}/api/json"
    # lastBuild, lastStableBuild, lastSuccessfulBuild, lastFailedBuild, lastUnstableBuild, lastUnsuccessfulBuild, lastCompletedBuild
    url = f"{jenkins_url}/job/{job_name}/lastCompletedBuild/api/json"

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()
        print (data.get('url'))
        if data.get('result') == "SUCCESS":
            color = 'white'
        else:
            color = 'red'
        print(colored("   Status: " + str(data.get('result')), color))
        print ("   Last Run: " + str(convert_epoc_to_date(data.get('timestamp'))) + " (" + str(day_ago_from_epoc(data.get('timestamp'))) + " days ago)" )

        # Optional to see if certain stages were successful
        # get_jenkins_stages (jenkins_url, job_name, auth, data.get("id"))
    else:
        print(f"Error: Unable to fetch build status. Status code: {response.status_code}")

def get_jenkins_stages(jenkins_url, job_name, auth, id):
    url = f"{jenkins_url}/job/{job_name}/wfapi/runs"
    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()

        for i in data:
            successful_inception = True
            if(i.get('id') == id):
                if i.get('status') == "SUCCESS":
                    color = 'white'
                else:
                    color = 'red'

                # Optional to see if certain stages were successful
                for j in i.get('stages'):
                    if look_for_specific_stage(j, "inception" ) == False:
                        successful_inception = False
                print("   Successful Inception: " + str(successful_inception))

    else:
        print(f"Error: Unable to fetch build status. Status code: {response.status_code}")

# This is helpful if you want to see if a clinic did a thing, like Inception
def look_for_specific_stage(stage, stage_qualifier):
    if stage_qualifier in stage.get('name'):
        if stage.get('status') != "SUCCESS":
            return False
        return True
    
def day_ago_from_epoc(epoc):
    today = datetime.datetime.now();
    future_dt = datetime.datetime.fromtimestamp(epoc/1000)
    difference = today - future_dt;
    return (difference.days)


def convert_epoc_to_date(epoc):
    return datetime.datetime.fromtimestamp(epoc/1000).strftime('%c')

if __name__ == "__main__":
    jenkins = "https://production-jenkins.build.98point6.com/job/rafastealth/job/"
    job_name = ""
    username = "you@email.com"
    # See https://www.baeldung.com/ops/jenkins-api-token
    api_token = "find-your-own"

    auth = HTTPBasicAuth(username, api_token)

    for repo in repos:
        jenkins_url = jenkins + repo
        if repo in ("kb-service", "eligibility-service"):
            job_name = "master"
        else:
            job_name = "main"
        print ("Repo: " + repo)
        get_jenkins_build_status(auth, jenkins_url, job_name)
        print ("---------------------------")
