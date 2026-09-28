# MPT Country Roads Marketplace — Social Posting Automation

Automated social media posting for [MPT Country Roads Marketplace](https://albertacountryroadsmrkt.whacka.app).

Posts fire Monday / Wednesday / Friday at **10am Mountain Time** via GitHub Actions, routing through **[Postiz](https://postiz.com)** — a multi-platform social scheduler. One workflow run reaches every channel you connect to your Postiz account: Reddit, Facebook, LinkedIn, X (Twitter), Instagram, and 30+ others.

---

## How it works

1. GitHub Actions triggers the cron on Mon/Wed/Fri at 10am MT.
2. `post_to_postiz.py` picks a post variant based on the run date (deterministic rotation across 6 variants).
3. The script calls the Postiz API (`POST /public/v1/posts`), passing the selected content to every connected channel.
4. Postiz handles the platform-specific formatting and publishing.

---

## Setup

### 1. Create a Postiz account

Sign up at [postiz.com](https://postiz.com) (cloud) or self-host.

### 2. Connect your social channels in Postiz

In the Postiz dashboard, connect the accounts you want to post to:
- **Reddit** — requires a Reddit account with posting permissions
- **Facebook Page** — requires a Facebook Page (not a personal profile)
- **LinkedIn** — personal profile or company page
- Any other platform Postiz supports (X, Instagram, TikTok, Bluesky, etc.)

### 3. Get your Postiz API key

In your Postiz dashboard: **Settings → API → Generate API Key**

Copy the key — you will add it as a GitHub Secret.

### 4. Add GitHub Secrets

Go to your repo on GitHub: **Settings → Secrets and variables → Actions → New repository secret**

#### Required

| Secret name | Value |
|---|---|
| `POSTIZ_API_KEY` | Your Postiz API key from step 3 |

#### Optional — pin specific channels

If you leave these out, the script auto-discovers **all** active channels connected to your Postiz account and posts to every one of them. Set these only if you want to restrict posting to specific channels:

| Secret name | How to find the value |
|---|---|
| `POSTIZ_REDDIT_INTEGRATION_ID` | In Postiz: Channels → click Reddit → copy the ID from the URL or API (`GET /public/v1/integrations`) |
| `POSTIZ_FACEBOOK_INTEGRATION_ID` | Same — Facebook Page channel |
| `POSTIZ_LINKEDIN_INTEGRATION_ID` | Same — LinkedIn channel |

To find integration IDs, call the Postiz API:
```bash
curl -H "Authorization: YOUR_API_KEY" https://api.postiz.com/public/v1/integrations
```
Each object in the response has an `"id"` field — that is the value to use.

---

## Files

| File | Purpose |
|---|---|
| `.github/workflows/social_post.yml` | GitHub Actions workflow — cron + manual trigger |
| `post_to_postiz.py` | Main script — picks post variant, calls Postiz API |
| `posts/post_variations.py` | 6 rotating post variants (founding-member scarcity hook) |
| `posts/__init__.py` | Package marker |
| `requirements.txt` | Python dependencies (`requests`) |

---

## Post content

6 rotating variants, all built around the founding-member scarcity hook:

- **App URL**: https://albertacountryroadsmrkt.whacka.app
- **Hook**: "99 of 100 founding member spots still open — free to join, free to post forever"
- Targeting Alberta buy/sell audience

Post content is in `posts/post_variations.py`. Edit the `POSTS` list there to change what gets sent.

---

## Schedule and timezone

Alberta observes:
- **MDT (UTC-6)** — mid-March to early November
- **MST (UTC-7)** — early November to mid-March

The workflow runs **both** cron entries (16:00 UTC and 17:00 UTC) so the post always lands at 10am MT regardless of DST. On the two annual transition weeks, two posts fire roughly 1 hour apart — this is harmless and self-corrects the following week.

---

## Platforms that receive posts

Any channel connected in your Postiz account is included automatically. Postiz supports 34 platforms including:

Reddit · Facebook · LinkedIn · X (Twitter) · Instagram · TikTok · Bluesky · Pinterest · YouTube · Discord · Slack · Telegram · Threads · Mastodon · and more.

**Reddit-specific note**: Reddit requires a title and subreddit in its API settings. The script posts to `r/Alberta` with the post title derived from the first line of each variant. If you want to post to additional subreddits, edit `post_to_postiz.py` → `build_platform_entry()` and add more entries to the `subreddit` array.

---

## Manual test

1. Go to **Actions** tab in the repo.
2. Select **Post to Social via Postiz**.
3. Click **Run workflow**.

The run logs show which integrations were found, which post variant was selected, and the Postiz API response.

---

## Rotating post selection

The variant is chosen deterministically:

```
index = (ISO_week_number x 3 + day_slot) % 6
day_slot: Mon=0, Wed=1, Fri=2
```

This means:
- Each week uses 3 consecutive variants (Mon, Wed, Fri).
- The starting variant shifts each week, so you never see the same text twice in a row across the full 6-variant pool.
- Given the same date, the same variant is always selected — reruns and manual triggers on the same day are idempotent.
