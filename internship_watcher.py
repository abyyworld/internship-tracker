#!/usr/bin/env python3
"""
internship_watcher.py v4 — universal academic & career platform
=================================================
Target:  Global internships, research assistant roles, PhD/postdoc fellowships,
         new-grad positions, robotics/embodied-AI startups, and UK programmes.

SOURCES AUTO-SCRAPED EVERY RUN:
  GitHub community repos  — SimplifyJobs (internships + new-grad), vanshb03, sndsh404
  Greenhouse JSON API     — trading, AI, software, robotics, research boards
  Ashby public job boards — AI, robotics, and science startups
  Lever public postings   — software, autonomy, defence, and research companies

CURATED ELITE + ACADEMIC WATCHLISTS (career hubs, never counted as postings):
  Jane Street, DE Shaw, Two Sigma, Citadel, Optiver, HRT, Five Rings, SIG,
  Google/DeepMind, Meta, Apple, Amazon, Microsoft Research, OpenAI, ARM,
  Netflix, Palantir; plus NSF REU, NIH, CERN, and major university career hubs

UK SPRING WEEKS (hardcoded, always in tracker):
  Jane Street FOCUS, Citadel Discover, Goldman Sachs, Morgan Stanley,
  JP Morgan, Two Sigma Discovery, Optiver/IMC insight days, Barclays

Run:   python3 internship_watcher.py
Needs: Python 3.8+ stdlib only.
"""

import csv, html, json, os, re, ssl, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
TRACKER_FILE   = "tracker.csv"
MANUAL_FILE    = "manual_checks.md"
TODAY          = date.today().isoformat()
DROP_CLOSED    = True
# Personal application state belongs in the ignored local cockpit/database, never
# in the public tracker committed by the scheduled workflow.
USER_COLS      = []
URGENT_DAYS    = 10   # roles whose deadline is within this many days get a top section
MISSING_RUNS_TO_CLOSE = 2

# ── FILTER TOGGLES ────────────────────────────────────────────────────────────
# Philosophy: INCLUDE roles and TAG them, so you filter in the CSV / dashboard.
# Nothing below is deleted from the data — these just control what's scraped in.
INCLUDE_SENIOR_FTE = False   # True also pulls Senior/Staff/Manager/Director FTE jobs
INCLUDE_OFF_LANE   = False   # True keeps non-SWE/AI/quant roles (marketing, HR, etc.)
# Everything else (country, citizenship, visa, degree level, term, role type) is a
# COLUMN you filter yourself — no role is hidden. See the columns in tracker.csv.

# Technical lane filter — a role must mention at least one of these to be included.
# Covers all CS/STEM domains: SWE, AI/ML, quant, data, research, HCI, security,
# biotech, physics, EE, and academic positions (postdoc, RA, PhD fellowship).
LANE = [
    # Core CS/SWE
    "software", "engineer", "developer", "swe", "backend", "frontend",
    "full stack", "full-stack", "systems", "platform", "infrastructure",
    "devops", "site reliability", "cloud", "distributed",
    # AI / ML / Data Science
    "machine learning", " ml", "ml ", " ai", "ai ", "artificial intelligence",
    "deep learning", "computer vision", "nlp", "natural language",
    "large language", "llm", "foundation model", "generative",
    "reinforcement learning", "multimodal",
    # Data / Analytics
    "data", "analytics", "business intelligence", "database", "data warehouse",
    "data pipeline", "etl", "spark", "hadoop",
    # Quant / Finance
    "quant", "quantitative", "trading", "trader", "algorithmic", "market making",
    "financial engineer", "risk", "portfolio",
    # Robotics / Autonomy
    "robotics", "mechatronics", "perception", "autonomous", "autonomy",
    "motion planning", "slam", "ros", "embodied", "manipulation", "humanoid",
    # HCI / UX / XR
    "hci", "human-computer", "user experience", "ux research",
    "virtual reality", "augmented reality", "mixed reality", "xr", "interaction",
    # Security / Crypto
    "security", "cybersecurity", "cryptography", "privacy", "infosec",
    "penetration", "vulnerability", "reverse engineering", "malware",
    # Hardware / Embedded / EE
    "fpga", "embedded", "firmware", "hardware", "electrical engineering",
    "ece", "vlsi", "chip", "asic", "dsp", "signal processing", "rf",
    "mechatronics", "circuit",
    # Computational Science / Research
    "research", "scientist", "applied", "computational",
    "bioinformatics", "computational biology", "genomics", "proteomics",
    "neuroscience", "cognitive science", "operations research",
    "climate", "atmospheric", "physics", "applied mathematics", "statistics",
    "mathematical", "optimization",
    # Academic positions (always pass these role types regardless of topic)
    "postdoc", "postdoctoral", "research assistant", "research associate",
    "phd fellowship", "doctoral", "fellowship",
    # Specific role titles
    "technology", "technical", "product engineer",
]

# Elite tier — a public discovery signal, not a personal application decision.
TIER_1 = {
    "jane street", "de shaw", "two sigma", "hudson river trading", "hrt",
    "citadel", "citadel securities", "optiver", "imc trading", "imc",
    "five rings", "susquehanna", "sig", "akuna capital", "akuna",
    "openai", "anthropic", "google deepmind", "deepmind", "xai", "x.ai",
    "microsoft research", "meta ai", "fair", "jump trading", "jump",
    "virtu", "virtu financial", "tower research", "squarepoint",
    "g-research", "gresearch", "xtx markets", "xtx", "marshall wace",
    "man group", "point72", "cubist", "qube research",
}
TIER_2 = {
    "palantir", "google", "alphabet", "meta", "facebook", "apple",
    "amazon", "microsoft", "netflix", "stripe", "waymo", "databricks",
    "scale ai", "figma", "hugging face", "cohere", "mistral", "together ai",
    "drw", "arm", "graphcore", "wayve", "isomorphic labs", "nvidia",
    "cloudflare", "brex", "verkada", "nuro", "perplexity", "ramp",
    "notion", "cursor", "anysphere", "cognition", "sierra", "harvey",
    "elevenlabs", "airbnb", "coinbase", "datadog", "spotify",
}

try:
    import certifi
except ImportError:  # GitHub Actions' Python normally has a usable system CA store
    certifi = None

SSL_CTX = ssl.create_default_context(cafile=certifi.where() if certifi else None)

# Robotics companies are classified independently from prestige.  `company_type`
# is deliberately coarse: it is a discovery signal, not an investment claim.
# Equity is never assumed to be included in an offer.
ROBOTICS_COMPANIES = {
    "figure":                  ("humanoid robotics",          "private-scaleup"),
    "kodiak":                  ("autonomous trucking",        "private-scaleup"),
    "formic":                  ("industrial robotics",        "startup"),
    "lodestar":                ("space robotics / autonomy",  "emerging-startup"),
    "bot auto":                ("autonomous trucking",        "startup"),
    "dusty robotics":          ("construction robotics",      "startup"),
    "agility robotics":        ("humanoid robotics",          "private-scaleup"),
    "anduril":                 ("autonomous systems",         "private-scaleup"),
    "apptronik":               ("humanoid robotics",          "private-scaleup"),
    "nuro":                    ("autonomous vehicles",        "private-scaleup"),
    "waymo":                   ("autonomous vehicles",        "established"),
    "locus robotics":          ("warehouse robotics",         "private-scaleup"),
    "torc robotics":           ("autonomous trucking",        "established"),
    "sunday robotics":         ("home robotics",              "emerging-startup"),
    "cobot":                   ("collaborative robotics",      "emerging-startup"),
    "collaborative robotics":  ("collaborative robotics",      "emerging-startup"),
    "deft robotics":           ("humanoid robotics",          "emerging-startup"),
    "graymatter robotics":     ("industrial robotics",        "startup"),
    "physical intelligence":   ("embodied AI",                "emerging-startup"),
    "generalist":              ("general-purpose robotics",   "emerging-startup"),
    "bedrock robotics":        ("construction autonomy",      "emerging-startup"),
    "the bot company":         ("home robotics",              "emerging-startup"),
    "sanctuary ai":            ("humanoid robotics",          "private-scaleup"),
    "1x":                      ("humanoid robotics",          "private-scaleup"),
    "anybotics":               ("legged robots",              "private-scaleup"),
    "waabi":                   ("autonomous trucking",        "startup"),
    "shield ai":               ("autonomous systems",         "private-scaleup"),
    "wayve":                   ("embodied AI / driving",      "private-scaleup"),
    "boston dynamics":         ("mobile robotics",            "established"),
    "intrinsic":               ("industrial robotics",        "established"),
    "skild ai":                ("robot foundation models",    "emerging-startup"),
    "rivr":                    ("last-mile robotics",          "emerging-startup"),
    "neura robotics":          ("cognitive robotics",         "private-scaleup"),
    "wandercraft":             ("mobility robotics",          "private-scaleup"),
    "exotec":                  ("warehouse robotics",         "private-scaleup"),
    "unitree":                 ("humanoid / quadruped robots","private-scaleup"),
    "dji":                     ("drones / autonomy",           "established"),
    "zipline":                 ("autonomous delivery",        "private-scaleup"),
    "applied intuition":       ("autonomy tooling",            "private-scaleup"),
    "arthur robotics":         ("robotics",                    "emerging-startup"),
    "dyna robotics":           ("robot learning",              "emerging-startup"),
    "gecko robotics":          ("inspection robotics",         "private-scaleup"),
    "genesis ai":              ("robot foundation models",     "emerging-startup"),
    "humanoid":                ("humanoid robotics",           "private-scaleup"),
    "lightwheel":              ("robot learning",              "emerging-startup"),
    "mecka ai":                ("robotics",                    "emerging-startup"),
    "moonlake":                ("robotics",                    "emerging-startup"),
    "reka ai":                 ("multimodal AI",               "startup"),
    "robco":                   ("industrial robotics",         "private-scaleup"),
    "saronic":                 ("autonomous marine systems",   "private-scaleup"),
    "serve robotics":          ("autonomous delivery",         "public"),
    "standard bots":           ("industrial robotics",         "private-scaleup"),
    "summer robotics":         ("robotics",                    "emerging-startup"),
    "sunrise robotics":        ("industrial robotics",         "emerging-startup"),
    "unitx":                   ("industrial inspection AI",    "startup"),
    "arx robotics":            ("autonomous ground systems",   "startup"),
    "aurora innovation":       ("autonomous trucking",         "public"),
    "avride":                  ("autonomous vehicles",         "private-scaleup"),
    "carbon robotics":         ("agricultural robotics",       "private-scaleup"),
    "diligent robotics":       ("healthcare robotics",         "private-scaleup"),
    "horizon surgical systems":("surgical robotics",           "emerging-startup"),
    "may mobility":            ("autonomous transit",          "private-scaleup"),
    "neuralink":               ("neural / surgical robotics",  "private-scaleup"),
    "outrider":                ("yard autonomy",               "private-scaleup"),
    "path robotics":           ("industrial robotics",         "private-scaleup"),
    "roboforce":               ("industrial robotics",         "emerging-startup"),
    "stack av":                ("autonomous trucking",         "private-scaleup"),
    "wing":                    ("autonomous delivery",         "subsidiary"),
    "chef robotics":           ("food robotics",               "startup"),
    "cobalt robotics":         ("security robotics",           "startup"),
    "dexterity":               ("warehouse robotics",          "private-scaleup"),
    "fieldai":                 ("field robotics",              "private-scaleup"),
    "field ai":                ("field robotics",              "private-scaleup"),
    "machina labs":            ("robotic manufacturing",       "private-scaleup"),
    "nomagic":                 ("warehouse robotics",          "private-scaleup"),
    "robotics ai institute":   ("robotics research",           "nonprofit"),
    "robust ai":               ("industrial robotics",         "startup"),
    "zoox":                    ("autonomous vehicles",         "subsidiary"),
    "bright machines":         ("industrial automation",       "private-scaleup"),
}

# ─────────────────────────────────────────────────────────────────────────────
# SOURCE DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────

GITHUB_SOURCES = [
    {
        "name": "Simplify2027",
        "url":  "https://raw.githubusercontent.com/SimplifyJobs/Summer2027-Internships/dev/README.md",
        "fmt":  "html",
        "term": "Summer 2027",
    },
    {
        "name": "Simplify2026",
        "url":  "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README.md",
        "fmt":  "html",
        "term": "Summer 2026",
    },
    {
        "name": "SimplifyNewGrad",
        "url":  "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/dev/README.md",
        "fmt":  "html",
        "term": "New Grad 2026",
    },
    {
        "name": "vanshb03_2027",
        "url":  "https://raw.githubusercontent.com/vanshb03/Summer2027-Internships/dev/README.md",
        "fmt":  "md_href",
        "term": "Summer 2027",
    },
    {
        "name": "sndsh404_2027",
        "url":  "https://raw.githubusercontent.com/sndsh404/summer-2027-internships/main/README.md",
        "fmt":  "md_link",
        "term": "Summer 2027",
    },
]

