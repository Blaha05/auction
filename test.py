import httpx

BASE_URL = "http://127.0.0.1:8000"  # Заміни на адресу свого API
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTEsImVtYWlsIjoidXNlckBleGFtcGxlLmNvbSIsImV4cCI6MTczMjU1MDEzM30.WOBHhbl6FMp0YtYjoPr56_KNKtg0QQGBPfx2uKslUQg"
  # Заміни на валідний токен

def get_users():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = httpx.get(f"{BASE_URL}/get_user", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed: {response.status_code}, {response.json()}")

if __name__ == "__main__":
    try:
        users = get_users()
        print("Users:", users)
    except Exception as e:
        print(e)
