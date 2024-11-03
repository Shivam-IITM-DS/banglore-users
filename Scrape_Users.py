import requests
import pandas as pd

#A header was created to send the request with a token, removed that piece of code as it was sensitive .

def get_users_in_bangalore():
    url = 'https://api.github.com/search/users'
    params = {
        'q': 'location:Bangalore followers:>100',
        'per_page': 100,
        'page': 1
    }
    
    users = []
    while True:
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()
        
        for user in data.get('items', []):
            users.append(user)
        
        if 'next' not in response.links:
            break
        params['page'] += 1

    return users

def clean_company_name(company):
    if company:
        return company.strip().lstrip('@').upper()
    return ''

def fetch_user_details(user_login):
    url = f'https://api.github.com/users/{user_login}'
    response = requests.get(url, headers=HEADERS)
    return response.json()

def create_users_csv(users):
    user_data = []
    for user in users:
        user_details = fetch_user_details(user.get('login'))

        user_info = {
            'login': user_details.get('login', ''),
            'name': user_details.get('name', ''),
            'company': clean_company_name(user_details.get('company', '')),
            'location': user_details.get('location', ''),
            'email': user_details.get('email', ''),
            'hireable': user_details.get('hireable', ''),
            'bio': user_details.get('bio', ''),
            'public_repos': user_details.get('public_repos', ''),
            'followers': user_details.get('followers', ''),
            'following': user_details.get('following', ''),
            'created_at': user_details.get('created_at', '')
        }

        user_data.append(user_info)
    
    df = pd.DataFrame(user_data)
    df.to_csv('users.csv', index=False)

users = get_users_in_bangalore()
#create_users_csv(users)




def get_repositories_for_user(username):
    url = f'https://api.github.com/users/{username}/repos'
    params = {
        'per_page': 100,
        'sort': 'pushed',
        'page':  1
    }
    
    repos = []
    while True:
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()
        
        for repo in data:
            repos.append({
                'login': username,
                'full_name': repo.get('full_name', ''),
                'created_at': repo.get('created_at', ''),
                'stargazers_count': repo.get('stargazers_count', 0),
                'watchers_count': repo.get('watchers_count', 0),
                'language': repo.get('language', ''),
                'has_projects': repo.get('has_projects', False),
                'has_wiki': repo.get('has_wiki', False),
                'license_name': repo.get('license')['name'] if repo.get('license') else ''
            })
        
        if 'next' not in response.links:
            break
        params['page'] += 1

    return repos

def create_repositories_csv(users):
    repo_data = []
    for user in users:
        repos = get_repositories_for_user(user['login'])
        repo_data.extend(repos)
    
    df = pd.DataFrame(repo_data)
    df.to_csv('repositories.csv', index=False)

create_repositories_csv(users)