# Verified via API test — these slugs return real data.
# Slugs that returned 404/timeout are NOT listed here (they'd just fail every run).
GREENHOUSE_BOARDS = [
    # slug                    display name              term
    ("jumptrading",          "Jump Trading",           None),
    ("imc",                  "IMC Trading",            None),
    ("akunacapital",         "Akuna Capital",          None),
    ("virtu",                "Virtu Financial",        None),
    ("towerresearchcapital", "Tower Research Capital", None),
    ("squarepointcapital",   "Squarepoint Capital",    None),
    ("anthropic",            "Anthropic",              None),
    ("janestreet",           "Jane Street",            None),
    ("xai",                  "xAI",                     None),
    ("waymo",                "Waymo",                   None),
    ("cloudflare",           "Cloudflare",             None),
    ("stripe",               "Stripe",                 None),
    ("databricks",           "Databricks",             None),
    ("scaleai",              "Scale AI",               None),
    ("brex",                 "Brex",                    None),
    ("figma",                "Figma",                   None),
    ("togetherai",           "Together AI",            None),
    ("verkada",              "Verkada",                 None),
    ("coreweave",            "CoreWeave",               None),
    ("nuro",                 "Nuro",                    None),
    ("mercury",              "Mercury",                 None),
    ("airbnb",               "Airbnb",                  None),
    ("wayve",                "Wayve",                   None),
    ("graphcore",            "Graphcore",               None),
    ("mangroup",             "Man Group",               None),
    ("monzo",                "Monzo",                   None),
    ("deepmind",             "DeepMind",                None),
    ("isomorphiclabs",       "Isomorphic Labs",         None),
    # Robotics / embodied AI / autonomy. These are official public ATS feeds.
    ("figureai",             "Figure",                  None),
    ("kodiak",               "Kodiak",                  None),
    ("formic",               "Formic",                  None),
    ("lodestarspace",        "Lodestar",                None),
    ("botauto",              "Bot Auto",                None),
    ("agilityrobotics",      "Agility Robotics",        None),
    ("andurilindustries",    "Anduril",                 None),
    ("apptronik",            "Apptronik",               None),
    ("locusrobotics",        "Locus Robotics",          None),
    ("torcrobotics",         "Torc Robotics",           None),
    ("arxroboticsgmbh",      "ARX Robotics",            None),
    ("aurorainnovation",     "Aurora Innovation",       None),
    ("avride",               "Avride",                  None),
    ("carbonrobotics",       "Carbon Robotics",         None),
    ("diligentrobotics",     "Diligent Robotics",       None),
    ("flyzipline",           "Zipline",                 None),
    ("horizonsurgicalsystems","Horizon Surgical Systems", None),
    ("maymobility",          "May Mobility",            None),
    ("neuralink",            "Neuralink",               None),
    ("outrider",             "Outrider",                None),
    ("pathrobotics",         "Path Robotics",           None),
    ("roboforce",            "RoboForce",               None),
    ("skildai-careers",      "Skild AI",                None),
    ("stackav",              "Stack AV",                None),
    ("wing",                 "Wing",                    None),
    # Broader tech / research companies
    ("nvidia",               "NVIDIA",                  None),
    ("amd",                  "AMD",                     None),
    ("qualcomm",             "Qualcomm",                None),
    ("arm",                  "Arm",                     None),
    ("intel",                "Intel",                   None),
    ("ibm",                  "IBM",                     None),
    ("samsungresearch",      "Samsung Research",        None),
    ("huggingface",          "Hugging Face",            None),
    ("mistral",              "Mistral AI",              None),
    ("groq",                 "Groq",                    None),
    ("lambdalabs",           "Lambda Labs",             None),
    ("modal",                "Modal",                   None),
    ("replit",               "Replit",                  None),
    ("coinbase",             "Coinbase",                None),
    ("ripple",               "Ripple",                  None),
    ("chime",                "Chime",                   None),
    ("plaid",                "Plaid",                   None),
    ("robinhood",            "Robinhood",               None),
    ("duolingo",             "Duolingo",                None),
    ("reddit",               "Reddit",                  None),
    ("discord",              "Discord",                 None),
    ("snap",                 "Snap",                    None),
    ("twilio",               "Twilio",                  None),
    ("snowflake",            "Snowflake",               None),
    ("mongodb",              "MongoDB",                 None),
    ("elastic",              "Elastic",                 None),
    ("hashicorp",            "HashiCorp",               None),
    ("1password",            "1Password",               None),
    ("cloudsmith",           "Cloudsmith",              None),
    # Defence / aerospace / space
    ("spacex",               "SpaceX",                  None),
    ("boeing",               "Boeing",                  None),
    ("l3harris",             "L3Harris",                None),
    ("bae-systems",          "BAE Systems",             None),
    ("northropgrumman",      "Northrop Grumman",        None),
    ("lockheedmartin",       "Lockheed Martin",         None),
    ("raytheon",             "Raytheon",                None),
    # Research / academic / biotech
    ("allen-institute",      "Allen Institute for AI",  None),
    ("calico",               "Calico (Google)",         None),
    ("modernatx",            "Moderna",                 None),
    ("genentech",            "Genentech",               None),
    ("biontech",             "BioNTech",                None),
    ("deepvariant",          "DeepVariant / Google",    None),
    # NOTE: palantir removed — their Greenhouse board is 404; already tracked via Lever
]

# Ashby boards — format: https://api.ashbyhq.com/posting-api/job-board/{slug}
# Direct role URLs. Verified live.
ASHBY_BOARDS = [
    ("openai",       "OpenAI",       None),
    ("perplexity",   "Perplexity",   None),
    ("cohere",       "Cohere",       None),
    ("ramp",         "Ramp",         None),
    ("notion",       "Notion",       None),
    ("elevenlabs",   "ElevenLabs",   None),
    ("sierra",       "Sierra",       None),
    ("harvey",       "Harvey",       None),
    ("cursor",       "Cursor",       None),
    ("cognition",    "Cognition",    None),
    # Robotics startups, from earliest teams through private scaleups.
    ("sunday",               "Sunday Robotics",         None),
    ("cobot",                "Collaborative Robotics",  None),
    ("deft-ai",              "Deft Robotics",           None),
    ("graymatter-robotics",  "GrayMatter Robotics",     None),
    ("physicalintelligence", "Physical Intelligence",   None),
    ("generalist",           "Generalist AI",           None),
    ("bedrock-robotics",     "Bedrock Robotics",        None),
    ("thebotcompany",        "The Bot Company",         None),
    ("1x",                   "1X",                       None),
    ("applied",              "Applied Intuition",       None),
    ("arthur",               "Arthur Robotics",         None),
    ("dyna-robotics",        "Dyna Robotics",           None),
    ("gecko-robotics",       "Gecko Robotics",          None),
    ("genesis",              "Genesis AI",              None),
    ("humanoid",             "Humanoid",                None),
    ("lightwheel",           "Lightwheel",              None),
    ("mecka.ai",             "Mecka AI",                None),
    ("moonlake",             "Moonlake",                None),
    ("reka",                 "Reka AI",                 None),
    ("robco",                "RobCo",                   None),
    ("saronic",              "Saronic",                 None),
    ("serverobotics",        "Serve Robotics",          None),
    ("standardbots",         "Standard Bots",           None),
    ("summer-robotics",      "Summer Robotics",         None),
    ("sunrise",              "Sunrise Robotics",        None),
    ("unitxlabs",            "UnitX",                   None),
    # More AI / research startups
    ("together",             "Together AI",             None),
    ("anyscale",             "Anyscale",                None),
    ("run-ai",               "Run:AI",                  None),
    ("weights-biases",       "Weights & Biases",        None),
    ("scale",                "Scale AI",                None),
    ("labelbox",             "Labelbox",                None),
    ("roboflow",             "Roboflow",                None),
    ("landing-ai",           "Landing AI",              None),
    ("covariant",            "Covariant",               None),
    ("nuro",                 "Nuro",                    None),
    ("voxel51",              "Voxel51",                 None),
    ("modal-labs",           "Modal Labs",              None),
    ("midjourney",           "Midjourney",              None),
    ("coreweave",            "CoreWeave",               None),
    ("recursion",            "Recursion Pharmaceuticals", None),
    ("insitro",              "insitro",                 None),
    ("etched",               "Etched AI",               None),
    ("groq",                 "Groq",                    None),
    ("sambanova",            "SambaNova Systems",       None),
    ("cerebras",             "Cerebras Systems",        None),
    ("tenstorrent",          "Tenstorrent",             None),
    # NOTE: mistral removed — Ashby slug 404; moved to Lever below
]

# Lever boards — format: https://api.lever.co/v0/postings/{slug}?mode=json
LEVER_BOARDS = [
    ("palantir",     "Palantir",     None),
    ("spotify",      "Spotify",      None),
    ("mistral",      "Mistral AI",   None),
    ("anybotics",    "ANYbotics",    None),
    ("waabi",        "Waabi",        None),
    ("shieldai",     "Shield AI",    None),
    ("ChefRobotics", "Chef Robotics", None),
    ("cobaltrobotics","Cobalt Robotics", None),
    ("dexterity",    "Dexterity",     None),
    ("field-ai",     "FieldAI",       None),
    ("MachinaLabs",  "Machina Labs",  None),
    ("Nomagic",      "Nomagic",       None),
    ("rai",          "Robotics & AI Institute", None),
    ("robust-ai",    "Robust AI",     None),
    ("zoox",         "Zoox",          None),
    ("brightmachines","Bright Machines", None),
    # Additional software / infra / research companies
    ("linear",       "Linear",        None),
    ("vercel",       "Vercel",        None),
    ("supabase",     "Supabase",      None),
    ("retool",       "Retool",        None),
    ("figma",        "Figma",         None),
    ("notion",       "Notion",        None),
    ("loom",         "Loom",          None),
    ("asana",        "Asana",         None),
    ("airtable",     "Airtable",      None),
    ("benchling",    "Benchling",     None),
    ("prefect",      "Prefect",       None),
    ("dbt-labs",     "dbt Labs",      None),
    ("airbyte",      "Airbyte",       None),
    ("astronomer",   "Astronomer",    None),
    ("temporal",     "Temporal",      None),
    ("earthly",      "Earthly",       None),
    # Cybersecurity
    ("crowdstrike",  "CrowdStrike",   None),
    ("sentinelone",  "SentinelOne",   None),
    ("lacework",     "Lacework",      None),
    ("snyk",         "Snyk",          None),
    ("semgrep",      "Semgrep",       None),
    # Climate / clean energy
    ("climateai",    "Climate AI",    None),
    ("watershed",    "Watershed",     None),
    ("energyvault",  "Energy Vault",  None),
]

# ─────────────────────────────────────────────────────────────────────────────
# CURATED ELITE WATCHLIST  (JS-heavy or own ATS — cannot auto-scrape)
# These rows are always present in the tracker. Check the URL manually.
# ─────────────────────────────────────────────────────────────────────────────
# Each URL points at the company's INTERNSHIP / EARLY-CAREERS section (not homepage).
# These firms use private application systems, so we can't pull individual postings —
# the link takes you to their student listings where you filter and apply.
ELITE_WATCHLIST = [
    # company                role hub                              location                 url                                                                          tier
    ("Jane Street",          "→ Internships (SWE / Quant / ML)",   "New York / London",     "https://www.janestreet.com/join-jane-street/internships/",                  "elite"),
    ("DE Shaw",              "→ Internships (SWE / Quant)",        "New York / London",     "https://www.deshaw.com/careers/internships",                                "elite"),
    ("Two Sigma",            "→ Students & Grads",                 "New York / London",     "https://careers.twosigma.com/careers/students",                             "elite"),
    ("Citadel",              "→ Students & Graduates",             "Chicago / London / NY", "https://www.citadel.com/careers/students-and-graduates/",                    "elite"),
    ("Citadel Securities",   "→ Students & Graduates",             "Chicago / London / NY", "https://www.citadelsecurities.com/careers/students-and-graduates/",          "elite"),
    ("Optiver",              "→ Early Careers (SWE / Trader)",     "Amsterdam / Chicago",   "https://optiver.com/working-at-optiver/early-careers/",                     "elite"),
    ("Hudson River Trading", "→ Campus (SWE / Algo)",              "New York / London",     "https://www.hudsonrivertrading.com/campus/",                                "elite"),
    ("Five Rings",           "→ Campus (SWE / Quant)",             "New York",              "https://fiverings.com/campus/",                                             "elite"),
    ("Susquehanna (SIG)",    "→ Students (Tech / Quant)",          "Philadelphia / Dublin", "https://careers.sig.com/students-graduates",                                "elite"),
    ("DRW",                  "→ Campus (SWE / Quant)",             "Chicago / London",      "https://drw.com/work-at-drw/campus/",                                       "elite"),
    ("Point72 / Cubist",     "→ Academy & Internships",            "New York / London",     "https://careers.point72.com/CSJoinTypesInternships",                        "elite"),
    # ---- London-heavy quant (great for a UK base) ----
    ("G-Research",           "→ Students & Graduates",             "London",                "https://www.gresearch.com/careers/?filter_category=students-graduates",      "elite"),
    ("XTX Markets",          "→ Early Careers",                    "London",                "https://www.xtxmarkets.com/careers/",                                       "elite"),
    ("Marshall Wace",        "→ Graduates & Interns",              "London",                "https://www.mwam.com/graduates-interns/",                                   "high"),
    ("Man Group",            "→ Early Careers",                    "London / Oxford",       "https://www.man.com/early-careers",                                         "high"),
    # ---- Big tech (own ATS; deep-linked to intern filters) ----
    ("Google",               "→ Internships (filter: intern)",     "Global (incl London)",  "https://www.google.com/about/careers/applications/jobs/results/?target_level=INTERN_AND_APPRENTICESHIP&employment_type=INTERN", "elite"),
    ("Google DeepMind",      "→ Careers (Student / Research)",     "London / Mountain View","https://deepmind.google/about/careers/",                                    "elite"),
    ("Meta",                 "→ Internships",                      "Global (incl London)",  "https://www.metacareers.com/jobs/?roles[0]=Internships",                     "elite"),
    ("Meta (FAIR / AI)",     "→ AI Research careers",              "London / Menlo Park",   "https://ai.meta.com/careers/",                                              "elite"),
    ("Apple",                "→ Internships",                      "Cupertino / Cambridge", "https://jobs.apple.com/en-us/search?team=internships-STDNT-INTRN",           "elite"),
    ("Microsoft Research",   "→ Internships",                     "Cambridge UK / Redmond","https://jobs.careers.microsoft.com/global/en/search?lc=United%20Kingdom&exp=Students%20and%20graduates", "elite"),
    ("Amazon",               "→ Student Programs (SDE / Applied)", "Global (incl London)",  "https://www.amazon.jobs/content/en/career-programs/student-programs",        "elite"),
    ("NVIDIA",               "→ University Recruiting",            "Global (incl UK)",      "https://www.nvidia.com/en-us/about-nvidia/careers/university-recruiting/",   "high"),
    ("Netflix",              "→ Students",                        "Los Gatos / Remote",    "https://explore.jobs.netflix.net/careers?query=intern",                     "high"),
    ("ARM",                  "→ Early Careers",                   "Cambridge, UK",         "https://careers.arm.com/early-careers",                                     "high"),
    # ---- Academic & research-specific watchlists ----
    ("Tesla",                "→ Internships (all teams)",          "Global / Fremont CA",   "https://www.tesla.com/careers/search/?type=3",                              "high"),
    ("IBM Research",         "→ Research Internships",             "Global",                "https://research.ibm.com/careers/",                                         "high"),
    ("Adobe Research",       "→ Research Internships",             "US / Global",           "https://research.adobe.com/careers/",                                       "high"),
    ("Samsung Research",     "→ Research roles",                   "UK / US / Korea",       "https://www.samsungresearch.com/careers",                                   "high"),
    ("Allen Institute for AI","→ Research / Engineering roles",    "Seattle",               "https://allenai.org/careers",                                               "high"),
]

