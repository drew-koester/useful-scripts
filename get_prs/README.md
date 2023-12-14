# Get PRs

This is a simple python script to get PRs that ready to be reviewed. 

## Usage

1. To use the script you need a git token.  If you have that you can skip ahead otherwise you can follow the instructions [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).
2. Update the script with your token (generated in the previous step).
3. Verify that the list of repos is valid for your use case.
4. Run the command
```bash
python get_prs.py
```

## Output
![alt text](/get_prs/img/script_output.png)


## Troubleshooting
Q: There is a PR open and it does't list it?
A: The script excludes the following: Draft Status, Title with "NEMO", "ORCA", "SEAL, "CI", and the label of WIP.
