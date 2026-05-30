import os
import time

import requests
from dotenv import load_dotenv


load_dotenv()


def get_required_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def build_headers(username, contact_email=None):
    contact = f"; contact: {contact_email}" if contact_email else ""
    return {
        "User-Agent": f"chess-profile-tool/1.2 (username: {username}{contact})",
        "Accept-Encoding": "gzip",
        "Accept": "application/json, text/plain, */*",
    }


def fetch_archives(username, headers):
    url = f"https://api.chess.com/pub/player/{username}/games/archives"
    response = requests.get(url, headers=headers, timeout=30)
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

def fetch_pgns(archive_list, headers):
    all_pgns = ""
    for archive_url in archive_list:
        time.sleep(1)
        pgn_response = requests.get(f"{archive_url}/pgn", headers=headers, timeout=30)
        print(f"Fetching PGNs from {archive_url}, Status Code: {pgn_response.status_code}")
        if pgn_response.status_code == 200:
            all_pgns += pgn_response.text + "\n\n"
            # retun all_pgns
        elif pgn_response.status_code == 429:
            print(f"Rate limit exceeded. Retrying after a delay.")
            time.sleep(60)
            pgn_response = requests.get(f"{archive_url}/pgn", headers=headers, timeout=30)
            if pgn_response.status_code == 200:
                all_pgns += pgn_response.text + "\n\n"
            else:
                print(f"Failed to fetch PGNs from {archive_url}")
    return all_pgns

def main():
    username = get_required_env("CHESS_COM_USERNAME")
    contact_email = os.getenv("CHESS_COM_CONTACT_EMAIL")
    output_file = os.getenv("CHESS_COM_OUTPUT_FILE", f"{username}_all_games.pgn")
    headers = build_headers(username, contact_email)

    print(f"Fetching game archives for user: {username}")
    archive_list = fetch_archives(username, headers)
    if archive_list:
        print(f"Found {len(archive_list)} archives. Fetching games...")
        all_pgns = fetch_pgns(archive_list, headers)
        with open(output_file, "w", encoding="utf-8") as pgn_file:
            if all_pgns.strip():
                pgn_file.write(all_pgns)
                print(f"All games have been saved to {output_file}")
            else:
                print("No PGNs were fetched.")
    else:
        print("No archives found or unable to fetch archive list.")

if __name__ == "__main__":
    main()