# Academic research programmes — funded, competitive, and time-limited.
# These are watchlist entries (career hubs), not individual job postings.
ACADEMIC_WATCHLIST = [
    # US federal research programmes
    ("NSF REU",              "Research Experience for Undergrads", "USA (various)",         "https://www.nsf.gov/crssprgm/reu/",                                         "high"),
    ("NIH Internship",       "NIH Intramural Research Training",   "Bethesda MD / Remote",  "https://www.training.nih.gov/programs/sip",                                 "high"),
    ("NASA OSSI",            "One Stop Shopping Initiative (NASA)","USA (various centres)",  "https://intern.nasa.gov/",                                                  "high"),
    ("DOE SULI",             "Science Undergraduate Lab Internship","USA (national labs)",   "https://science.osti.gov/wdts/suli",                                        "high"),
    ("DOE CCI",              "Community College Internships",       "USA (national labs)",   "https://science.osti.gov/wdts/cci",                                         "high"),
    ("CERN openlab",         "CERN Summer Student / openlab",       "Geneva, Switzerland",   "https://openlab.cern/education",                                            "high"),
    ("CERN",                 "CERN Technical / Doctoral Student",   "Geneva, Switzerland",   "https://careers.cern/",                                                     "high"),
    ("European Space Agency","ESA Young Graduate Trainee",          "Darmstadt / Noordwijk", "https://www.esa.int/About_Us/Careers_at_ESA/Young_Graduate_Trainees",        "high"),
    # UK national labs / universities
    ("The Alan Turing Institute","Research internships / studentships","London, UK",         "https://www.turing.ac.uk/work-turing/",                                     "high"),
    ("Wellcome Sanger Institute","Internships / PhD studentships",  "Cambridge, UK",         "https://www.sanger.ac.uk/about/work-with-us/",                             "high"),
    ("EMBL-EBI",             "Internships / PhD positions",          "Cambridge, UK",         "https://www.ebi.ac.uk/about/jobs/",                                         "high"),
    ("STFC / RAL",           "Placement / Research roles",           "Harwell, UK",           "https://www.ukri.org/careers/",                                             "high"),
    # University career hubs (funnel students to research + intern roles)
    ("MIT Career Office",    "→ MIT students / research roles",     "Cambridge MA",          "https://capd.mit.edu/",                                                     "high"),
    ("Stanford Career Ed",   "→ Stanford students / research",      "Stanford CA",           "https://careereducation.stanford.edu/",                                     "high"),
    ("CMU Career Centre",    "→ CMU students / research",           "Pittsburgh PA",         "https://www.cmu.edu/career/",                                               "high"),
    ("Oxford Careers",       "→ Oxford students / DPhil roles",     "Oxford, UK",            "https://www.careers.ox.ac.uk/",                                             "high"),
    ("Cambridge Careers",    "→ Cambridge students / PhD roles",    "Cambridge, UK",         "https://www.careers.cam.ac.uk/",                                            "high"),
    ("Imperial Careers",     "→ Imperial students / research",      "London, UK",            "https://www.imperial.ac.uk/careers/",                                       "high"),
    # European research funding / job boards
    ("EURAXESS",             "→ European PhD / postdoc / RA jobs",  "Europe (various)",      "https://euraxess.ec.europa.eu/jobs",                                        "high"),
    ("jobs.ac.uk",           "→ UK academic jobs (all levels)",     "UK (various)",          "https://www.jobs.ac.uk/",                                                   "high"),
    ("Academic Positions",   "→ PhD / postdoc / faculty (EU)",      "Europe (various)",      "https://academicpositions.eu/",                                             "high"),
    # AI-specific research programmes
    ("Google Research",      "→ Student Researcher / intern",       "Global",                "https://research.google/careers/",                                          "elite"),
    ("OpenAI Research",      "→ Research roles",                    "San Francisco CA",      "https://openai.com/careers/",                                               "elite"),
    ("DeepMind Research",    "→ Research Scientist / Intern",       "London / Mountain View","https://deepmind.google/about/careers/",                                    "elite"),
]

# Top robotics organisations whose ATS cannot be read reliably. These are career
# hubs only, so they are labelled watchlist rather than pretending a job is open.
ROBOTICS_WATCHLIST = [
    ("Boston Dynamics", "Robotics careers",             "US",                 "https://bostondynamics.com/careers/"),
    ("Tesla Optimus",   "AI & Robotics careers",        "Global",             "https://www.tesla.com/careers/search/?query=robotics"),
    ("NVIDIA Robotics", "Robotics / embodied AI roles", "Global",             "https://www.nvidia.com/en-us/about-nvidia/careers/"),
    ("Intrinsic",       "Industrial robotics roles",    "US / Germany",        "https://www.intrinsic.ai/careers"),
    ("Skild AI",        "Robot foundation-model roles", "US",                 "https://www.skild.ai/careers"),
    ("Field AI",        "Field robotics roles",         "US",                 "https://www.fieldai.com/careers"),
    ("RIVR",            "Last-mile robotics roles",     "Switzerland / UK",    "https://rivr.ai/careers"),
    ("NEURA Robotics",  "Cognitive robotics roles",     "Germany",            "https://neura-robotics.com/career"),
    ("Wandercraft",     "Mobility robotics roles",      "France / US",         "https://www.wandercraft.eu/careers"),
    ("Exotec",          "Warehouse robotics roles",     "Europe / Global",     "https://www.exotec.com/careers/"),
    ("Unitree",         "Humanoid / quadruped roles",   "China",               "https://www.unitree.com/career"),
    ("DJI",             "Drones / autonomy roles",      "China / Global",      "https://we.dji.com/jobs"),
    ("Zipline",         "Autonomous delivery roles",    "US / Africa / Global","https://www.flyzipline.com/careers"),
    ("Sanctuary AI",     "Humanoid robotics roles",      "Canada",              "https://careers.kula.ai/sanctuary-ai"),
    ("Mentee Robotics",  "Humanoid robotics roles",      "Israel",              "https://www.comeet.com/jobs/mentee_robotics/6A.002"),
    ("Starship",         "Delivery robotics roles",      "Europe / US",         "https://starship.teamtailor.com/jobs"),
    ("Agile Robots",     "Industrial robotics roles",    "Germany / Global",    "https://www.agile-robots.com/en/career/"),
    ("Enchanted Tools",  "Humanoid robotics roles",      "France",              "https://enchanted.tools/jobs/"),
    ("Oxa",              "Autonomous vehicle roles",     "UK / US",             "https://oxa.tech/careers/"),
    ("Opteran",          "Nature-inspired autonomy",     "UK / US",             "https://opteran.com/careers"),
    ("RLWRLD",           "Robot foundation-model roles","Korea / US / Japan",  "https://www.rlwrld.ai/en/careers"),
    ("LimX Dynamics",    "Humanoid robotics roles",      "China",               "https://ai.limxdynamics.com/en/join-us/"),
    ("Fourier",          "Humanoid robotics roles",      "Singapore / China",   "https://www.fftai.com/career"),
    ("AgiBot",           "Humanoid robotics roles",      "China",               "https://finch.agibot.com/join-us"),
    ("Skydio",           "Autonomous drone roles",       "US",                  "https://www.skydio.com/careers"),
    ("Cartken",          "Delivery robotics roles",      "US / Germany",        "https://www.cartken.com/careers/careers"),
    ("Turing",           "Autonomous vehicle roles",     "Japan",               "https://jobs.tur.ing/en/"),
    ("Crest Robotics",   "Field robotics roles",         "Australia",           "https://crestrobotics.com.au/jobs.html"),
    ("Reach Robotics",   "Underwater robotics roles",    "Australia",           "https://reachrobotics.com/careers/"),
    ("Rapyuta Robotics", "Warehouse robotics roles",     "Japan / India",       "https://www.rapyuta-robotics.com/careers/"),
]

# ─────────────────────────────────────────────────────────────────────────────
# UK SPRING WEEKS & TERM-TIME PROGRAMS
# Applications open ~Sept–Nov 2026; programs run Spring/Easter 2027
# ─────────────────────────────────────────────────────────────────────────────
SPRING_WEEKS = [
    # company            role/program                       location      url                                                               deadline           tier
    ("Jane Street",      "FOCUS (First-Year Insight)",      "London/NY",  "https://www.janestreet.com/join-jane-street/open-roles/",        "Oct–Nov 2026",    "elite"),
    ("Two Sigma",        "Discovery Program",               "London/NY",  "https://careers.twosigma.com/careers/jobListings",               "Oct–Jan 2027",    "elite"),
    ("Citadel",          "Discover Citadel (Spring Week)",  "London",     "https://www.citadel.com/careers/",                               "Oct–Nov 2026",    "elite"),
    ("Optiver",          "Insight Day / Spring Program",    "Amsterdam",  "https://optiver.com/working-at-optiver/career-opportunities/",   "Rolling Oct–Feb", "elite"),
    ("IMC Trading",      "Insight Day",                     "Amsterdam",  "https://www.imc.com/eu/careers/",                                "Rolling Oct–Feb", "elite"),
    ("Goldman Sachs",    "Engineering Spring Insight (UK)", "London",     "https://www.goldmansachs.com/careers/",                          "Oct–Dec 2026",    "high"),
    ("Morgan Stanley",   "Technology Spring Insight (UK)",  "London",     "https://www.morganstanley.com/people-opportunities/",            "Oct–Dec 2026",    "high"),
    ("JP Morgan",        "Technology Spring Week (UK)",     "London",     "https://careers.jpmorgan.com/",                                  "Oct–Nov 2026",    "high"),
    ("Barclays",         "Technology Spring Intern (UK)",   "London",     "https://home.barclays/careers/",                                 "Nov–Jan 2027",    "medium"),
    ("Hudson River Trading","Insight Day / Campus Event",   "London/NY",  "https://www.hudsonrivertrading.com/careers/",                    "Rolling",         "elite"),
    ("Susquehanna (SIG)","Quant Finance Insight Days",      "Dublin",     "https://careers.sig.com/",                                       "Rolling",         "elite"),
    ("Five Rings",       "Summer Smash / Insight Event",    "New York",   "https://fiverings.com/careers/",                                 "Rolling",         "elite"),
]

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "internship-watcher/2"})
    with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as r:
        return r.read().decode("utf-8", "replace")


def first_url(cell):
    for m in re.finditer(r'href="([^"]+)"', cell):
        u = m.group(1)
        if "i.imgur.com" in u:
            continue
        if "simplify.jobs" not in u:
            return html.unescape(u)
    m = re.search(r"\]\((https?://[^)]+)\)", cell)
    if m:
        return html.unescape(m.group(1))
    m = re.search(r'href="([^"]+)"', cell)
    return html.unescape(m.group(1)) if m else ""


def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"\s+", " ", s)).strip()


def days_until(deadline):
    """Return whole days from today to an ISO (YYYY-MM-DD) deadline, else None.
    Text windows like 'Oct–Nov 2026' return None (shown separately, not counted)."""
    if not deadline:
        return None
    m = re.match(r"\s*(\d{4})-(\d{2})-(\d{2})", deadline)
    if not m:
        return None
    try:
        d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None
    return (d - date.today()).days


def clean_loc(s):
    s = s.replace("</br>", " / ").replace("<br>", " / ").replace("<br/>", " / ")
    return strip_html(s).strip(" /")


US_ST = set(("al ak az ar ca co ct de fl ga hi id il in ia ks ky la me md ma mi "
             "mn ms mo mt ne nv nh nj nm ny nc nd oh ok or pa ri sc sd tn tx ut "
             "vt va wa wv wi wy dc").split())
CA_PROVINCES = set("ab bc mb nb nl ns nt nu on pe qc sk yt".split())


def regions_of(loc):
    """Return every geography explicitly supported by a location string."""
    l = f" {loc.lower()} "
    found = []

    def add(region):
        if region not in found:
            found.append(region)

    # Qualifiers beat ambiguous city names.
    if (re.search(r",\s*(" + "|".join(US_ST) + r")\b", l)
            or re.search(r"\b(united states|u\.s\.a?\.?|usa|us)\b", l)
            or re.search(r"\b(multiple us|washington,?\s*d\.?c\.?|"
                         r"california|texas|los angeles|dallas|sf|la)\b", l)
            or re.search(r"\b(nyc|san francisco|new york|seattle|boston|austin|"
                         r"chicago|palo alto|menlo park|redmond|sunnyvale|"
                         r"santa clara|mountain view|bay area|silicon valley)\b", l)):
        add("US")
    if (re.search(r",\s*(" + "|".join(CA_PROVINCES) + r")\b", l)
            or " canada " in l or " toronto " in l or " vancouver " in l
            or " montreal " in l):
        add("Canada")
    if (re.search(r"\b(united kingdom|u\.k\.|uk|england|scotland|wales|"
                  r"northern ireland)\b", l)
            or re.search(r"\b(london|cambridge|birmingham|belfast|edinburgh|"
                         r"cardiff|bristol|manchester|southampton)\s*,?\s*(uk|"
                         r"united kingdom|england|scotland|wales|northern ireland)\b", l)
            or re.search(r"\blondon\s*/", l)
            or (" london " in l and not re.search(r"\blondon\s*,\s*on\b", l))):
        add("UK")
    if (" republic of ireland " in l
            or re.search(r"\b(dublin|cork|galway)\s*,?\s*ireland\b", l)):
        add("Ireland")
    if re.search(r"\b(netherlands|amsterdam|eindhoven)\b", l):
        add("Netherlands")
    if re.search(r"\b(germany|berlin|munich|stuttgart|hamburg)\b", l):
        add("Germany")
    if re.search(r"\b(france|paris|toulouse)\b", l):
        add("France")
    if re.search(r"\b(switzerland|zurich|zürich|lausanne)\b", l):
        add("Switzerland")
    if re.search(r"\b(norway|oslo)\b", l):
        add("Norway")
    country_patterns = (
        ("Sweden", r"\bsweden\b|\bstockholm\b|\bgothenburg\b"),
        ("Denmark", r"\bdenmark\b|\bcopenhagen\b"),
        ("Finland", r"\bfinland\b|\bhelsinki\b"),
        ("Spain", r"\bspain\b|\bmadrid\b|\bbarcelona\b"),
        ("Italy", r"\bitaly\b|\bmilan\b|\brome\b"),
        ("Austria", r"\baustria\b|\bvienna\b"),
        ("Belgium", r"\bbelgium\b|\bbrussels\b"),
        ("Portugal", r"\bportugal\b|\blisbon\b"),
        ("Poland", r"\bpoland\b|\bwarsaw\b|\bkrakow\b"),
        ("Czechia", r"\bczechia\b|\bczech republic\b|\bprague\b"),
        ("Estonia", r"\bestonia\b|\btallinn\b"),
        ("Serbia", r"\bserbia\b|\bbelgrade\b"),
        ("Israel", r"\bisrael\b|\btel aviv\b"),
        ("Singapore", r"\bsingapore\b"),
        ("Japan", r"\bjapan\b|\btokyo\b"),
        ("South Korea", r"\bsouth korea\b|\brepublic of korea\b|\bseoul\b"),
        ("India", r"\bindia\b|\bbengaluru\b|\bbangalore\b|\bhyderabad\b"),
        ("China", r"\bchina\b|\bshanghai\b|\bbeijing\b|\bshenzhen\b"),
        ("Hong Kong", r"\bhong kong\b"),
        ("Taiwan", r"\btaiwan\b|\btaipei\b"),
        ("Australia", r"\baustralia\b|\bsydney\b|\bmelbourne\b|\bbrisbane\b"),
        ("New Zealand", r"\bnew zealand\b|\bauckland\b"),
        ("UAE", r"\bunited arab emirates\b|\bdubai\b|\babu dhabi\b"),
        ("Brazil", r"\bbrazil\b|\bsao paulo\b|\bsão paulo\b"),
        ("Mexico", r"\bmexico\b|\bmexico city\b"),
    )
    for region, pattern in country_patterns:
        if re.search(pattern, l):
            add(region)
    if re.search(r"\beurope\b|\beu\b", l):
        add("Europe")
    if re.search(r"\b(global|worldwide|multiple locations)\b", l):
        add("Global")
    if not found and "remote" in l:
        add("Remote")
    return found or ["Unknown"]


