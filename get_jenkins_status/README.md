# Get Jenkins Status

This is a simple python script to get the status of a Jenkins job.  It does so by looping through a list of pre-defined repoes and call the jenkins API to get the status.

## Usage

1. To use this script you must first have a jenkins token.  If you have that you can skip ahead otherwise you can follow the instructions [here](https://www.jenkins.io/blog/2018/07/02/new-api-token-system/).
2. Update the script with your token (generated in the previous step) and your email address.
3. Verify that the list of repos is valid for your use case.
4. Log onto the VPN (as jenkins is only accessible from the VPN)
5. Run the command
```bash
python get_jenkins_status.py
```

## Output
![alt text](/get_jenkins_status/img/script_output.png)


## Troubleshooting
Q: The script displays "Error: Unable to fetch build status. Status code: 404" for a repo that I added?
A: The majority of the repos leverage "main" as their primary branch, but a few use "master".  If you added a repo that uses "master" you will need to update the script to include that branch.

Q: The script is slow to respond and seems to hang?
A: The script is making a call to the jenkins API for each repo.  If you have a large number of repos it can take a while to get the status for each one. 

Q: This is dumb, why not just use the jenkins UI?
A: I agree, but I create this script since the UI is often slow and tedius to look at each repo.  I'm sure there are other use cases for this script, but I don't know what they are.  If you have a use case please let me know and I'll update the README.