import requests

BASE_URL = "http://localhost:80"

def login(username: str, password: str):
    url = f"{BASE_URL}/login"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def save_session(token: str, password: str, file_path: str):
    url = f"{BASE_URL}/saveSession"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    files = {
        "file": open(file_path, "rb")
    }
    data = {
        "password": password
    }
    response = requests.post(url, headers=headers, files=files, data=data)
    response.raise_for_status()
    return response.json()

def get_session(token: str, password: str, file_id: str):
    url = f"{BASE_URL}/getSession"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "file_id": file_id,
        "password": password
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()

    file_path = f"{file_id}.csv"
    with open(file_path, 'wb') as file:
        file.write(response.content)
    
    return file_path

def main():
    username = "test"
    password = "secret"
    file_password = "macromedia"
    file_path = "test.csv"

    print("Logging in...")
    token = login(username, password)
    print(f"Access Token: {token}")

    print("Saving session...")
    save_response = save_session(token, file_password, file_path)
    print(f"Save Session Response: {save_response}")

    print("Getting session...")
    file_id = save_response["file_id"]
    get_response = get_session(token, file_password, file_id)
    print(f"Get Session Response: {get_response}")

if __name__ == "__main__":
    main()
