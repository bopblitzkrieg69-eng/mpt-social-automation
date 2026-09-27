"""post_variations.py

Rotating Reddit post content for MPT Country Roads Marketplace.
Posts are selected by index derived from the week number so the sequence
is deterministic (same post never repeats back-to-back across a full cycle).

App URL: https://albertacountryroadsmrkt.whacka.app
"""

POSTS = [
    {
        "title": "Only 99 founding member spots left on Alberta's newest buy/sell marketplace — free forever",
        "body": (
            "Hey r/Alberta — wanted to share something local I've been building.\n\n"
            "**MPT Country Roads Marketplace** is a free Alberta buy/sell app with 12 categories: "
            "Vehicles, Housing, Electronics, Clothing, Tools, Gaming, Outdoor, Pets, Kids, Jobs, Home & Garden, and more.\n\n"
            "Joining is completely free — no membership fees, no catch. You can post and browse forever at no cost.\n\n"
            "Right now we're down to **99 of 100 founding member spots**. Founding members get in at the ground floor "
            "of something that's built for Alberta, not Silicon Valley.\n\n"
            "Check it out: https://albertacountryroadsmrkt.whacka.app\n\n"
            "Happy to answer any questions in the comments."
        ),
        "subreddits": ["Alberta"],
    },
    {
        "title": "Free Alberta marketplace app — 99 founding spots still open (Vehicles, Housing, Pets, Jobs + more)",
        "body": (
            "If you're buying or selling anything in Alberta, this might be worth a look.\n\n"
            "**Alberta Country Roads Marketplace** is a local marketplace app — 100% free to join and use. "
            "12 categories live right now: Vehicles, Housing, Electronics, Clothing, Tools, Gaming, Outdoor, Pets, "
            "Kids, Jobs, Home & Garden, and more.\n\n"
            "We're still in founding-member territory — **99 spots remain** out of the first 100. "
            "No cost, no pressure, just a made-in-Alberta platform growing from the ground up.\n\n"
            "App link: https://albertacountryroadsmrkt.whacka.app\n\n"
            "Let me know if you have questions!"
        ),
        "subreddits": ["Alberta"],
    },
    {
        "title": "Built a local Alberta buy/sell marketplace — looking for founding members (it's free)",
        "body": (
            "Long-time Albertan here. Frustrated with the big platforms that don't understand rural and small-city selling, "
            "so I built something local.\n\n"
            "**MPT Country Roads Marketplace** — free Alberta buy/sell app covering 12 categories. "
            "Completely free to join and post. The only paid feature is a $2.99 listing boost if you want more visibility.\n\n"
            "Still have **99 of 100 founding member spots** open. If you want to be part of building "
            "an Alberta-first platform, now's the time.\n\n"
            "https://albertacountryroadsmrkt.whacka.app\n\n"
            "Appreciate any feedback from this community."
        ),
        "subreddits": ["Alberta"],
    },
    {
        "title": "Alberta buy/sell app with 12 categories — founding members still open, completely free",
        "body": (
            "Quick share for anyone buying or selling in Alberta.\n\n"
            "**Alberta Country Roads Marketplace** just launched — a local marketplace app with categories for "
            "Vehicles, Housing, Electronics, Clothing, Tools, Gaming, Outdoor, Pets, Kids, Jobs, Home & Garden, and more.\n\n"
            "It's free to join and free to post. The only optional paid feature is a $2.99 boost to push "
            "your listing to the top of a category.\n\n"
            "**99 founding member spots** are still available. Founding members are the people who shape "
            "what this platform becomes.\n\n"
            "https://albertacountryroadsmrkt.whacka.app"
        ),
        "subreddits": ["Alberta"],
    },
    {
        "title": "Local Alberta marketplace — still taking founding members (free to join, free to post)",
        "body": (
            "Sharing this because I think Alberta deserves its own buy/sell platform that isn't Kijiji or Facebook.\n\n"
            "**MPT Country Roads Marketplace** is live with 12 categories: Vehicles, Housing, Electronics, "
            "Clothing, Tools, Gaming, Outdoor, Pets, Kids, Jobs, Home & Garden, and more. "
            "Free to join, free to post, forever.\n\n"
            "We're in early days — **99 of the first 100 founding spots** are still open. "
            "Being a founding member just means you were here first. No cost attached.\n\n"
            "https://albertacountryroadsmrkt.whacka.app\n\n"
            "Happy to hear thoughts from this community."
        ),
        "subreddits": ["Alberta"],
    },
    {
        "title": "r/Calgary — free local marketplace app, 99 founding spots left, built for Alberta",
        "body": (
            "Hey Calgary — built something local I wanted to share here.\n\n"
            "**MPT Country Roads Marketplace** is a free Alberta buy/sell app. 12 categories: Vehicles, Housing, "
            "Electronics, Clothing, Tools, Gaming, Outdoor, Pets, Kids, Jobs, Home & Garden, and more.\n\n"
            "Completely free — no membership cost, no posting fee. The only paid option is an optional $2.99 "
            "listing boost. **99 of 100 founding member spots** still available.\n\n"
            "https://albertacountryroadsmrkt.whacka.app\n\n"
            "Appreciate any thoughts or feedback!"
        ),
        "subreddits": ["Calgary"],
    },
]
