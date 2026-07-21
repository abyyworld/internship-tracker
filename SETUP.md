# Setup & Deployment

**Where to host it:** GitHub. It's the right choice for exactly your reasons —
GitHub Actions runs the scraper on a daily cron **for free** with no server and no
computer switched on, and the result renders as a clean page (`README.md`) that
anyone can view at a URL you share. Google Sheets can't self-scrape without fragile
Apps Script; a hosted web app costs money and maintenance. GitHub wins.

The repo is **already initialised and committed locally**. You just need to create
the GitHub repo and push. ~3 minutes.

---

## Step 1 — Create the GitHub repo

Go to <https://github.com/new> and make a repo named e.g. `internship-tracker`.
- **Don't** add a README, .gitignore, or licence (this repo already has them).
- Public if you want to share it openly; private if you'd rather invite people.

## Step 2 — Push (copy-paste, swap in the repo name if you changed it)

```bash
cd "/Users/abyyworld/Desktop/internship watcher"
git remote add origin https://github.com/abyyworld/internship-tracker.git
git push -u origin main
```

If it asks for a password, use a **Personal Access Token** (GitHub no longer accepts
your account password over HTTPS): <https://github.com/settings/tokens> → "Generate
new token (classic)" → tick `repo` → paste it as the password.

*Prefer the `gh` CLI? Install it (`brew install gh`), run `gh auth login`, then
`gh repo create internship-tracker --public --source=. --push` does steps 1–2 in one line.*

## Step 3 — Turn on the daily auto-run

The workflow (`.github/workflows/watch.yml`) is already in the repo. After pushing:

1. Repo → **Settings → Actions → General → Workflow permissions**
2. Select **"Read and write permissions"** → Save.
   *(This lets the daily job commit new roles back to the repo.)*
3. Repo → **Actions** tab → if prompted, click **"I understand, enable workflows"**.
4. Click the **"Daily internship watch"** workflow → **Run workflow** to test it now.

That's it. From then on it runs every morning at **07:00 UTC** and commits any new roles.
Change the time by editing the `cron:` line in the workflow.

## Step 4 (optional) — Get emailed when new roles drop

GitHub → your avatar → **Settings → Notifications → Actions** → enable email.
You'll get a mail every time the daily job commits changes.
*(For a Discord/Telegram ping instead, say the word and I'll add a webhook step.)*

---

## Sharing it

Just send people the repo URL: `https://github.com/abyyworld/internship-tracker`.
The `README.md` dashboard is what they'll see first. Anyone can **Fork** it and enable
Actions to get their own auto-updating copy.

Want a prettier standalone site? Enable **Settings → Pages** and I'll add an HTML
dashboard generator — but the README already looks clean on GitHub.

---

## Running it locally (optional)

```bash
python3 internship_watcher.py
```

No installs — Python 3.8+ stdlib only. Regenerates `README.md`, `tracker.csv`,
`manual_checks.md`, and a `new_roles_<date>.md` digest.

### Local daily cron (Mac, if you'd rather not use Actions)
```bash
(crontab -l 2>/dev/null; echo "0 8 * * * cd '/Users/abyyworld/Desktop/internship watcher' && python3 internship_watcher.py >> watcher.log 2>&1") | crontab -
```

---

## Files in this repo

| File | What it is |
|------|-----------|
| `README.md` | **The live dashboard** — regenerated every run. This is the shared page. |
| `internship_watcher.py` | The scraper. Stdlib only. |
| `tracker.csv` | Full data + your own `my_status`/`priority`/`applied_date`/`notes` columns (never overwritten). |
| `manual_checks.md` | Elite firms with private ATS + UK spring-week deadlines. |
| `new_roles_<date>.md` | Digest of what opened on a given run. |
| `.github/workflows/watch.yml` | The daily GitHub Actions job. |

---

## What it scrapes

- **GitHub community boards:** SimplifyJobs (2026 + 2027 when it launches), vanshb03 2027, sndsh404 2027.
- **21 Greenhouse company APIs (live JSON, no auth):** Jump Trading, IMC, Akuna Capital,
  Virtu, Anthropic, Jane Street, xAI, Waymo, Cloudflare, Stripe, Databricks, Scale AI,
  Brex, Figma, Together AI, Verkada, CoreWeave, Nuro, Mercury, Wayve, DeepMind.
- **Curated elite watchlist (24 firms, private ATS):** DE Shaw, Two Sigma, Citadel,
  Optiver, HRT, Five Rings, SIG, Google, DeepMind, Meta, Apple, MSR, OpenAI, Palantir,
  ARM, Netflix, Isomorphic Labs, Graphcore, DRW.
- **12 UK spring weeks / insight days** with application windows.

### Add more Greenhouse boards
Find the slug from a company's board URL (`boards.greenhouse.io/SLUG`) and add a line to
`GREENHOUSE_BOARDS` in the script:
```python
("slug", "Company Name", "Summer 2027"),
```

### Tune what counts as "elite"
Edit the `TIER_1` / `TIER_2` sets at the top of `internship_watcher.py`.

### Broaden/narrow which roles match
Edit `KEYWORDS` (e.g. add `"vr", "xr", "human-computer"` for the HCI side).

---

## Honest limitations

- Community repos are community-maintained; roles can lag a few hours behind official postings.
- Greenhouse only shows currently-posted roles. Seasonal ones (Jane Street SWE, Citadel)
  go live Aug–Oct — the boards are watched from now, so you'll catch them the next morning.
- Private-ATS firms (DE Shaw, Two Sigma, Citadel, Google, Meta, Apple…) can't be
  auto-scraped — `manual_checks.md` lists their pages; check weekly.
- Spring-week deadlines are estimates — verify on company pages before relying on them.
- The SimplifyJobs 2027 repo 404s until it launches (~Aug 2026); the watcher skips it
  gracefully and picks it up automatically once it exists.
