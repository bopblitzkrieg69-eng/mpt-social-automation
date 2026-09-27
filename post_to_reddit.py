#!/usr/bin/env python3
"""post_to_reddit.py

Posts a rotating promotional message for MPT Country Roads Marketplace to Reddit.
Designed to run inside GitHub Actions on a Mon/Wed/Fri schedule.

Required environment variables (set as GitHub Secrets):
  REDDIT_CLIENT_ID      — OAuth2 client ID from your Reddit app
  REDDIT_CLIENT_SECRET  — OAuth2 client secret from your Reddit app
  REDDIT_USERNAME       — Reddit account username
  REDDIT_PASSWORD       — Reddit account password
  REDDIT_USER_AGENT     — Identifies your script (e.g. 'mpt-social-bot/1.0 by YourUsername')

Optional:
  POST_INDEX_OVERRIDE   — Integer 0-5; forces a specific post variant (for testing)

App URL: https://albertacountryroadsmrkt.whacka.app
"""

import os
import sys
import datetime
import praw
from posts.post_variations import POSTS


def get_post_index() -> int:
    """Return a post index that rotates by week-of-year * 3 + day-of-week position.
    Mon = slot 0, Wed = slot 1, Fri = slot 2 within a given week cycle.
    Wraps across the full POSTS list so no two consecutive runs show the same text.
    """
    override = os.environ.get("POST_INDEX_OVERRIDE")
    if override is not None:
        return int(override) % len(POSTS)

    today = datetime.date.today()
    week_num = today.isocalendar()[1]
    # weekday(): Mon=0, Tue=1, Wed=2, Thu=3, Fri=4
    day_slot = {0: 0, 2: 1, 4: 2}.get(today.weekday(), 0)
    return (week_num * 3 + day_slot) % len(POSTS)


def build_reddit_client() -> praw.Reddit:
    required = [
        "REDDIT_CLIENT_ID",
        "REDDIT_CLIENT_SECRET",
        "REDDIT_USERNAME",
        "REDDIT_PASSWORD",
        "REDDIT_USER_AGENT",
    ]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print(f"ERROR: Missing required secrets: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
    )


def main():
    reddit = build_reddit_client()
    index = get_post_index()
    variant = POSTS[index]

    print(f"Selected post variant #{index}: '{variant['title']}'")

    for subreddit_name in variant["subreddits"]:
        subreddit = reddit.subreddit(subreddit_name)
        submission = subreddit.submit(
            title=variant["title"],
            selftext=variant["body"],
        )
        print(f"Posted to r/{subreddit_name}: https://reddit.com{submission.permalink}")

    print("Done.")


if __name__ == "__main__":
    main()