def region_of(loc):
    return " / ".join(regions_of(loc))


def work_mode_of(loc):
    l = loc.lower()
    if "hybrid" in l:
        return "hybrid"
    if "remote" in l:
        return "remote"
    if re.search(r"\bon-?site\b|\bin[- ]office\b", l):
        return "onsite"
    return "unspecified"


def norm_role(role):
    r = role.lower()
    r = re.sub(r"\(.*?\)|\[.*?\]", "", r)
    r = re.sub(r"summer\s*20\d\d|co-?op|intern(ship)?|campus|20\d\d", "", r)
    r = re.sub(r"[^a-z ]", " ", r)
    r = re.sub(r"\s+", " ", r).strip()
    r = r.replace("engineering", "engineer").replace("developer", "engineer")
    return r


def make_id(company, role, loc):
    city = loc.split("/")[0].split(",")[0].strip().lower()
    key = f"{company.lower().strip()}|{norm_role(role)}|{city}"
    return re.sub(r"[^a-z0-9]", "", key)[:64]


TRACKING_QUERY_KEYS = {
    "gh_src", "source", "ref", "referrer", "iis", "iisn",
    "lever-source", "ashby_jid",
}


def safe_url(url):
    try:
        p = urlsplit((url or "").strip())
    except ValueError:
        return ""
    return url if p.scheme in ("http", "https") and bool(p.hostname) else ""


def spreadsheet_safe(value):
    """Neutralize cells that spreadsheet programs could interpret as formulas."""
    text = "" if value is None else str(value)
    if re.match(r"^\s*[=+\-@]", text):
        return "'" + text
    return text


def canonical_url(url):
    """Normalize tracking variants while retaining application semantics."""
    url = safe_url(url)
    if not url:
        return ""
    p = urlsplit(url)
    host = p.hostname.lower()
    if host == "boards.greenhouse.io":
        host = "job-boards.greenhouse.io"
    greenhouse_id_in_path = (
        "greenhouse.io" in host
        and bool(re.search(r"/jobs/(?:[^/]+/)?\d+(?:/|$)", p.path))
    )
    query = []
    for key, value in parse_qsl(p.query, keep_blank_values=True):
        lk = key.lower()
        if (
            lk.startswith("utm_")
            or lk in TRACKING_QUERY_KEYS
            or (lk == "gh_jid" and greenhouse_id_in_path)
        ):
            continue
        query.append((key, value))
    path = re.sub(r"/+", "/", p.path).rstrip("/") or "/"
    return urlunsplit((p.scheme.lower(), host, path, urlencode(query), ""))


def provider_job_key(url):
    """Return an ATS-owned job identity when one can be proven from the URL."""
    raw = safe_url(url)
    if not raw:
        return ""
    raw_parts = urlsplit(raw)
    raw_host = (raw_parts.hostname or "").lower()
    raw_path = re.sub(r"/+", "/", raw_parts.path)
    raw_query = dict(parse_qsl(raw_parts.query, keep_blank_values=True))

    greenhouse_id = raw_query.get("gh_jid", "")
    if not str(greenhouse_id).isdigit() and "greenhouse.io" in raw_host:
        greenhouse_id = raw_query.get("token", "")
    if str(greenhouse_id).isdigit():
        return f"greenhouse:{greenhouse_id}"

    if "greenhouse.io" in raw_host:
        match = re.search(r"/jobs/(?:[^/]+/)?(\d+)(?:/|$)", raw_path)
        if match:
            return f"greenhouse:{match.group(1)}"

    # Some employers front Greenhouse with their own careers domain.
    if raw_host in {"www.imc.com", "imc.com"}:
        match = re.search(r"/careers/jobs/(\d+)(?:/|$)", raw_path)
        if match:
            return f"greenhouse:{match.group(1)}"

    if raw_host in {"www.google.com", "google.com"}:
        match = re.search(r"/jobs/results/(\d+)(?:-|/|$)", raw_path)
        if match:
            return f"google:{match.group(1)}"

    if raw_host == "jobs.apple.com":
        match = re.search(r"/details/(\d+)(?:-\d+)?(?:/|$)", raw_path)
        if match:
            return f"apple:{match.group(1)}"

    if raw_host == "careers.sig.com":
        match = re.search(r"/jobs/(\d+)(?:/|$)", raw_path)
        if match:
            return f"sig:{match.group(1)}"

    if ".myworkdayjobs.com" in raw_host or ".myworkdaysite.com" in raw_host:
        match = re.search(r"_((?:JR|R)\d+)(?:-\d+)?(?:/|$)", raw_path, re.I)
        if match:
            tenant = raw_host.split(".wd", 1)[0]
            return f"workday:{tenant}:{match.group(1).upper()}"

    normalized = canonical_url(raw)
    if not normalized:
        return ""
    p = urlsplit(normalized)
    path = p.path
    if p.hostname == "jobs.lever.co":
        m = re.search(r"/([0-9a-f]{8}-[0-9a-f-]{27,})", path, re.I)
        if m:
            return "lever:" + m.group(1).lower()
    if "ashbyhq.com" in p.hostname:
        m = re.search(r"/([0-9a-f]{8}-[0-9a-f-]{27,})", path, re.I)
        if m:
            return "ashby:" + m.group(1).lower()
    return "url:" + normalized


def tier_of(company):
    c = company.lower()
    # Use word-boundary matching to avoid "sig" matching "design", etc.
    def wbmatch(pattern, text):
        return bool(re.search(r"(?<![a-z])" + re.escape(pattern) + r"(?![a-z])", text))
    for t1 in TIER_1:
        if wbmatch(t1, c):
            return "elite"
    for t2 in TIER_2:
        if wbmatch(t2, c):
            return "high"
    return ""


def emoji_flags(text):
    f = []
    if "🛂" in text: f.append("NO-SPONSORSHIP")
    if "🇺🇸" in text: f.append("US-CITIZEN-ONLY")
    if "🎓" in text: f.append("ADV-DEGREE")
    if "🔥" in text: f.append("HOT")
    return f


# ─── Role classification (TAG, don't drop) ────────────────────────────────────
def lane_match(role):
    t = " " + role.lower() + " "
    return any(k in t for k in LANE)

def degree_level(text, flags=None):
    """Return only eligibility supported by explicit evidence."""
    t = text.lower()
    flags = flags or []
    if re.search(r"\b(bachelor'?s?|undergrad(?:uate)?|b\.?s\.?c?|bs)\b", t):
        return "Undergraduate eligible"
    if re.search(r"\b(ph\.?\s?d|doctoral|doctorate)\b", t):
        return "PhD"
    if re.search(r"\b(msc|m\.?s\.?c?|master'?s?|mba|graduate degree)\b", t):
        return "Masters"
    if "ADV-DEGREE" in flags:
        return "Advanced/unknown"
    return "Unknown"

def role_type(role):
    t = role.lower()
    # Academic / research positions — checked before generic "graduate" catch
    if re.search(r"\bpostdoc(?:toral)?\b|\bpost-doctoral\b", t): return "postdoc"
    if re.search(r"\bph\.?\s?d\.?\b(?!\s*(?:intern|student))|"
                 r"\bdoctoral (?:student|fellow|candidate|position|programme)\b|"
                 r"\bphd (?:student|fellow|candidate|position|programme|thesis)\b", t,
                 re.I):
        return "phd-fellowship"
    if re.search(r"\bm(?:sc|\.sc\.?|asters?)[- ](?:student|research|thesis|intern|"
                 r"position|fellow)\b|\bmaster'?s? research\b", t, re.I):
        return "masters-research"
    if re.search(r"\bresearch (?:assistant|associate|trainee)\b|\bra \b", t):
        return "research-assistant"
    # Standard early-career types
    if re.search(r"\bnew grad(uate)?\b", t):              return "new-grad"
    if "spring" in t and ("week" in t or "insight" in t): return "spring-week"
    if re.search(r"\bco-?op\b", t):                       return "co-op"
    if re.search(r"^(placement)\b|\b(industrial|student|year[- ]long|"
                 r"12[- ]month) placement\b|\bplacement (student|intern|year)\b", t):
        return "placement"
    if re.search(r"\bapprentice(ship)?\b", t):            return "apprenticeship"
    if re.search(r"\bfellowship\b|\bresidency\b", t):     return "fellowship"
    if re.search(r"\bintern\b|\binternships?\b|\bco-?op\b", t): return "intern"
    if re.search(r"\bsummer analyst\b", t):               return "summer-analyst"
    if re.search(r"\bgraduate\b", t):                     return "graduate"
    if re.search(r"\bentry[- ]level\b|\bearly career\b", t): return "entry-level"
    if re.search(r"\bcampus\b", t):                       return "campus"
    return "other"

def is_senior_fte(role):
    """Senior / staff / management / recruiter FTE roles (NOT student roles).
    A 'Senior ... Intern' is not senior — the intern signal wins."""
    t = role.lower()
    if re.search(r"\b(senior|staff|principal|director|head of|vice president|vp|"
                 r"recruiter|engineering manager)\b", t) or "manager," in t or "lead," in t:
        return not re.search(r"\bintern(ship)?\b|\bco-?op\b", t)
    return False

def early_career(role):
    """True for student, intern, research, and PhD/postdoc roles — anything non-senior.
    'graduate' is intentionally excluded: "Graduate Software Engineer" is an FTE title
    at many companies and should NOT auto-pass the strict_intern gate on ATS boards.
    New-grad positions from GitHub repos (SimplifyJobs/New-Grad-Positions) are still
    collected because those sources run without strict_intern=True.
    """
    return role_type(role) in {
        "intern", "co-op", "placement", "spring-week", "summer-analyst",
        "apprenticeship", "fellowship", "new-grad", "entry-level",
        "research-assistant", "phd-fellowship", "postdoc", "masters-research",
    }

def keep(company, role, closed, strict_intern=False):
    """Keep = in your lane + (for APIs) a real early-career signal. PhD/MSc roles
    are KEPT (tagged via degree_level). Senior FTE and off-lane are toggle-gated."""
    if not company or not role:
        return False
    if DROP_CLOSED and closed:
        return False
    if not INCLUDE_SENIOR_FTE and is_senior_fte(role):
        return False
    if not INCLUDE_OFF_LANE and not lane_match(role):
        return False
    if strict_intern and not early_career(role):
        return False
    return True


def infer_term(text, fallback=None):
    t = text.lower()
    year = re.search(r"(?<!\d)(20(?:2[5-9]|3[0-2]))(?!\d)", t)
    y = year.group(1) if year else ""
    paired = re.search(r"\b(spring|summer|fall|autumn|winter)\s*[/&-]\s*"
                       r"(spring|summer|fall|autumn|winter)\b", t)
    if paired:
        a, b = paired.groups()
        a = "Fall" if a == "autumn" else a.title()
        b = "Fall" if b == "autumn" else b.title()
        return f"{a}/{b}" + (f" {y}" if y else "")
    season = re.search(r"\b(spring|summer|fall|autumn|winter)\b", t)
    if season:
        s = "Fall" if season.group(1) == "autumn" else season.group(1).title()
        return f"{s} {y}".strip()
    if y:
        return y
    return fallback or "Unknown"


def term_from_evidence(text, fallback=None):
    """Return (term, explicit) so feed-season fallbacks cannot silently win."""
    explicit = infer_term(text)
    if explicit != "Unknown":
        return explicit, True
    return fallback or "Unknown", False


def _robotics_meta(company):
    c = re.sub(r"[^a-z0-9]+", " ", company.lower()).strip()
    if c in ROBOTICS_COMPANIES:
        return ROBOTICS_COMPANIES[c]
    for name, meta in ROBOTICS_COMPANIES.items():
        normalized_name = re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()
        if (
            c == normalized_name
            or c.startswith(normalized_name + " ")
            or c.endswith(" " + normalized_name)
        ):
            return meta
    return ("", "")


def category_of(company, role, description=""):
    t = f" {company} {role} {description} ".lower()
    # Quant / HFT — most specific financial domain
    if re.search(r"\b(quant|quantitative|trading|trader|market making|"
                 r"algorithmic trading|high frequency|hft)\b", t):
        return "Quant / Finance"
    # Security — its own domain
    if re.search(r"\b(security|cybersecurity|infosec|cryptography|"
                 r"penetration test|vulnerability|malware|reverse engineering|"
                 r"zero.?day|exploit|threat intel)\b", t):
        return "Security"
    # HCI / XR
    if re.search(r"\b(hci|human.computer interaction|ux research|"
                 r"virtual reality|augmented reality|mixed reality|xr|"
                 r"interaction design)\b", t):
        return "HCI / XR"
    # Robotics & Embodied AI
    if _robotics_meta(company)[0] or re.search(
        r"\b(robot(?:ics?)?|mechatronics|embodied ai|"
        r"autonomous (?:vehicle|driving|systems?)|perception|motion planning|"
        r"slam|ros2?|manipulation|humanoid|legged|quadruped)\b", t
    ):
        return "Robotics & Embodied AI"
    # AI / ML / Research
    if re.search(r"\b(machine learning|deep learning|computer vision|nlp|"
                 r"natural language|large language|llm|foundation model|"
                 r"artificial intelligence|research scientist|generative ai|"
                 r"reinforcement learning|multimodal)\b", t):
        return "AI / ML"
    # Bioinformatics / Computational Science
    if re.search(r"\b(bioinformatics|computational biology|genomics|proteomics|"
                 r"drug discovery|structural biology|cheminformatics|"
                 r"biotech|neuroscience|cognitive science|climate model)\b", t):
        return "Computational Science"
    # Data / Analytics
    if re.search(r"\b(data scientist|data engineer|analytics|business intelligence|"
                 r"data warehouse|etl|data pipeline|spark|hadoop)\b", t):
        return "Data"
    # Systems / Infrastructure / Cloud
    if re.search(r"\b(systems engineer|infrastructure|platform engineer|"
                 r"devops|site reliability|cloud engineer|distributed systems|"
                 r"kernel|operating systems|compiler|storage|networking)\b", t):
        return "Systems & Infra"
    # Hardware / EE / Embedded
    if re.search(r"\b(fpga|embedded|firmware|hardware engineer|electrical engineer|"
                 r"vlsi|asic|chip design|dsp|signal processing|pcb)\b", t):
        return "Hardware / EE"
    return "Software Engineering"


