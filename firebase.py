import requests
from config import FIREBASE
from session import userbot

def fetch_and_append_sessions():
    url = f"{FIREBASE}/userbot.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error fetching data from Firebase:", e)
        return

    data = response.json()
    if not data:
        print("No data found in Firebase")
        return

    sessions = []
    for user_id, user_data in data.items():
        session = user_data.get("session")
        if session:
            sessions.append(session)

    existing = set(userbot.setdefault("client", []))
    count = 0
    for session in sessions:
        if session not in existing:
            userbot["client"].append(session)
            existing.add(session)
            count += 1

    print(f"Fetched {len(sessions)} sessions from Firebase, appended {count} new sessions")


def add_new_user(data: dict):
    user_id = data.get("user_id")
    if not user_id:
        print("❌ user_id not found in data")
        return False
    
    url = f"{FIREBASE}/users/{user_id}.json"
    response = requests.put(url, json=data)

    if response.status_code == 200:
        print("✅ New user started")
        return True
    else:
        print(f"❌ Failed to add data: {response.text}")
        return False


def fetch_user():
    try:
        # Get all users from Firebase
        response = requests.get(f"{FIREBASE}/users.json")

        if response.status_code != 200 or response.json() is None:
            print("❌ Failed to fetch users or no data found.")
            return None

        data = response.json()  # dictionary of key -> value

        # Extract all keys from users
        keys_list = list(data.keys()) if isinstance(data, dict) else None

        return keys_list

    except Exception as e:
        print(f"❌ Error while fetching user keys: {e}")
        return None