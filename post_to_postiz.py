#!/usr/bin/env python3
"""post_to_postiz.py
Posts a rotating MPT Country Roads Marketplace promo through the Postiz API.
Postiz handles cross-platform delivery: Reddit, Facebook, LinkedIn, and any
other channel connected to the Postiz account.

Schedule: Monday / Wednesday / Friday at 10am Mountain Time (MDT = UTC-6).
Triggered by GitHub Actions cron or workflow_dispatch.

Required GitHub Secret:
  POSTIZ_API_KEY — API key from your Postiz dashboard (Settings → API)

Optional GitHub Secrets (only needed if Postiz isn't already connected to these):
  POSTIZ_REDDIT_INTEGRATION_ID   — Postiz integration ID for Reddit
  POSTIZ_FACEBOOK_INTEGRATION_ID — Postiz integration ID for Facebook Page
  POSTIZ_LINKEDIN_INTEGRATION_ID — Postiz integration ID for LinkedIn

If the optional secrets are not set, the script fetches all connected
integrations from Postiz at runtime and posts to every active channel.
"""

import os
import sys
import json
import datetime
import requests

from posts.post_variations import POSTS

POSTIZ_API_BASE = "https://api.postiz.com/public/v1"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_headers():
    api_key = os.environ.get("POSTIZ_API_KEY", "").strip()
    if not api_key:
        print("ERROR: POSTIZ_API_KEY secret is not set.")
        sys.exit(1)
    return {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }


def get_integrations(headers):
    """Return list of active Postiz integrations for this account."""
    resp = requests.get(f"{POSTIZ_API_BASE}/integrations", headers=headers, timeout=30)
    if resp.status_code != 200:
        print(f"ERROR: Failed to fetch integrations ({resp.status_code}): {resp.text}")
        sys.exit(1)
    data = resp.json()
    # The API returns a list directly or a dict with an array — handle both shapes.
    if isinstance(data, list):
        integrations = data
    else:
        integrations = data.get("integrations", data.get("channels", []))
    return integrations


def pick_integration_ids(integrations):
    """
    Build a list of integration IDs to post to.

    Priority order:
      1. Use individual POSTIZ_*_INTEGRATION_ID secrets when set.
      2. Fall back to all active integrations discovered from the API.
    """
    explicit_ids = []
    for env_var in (
        "POSTIZ_REDDIT_INTEGRATION_ID",
        "POSTIZ_FACEBOOK_INTEGRATION_ID",
        "POSTIZ_LINKEDIN_INTEGRATION_ID",
    ):
        val = os.environ.get(env_var, "").strip()
        if val:
            explicit_ids.append(val)

    if explicit_ids:
        print(f"Using explicit integration IDs from secrets: {explicit_ids}")
        return explicit_ids

    # Auto-discover: use every integration that is marked active/connected.
    # The exact field name for active status varies by Postiz version.
    active = []
    for intg in integrations:
        # Accept an integration if it has no explicit disabled/inactive flag.
        disabled = intg.get("disabled", False) or intg.get("inactive", False)
        if not disabled and intg.get("id"):
            active.append(intg["id"])
            print(f"  Found integration: {intg.get('name', 'unknown')} "
                  f"({intg.get('providerIdentifier', '?')}) — id={intg['id']}")

    if not active:
        print("ERROR: No active Postiz integrations found. "
              "Connect at least one channel in your Postiz dashboard.")
        sys.exit(1)

    print(f"Auto-discovered {len(active)} integration(s).")
    return active