def focus_tags(company, role, description=""):
    t = f" {company} {role} {description} ".lower()
    rules = [
        # Robotics / autonomy
        ("embodied-ai",     r"\bembodied ai\b|foundation model"),
        ("humanoid",        r"\bhumanoid\b"),
        ("perception",      r"\bperception\b|computer vision|sensor fusion"),
        ("autonomy",        r"\bautonom"),
        ("controls",        r"\bcontrol(?:s)?\b|motion planning|trajectory"),
        ("manipulation",    r"\bmanipulation\b|grasp"),
        ("robot-software",  r"\brobot(?:ics?)?\b.*\bsoftware\b|\bros2?\b"),
        ("hardware",        r"\bfirmware\b|\bembedded\b|\bmechanical\b|"
                            r"\belectrical\b|\bmechatronics\b|\bfpga\b|\bvlsi\b"),
        # AI / ML subdomains
        ("llm",             r"\bllm\b|large language|gpt|transformer\b"),
        ("computer-vision", r"\bcomputer vision\b|\bcv\b(?= )|image recognition|"
                            r"object detect|segmentation"),
        ("nlp",             r"\bnlp\b|natural language processing"),
        ("rl",              r"\breinforcement learning\b|\brl\b(?= )"),
        ("multimodal",      r"\bmultimodal\b"),
        # Data / systems
        ("data-eng",        r"\bdata engineer|etl\b|data pipeline|spark\b"),
        ("infra",           r"\binfrastructure\b|devops|site reliability|kubernetes|"
                            r"cloud infra"),
        ("distributed",     r"\bdistributed systems?\b"),
        # Security
        ("security",        r"\bsecurity\b|cryptography|penetration|exploit"),
        # Science / research
        ("research",        r"\bresearch\b"),
        ("bioinformatics",  r"\bbioinformatics\b|genomics|proteomics|drug discovery"),
        ("climate",         r"\bclimate\b|atmospheric|carbon|sustainability"),
        ("neuroscience",    r"\bneuroscience\b|neural|brain"),
        # Academic level signals
        ("phd-position",    r"\bphd\b|doctoral|postdoc"),
        ("funded",          r"\bfunded\b|\bstipend\b|\bfellowship\b"),
    ]
    tags = [name for name, pattern in rules if re.search(pattern, t)]
    return ",".join(tags)


def company_signals(company, description=""):
    focus, company_type = _robotics_meta(company)
    d = description.lower()
    if re.search(r"\bequity\b|\bstock options?\b|\brsus?\b", d):
        equity = "posting mentions equity"
    elif company_type in ("emerging-startup", "startup", "private-scaleup"):
        equity = "private company; verify offer"
    elif company_type == "established":
        equity = "company-dependent"
    else:
        equity = "unknown"
    return focus, company_type or "unknown", equity


def derive_flags(text, initial=None):
    t = strip_html(text).lower()
    flags = set(initial or [])
    if re.search(
        r"\b(?:must|needs? to|required to)\s+(?:be|hold)\s+(?:a )?"
        r"u\.?s\.? citizen\b|"
        r"\bu\.?s\.? citizenship (?:is )?(?:required|mandatory)\b|"
        r"\b(?:only|limited to) u\.?s\.? citizens?\b",
        t,
    ):
        flags.add("US-CITIZEN-ONLY")
    if re.search(
        r"\b(?:must|needs? to|required to)\s+be\s+(?:a )?u\.?s\.? persons?\b|"
        r"\bu\.?s\.? person status (?:is )?(?:required|mandatory)\b",
        t,
    ):
        flags.add("US-PERSON-REQUIRED")
    if re.search(
        r"\b(?:must|needs? to|required to)\s+be\s+(?:a )?"
        r"(?:green card holder|permanent resident)\b",
        t,
    ):
        flags.add("PERMANENT-RESIDENT-REQUIRED")
    if re.search(r"\b(no|cannot|unable to|will not) (?:provide |offer )?"
                 r"(?:visa |immigration )?sponsorship\b|"
                 r"\bwithout (?:current or future )?sponsorship\b", t):
        flags.add("NO-SPONSORSHIP")
    return sorted(flags)


# ─────────────────────────────────────────────────────────────────────────────
# PARSERS
# ─────────────────────────────────────────────────────────────────────────────
def parse_html_table(text, term):
    rows, last = [], ""
    for tr in re.findall(r"<tr>(.*?)</tr>", text, re.S):
        tds = re.findall(r"<td.*?>(.*?)</td>", tr, re.S)
        if len(tds) < 4:
            continue
        raw_co = tds[0]
        company = strip_html(raw_co)
        if company in ("↳", ""):
            company = last
        else:
            last = company
        role = strip_html(tds[1])
        loc  = clean_loc(tds[2])
        url  = first_url(tds[3])
        closed = "🔒" in tr
        if not keep(company, role, closed):
            continue
        flags = derive_flags(raw_co + role + tr, emoji_flags(raw_co + role + tr))
        inferred, explicit = term_from_evidence(f"{role} {url}", term)
        rows.append(dict(company=company, role=role, location=loc, url=safe_url(url),
                         term=inferred, term_explicit=explicit,
                         flags=flags, description=""))
    return rows


def parse_md_pipe(text, term):
    rows, last, headers = [], "", []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        first = strip_html(cells[0]).lower()
        if first in ("company", "org", "organization"):
            headers = [strip_html(cell).lower() for cell in cells]
            continue
        if not first or set(cells[0]) <= set("- :"):
            continue
        if headers and (
            "location" not in headers
            or not any(
                any(token in name for token in ("apply", "application", "link"))
                for name in headers
            )
        ):
            # Programme/interest tables often put a type or deadline in the
            # third column. They are not verified location-bearing job rows.
            continue
        raw_co = cells[0]
        company = strip_html(raw_co)
        if company in ("↳", ""):
            company = last
        else:
            last = company
        raw_role = cells[1]
        role_url = first_url(raw_role)  # URL may be embedded as [title](url) in role cell
        role   = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', strip_html(raw_role))
        loc    = clean_loc(cells[2])
        apply  = cells[3] if len(cells) > 3 else ""
        closed = "🔒" in apply or "🔒" in line
        url    = "" if closed else (first_url(apply) or role_url)
        if not keep(company, role, closed):
            continue
        flags = derive_flags(line, emoji_flags(line))
        inferred, explicit = term_from_evidence(f"{role} {url}", term)
        rows.append(dict(company=company, role=role, location=loc, url=safe_url(url),
                         term=inferred, term_explicit=explicit,
                         flags=flags, description=""))
    return rows


def parse_greenhouse(slug, display_name, term):
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    try:
        data = json.loads(fetch(url, timeout=15))
    except Exception as e:
        return None, str(e)
    if not isinstance(data, dict) or not isinstance(data.get("jobs"), list):
        return None, "degraded: Greenhouse response has no jobs list"
    rows = []
    for j in data.get("jobs", []):
        role = j.get("title", "")
        if not keep(display_name, role, False, strict_intern=True):
            continue
        loc_raw = j.get("location", {})
        loc = loc_raw.get("name", "") if isinstance(loc_raw, dict) else str(loc_raw)
        departments = " ".join(
            x.get("name", "") for x in j.get("departments", [])
            if isinstance(x, dict)
        )
        description = strip_html(j.get("content", "") or departments)
        flags = derive_flags(description)
        inferred, explicit = term_from_evidence(role, term)
        rows.append(dict(company=display_name, role=role, location=loc,
                         url=safe_url(j.get("absolute_url", "")),
                         term=inferred, term_explicit=explicit,
                         flags=flags, deadline="", description=description))
    return rows, None


def parse_ashby(slug, display_name, term):
    url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
    try:
        data = json.loads(fetch(url, timeout=15))
    except Exception as e:
        return None, str(e)
    if not isinstance(data, dict) or not isinstance(data.get("jobs"), list):
        return None, "degraded: Ashby response has no jobs list"
    rows = []
    for j in data.get("jobs", []):
        role = j.get("title", "")
        if not keep(display_name, role, False, strict_intern=True):
            continue
        loc = j.get("locationName") or j.get("location") or ""
        if j.get("isRemote") and "remote" not in str(loc).lower():
            loc = f"Remote - {loc}".strip(" -")
        url_ = j.get("jobUrl") or j.get("applyUrl") or ""
        description = strip_html(
            j.get("descriptionPlain")
            or j.get("descriptionHtml")
            or j.get("description")
            or ""
        )
        flags = derive_flags(description)
        inferred, explicit = term_from_evidence(role, term)
        rows.append(dict(company=display_name, role=role, location=str(loc),
                         url=safe_url(url_),
                         term=inferred, term_explicit=explicit,
                         flags=flags, deadline="", description=description))
    return rows, None


def parse_lever(slug, display_name, term):
    url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
    try:
        data = json.loads(fetch(url, timeout=15))
    except Exception as e:
        return None, str(e)
    if not isinstance(data, list):
        return None, "degraded: Lever response is not a list"
    rows = []
    for j in data:
        role = j.get("text", "")
        if not keep(display_name, role, False, strict_intern=True):
            continue
        loc = j.get("categories", {}).get("location", "")
        list_text = " ".join(
            f"{item.get('text', '')} {item.get('content', '')}"
            for group in j.get("lists", []) if isinstance(group, dict)
            for item in [group]
        )
        description = strip_html(
            (j.get("descriptionPlain") or j.get("description") or "")
            + " " + list_text
            + " " + (j.get("additionalPlain") or j.get("additional") or "")
        )
        flags = derive_flags(description)
        inferred, explicit = term_from_evidence(role, term)
        rows.append(dict(company=display_name, role=role, location=str(loc),
                         url=safe_url(j.get("hostedUrl", "")),
                         term=inferred, term_explicit=explicit,
                         flags=flags, deadline="", description=description))
    return rows, None


# ─────────────────────────────────────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
def _gather_legacy():
    merged = {}    # id -> record
    failed = []

    def add(r, source):
        rid = make_id(r["company"], r["role"], r["location"])
        if rid in merged:
            if source not in merged[rid]["sources"]:
                merged[rid]["sources"].append(source)
            if not merged[rid]["url"] and r.get("url"):
                merged[rid]["url"] = r["url"]
        else:
            flags = r.get("flags", [])
            merged[rid] = dict(
                id=rid,
                company=r["company"],
                role=r["role"],
                location=r["location"],
                region=region_of(r["location"]),
                url=r.get("url", ""),
                term=r.get("term", "Summer 2027"),
                deadline=r.get("deadline", ""),
                level=degree_level(r["role"]),
                role_type=role_type(r["role"]),
                citizenship="US only" if "US-CITIZEN-ONLY" in flags else "",
                sponsorship="no sponsorship" if "NO-SPONSORSHIP" in flags else "",
                sources=[source],
                flags=flags,
                elite_tier=tier_of(r["company"]),
            )

    # — GitHub repos —
    for src in GITHUB_SOURCES:
        try:
            text = fetch(src["url"])
        except Exception as e:
            failed.append((src["name"], str(e)))
            print(f"  {src['name']:<20} SKIP  {str(e)[:55]}", file=sys.stderr)
            continue
        if src["fmt"] == "html":
            rows = parse_html_table(text, src["term"])
        else:
            rows = parse_md_pipe(text, src["term"])
        for r in rows:
            add(r, src["name"])
        print(f"  {src['name']:<20} {len(rows):>4} roles")

    # — Greenhouse boards —
    gh_ok = gh_fail = 0
    for slug, name, term in GREENHOUSE_BOARDS:
        rows, err = parse_greenhouse(slug, name, term)
        if rows is None:
            gh_fail += 1
            failed.append((name, err))
        else:
            gh_ok += 1
            for r in rows:
                add(r, f"Greenhouse/{slug}")
    print(f"  Greenhouse          {gh_ok}/{gh_ok+gh_fail} boards OK, "
          f"{sum(1 for r in merged.values() if 'Greenhouse' in ','.join(r['sources']))} roles")

    # — Ashby boards —
    ash_ok = ash_fail = 0
    for slug, name, term in ASHBY_BOARDS:
        rows, err = parse_ashby(slug, name, term)
        if rows is None:
            ash_fail += 1
            failed.append((f"Ashby/{name}", err))
        else:
            ash_ok += 1
            for r in rows:
                add(r, f"Ashby/{slug}")
    print(f"  Ashby               {ash_ok}/{ash_ok+ash_fail} boards OK, "
          f"{sum(1 for r in merged.values() if 'Ashby' in ','.join(r['sources']))} roles")

    # — Lever boards —
    lev_ok = lev_fail = 0
    for slug, name, term in LEVER_BOARDS:
        rows, err = parse_lever(slug, name, term)
        if rows is None:
            lev_fail += 1
            failed.append((f"Lever/{name}", err))
        else:
            lev_ok += 1
            for r in rows:
                add(r, f"Lever/{slug}")
    print(f"  Lever               {lev_ok}/{lev_ok+lev_fail} boards OK, "
          f"{sum(1 for r in merged.values() if 'Lever' in ','.join(r['sources']))} roles")

    # — Curated elite watchlist (always present) —
    for (company, role, loc, url, tier) in ELITE_WATCHLIST:
        rid = make_id(company, role, loc)
        if rid not in merged:
            merged[rid] = dict(
                id=rid, company=company, role=role, location=loc,
                region=region_of(loc), url=url, term="Summer 2027",
                sources=["career_page"], flags=[], elite_tier=tier,
            )
        else:
            if "career_page" not in merged[rid]["sources"]:
                merged[rid]["sources"].append("career_page")

    # — Spring weeks —
    for (company, role, loc, url, deadline, tier) in SPRING_WEEKS:
        rid = make_id(company, role, loc)
        if rid not in merged:
            merged[rid] = dict(
                id=rid, company=company, role=role, location=loc,
                region=region_of(loc), url=url, term="Spring Week 2027",
                deadline=deadline,
                sources=["spring_weeks"], flags=[], elite_tier=tier,
            )

    return merged, failed


def previous_source_counts(existing):
    counts = {}
    for row in existing.values():
        if row.get("record_kind", "posting") != "posting":
            continue
        for source in filter(None, row.get("sources", "").split(",")):
            counts[source] = counts.get(source, 0) + 1
    return counts


def _location_quality(value):
    location = (value or "").strip()
    if not location:
        return -100
    generic = bool(
        re.fullmatch(
            r"(?i)(in[- ]office|onsite|hybrid|remote|"
            r".*(?:intern|fellowship|program|programme).*)",
            location,
        )
    )
    regions = regions_of(location)
    explicit = regions != ["Unknown"]
    return (40 if explicit else 0) + min(len(location), 80) - (50 if generic else 0)


def _url_quality(value):
    url = safe_url(value)
    if not url:
        return -100
    host = (urlsplit(url).hostname or "").lower()
    supported_ats = (
        "greenhouse.io" in host
        or host == "jobs.lever.co"
        or "ashbyhq.com" in host
    )
    return (100 if supported_ats else 0) + len(url)


