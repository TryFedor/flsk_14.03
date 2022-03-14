from requests import post

print(post('http://localhost:5000/api/jobs',
           json={'id': 1,
                 'job': 'Заголовок',
                 'team_leader': 1,
                 'work_size': 23,
                 'collaborators': '7, 7, 7',
                 'is_finished': True
                 }).json())

print(post('http://localhost:5000/api/jobs').json())  # pustoy

print(post('http://localhost:5000/api/jobs', # norm
           json={'id': 4,
                 'job': 'ok',
                 'team_leader': 1,
                 'work_size': 23,
                 'collaborators': '7, 7, 7',
                 'is_finished': True
                 }).json())
