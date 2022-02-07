import argparse

from gitlab import Gitlab, GitlabCreateError, GitlabGetError

def read_file(path: str) -> str:
    f = open(path, 'r', encoding='iso8859-1')
    content = f.read()
    f.close()
    return content


accessToken = read_file('access_token').strip()
host = read_file('host').strip()
gl = Gitlab(url=host, private_token=accessToken)

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

args = parser.parse_args()

name = args.name[0]
branch = name+'_was_here'

if args.group:
    group = gl.groups.get(args.group[0])
elif args.user:
    group = gl.users.list(username=args.user[0])[0]
else:
    raise RuntimeError('Either specify a group or user')

created = 0

for project in group.projects.list(include_subgroups=True):
    print(project.name)
    manageable_project = gl.projects.get(project.id, lazy=True)
    main_or_master = "main"
    try:
        manageable_project.branches.get('main')
    except GitlabGetError:
        main_or_master = "master"
    try:
        manageable_project.branches.create({'branch': branch,
                                            'ref': main_or_master})
    except GitlabCreateError:
        print(f'{project.name} has neither master nor main branch, spare it as folks use git in a funny way :)')
        continue
    
    #commit my message
    content = open('I_was_here.md').read()
    content = content.replace('<group>', group.name)
    content = content.replace('<name>', name)
    data = {
        'branch': branch,
        'commit_message': name + ' was here.',
        'actions': [
            {
                'action': 'create',
                'file_path': name+'_was_here.md',
                'content': content,
            }
        ]
    }
    commit = manageable_project.commits.create(data)

    #create the merge request
    mr = manageable_project.mergerequests.create({'source_branch': branch,
                                                'target_branch': main_or_master,
                                                'title': name+' was here! Please delete my access to this group!'})
    created += 1

print(f'{created} branches and merge requests were created')
