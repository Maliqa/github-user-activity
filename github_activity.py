import sys
import json
import urllib.request
import urllib.error


def fetch_activity(username):
    url = f"https://api.github.com/users/{username}/events/public"

    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("❌ User not found.")
        else:
            print("❌ Failed to fetch data from GitHub.")
        sys.exit(1)


def show_activity(events):
    if not events:
        print("No recent activity found.")
        return

    for event in events[:5]:
        event_type = event.get("type")
        repo = event.get("repo", {}).get("name", "unknown repo")

        if event_type == "PushEvent":
            commits = event.get("payload", {}).get("commits", [])
            print(f"- Pushed {len(commits)} commits to {repo}")

        elif event_type == "IssuesEvent":
            print(f"- Opened a new issue in {repo}")

        elif event_type == "WatchEvent":
            print(f"- Starred {repo}")

        elif event_type == "CreateEvent":
            print(f"- Created repository {repo}")

        else:
            print(f"- {event_type} in {repo}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python github_activity.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    events = fetch_activity(username)
    show_activity(events)


if __name__ == "__main__":
    main()