def pick_post(run_date=None):
    """
    Select a post variant deterministically from the run date.

    Rotation: (ISO week number * 3 + day_slot) % len(POSTS)
    day_slot:  Mon=0, Wed=1, Fri=2 (the three scheduled run days)

    This guarantees the same post is always selected for a given
    Monday/Wednesday/Friday within a given ISO week, and the selection
    shifts each week so no two consecutive runs show the same text.
    """
    if run_date is None:
        run_date = datetime.date.today()

    iso_week = run_date.isocalendar()[1]
    weekday  = run_date.weekday()          # Mon=0 ... Sun=6
    day_slot = {0: 0, 2: 1, 4: 2}.get(weekday, 0)   # Mon/Wed/Fri -> 0/1/2

    index = (iso_week * 3 + day_slot) % len(POSTS)
    post  = POSTS[index]
    print(f"Run date: {run_date}  |  ISO week: {iso_week}  |  "
          f"day_slot: {day_slot}  |  post index: {index}")
    return post


def build_platform_entry(integration_id, content, platform_identifier=None):
    """
    Build one entry in the Postiz 'posts' array.

    For Reddit, Postiz requires platform-specific settings (subreddit, title,
    post type).  For all other platforms (Facebook, LinkedIn, X, etc.) the
    generic text-post shape is sufficient — Postiz handles the per-platform
    formatting internally.

    The 'content' field for Reddit carries the body text; the title is passed
    in settings.subreddit[].value.title.
    """
    # Determine the platform from the identifier string if provided.
    is_reddit = platform_identifier and "reddit" in platform_identifier.lower()

    entry = {
        "integration": {"id": integration_id},
        "value": [{"content": content, "image": []}],
    }

    if is_reddit:
        # Reddit needs subreddit, title, and post type in settings.
        # type "self" = text post (no external URL required).
        entry["settings"] = {
            "__type": "reddit",
            "subreddit": [
                {
                    "value": {
                        "subreddit": "/r/Alberta",
                        "title": content.split("\n")[0][:299],
                        "type": "self",
                        "is_flair_required": False,
                    }
                }
            ],
        }
    else:
        # Generic shape — works for Facebook, LinkedIn, X, Bluesky, etc.
        entry["settings"] = {"__type": "general"}

    return entry


def build_request_body(post, integration_ids, integrations_meta):
    """
    Assemble the full Postiz create-post request body.
    type='now' publishes immediately (the workflow already fires at the
    correct schedule time via cron).
    """
    # Build a lookup of integration id -> providerIdentifier for Reddit detection.
    id_to_provider = {
        intg["id"]: intg.get("providerIdentifier", "")
        for intg in integrations_meta
        if intg.get("id")
    }

    posts_entries = []
    for iid in integration_ids:
        provider = id_to_provider.get(iid, "")
        # Compose post body: for Reddit use body text, for others merge title + body.
        body_text = post.get("body", "")
        title_text = post.get("title", "")

        if provider and "reddit" in provider.lower():
            # Reddit: body goes in value[0].content; title goes in settings.
            content = body_text
        else:
            # Facebook / LinkedIn / X etc.: combine title + body into one block.
            content = f"{title_text}\n\n{body_text}" if title_text else body_text

        entry = build_platform_entry(iid, content, platform_identifier=provider)
        posts_entries.append(entry)

    return {
        "type": "now",
        "shortLink": False,
        "tags": [],
        "posts": posts_entries,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=== MPT Country Roads Marketplace — Postiz multi-platform poster ===")

    headers      = get_headers()
    integrations = get_integrations(headers)

    print(f"Total integrations on Postiz account: {len(integrations)}")
    integration_ids = pick_integration_ids(integrations)

    post = pick_post()
    print(f"Selected post title: {post['title']}")

    body = build_request_body(post, integration_ids, integrations)
    print(f"\nPosting to {len(body['posts'])} platform(s) via Postiz...")

    resp = requests.post(
        f"{POSTIZ_API_BASE}/posts",
        headers=headers,
        data=json.dumps(body),
        timeout=60,
    )

    print(f"HTTP {resp.status_code}")
    if resp.status_code in (200, 201):
        result = resp.json()
        print("Success! Postiz response:")
        print(json.dumps(result, indent=2))
    else:
        print(f"ERROR: Postiz returned {resp.status_code}:")
        print(resp.text)
        sys.exit(1)

    print("\nDone.")


if __name__ == "__main__":
    main()
