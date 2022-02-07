import argparse

from gitlab import Gitlab, GitlabGetError
from gitlab.const import SEARCH_SCOPE_MERGE_REQUESTS

#this is a helper method to read in the access token and config file
def read_file(path: str) -> str:
    f = open(path, 'r', encoding='iso8859-1')
    content = f.read()
    f.close()
    return content

#the access token, read from file
accessToken = read_file('access_token').strip()
#the config, read from file
host = read_file('host').strip()

#gl is the gitlab object that is used to communicate to the GitLab server
#the url is configured in the config file
gl = Gitlab(url=host, private_token=accessToken)

#this specified which arguments can be used to start the program on the command line
parser = argparse.ArgumentParser()
parser.add_argument('-group',
                    help='The top level GitLab group you want to be removed from',
                    nargs='+',
                    default=[],
                    required=False)
parser.add_argument('-user',
                    help='For testing: the user name to test branch and mr creation on',
                    nargs='+',
                    default=[],
                    required=False)
parser.add_argument('-name',
                    help='The name to be added in the I was here message',
                    nargs='+',
                    default=['I'],
                    required=False)  

#parse the arguments from the command line
args = parser.parse_args()

#this is the name you see in the created branches and merge requests
#you can specify it on the command line using -name <name>
name = args.name[0]
#the branch name that contains the name and '_was_here'
branch = name+'_was_here'

#this is the group that the user wants to be deleted from
#it is used to delete the branches and merge requests from its sub-projects
#the group is specified using the -group <group> command line parameter
#for testing purposes, you can specify -user instead
if args.group:
    group = gl.groups.get(args.group[0])
elif args.user:
    group = gl.users.list(username=args.user[0])[0]
else:
    raise RuntimeError('Either specify a group or user')

#remove the generated branches and merge requests
#the two counters make sure both branches and merge requests are removed
deleted_mrs = 0
deleted_branches = 0

#retrieve all the projects in this group and its subgroups
projects_in_group = group.projects.list(include_subgroups=True)

#iterate through all the projects and ...
for project in projects_in_group:
    print(project.name)
    #... generate a manageable project, which is just required to delete branches and merge requests
    manageable_project = gl.projects.get(project.id, lazy=True)

    #... get all the merge requests in this project that have the correct title
    #the title is so unique that there cannot be serious other merge requests with the same title :)
    mrs = manageable_project.search(SEARCH_SCOPE_MERGE_REQUESTS, name+' was here! Please delete my access to this group!')
    #when there is a merge request with this title
    if mrs and len(mrs)>0:
        #get the merge request object by the id (iid is the project-internal id, id would be the one you use in searches on gitlab)
        mr = manageable_project.mergerequests.get(mrs[0]['iid'])
        try:
            #delete the merge request
            mr.delete()
            deleted_mrs += 1
        except RuntimeError as e:
            print(e)
    #... get the branch with the correct branch name and delete it
    try:
        br = manageable_project.branches.get(branch)
        br.delete()
        deleted_branches += 1
    except GitlabGetError:
        #it is entirely possible that the project does not have such a branch, 
        #as it is only created when a branch named master or main exists
        print(f'{project.name} does not have a branch named {branch}')

#inform about how many branches and merge requests were deleted
print(f'{deleted_mrs} merge requests were deleted')
print(f'{deleted_branches} branches were deleted')