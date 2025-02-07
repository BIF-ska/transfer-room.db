import requests
import json
import responses
import os

# 1) Define a dummy base URL that doesn't actually exist.
#    We'll let 'responses' intercept calls to this domain.
DUMMY_BASE_URL = "http://dummyserver.local/api/external"

# 2) Point base_dir to the folder where your json_data/ folder actually is.
#    For a Windows path, you can do one of the following:
#    - use raw string (r"")
#    - or double backslashes
#    - or forward slashes
base_dir = r"C:\Users\sad\Documents\GitHub\transfer-room.db\python_code"
@responses.activate
def get_test_response(url):
    """
    Intercepts any GET request to the dummy URL and returns local JSON data.
    """

    # -------------------------------------------------------------------------
    # 1. Load local JSON for competitions
    # -------------------------------------------------------------------------
    competitions_path = os.path.join(base_dir, "json_data", "competitions.json")
    with open(competitions_path, 'r', encoding='utf-8') as f:
        json_competition_file = json.load(f)

    # 2. Load local JSON for coaches
    coach_path = os.path.join(base_dir, "json_data", "coach_data.json")
    with open(coach_path, 'r', encoding='utf-8') as f:
        json_coach_file = json.load(f)

    # 3. If it's a "players" URL, parse competition ID (e.g. competitionid=1575)
    if "players" in url and "competitionid=" in url:
        comp_id = url.split("competitionid=")[1]
    else:
        # fallback ID if not found
        comp_id = "724"

    # 4. Load local JSON for players based on comp_id, e.g. 1575.json
    player_file_path = os.path.join(base_dir, "json_data", f"{comp_id}.json")
    if os.path.exists(player_file_path):
        with open(player_file_path, 'r', encoding='utf-8') as f:
            json_player_file = json.load(f)
    else:
        json_player_file = {}  # fallback if no file found

    # -------------------------------------------------------------------------
    # 5. Register mocked responses for each endpoint
    #    So whenever `requests.get(...)` is called with these URLs,
    #    they will return our local JSON.
    # -------------------------------------------------------------------------

    # Mock players
    # e.g. http://dummyserver.local/api/external/players?position=...&competitionid=1575
    responses.add(
        method=responses.GET,
        url=f"{DUMMY_BASE_URL}/players?position=0&amount=1000&competitionid={comp_id}",
        json=json_player_file,
        status=200
    )

    # Mock competitions
    responses.add(
        method=responses.GET,
        url=f"{DUMMY_BASE_URL}/competitions",
        json=json_competition_file,
        status=200
    )

    # Mock coaches
    responses.add(
        method=responses.GET,
        url=f"{DUMMY_BASE_URL}/coaches",
        json=json_coach_file,
        status=200
    )

    # -------------------------------------------------------------------------
    # 6. Actually call `requests.get(url)`.
    #    Because of @responses.activate, the request will be intercepted
    #    and you'll get back the JSON from the relevant "responses.add".
    # -------------------------------------------------------------------------
    resp = requests.get(url)
    return resp


def get_response(request_url, test_mode=False):
    """
    If test_mode=True, use our local JSON mock response (via get_test_response).
    Otherwise, do a real request (not recommended here since you do not have access).
    """
    if test_mode:
        response = get_test_response(request_url)
    else:
        # REAL request - only if you have the real endpoint and credentials
        response = requests.get(request_url)

    return response.json()  # Convert response to JSON dictionary or list


if __name__ == "__main__":
    # Example usage: we point at our dummy base URL and specify competitionid=1575
    #   => This should load 1575.json from your "json_data" folder.
    url = f"{DUMMY_BASE_URL}/players?position=0&amount=1000&competitionid=1575"

    # We do test_mode=True so it won't make a real HTTP request.
    data = get_response(url, test_mode=True)
    print(data)
