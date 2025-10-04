import requests

owner = input("Enter the name of the repository owner: ")
repo = input("Enter the name of the repository: ")

url = f"https://api.github.com/repos/{owner}/{repo}"
url2 = f"https://api.github.com/repos/{owner}/{repo}/contributors"
url3 = f"https://api.github.com/repos/{owner}/{repo}/commits"

Running = True

response = requests.get(url)
response2 = requests.get(url2)
response3 = requests.get(url3)

while Running:
    
    if response.status_code == 200:
        data = response.json()
        data2 = response2.json()
        data3 = response3.json()
        print(f"Repository Name: {data['name']}")
        print(f"Description: {data['description']}")
        print(f"Repository owner: {data['owner']['login']}")
        print(f"Repository URL: {data['html_url']}")
        print(f"Contributors: {[contributor['login'] for contributor in data2]}")
        print(f"Stars: {data['stargazers_count']}")
        print(f"Forks: {data['forks_count']}")
        print(f"Open Issues: {data['open_issues_count']}")
        print(f"Watchers: {data['watchers_count']}")
        print(f"Language: {data['language']}")
        print(f"Default Branch: {data['default_branch']}")
        print(f"License: {data['license']['name'] if data['license'] else 'No license'}")
        print(f"Created on: {data['created_at']}")
        print(f"Last updated on: {data['updated_at']}")
        print(f"Recent Commits: {[commit['commit']['message'] for commit in data3[:5]]}")
    
    else:
        print("Error fetching repository data.")
        
        
    print("Do you want to check another repository?")
    choice = input("Enter 'y' for yes or 'n' for no: ")
    
    if choice.lower() == 'y':
        Running = True
    elif choice.lower() == 'n':
        print("Exiting the program.")
        print("Thank you for using the GitHub Repository Analyzer!")
        Running = False