def gather(existing=None):
    """Fetch listings and report per-source health.

    Reconciliation treats a valid empty response differently from a failed or
    malformed source, so a network incident cannot close every role.
    """
    merged, identities = {}, {}
    failed, health = [], {}
    old_counts = previous_source_counts(existing or {})

    def refresh(rec):
        text = f"{rec['role']} {rec.get('description', '')}"
        rec["flags"] = sorted(set(rec.get("flags", [])))
        # Dates in requirements often describe graduation eligibility rather
        # than the internship term, so term inference uses the title (or the
        # source-specific fallback) only.
        rec["term"] = infer_term(rec["role"], rec.get("term"))
        rec["level"] = degree_level(text, rec["flags"])
        rec["role_type"] = role_type(rec["role"])
        citizenship_requirements = []
        if "US-CITIZEN-ONLY" in rec["flags"]:
            citizenship_requirements.append("US citizenship required")
        if "US-PERSON-REQUIRED" in rec["flags"]:
            citizenship_requirements.append("US-person status required")
        if "PERMANENT-RESIDENT-REQUIRED" in rec["flags"]:
            citizenship_requirements.append("permanent residence required")
        rec["citizenship"] = (
            "; ".join(citizenship_requirements)
            if citizenship_requirements else "unknown"
        )
        rec["sponsorship"] = (
            "unavailable" if "NO-SPONSORSHIP" in rec["flags"] else "unknown"
        )
        # The public watcher has no private citizenship or permit facts. A
        # requirement is evidence to review, never proof that this user is blocked.
        if rec["sponsorship"] == "unavailable":
            rec["eligibility"] = "work-rights review"
        else:
            rec["eligibility"] = "review required"
        rec["category"] = category_of(
            rec["company"], rec["role"], rec.get("description", "")
        )
        rec["focus_tags"] = focus_tags(
            rec["company"], rec["role"], rec.get("description", "")
        )
        focus, company_type, equity = company_signals(
            rec["company"], rec.get("description", "")
        )
        rec["robotics_focus"] = focus
        rec["company_type"] = company_type
        rec["equity_signal"] = equity

    def add(r, source):
        url = safe_url(r.get("url", ""))
        semantic = "semantic:" + make_id(r["company"], r["role"], r["location"])
        identity = provider_job_key(url)
        if not identity:
            identity = ("url:" + canonical_url(url)) if url else semantic
        rid = identities.get(identity) or identities.get(semantic)
        if rid and rid in merged:
            rec = merged[rid]
            if source not in rec["sources"]:
                rec["sources"].append(source)
            rec["flags"] = sorted(set(rec["flags"]) | set(r.get("flags", [])))
            if _url_quality(url) > _url_quality(rec.get("url", "")):
                rec["url"] = url
            incoming_description = r.get("description", "")
            if len(incoming_description) > len(rec.get("description", "")):
                # Official ATS records carry the most authoritative employer
                # and title spelling, while location is selected independently.
                if source.startswith(("Greenhouse/", "Ashby/", "Lever/")):
                    rec["company"] = r["company"]
                    rec["role"] = r["role"]
                rec["description"] = r["description"]
            if _location_quality(r.get("location")) > _location_quality(
                rec.get("location")
            ):
                rec["location"] = r["location"]
                rec["region"] = region_of(r["location"])
                rec["work_mode"] = work_mode_of(r["location"])

            candidates = set(rec.get("_term_candidates", []))
            explicit_terms = set(rec.get("_explicit_terms", []))
            incoming_term = r.get("term") or "Unknown"
            if incoming_term != "Unknown":
                candidates.add(incoming_term)
            if r.get("term_explicit") and incoming_term != "Unknown":
                explicit_terms.add(incoming_term)
            rec["_term_candidates"] = sorted(candidates)
            rec["_explicit_terms"] = sorted(explicit_terms)
            selected_terms = explicit_terms or candidates
            rec["term"] = (
                next(iter(selected_terms))
                if len(selected_terms) == 1
                else "Ambiguous" if selected_terms
                else "Unknown"
            )
            refresh(rec)
            identities[identity] = rid
            identities[semantic] = rid
            identities[
                "semantic:" + make_id(
                    rec["company"], rec["role"], rec["location"]
                )
            ] = rid
            return

        rid = make_id(r["company"], r["role"], r["location"])
        if rid in merged:
            suffix = re.sub(r"[^a-z0-9]", "", identity)[-10:]
            rid = (rid[:53] + suffix)[:64]
        flags = sorted(set(r.get("flags", [])))
        rec = dict(
            id=rid, company=r["company"], role=r["role"],
            location=r["location"], region=region_of(r["location"]),
            work_mode=work_mode_of(r["location"]), url=url,
            term=r.get("term") or "Unknown",
            deadline=r.get("deadline", ""), sources=[source], flags=flags,
            elite_tier=tier_of(r["company"]),
            description=r.get("description", ""),
            _term_candidates=(
                [r.get("term")]
                if r.get("term") and r.get("term") != "Unknown" else []
            ),
            _explicit_terms=(
                [r.get("term")]
                if r.get("term_explicit") and r.get("term") != "Unknown" else []
            ),
            record_kind="posting", source_status="open",
        )
        refresh(rec)
        merged[rid] = rec
        identities[identity] = rid
        identities[semantic] = rid

    def mark_bad(source, label, error):
        state = "degraded" if str(error).startswith("degraded:") else "failed"
        health[source] = state
        failed.append((label, str(error)))

    for src in GITHUB_SOURCES:
        source = src["name"]
        try:
            text = fetch(src["url"])
        except Exception as e:
            mark_bad(source, source, e)
            print(f"  {source:<20} SKIP  {str(e)[:55]}", file=sys.stderr)
            continue
        if src["fmt"] == "html":
            has_table = "<tr" in text and "<td" in text
        elif src["fmt"] == "md_href":
            has_table = any(
                line.startswith("|") and ("href=" in line or "](" in line)
                for line in text.splitlines()
            )
        else:
            has_table = any(
                line.startswith("|") and "](" in line for line in text.splitlines()
            )
        if not has_table:
            mark_bad(source, source, "degraded: expected jobs table not found")
            continue
        rows = (parse_html_table(text, src["term"]) if src["fmt"] == "html"
                else parse_md_pipe(text, src["term"]))
        if not rows and old_counts.get(source, 0) >= 5:
            mark_bad(source, source, "degraded: parsed zero roles unexpectedly")
            continue
        health[source] = "ok"
        for r in rows:
            add(r, source)
        print(f"  {source:<20} {len(rows):>4} roles")

    def collect(boards, parser, provider):
        ok = bad = 0
        results = {}
        with ThreadPoolExecutor(max_workers=min(12, len(boards) or 1)) as pool:
            futures = {
                pool.submit(parser, slug, name, term): (slug, name)
                for slug, name, term in boards
            }
            for future in as_completed(futures):
                slug, name = futures[future]
                try:
                    results[slug] = (name, *future.result())
                except Exception as exc:
                    results[slug] = (name, None, str(exc))
        for slug, name, _term in boards:
            name, rows, err = results[slug]
            source = f"{provider}/{slug}"
            if rows is None:
                bad += 1
                mark_bad(source, f"{provider}/{name}", err)
                continue
            ok += 1
            health[source] = "ok"
            for r in rows:
                add(r, source)
        count = sum(
            1 for rec in merged.values()
            if any(s.startswith(provider + "/") for s in rec["sources"])
        )
        print(f"  {provider:<18} {ok}/{ok + bad} boards OK, {count} roles")

    collect(GREENHOUSE_BOARDS, parse_greenhouse, "Greenhouse")
    collect(ASHBY_BOARDS, parse_ashby, "Ashby")
    collect(LEVER_BOARDS, parse_lever, "Lever")

    def add_static(company, role, loc, url, tier, source, status,
                   deadline="", category=""):
        rid = make_id(company, role, loc)
        if rid in merged:
            return
        focus, company_type, equity = company_signals(company)
        merged[rid] = dict(
            id=rid, company=company, role=role, location=loc,
            region=region_of(loc), work_mode=work_mode_of(loc),
            url=safe_url(url),
            term="Watchlist" if status == "watchlist" else "Spring Week 2027",
            deadline=deadline, level="Unknown", role_type="watchlist",
            citizenship="unknown", sponsorship="unknown",
            eligibility="review required", sources=[source], flags=[],
            elite_tier=tier, category=category or category_of(company, role),
            focus_tags=focus_tags(company, role), robotics_focus=focus,
            company_type=company_type, equity_signal=equity,
            record_kind="watchlist", source_status=status, description="",
        )

    for company, role, loc, url, tier in ELITE_WATCHLIST:
        add_static(company, role, loc, url, tier, "career_page", "watchlist")
    for company, role, loc, url in ROBOTICS_WATCHLIST:
        add_static(company, role, loc, url, tier_of(company),
                   "robotics_watchlist", "watchlist",
                   category="Robotics & Embodied AI")
    for company, role, loc, url, tier in ACADEMIC_WATCHLIST:
        add_static(company, role, loc, url, tier, "academic_watchlist", "watchlist")
    for company, role, loc, url, deadline, tier in SPRING_WEEKS:
        add_static(company, role, loc, url, tier, "spring_weeks", "planned",
                   deadline=deadline)

    return merged, health, failed


def load_existing(path):
    if not os.path.exists(path):
        return {}
    with open(path, newline="", encoding="utf-8") as f:
        return {row["id"]: row for row in csv.DictReader(f) if row.get("id")}


def _prefer_existing(a, b):
    """Prefer the duplicate row containing user-maintained application data."""
    def score(row):
        return sum(bool(row.get(c)) for c in USER_COLS) * 10 + (
            row.get("source_status") in ("open", "stale/source-error")
        )
    return b if score(b) > score(a) else a


def reconcile(current, existing, source_health, today=TODAY):
    """Merge a fetch into stored rows without turning outages into closures."""
    by_identity, by_semantic = {}, {}
    identity_ids, semantic_ids = {}, {}
    for old in existing.values():
        old_id = old.get("id", "")
        identity = provider_job_key(old.get("url", ""))
        if identity:
            by_identity[identity] = _prefer_existing(
                by_identity.get(identity, old), old
            )
            identity_ids.setdefault(identity, set()).add(old_id)
        canon = canonical_url(old.get("url", ""))
        if canon:
            key = "url:" + canon
            by_identity[key] = _prefer_existing(by_identity.get(key, old), old)
            identity_ids.setdefault(key, set()).add(old_id)
        sem = make_id(old.get("company", ""), old.get("role", ""),
                      old.get("location", ""))
        by_semantic[sem] = _prefer_existing(by_semantic.get(sem, old), old)
        semantic_ids.setdefault(sem, set()).add(old_id)

    used_old, new_ids, rows_out = set(), [], []
    new_fields = {
        "work_mode": "unspecified", "category": "Software Engineering",
        "focus_tags": "", "robotics_focus": "", "company_type": "unknown",
        "equity_signal": "unknown", "eligibility": "review required",
        "record_kind": "posting", "missing_runs": "0",
        "last_healthy_miss": "", "new_on": "",
    }

    for rid, rec in current.items():
        identity = provider_job_key(rec.get("url", ""))
        canon = canonical_url(rec.get("url", ""))
        semantic = make_id(rec["company"], rec["role"], rec["location"])
        candidates = [
            existing.get(rid),
            by_identity.get(identity) if identity else None,
            by_identity.get("url:" + canon) if canon else None,
            by_semantic.get(semantic),
        ]
        matched_old_ids = set()
        if rid in existing:
            matched_old_ids.add(rid)
        if identity:
            matched_old_ids.update(identity_ids.get(identity, set()))
        if canon:
            matched_old_ids.update(identity_ids.get("url:" + canon, set()))
        matched_old_ids.update(semantic_ids.get(semantic, set()))
        prev = None
        for candidate in filter(None, candidates):
            prev = candidate if prev is None else _prefer_existing(prev, candidate)
        if prev:
            matched_old_ids.add(prev.get("id", ""))
            used_old.update(matched_old_ids)
            matched_old_rows = [
                existing[old_id]
                for old_id in matched_old_ids
                if old_id in existing
            ]
            seen_dates = sorted(
                row.get("first_seen", "")
                for row in matched_old_rows
                if row.get("first_seen")
            )
            first_seen = seen_dates[0] if seen_dates else today
            user = {c: prev.get(c, "") for c in USER_COLS}
            new_dates = {
                row.get("new_on", "")
                for row in matched_old_rows
                if row.get("new_on")
            }
            previous_new_on = today if today in new_dates else (
                sorted(new_dates)[-1] if new_dates else ""
            )
            legacy_new_today = (
                not previous_new_on
                and any(
                    row.get("NEW") == "YES"
                    and row.get("first_seen") == today
                    for row in matched_old_rows
                )
            )
            is_new = (
                (previous_new_on == today or legacy_new_today)
                and rec.get("record_kind") == "posting"
                and rec.get("source_status") == "open"
            )
            new_on = today if is_new else previous_new_on
            if is_new:
                new_ids.append(rid)
        else:
            first_seen = today
            user = {c: "" for c in USER_COLS}
            is_new = (
                rec.get("record_kind") == "posting"
                and rec.get("source_status") == "open"
            )
            new_on = today if is_new else ""
            if is_new:
                new_ids.append(rid)

        status = rec.get("source_status", "open")
        row = dict(
            id=rid, NEW="YES" if is_new else "",
            company=rec["company"], role=rec["role"],
            category=rec.get("category", ""),
            focus_tags=rec.get("focus_tags", ""),
            robotics_focus=rec.get("robotics_focus", ""),
            company_type=rec.get("company_type", "unknown"),
            equity_signal=rec.get("equity_signal", "unknown"),
            region=rec["region"], work_mode=rec.get("work_mode", "unspecified"),
            location=rec["location"], term=rec.get("term", "Unknown"),
            deadline=rec.get("deadline", ""), level=rec.get("level", "Unknown"),
            role_type=rec.get("role_type", ""),
            citizenship=rec.get("citizenship", "unknown"),
            sponsorship=rec.get("sponsorship", "unknown"),
            eligibility=rec.get("eligibility", "review required"),
            elite_tier=rec.get("elite_tier", ""),
            record_kind=rec.get("record_kind", "posting"),
            source_status=status,
            missing_runs="0",
            last_healthy_miss="",
            new_on=new_on,
            block=(
                "CITIZENSHIP REVIEW"
                if set(rec.get("flags", [])) & {
                    "US-CITIZEN-ONLY",
                    "US-PERSON-REQUIRED",
                    "PERMANENT-RESIDENT-REQUIRED",
                }
                else ""
            ),
            flags=",".join(rec.get("flags", [])),
            sources=",".join(rec.get("sources", [])),
            url=safe_url(rec.get("url", "")),
            first_seen=first_seen,
            last_seen=today if status == "open" else (prev or {}).get("last_seen", ""),
            **user,
        )
        rows_out.append(row)

    for old_id, prev_original in existing.items():
        if old_id in used_old:
            continue
        prev = dict(prev_original)
        if prev.get("record_kind", "posting") != "posting":
            # Static rows are regenerated from configuration. Dropped config rows
            # should disappear rather than linger as fake closed jobs.
            continue
        prior_sources = [s for s in prev.get("sources", "").split(",") if s]
        states = [source_health.get(s, "not-run") for s in prior_sources]
        healthy_absence = bool(states) and all(s == "ok" for s in states)
        try:
            misses = int(prev.get("missing_runs") or 0)
        except ValueError:
            misses = 0
        if healthy_absence:
            if (
                not prev.get("last_healthy_miss")
                and prev.get("source_status") == "stale/not-seen"
                and misses > 0
            ):
                # One-time migration for trackers written before this column
                # existed. Prefer delaying a closure over counting a same-day
                # manual rerun as a second independent miss.
                prev["last_healthy_miss"] = today
            if prev.get("last_healthy_miss", "") != today:
                misses += 1
                prev["last_healthy_miss"] = today
            prev["source_status"] = (
                "gone/closed?" if misses >= MISSING_RUNS_TO_CLOSE
                else "stale/not-seen"
            )
        else:
            prev["source_status"] = "stale/source-error"
        prev["missing_runs"] = str(misses)
        previous_new_on = prev.get("new_on", "")
        legacy_new_today = (
            not previous_new_on
            and prev.get("NEW") == "YES"
            and prev.get("first_seen") == today
        )
        is_new = previous_new_on == today or legacy_new_today
        prev["NEW"] = "YES" if is_new else ""
        if is_new:
            prev["new_on"] = today
            new_ids.append(old_id)
        for key, value in new_fields.items():
            prev.setdefault(key, value)
        flags = [flag for flag in prev.get("flags", "").split(",") if flag]
        requirements = []
        if "US-CITIZEN-ONLY" in flags:
            requirements.append("US citizenship required")
        if "US-PERSON-REQUIRED" in flags:
            requirements.append("US-person status required")
        if "PERMANENT-RESIDENT-REQUIRED" in flags:
            requirements.append("permanent residence required")
        prev["citizenship"] = "; ".join(requirements) if requirements else "unknown"
        prev["sponsorship"] = (
            "unavailable" if "NO-SPONSORSHIP" in flags else "unknown"
        )
        prev["eligibility"] = (
            "work-rights review"
            if prev["sponsorship"] == "unavailable"
            else "review required"
        )
        prev["block"] = "CITIZENSHIP REVIEW" if requirements else ""
        prev["region"] = region_of(prev.get("location", ""))
        prev["work_mode"] = work_mode_of(prev.get("location", ""))
        prev["category"] = category_of(
            prev.get("company", ""), prev.get("role", "")
        )
        prev["focus_tags"] = focus_tags(
            prev.get("company", ""), prev.get("role", "")
        )
        focus, company_type, equity = company_signals(prev.get("company", ""))
        prev["robotics_focus"] = focus
        prev["company_type"] = company_type
        prev["equity_signal"] = equity
        prev["level"] = degree_level(prev.get("role", ""), flags)
        prev["role_type"] = role_type(prev.get("role", ""))
        prev["elite_tier"] = tier_of(prev.get("company", ""))
        prev["url"] = safe_url(prev.get("url", ""))
        rows_out.append(prev)

    tier_rank = {"elite": 0, "high": 1, "": 2}
    status_rank = {"open": 0, "watchlist": 1, "planned": 2,
                   "stale/source-error": 3, "stale/not-seen": 4,
                   "gone/closed?": 5}
    rows_out.sort(key=lambda r: (
        r.get("NEW") != "YES",
        status_rank.get(r.get("source_status", ""), 9),
        tier_rank.get(r.get("elite_tier", ""), 2),
        r.get("company", ""),
        r.get("role", ""),
    ))
    return new_ids, rows_out


