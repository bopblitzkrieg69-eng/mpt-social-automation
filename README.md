# MPT Country Roads — Reddit Social Automation

Automatically posts rotating promotional content for [Alberta Country Roads Marketplace](https://albertacountryroadsmrkt.whacka.app) to r/Alberta and r/Calgary on a Monday / Wednesday / Friday schedule at 10am Mountain Time.

---

## How it works

- **GitHub Actions** runs `post_to_reddit.py` on the configured cron schedule.
- The script picks one of 6 rotating post variants, determined by the week number and day, so the same text never runs in back-to-back posts.
- Reddit credentials are read entirely from **GitHub Secrets** — nothing sensitive is stored in the code.

---

## Setup — 5 steps

### 1. Create a Reddit app for the posting account

1. Log in to the Reddit account you want to post from.
2. Go to **https://www.reddit.com/prefs/apps**.
3. Click **Create App** (or **Create Another App**).
4. Fill in:
   - **Name**: `mpt-social-bot` (or anything you like)
   - **Type**: choose **script**
   - **Redirect URI**: `http://localhost:8080` (required by Reddit, not actually used)
5. Click **Create app**.
6. Note the two values shown:
   - The short string under your app name — that is your **Client ID**.
   - The longer string next to **secret** — that is your **Client Secret**.

---

### 2. Add GitHub Secrets

In this repo: **Settings → Secrets and variables → Actions → New repository secret**

Add each of the following secrets exactly as named:

| Secret name | What to put in it |
|---|---|
| `REDDIT_CLIENT_ID` | The Client ID from step 1 (short string under app name) |
| `REDDIT_CLIENT_SECRET` | The Client Secret from step 1 (string next to "secret") |
| `REDDIT_USERNAME` | The Reddit username of the posting account (no `u/` prefix) |
| `REDDIT_PASSWORD` | The Reddit account password |
| `REDDIT_USER_AGENT` | A short identifier, e.g. `mpt-social-bot/1.0 by YourRedditUsername` |

**All 5 secrets are required.** The workflow will fail with a clear error message if any are missing.

---

### 3. (One-time) Make sure the Reddit account has enough karma to post

Reddit restricts new accounts from posting in large subreddits like r/Alberta until they have some karma history. If posts fail with a `403` or `RATELIMIT` error, the account may need to build karma first by commenting on other posts.

See `knowledge/reddit-rate-limit-fresh-account.md` if you hit this.

---

### 4. Test the workflow manually

Before waiting for the scheduled run:

1. Go to the **Actions** tab in this repo.
2. Select **Post to Reddit**.
3. Click **Run workflow** → **Run workflow**.

This fires the script immediately. Check the run log for the URL of the post it created.

---

### 5. Schedule (automatic)

Once secrets are in place the workflow fires automatically:

- **Monday at 10am MT**
- **Wednesday at 10am MT**
- **Friday at 10am MT**

Alberta observes MDT (UTC-6) in summer. The cron in the workflow file uses `16:00 UTC`. A commented-out line for `17:00 UTC` (MST, UTC-7, winter) is included — uncomment it in October when clocks fall back.

---

## File layout

```
mpt-social-automation/
├── .github/
│   └── workflows/
│       └── reddit_post.yml      # GitHub Actions workflow (cron + job definition)
├── posts/
│   ├── __init__.py
│   └── post_variations.py       # 6 rotating post variants with titles and body text
├── post_to_reddit.py            # Main script: picks variant, authenticates, posts
├── requirements.txt             # Python dependency (praw)
└── README.md                    # This file
```

---

## Customising posts

Edit `posts/post_variations.py` to add, remove, or reword variants. Each entry is a dict with:
- `title` — the Reddit post title
- `body` — the self-text body (Markdown)
- `subreddits` — list of subreddit names to post to (e.g. `["Alberta"]` or `["Calgary"]`)

The app URL in every variant points to **https://albertacountryroadsmrkt.whacka.app**.

---

## Secrets reference (quick lookup)

```
REDDIT_CLIENT_ID       short string under app name on reddit.com/prefs/apps
REDDIT_CLIENT_SECRET   string next to "secret" on the same page
REDDIT_USERNAME        Reddit username (no u/ prefix)
REDDIT_PASSWORD        Reddit password
REDDIT_USER_AGENT      e.g.  mpt-social-bot/1.0 by YourRedditUsername
```
