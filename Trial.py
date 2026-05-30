import requests
import time

username = "laluboom"
contact_email = "viseshakbari@gmail.com"

headers = {
    'User-Agent': f'my-profile-tool/1.2 (username: {username}; contact: {contact_email})',
    'Accept-Encoding': 'gzip',
    'Accept': 'application/json, text/plain, */*'
}

def fetch_archives(username):
    url = f"https://api.chess.com/pub/player/{username}/games/archives"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            return response.json().get('archives', [])
        except ValueError:
            print("Error: Received non-JSON response")
            print(response.text)
            return []
    else:
        print(f"Error: Failed to fetch archives. Status Code: {response.status_code}")
        print(response.text)
        return []

def fetch_pgns(archive_list):
    all_pgns = ""
    for archive_url in archive_list:
        time.sleep(1)
        pgn_response = requests.get(f"{archive_url}/pgn", headers=headers)
        print(f"Fetching PGNs from {archive_url}, Status Code: {pgn_response.status_code}")
        if pgn_response.status_code == 200:
            all_pgns += pgn_response.text + "\n\n"
            # retun all_pgns
        elif pgn_response.status_code == 429:
            print(f"Rate limit exceeded. Retrying after a delay.")
            time.sleep(60)
            pgn_response = requests.get(f"{archive_url}/pgn", headers=headers)
            if pgn_response.status_code == 200:
                all_pgns += pgn_response.text + "\n\n"
            else:
                print(f"Failed to fetch PGNs from {archive_url}")
    return all_pgns

def main():
    print(f"Fetching game archives for user: {username}")
    archive_list = fetch_archives(username)
    if archive_list:
        print(f"Found {len(archive_list)} archives. Fetching games...")
        all_pgns = fetch_pgns(archive_list)
        filename = f"{username}_all_games.pgn"
        with open(filename, "w") as pgn_file:
            if all_pgns.strip():
                pgn_file.write(all_pgns)
                print(f"All games have been saved to {filename}")
            else:
                print("No PGNs were fetched.")
    else:
        print("No archives found or unable to fetch archive list.")

if __name__ == "__main__":
    main()
