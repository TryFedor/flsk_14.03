from requests import get, delete, post

port = 5022

print(get(f'http://localhost:{port}/api/v2/users').json())
print(get(f'http://localhost:{port}/api/v2/users/1').json())
print(get(f'http://localhost:{port}/api/users/-1').json())
print(get(f'http://localhost:{port}/api/users/job2').json())

print(post(f'http://localhost:{port}/api/v2/users').json())
print(post(f'http://localhost:{port}/api/v2/users', json={'surname': 'Баранов',
                                                           'name': 'Баран',
                                                           'age': 337,
                                                           'position': 'Правый',
                                                           'speciality': 'Копатыч',
                                                           'address': 'луна',
                                                           'email': 'email1239999@email.com',
                                                           'password': '777'}).json())

print(delete(f'http://localhost:{port}/api/v2/users/3').json())
print(delete(f'http://localhost:{port}/api/v2/users/-1').json())
