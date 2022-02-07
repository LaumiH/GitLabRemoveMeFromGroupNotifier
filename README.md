# GitLabRemoveMeFromGroupNotifier
This project is a prank I wrote for work. I asked to get removed from a GitLab group multiple times, and after a year I wanted to emphasize my wish in a non-destructive way.

The prank has *non-destructive effects* on the projects in the GitLab group and sub-groups. It only creates a branch and a merge request. If your name was LaumiH and the group's name was Unwanted, the following would happen:
- Create a branch named "LaumiH_was_here" from main or master (if there is no such branch, the script does nothing in this project)
- Add a Markdown file "LaumiH_was_here.md" with the contents you specify (ideally a plea for removal from the group)
- Create a merge request with the title "LaumiH was here! Please remove me from the Unwanted group!"

# Usage - for the affected
First, let me describe how you can delete the created branches and merge requests in an automated way. 
Please follow the steps described in [Getting Started](#get_started) below, so install the stuff and make sure you have the `host` and `access_token` files along the downloaded `de-prank.py` file. You can create a GitLab access token as described [here](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html).
Then simply execute `python3 de-prank.py -group <group> -name <name>`. Replace `<group>` with the name of the top-level GitLab group the user wants to be removed from. Replace `<name>` with the user's name that they added in the "... was here" messages. That's it.

*Remember to remove the user from the group after all :)*

You can of course also contact the prankster and ask for their help.

# Usage
If you are in a similar situation like me, you might consider playing this simple and *non-desctructive prank* on the group's admins that would not listen to you. 

## <a name="get_started"></a> Getting started
Execute the following steps to get started:
- Install `Python3` and the modules `argparse` and `python-gitlab`
- Download prank.py, de-prank.py and I_was_here.md to a directory, say `dir`
- Create two files in `dir`:
  - host: place the GitLab url here, e.g. gitlab.company.com, without ""
  - access_token: your GitLab access token, without ""
- Take a look at I_was_here.md. `<group>` and `<name>` will be replaced by what you enter to the command line later (see below). Please leave in the hint to this repository, so that people can at least delete the outcomes of your prank. Other than that, feel free to add your own message.

## Testing
To be sure that the scripts behave correctly, you might want to test the prank on your private projects. You can do this via `python3 prank.py -user <user> -name <name>`, where your replace `<user>` with your gitlab username and `<name>` with the name you want to see in the "... was here" message.
This will prank only your own projects.

Please also try out the automated deletion of the created branches and merge requests with `python3 de-prank.py -user <user> -name <name>`.

## Showtime
When you are absolutely sure that you don't destroy anything for good, it's time for the real prank. Simply type `python3 prank.py -group <group> -name <name>`, replacing `<group>` with the name of the GitLab group you want to be removed from, and `<name>` with the name you want to see in the "... was here" message. Have fun :)