def write_manual_checks(failed):
    lines = [f"# Manual Check List — {TODAY}\n",
             "These are career hubs, not confirmed open jobs. Check the official page directly.\n",
             "Use the local cockpit or private autoapply database to record your "
             "decision; personal application history is not written to tracker.csv.\n\n"]

    lines.append("## Elite Manual Checks (own ATS — go straight to their intern page)\n")
    lines.append("| Company | Section | Location | Link |\n")
    lines.append("|---------|---------|----------|------|\n")
    for (company, role, loc, url, _tier) in ELITE_WATCHLIST:
        lines.append(f"| {company} | {role} | {loc} | [Open]({url}) |\n")

    lines.append("\n## Global Robotics Watchlist\n")
    lines.append("| Company | Focus | Location | Link |\n")
    lines.append("|---------|-------|----------|------|\n")
    for company, role, loc, url in ROBOTICS_WATCHLIST:
        lines.append(f"| {company} | {role} | {loc} | [Careers]({url}) |\n")

    lines.append("\n## Academic & Research Programmes\n")
    lines.append("| Organisation | Programme | Location | Link |\n")
    lines.append("|--------------|-----------|----------|------|\n")
    for company, role, loc, url, _tier in ACADEMIC_WATCHLIST:
        lines.append(f"| {company} | {role} | {loc} | [Apply]({url}) |\n")

    lines.append("\n## UK Spring Weeks (planned windows — verify before applying)\n")
    lines.append("| Company | Program | Location | Deadline | Link |\n")
    lines.append("|---------|---------|----------|----------|------|\n")
    for (company, role, loc, url, deadline, _tier) in SPRING_WEEKS:
        lines.append(f"| {company} | {role} | {loc} | {deadline} | [Apply]({url}) |\n")

    if failed:
        lines.append("\n## Sources that failed this run\n")
        lines.append("Roles previously seen only in these sources remain stale; they are not marked closed.\n\n")
        for name, err in failed:
            lines.append(f"- **{name}**: {err}\n")

    with open(MANUAL_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)


# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD  — the shareable README.md front page (regenerated every run)
# ─────────────────────────────────────────────────────────────────────────────
def _cell(s):
    """Make a string safe for a markdown table cell."""
    value = html.escape(str(s), quote=False).replace("\n", " ").strip()
    for character in ("\\", "|", "[", "]", "(", ")"):
        value = value.replace(character, "\\" + character)
    return value


def _role_row(r, cols=("company", "role", "region", "term")):
    url = safe_url(r.get("url", ""))
    company = _cell(r.get("company", ""))
    role = _cell(r.get("role", ""))
    if url:
        role = f"[{role}]({url})"
    flag = ""
    if r.get("block") == "CITIZENSHIP REVIEW":
        flag = " ⚠️"
    elif "NO-SPONSORSHIP" in r.get("flags", ""):
        flag = " 🛂"
    cells = {
        "company": f"**{company}**",
        "role": role + flag,
        "region": _cell(r.get("region", "")),
        "term": _cell(r.get("term", "")),
        "location": _cell(r.get("location", "")),
    }
    return "| " + " | ".join(cells[c] for c in cols) + " |"


def _build_dashboard_legacy(rows_out, new_ids, current):
    live = [r for r in rows_out if r.get("source_status") == "open"]
    elite = [r for r in live if r.get("elite_tier") == "elite"]
    high  = [r for r in live if r.get("elite_tier") == "high"]
    new_rows = [r for r in rows_out if r.get("NEW") == "YES"]
    spring = [r for r in live if r.get("term") == "Spring Week 2027"]

    from collections import Counter
    region_counts = Counter(r.get("region", "?") for r in live)

    L = []
    L.append("# 🎯 Universal Academic & Career Tracker — Internships · Research · PhD · New Grad\n")
    L.append(f"> **Auto-updated daily** by GitHub Actions · Last run: **{TODAY}** · "
             f"**{len(live)} live roles** tracked\n")
    L.append("\nCovers **Internships · Research Assistantships · PhD Fellowships · Postdocs · "
             "New Grad** across **SWE · AI/ML · Quant · Data · Security · Robotics · "
             "Hardware · Computational Science**. "
             "Scrapes community boards + Greenhouse, Ashby & Lever company APIs "
             "every day, merges + de-dupes, and flags what newly opened. "
             "Every role is **tagged, not filtered out** — sort/slice by region, "
             "degree level, citizenship, visa, term and role type in "
             "[tracker.csv](tracker.csv).\n")
    L.append("\n🚫 = US-citizen-only   🛂 = no visa sponsorship   "
             "🎓 = PhD/MSc-targeted (still listed, just tagged)\n")

    # Deadline computations
    dated = [(days_until(r.get("deadline", "")), r) for r in live]
    dated = [(d, r) for d, r in dated if d is not None]
    dated.sort(key=lambda x: x[0])
    urgent = [(d, r) for d, r in dated if 0 <= d <= URGENT_DAYS]
    windows = [r for r in live if r.get("deadline") and days_until(r.get("deadline")) is None]

    # At a glance
    L.append("\n## 📊 At a glance\n")
    L.append("| Metric | Count |\n|--------|------:|\n")
    L.append(f"| Total live roles | {len(live)} |\n")
    L.append(f"| 🏆 Elite tier | {len(elite)} |\n")
    L.append(f"| ⭐ High tier | {len(high)} |\n")
    L.append(f"| 🆕 New this run | {len(new_ids)} |\n")
    L.append(f"| ⏰ Closing ≤{URGENT_DAYS} days | {len(urgent)} |\n")
    reg_str = " · ".join(f"{k} {v}" for k, v in region_counts.most_common())
    L.append(f"\n**By region:** {reg_str}\n")
    lvl = Counter(r.get("level", "Any") for r in live)
    L.append(f"**By degree level:** " + " · ".join(f"{k} {v}" for k, v in lvl.most_common()) +
             "  _(Any = undergrad-friendly)_\n")
    typ = Counter(r.get("role_type", "") for r in live)
    L.append(f"**By type:** " + " · ".join(f"{k} {v}" for k, v in typ.most_common() if k) + "\n")
    us_only = sum(1 for r in live if r.get("citizenship") == "US only")
    L.append(f"**Citizenship:** {us_only} are US-citizen-only (tagged 🚫); the rest are open to you.\n")

    # Filter guide
    L.append("\n<details><summary>🔎 <b>How to filter this tracker</b></summary>\n\n")
    L.append("Open [tracker.csv](tracker.csv) in Google Sheets/Excel → Data → Create a filter. "
             "Useful columns:\n\n")
    L.append("- **`region`** — UK · US · Ireland · Netherlands · Canada · Remote · Global\n")
    L.append("- **`level`** — `Any` (undergrad-friendly) · `MSc` · `PhD`\n")
    L.append("- **`role_type`** — `intern` · `new-grad` · `placement` · `spring-week` · `graduate`\n")
    L.append("- **`citizenship`** — blank = open to you · `US only` = skip\n")
    L.append("- **`sponsorship`** — `no sponsorship` = needs work authorisation\n")
    L.append("- **`term`** — Summer 2027 · Summer 2026 · Spring Week 2027\n")
    L.append("- **`elite_tier`** — `elite` · `high`\n")
    L.append("- **`deadline`** — sort ascending to see what closes first\n")
    L.append("\n</details>\n")

    # ⏰ Closing within N days — the top-priority section
    L.append(f"\n## ⏰ Closing within {URGENT_DAYS} days\n")
    if urgent:
        L.append("**Apply to these first.**\n\n")
        L.append("| Days left | Deadline | Company | Role | Region |\n|--:|--|--|--|--|\n")
        for d, r in urgent:
            L.append(f"| **{d}** | {_cell(r.get('deadline',''))} | **{_cell(r['company'])}** | "
                     f"{_cell(r['role'])} | {_cell(r['region'])} |\n")
    else:
        L.append("_Nothing with a hard deadline inside the window right now._ "
                 "Most software/quant internships are **rolling** — the real deadline is "
                 "\"before they fill up,\" so apply to open elite roles ASAP. Dated deadlines "
                 "(spring weeks) appear here automatically as autumn approaches.\n")
    if windows:
        L.append("\n**Dated application windows** (verify exact date on the site):\n\n")
        L.append("| Company | Program | Window | Region |\n|--|--|--|--|\n")
        for r in sorted(windows, key=lambda r: r.get("company", "")):
            L.append(f"| **{_cell(r['company'])}** | {_cell(r['role'])} | "
                     f"{_cell(r.get('deadline',''))} | {_cell(r['region'])} |\n")

    # NEW roles
    if new_rows:
        elite_new = [r for r in new_rows if r.get("elite_tier") in ("elite", "high")]
        L.append(f"\n## 🆕 Newly opened ({len(new_rows)})\n")
        shown = elite_new if elite_new else new_rows
        L.append("| Company | Role | Region | Term |\n|--|--|--|--|\n")
        for r in shown[:40]:
            L.append(_role_row(r) + "\n")
        if len(shown) > 40:
            L.append(f"\n_…and {len(shown)-40} more — see [tracker.csv](tracker.csv)_\n")

    # Elite roles by region (collapsible)
    L.append(f"\n## 🏆 Elite roles — live & auto-scraped ({len(elite)})\n")
    by_region = {}
    for r in elite:
        by_region.setdefault(r.get("region", "Other"), []).append(r)
    order = ["UK", "US", "Netherlands", "Ireland", "Canada", "Remote", "Global", "Other"]
    for reg in sorted(by_region, key=lambda x: order.index(x) if x in order else 99):
        rs = sorted(by_region[reg], key=lambda r: r.get("company", ""))
        L.append(f"\n<details><summary><b>{reg}</b> — {len(rs)} roles</summary>\n\n")
        L.append("| Company | Role | Term |\n|--|--|--|\n")
        for r in rs:
            L.append(_role_row(r, cols=("company", "role", "term")) + "\n")
        L.append("\n</details>\n")

    # Spring weeks — urgent
    if spring:
        L.append("\n## 🇬🇧 UK Spring Weeks & Insight Days — APPLY OCT–NOV 2026\n")
        L.append("First-year/early insight programs that feed directly into summer offers. "
                 "**These deadlines come first — don't miss them.**\n\n")
        L.append("| Company | Program | Location | Link |\n|--|--|--|--|\n")
        for r in sorted(spring, key=lambda r: r.get("company", "")):
            url = r.get("url", "")
            link = f"[Apply]({url})" if url else ""
            L.append(f"| **{_cell(r['company'])}** | {_cell(r['role'])} | "
                     f"{_cell(r.get('location',''))} | {link} |\n")

    # High tier (collapsible, compact)
    if high:
        L.append(f"\n## ⭐ High-tier roles ({len(high)})\n")
        L.append("<details><summary>Show all</summary>\n\n")
        L.append("| Company | Role | Region | Term |\n|--|--|--|--|\n")
        for r in sorted(high, key=lambda r: (r.get("region",""), r.get("company",""))):
            L.append(_role_row(r) + "\n")
        L.append("\n</details>\n")

    # Manual-check elites
    L.append("\n## 📋 Elite companies — check these career pages directly\n")
    L.append("_These firms use private application systems that can't be auto-scraped. "
             "They're your highest-priority targets — check weekly._\n\n")
    L.append("| Company | Section | Location | Link |\n|--|--|--|--|\n")
    for (company, role, loc, url, _t) in ELITE_WATCHLIST:
        L.append(f"| **{_cell(company)}** | {_cell(role)} | {_cell(loc)} | [Open]({url}) |\n")

    # Footer
    L.append("\n---\n")
    L.append("\n## ⚙️ How this works\n")
    L.append("- A Python scraper (`internship_watcher.py`) runs **every morning via "
             "GitHub Actions** — no server, no computer needed.\n")
    L.append("- It pulls [SimplifyJobs](https://github.com/SimplifyJobs), "
             "[vanshb03](https://github.com/vanshb03/Summer2027-Internships), "
             "sndsh404, plus company job APIs directly: **Greenhouse** (Jump, IMC, "
             "Jane Street, Tower, Squarepoint, Anthropic…), **Ashby** (OpenAI, "
             "Perplexity, Cohere…) and **Lever** (Palantir, Spotify).\n")
    L.append("- Public discovery data lives in [tracker.csv](tracker.csv). "
             "Personal status stays in the local cockpit/database. Manual-check links in "
             "[manual_checks.md](manual_checks.md).\n")
    L.append("- Want your own copy? Fork this repo and enable Actions. "
             "Zero dependencies — Python stdlib only.\n")
    L.append("\n_Data is community-sourced; verify every posting before applying._\n")

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(L)


