import os
import random
import time
import subprocess
from datetime import datetime
import sys

def run_command(command, cwd=None, env=None):
    process = subprocess.Popen(command, shell=True, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode('utf-8').strip(), stderr.decode('utf-8').strip()

def main():
    print("========================================")
    print("   Multi-Repo Invisible Committer       ")
    print("========================================")
    print("This script runs indefinitely, making EMPTY commits")
    print("(which change NO files and break NO code) across")
    print("your specified repositories to boost activity.\n")

    repos_file = "repos.txt"
    # Create the config file if it doesn't exist
    if not os.path.exists(repos_file):
        with open(repos_file, "w") as f:
            f.write("# Add the FULL paths to your 10-12 repositories below, one per line.\n")
            f.write("# Example: C:\\Users\\Raghav\\Desktop\\raga\\ml face classifier\n")
            f.write("# Example: C:\\Users\\Raghav\\Documents\\my_project\n")
        print(f"Created '{repos_file}'!")
        print(f"Please open '{repos_file}', add the paths to your 10-12 repositories,")
        print("and then restart this script.")
        return

    # Read repos
    with open(repos_file, "r") as f:
        repos = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]
    
    if not repos:
        print(f"WARNING: '{repos_file}' is empty. Please add some repository paths to it!")
        return

    print(f"Loaded {len(repos)} repositories from {repos_file}:")
    valid_repos = []
    for r in repos:
        if not os.path.isdir(r):
            print(f"  [!] Invalid path (Skipping): {r}")
        elif not os.path.exists(os.path.join(r, ".git")):
            print(f"  [!] Not a Git repository (Skipping): {r}")
        else:
            print(f"  [*] Ready: {r}")
            valid_repos.append(r)

    if not valid_repos:
        print("\nError: No valid Git repositories found. Exiting.")
        sys.exit(1)

    print("\nStarting auto-commit loop. Press Ctrl+C to stop.")

    commit_messages = [
        "Routine repository maintenance",
        "Trigger CI build",
        "Invisible heartbeat commit",
        "Sync repository state",
        "Keep-alive update"
    ]

    try:
        while True:
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            
            # Randomly pick ONE repository from your list to commit to.
            # This makes the activity look very organic (different repo every 15-20 mins)
            target_repo = random.choice(valid_repos)
            repo_name = os.path.basename(os.path.normpath(target_repo))
            
            message = random.choice(commit_messages)
            
            # Make an EMPTY commit. This modifies ZERO files in the repo!
            commit_cmd = f'git commit --allow-empty -m "{message} - {formatted_date}"'
            ret_code, out, err = run_command(commit_cmd, cwd=target_repo)
            
            if ret_code == 0:
                print(f"\n[{formatted_date}] Created invisible commit in '{repo_name}'")
                
                print(f"--> Syncing '{repo_name}' with GitHub...")
                # Pull just in case you did work manually
                run_command("git pull --no-edit", cwd=target_repo)
                
                print(f"--> Pushing '{repo_name}' to GitHub...")
                push_ret, push_out, push_err = run_command("git push", cwd=target_repo)
                if push_ret == 0:
                    print("--> Successfully pushed!")
                else:
                    print(f"--> Failed to push: {push_err}")
            else:
                print(f"\n[{formatted_date}] Failed to commit in '{repo_name}': {err}")

            # Wait for 15-20 minutes
            wait_time_minutes = random.randint(15, 20)
            wait_time_seconds = wait_time_minutes * 60
            
            print(f"\nWaiting for {wait_time_minutes} minutes before the next commit...")
            time.sleep(wait_time_seconds)

    except KeyboardInterrupt:
        print("\nAuto-commit loop stopped by user. Exiting gracefully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