def build_dashboard(rows_out, new_ids, current):
    """Build an honest dashboard from verified postings and separate watchlists."""
    from collections import Counter

    live = [
        r for r in rows_out
        if r.get("record_kind", "posting") == "posting"
        and r.get("source_status") == "open"
    ]
    new_live = [r for r in live if r.get("NEW") == "YES"]
    robotics = [
        r for r in live if r.get("category") == "Robotics & Embodied AI"
    ]
    startup_robotics = [
        r for r in robotics
        if r.get("company_type") in (
            "emerging-startup", "startup", "private-scaleup"
        )
    ]
    elite = [r for r in live if r.get("elite_tier") == "elite"]
    high = [r for r in live if r.get("elite_tier") == "high"]
    planned = [r for r in rows_out if r.get("source_status") == "planned"]
    stale_error = [
        r for r in rows_out if r.get("source_status") == "stale/source-error"
    ]
    unknown_eligibility = sum(
        1 for r in live
        if r.get("eligibility") in ("review required", "work-rights review")
    )

    tier_rank = {"elite": 0, "high": 1, "": 2}

    def ranked(rows):
        return sorted(
            rows,
            key=lambda r: (
                tier_rank.get(r.get("elite_tier", ""), 2),
                r.get("company_type") != "emerging-startup",
                r.get("company", ""),
                r.get("role", ""),
            ),
        )

    def app_link(r):
        url = safe_url(r.get("url", ""))
        role = _cell(r.get("role", ""))
        return f"[{role}]({url})" if url else role

    def posting_table(lines, rows, limit=None, startup=False):
        shown = ranked(rows)
        if limit:
            shown = shown[:limit]
        if startup:
            lines.append("| Company | Role | Region | Focus | Company signal | Equity signal |\n")
            lines.append("|--|--|--|--|--|--|\n")
            for r in shown:
                lines.append(
                    f"| **{_cell(r['company'])}** | {app_link(r)} | "
                    f"{_cell(r.get('region', ''))} | "
                    f"{_cell(r.get('robotics_focus') or r.get('focus_tags', ''))} | "
                    f"{_cell(r.get('company_type', 'unknown'))} | "
                    f"{_cell(r.get('equity_signal', 'unknown'))} |\n"
                )
        else:
            lines.append("| Company | Role | Category | Region | Term | Eligibility |\n")
            lines.append("|--|--|--|--|--|--|\n")
            for r in shown:
                lines.append(
                    f"| **{_cell(r['company'])}** | {app_link(r)} | "
                    f"{_cell(r.get('category', ''))} | {_cell(r.get('region', ''))} | "
                    f"{_cell(r.get('term', 'Unknown'))} | "
                    f"{_cell(r.get('eligibility', 'review required'))} |\n"
                )

    regions = Counter(r.get("region", "Unknown") for r in live)
    categories = Counter(r.get("category", "Unknown") for r in live)
    levels = Counter(r.get("level", "Unknown") for r in live)
    urgent_pairs = []
    for row in live:
        days = days_until(row.get("deadline", ""))
        if days is not None and 0 <= days <= URGENT_DAYS:
            urgent_pairs.append((days, row))
    urgent_pairs.sort(key=lambda item: item[0])

    lines = [
        "# Internship + Robotics Opportunity Watcher\n",
        f"\n> Last verified run: **{TODAY}** · **{len(live)} verified-open postings** · "
        f"**{len(robotics)} robotics / embodied-AI postings**\n",
        "\nThis tracker watches community internship boards and official Greenhouse, "
        "Ashby, and Lever feeds. Career hubs and forecast programmes are kept "
        "separate from real postings. Unknown work-authorisation or sponsorship "
        "data means **review required**, never assumed eligible.\n",
        "\n## Filter jobs, generate a CV, then use Simplify\n",
        "\n[Open the filterable Role Radar dashboard]"
        "(https://abyyworld.github.io/internship-tracker/) for search, category, "
        "region, term, degree, company-type, robotics-startup, and CV-support filters.\n",
        "\nThe private helper is configured to start automatically on the owner's "
        "Mac. Double-click `start-autoapply.command` once to connect the browser, "
        "or run:\n",
        "\n```bash\ncd \"$HOME/Desktop/internship watcher\"\n"
        "./start-autoapply.command\n```\n",
        "\nEvery dashboard card has a native **⚡ Tailor CV + Apply** button; "
        "Tampermonkey is not required for the dashboard. It reads the live job page "
        "when possible, generates evidence-checked wording edits with the local "
        "Ollama model, downloads a job-specific PDF, and opens the employer "
        "application page where Simplify can autofill. If an employer blocks live "
        "page reading, the screen explicitly says that public tracker metadata was "
        "used as the fallback.\n",
        "\nThe GitHub repository never receives the private profile or fact bank. "
        "The CV is generated on `127.0.0.1`, remains a draft requiring review, and "
        "is never submitted by the bridge.\n",
    ]
    if stale_error:
        lines.append(
            f"\n> ⚠️ **{len(stale_error)} previously seen roles are stale because at "
            "least one source failed or was not checked. They were not marked closed.**\n"
        )

    lines.extend([
        "\n## At a glance\n",
        "\n| Metric | Count |\n|--|--:|\n",
        f"| Verified-open postings | {len(live)} |\n",
        f"| Roles discovered today | {len(new_ids)} |\n",
        f"| New verified postings | {len(new_live)} |\n",
        f"| Robotics / embodied AI | {len(robotics)} |\n",
        f"| Robotics at private startups / scaleups | {len(startup_robotics)} |\n",
        f"| Elite tier | {len(elite)} |\n",
        f"| High tier | {len(high)} |\n",
        f"| Eligibility still needs review | {unknown_eligibility} |\n",
        f"| Deadlines within {URGENT_DAYS} days | {len(urgent_pairs)} |\n",
        "\n**By category:** " + " · ".join(
            f"{k} {v}" for k, v in categories.most_common()
        ) + "\n",
        "\n**By region:** " + " · ".join(
            f"{k} {v}" for k, v in regions.most_common()
        ) + "\n",
        "\n**By degree evidence:** " + " · ".join(
            f"{k} {v}" for k, v in levels.most_common()
        ) + "\n",
    ])

    if new_live:
        lines.append(f"\n## Newly opened ({len(new_live)})\n\n")
        posting_table(lines, new_live, limit=60)
        if len(new_live) > 60:
            lines.append(
                f"\n_{len(new_live) - 60} more are in [tracker.csv](tracker.csv)._\n"
            )

    lines.append(f"\n## Robotics & embodied AI ({len(robotics)} live)\n\n")
    lines.append(
        "Includes directly robotics-focused work and technical roles at robotics "
        "companies: robot learning, perception, autonomy, controls, manipulation, "
        "firmware, mechatronics, and field robotics. Live geography reflects what "
        "official feeds expose today; the worldwide career-hub watchlist is kept "
        "separately in [manual_checks.md](manual_checks.md).\n\n"
    )
    if robotics:
        posting_table(lines, robotics, limit=100, startup=True)
        if len(robotics) > 100:
            lines.append(
                f"\n_{len(robotics) - 100} more are in [tracker.csv](tracker.csv)._\n"
            )
    else:
        lines.append("_No matching verified posting is live in this run._\n")

    lines.append("\n### Early-company / equity reality check\n\n")
    lines.append(
        "The company signal is a discovery aid, not a prediction. Private-company "
        "options can become valuable, but can also expire, dilute, remain illiquid, "
        "or end up worth zero. `private company; verify offer` means the posting "
        "does not prove that equity is included. Ask for the option count **and fully "
        "diluted percentage**, strike price, vesting/cliff, exercise window, latest "
        "common valuation, and liquidation preferences.\n"
    )

    if urgent_pairs:
        lines.append(f"\n## Closing within {URGENT_DAYS} days\n\n")
        lines.append("| Days | Deadline | Company | Role | Region |\n|--:|--|--|--|--|\n")
        for days, r in urgent_pairs:
            lines.append(
                f"| {days} | {_cell(r.get('deadline', ''))} | "
                f"**{_cell(r['company'])}** | {app_link(r)} | "
                f"{_cell(r.get('region', ''))} |\n"
            )

    if elite or high:
        lines.append(f"\n## Elite and high-tier live postings ({len(elite) + len(high)})\n\n")
        posting_table(lines, elite + high, limit=100)
        if len(elite) + len(high) > 100:
            lines.append(
                f"\n_{len(elite) + len(high) - 100} more are in "
                "[tracker.csv](tracker.csv)._\n"
            )

    if planned:
        lines.append("\n## Planned spring / insight programmes\n\n")
        lines.append(
            "These are expected programme windows, not verified-open applications.\n\n"
        )
        lines.append("| Company | Programme | Window | Link |\n|--|--|--|--|\n")
        for r in sorted(planned, key=lambda x: x.get("company", "")):
            url = safe_url(r.get("url", ""))
            link = f"[Check official page]({url})" if url else ""
            lines.append(
                f"| **{_cell(r['company'])}** | {_cell(r['role'])} | "
                f"{_cell(r.get('deadline', ''))} | {link} |\n"
            )

    lines.extend([
        "\n## Filtering and application workflow\n",
        "\nOpen [tracker.csv](tracker.csv) in a spreadsheet. Useful columns include "
        "`category`, `focus_tags`, `company_type`, `region`, `work_mode`, `term`, "
        "`level`, `eligibility`, `source_status`, and `equity_signal`.\n",
        "\n- `source_status=open` means the individual posting was returned by a live source.\n",
        "- `watchlist` or `planned` is a career hub, not proof of an opening.\n",
        "- `stale/source-error` is protected during an outage; it is not closed.\n",
        "- A role closes only after two consecutive healthy runs do not see it.\n",
        "- Run `python3 copilot.py` for local triage, or `python3 -m autoapply doctor` "
        "for the guarded local application pipeline.\n",
        "\nSee [manual_checks.md](manual_checks.md) for official robotics and elite "
        "career pages that need a browser check.\n",
        "\n---\n",
        "\nThe watcher is free and uses public job feeds. Always verify the posting and "
        "every application answer before approval.\n",
    ])

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(lines)


def write_new_digest(rows_out, new_ids):
    """Write today's discovery history, including outage-protected postings."""
    if not new_ids:
        return
    records_by_id = {row["id"]: row for row in rows_out}
    stale_count = sum(
        records_by_id[rid].get("source_status") != "open" for rid in new_ids
    )
    fn = f"new_roles_{TODAY}.md"
    with open(fn, "w", encoding="utf-8") as f:
        f.write(f"# {len(new_ids)} roles discovered — {TODAY}\n\n")
        if stale_count:
            f.write(
                f"> {stale_count} role(s) were verified earlier today but their "
                "source later failed. They remain in this discovery history and "
                "are not treated as currently verified-open.\n\n"
            )
        for rid in sorted(
            new_ids,
            key=lambda x: (
                records_by_id[x].get("category") != "Robotics & Embodied AI",
                records_by_id[x].get("elite_tier") not in ("elite", "high"),
                records_by_id[x].get("company", ""),
            ),
        ):
            rec = records_by_id[rid]
            company = _cell(rec.get("company", ""))
            role = _cell(rec.get("role", ""))
            category = _cell(rec.get("category", ""))
            region = _cell(rec.get("region", ""))
            term = _cell(rec.get("term", ""))
            tier = (
                f" **[{rec['elite_tier'].upper()}]**"
                if rec.get("elite_tier") else ""
            )
            blocked = (
                " _(US citizen only — blocked)_"
                if "US-CITIZEN-ONLY" in rec.get("flags", "") else ""
            )
            stale = (
                f" _(source status: {rec.get('source_status')})_"
                if rec.get("source_status") != "open" else ""
            )
            f.write(
                f"- **{company}**{tier} — {role} "
                f"[{category}; {region}; {term}]{blocked}{stale}\n"
                f"  {rec['url']}\n"
            )


def run():
    print(f"\ninternship watcher v3 — {TODAY}")
    print("=" * 56)

    existing = load_existing(TRACKER_FILE)
    current, source_health, failed = gather(existing)
    new_ids, rows_out = reconcile(current, existing, source_health)
    records_by_id = {row["id"]: row for row in rows_out}

    fields = [
        "NEW", "company", "role", "category", "focus_tags",
        "robotics_focus", "company_type", "equity_signal",
        "region", "work_mode", "location", "term", "deadline", "level",
        "role_type", "citizenship", "sponsorship", "eligibility",
        "elite_tier", "record_kind", "source_status", "missing_runs",
        "last_healthy_miss", "new_on", "block", "flags", "sources", "url",
        "first_seen", "last_seen",
        "id",
    ]

    with open(TRACKER_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
        )
        w.writeheader()
        for r in rows_out:
            w.writerow({
                field: spreadsheet_safe(r.get(field, ""))
                for field in fields
            })

    write_new_digest(rows_out, new_ids)

    write_manual_checks(failed)
    build_dashboard(rows_out, new_ids, records_by_id)

    # Summary
    live = [r for r in rows_out if r.get("source_status") == "open"]
    total_elite = sum(1 for r in live if r.get("elite_tier") == "elite")
    total_high = sum(1 for r in live if r.get("elite_tier") == "high")
    robotics = sum(
        1 for r in live if r.get("category") == "Robotics & Embodied AI"
    )
    print(f"\n  tracked roles       : {len(rows_out)}")
    print(f"  verified open       : {len(live)}")
    print(f"  robotics / embodied : {robotics}")
    print(f"  elite tier          : {total_elite}")
    print(f"  high tier           : {total_high}")
    print(f"  discovered today    : {len(new_ids)}")

    elite_new = [rid for rid in new_ids if records_by_id[rid].get("elite_tier")]
    if elite_new:
        print(f"\n  NEW elite/high roles ({len(elite_new)}):")
        for rid in elite_new[:15]:
            rec = records_by_id[rid]
            print(f"    [{rec['elite_tier'].upper():5}] {rec['company']} — {rec['role'][:55]} [{rec['region']}]")
    if new_ids and not elite_new:
        print(f"\n  sample new roles:")
        for rid in new_ids[:8]:
            rec = records_by_id[rid]
            print(f"    {rec['company']} — {rec['role'][:60]} [{rec['region']}]")

    print(f"\n  tracker  -> {TRACKER_FILE}")
    print(f"  manual   -> {MANUAL_FILE}")
    if new_ids:
        print(f"  new digest -> new_roles_{TODAY}.md")
    print()


if __name__ == "__main__":
    run()
