# Setup and Safe Local Workflow

The watcher, cockpit, PDF editor, and guarded application assistant run locally.
The watcher itself uses the Python standard library. The application assistant
uses free Python packages and an installed copy of Microsoft Edge, and requires
Python 3.11 or newer. AI CV suggestions use your own account with whichever
OpenAI-compatible provider you select in the editor; browsing, manual editing,
accepting/rejecting prior suggestions, PDF export, and the job tracker do not
consume API credits.

The system deliberately separates discovery from submission:

1. The watcher discovers and classifies postings.
2. The cockpit helps you triage them.
3. The local assistant prepares a CV and inspects the real form.
4. You review every application fact and unresolved question.
5. A one-time approval authorises one final submit click for one unchanged form.

There is no unattended bulk-submit mode. Unknown legal, eligibility, consent, or
demographic answers remain unresolved.

## 1. Create the local environment

From the repository directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-autoapply.txt
```

The guarded browser workflow currently expects Microsoft Edge to be installed.

No local model download is required for the AI CV Studio. The first time an
editor opens, choose a provider in the right panel — OpenAI, Groq, OpenRouter,
Cerebras, Together, GitHub Models, Google AI Studio, or a model running on this
machine under Ollama, which needs no key at all — and paste that provider's key
into the key card below it. The bridge stores each provider's key in its own
file (`private/openai.key`, `private/gemini.key`, and so on) with mode 0600, and
never exposes it to the public dashboard or browser URL. Switching provider
therefore asks for the new provider's key rather than sending the previous one
to an account that never issued it. A key left in the environment under the
provider's own variable (`OPENAI_API_KEY`, `GEMINI_API_KEY`, `GROQ_API_KEY`, …)
is used when no file is saved, which is what a headless run reads. Pressing
**Generate suggestions** sends the job description and master CV text to the
chosen provider through that account; opening the editor and exporting locally
do not call the API.

**Test this provider** in the editor sends one 24-token request and reports
exactly what came back: the endpoint, the model, the status, the provider's own
words, any request parameters that endpoint refused, and the models it says it
can run. Use it before blaming a rewrite — a rejected key and a working one look
identical until something asks. The same check runs from the terminal with
`python3 -m autoapply doctor --probe`, which also prints the endpoint, model and
where the key is being read from.

### When a fix does not seem to arrive

The helper is started once and left running for weeks. The checkout moves on, a
macOS login service quietly respawns the old process, and the editor keeps being
answered by code that is no longer on disk — so a fix that is pushed, pulled and
tested still does not reach the browser. `update-autoapply.command` does every
step of that in one go and says which build ends up serving:

```bash
./update-autoapply.command                 # update the current branch
./update-autoapply.command some-branch     # switch to that branch first
```

It reports the build answering right now, parks local changes with `git stash`
(never discards them), fast-forwards, stops the bridge *including a login
service that would otherwise restart the old copy*, and starts the helper from
this folder. To check which code is serving without changing anything:

```bash
curl -s -H "X-Autoapply-Token: $(cat private/bridge.token)" \
  http://127.0.0.1:8765/health
```

A reply with no `"build"` field is a helper from before August 2026.

The editor's right-hand column ends with the bridge **build** — the timestamp of
the code answering the page. A bridge is started once and left running for weeks
while the checkout moves on, so a symptom can belong to a version no longer on
disk; `start-autoapply.command` now compares the running build with the working
copy and restarts a stale helper instead of reusing it.

The daily watcher and cockpit do not require the extra packages:

```bash
python3 internship_watcher.py
python3 copilot.py
open apply_cockpit.html
```

`apply_cockpit.html` is generated locally and ignored by Git.

Venture programmes are a curated dataset rather than a scrape, in `data/ventures.json`,
and can be listed from the terminal for a particular person:

```bash
python3 ventures.py --audience phd --region GB
python3 ventures.py --audience students --stage idea
```

The rules for that dataset are the same as for funding: cheque sizes and equity
only where the programme publishes them, no cohort dates (they move every year),
and every entry links to the page that governs it. `tests/test_ventures.py`
enforces those rules, including a check that no cycle string contains a year.

### Checking the editor itself

The unit suite runs with no browser and no network:

```bash
python3 -m unittest discover -s tests -t .
```

The editor page is a single-page application, so its own behaviour is checked by
driving it in a real browser against a fake OpenAI-compatible provider — opening
the editor, testing the provider, generating a rewrite, accepting it, exporting
the PDF, drafting the answers, and saving the tailoring as its own CV:

```bash
python3 tests/browser_editor_flow.py
```

It is deliberately not collected by `unittest discover`, because it needs a
browser the read-only CI job does not have.

## GitHub click-to-tailor workflow

This is the fastest workflow when Simplify is already installed:

1. Double-click `start-autoapply.command` in the project folder. It connects the
   browser to the private local helper and opens the dashboard.
2. Open the filterable dashboard later at:

   ```bash
   open https://abyyworld.github.io/internship-tracker/
   ```

3. Double-clicking `start-autoapply.command` installs the helper as a macOS
   login service and starts it: it then comes back at every login, restarts
   itself if it stops, and needs no window kept open — closing the window that
   installed it changes nothing. Double-click it again after moving the project
   folder, and it re-points at the new location. `--window` runs a one-off
   helper in a window instead, which dies with the window.
4. Search or filter jobs on the dashboard and click
   **✦ Edit CV for this job** beside any role.

If you deliberately want to start it in Terminal, first change to the repository
directory. Running `.venv/bin/activate` from `~` will fail because `.venv` is inside
the project:

```bash
cd "$HOME/Desktop/other projects/internship watcher"
./start-autoapply.command
```

The localhost bridge imports every open HTTPS role in the current tracker. The
editor immediately displays the complete master CV without spending API credits.
Press **Generate suggestions** to fetch the current job description and ask the
configured provider for a small patch set. Accept, reject, or directly edit each proposal,
then press **Export accepted PDF**. Simplify can autofill the employer form;
choose the newly downloaded PDF as the resume and review the whole application.

### Tailoring for a posting the tracker has never seen

The watcher follows a few hundred boards, and the job you actually want is
routinely on none of them — a company careers page, a lab's own site, a link
from a friend. Install `tailor-anywhere.user.js` in Tampermonkey and a small
**✦ Tailor my CV** button appears on any page that reads like a job advert
(always available from the Tampermonkey menu, whatever the page). It reads the
posting — schema.org JobPosting where the site publishes it, the densest block
of advert prose otherwise — hands it to the helper on `127.0.0.1`, and opens the
same editor for it. The page text goes to the local helper and nowhere else.

The bridge does not control or impersonate Simplify, fill legal answers, or click
Submit. The optional Tampermonkey userscript still enhances links in the GitHub
README, but the dashboard's native CV button does not depend on Tampermonkey.

### What the local AI is allowed to edit

The model can propose rephrasing a few bullets and the summary for the job. Every
suggestion remains linked to an original private fact ID. Generated wording is
rejected when it adds a new number, named technology/entity, unsupported
qualification, or loses too much evidence overlap. The master document cannot be
shortened: pending and rejected patches use their exact original text, and every
master entry remains in the export. Private per-job drafts preserve review status.

This is a draft-generation accelerator, not proof that every sentence is correct.
Read the downloaded PDF before attaching it. The application approval gate remains
separate from CV generation.

## 2. Create the private profile

The default private-data directory is `private/` inside the repository. It is
gitignored. You may instead set `AUTOAPPLY_HOME` to another private directory.

```bash
mkdir -p private
cp config/profile.example.yaml private/profile.yaml
cp config/resume_facts.example.yaml private/resume_facts.yaml
chmod 700 private
chmod 600 private/profile.yaml private/resume_facts.yaml
```

Replace every `REPLACE_ME` value before running the assistant. `doctor` rejects
unfinished examples.

```bash
python -m autoapply doctor
```

### Facts you must confirm yourself

In `profile.yaml`, verify:

- Legal and preferred names.
- Email, phone number, phone country code, current location, and profile links.
- Institution, exact degree, field of study, degree level, and graduation date.
- Each citizenship using an ISO country code.
- Work authorisation separately for every relevant country.
- Whether that authorisation is `unrestricted`, `limited`, `program_specific`,
  or `unknown`.
- Whether sponsorship is required now or in the future in each country.
- Your EEO preference: manual, or decline only when one exact decline option exists.

Do not infer citizenship from residence, work authorisation from citizenship, or
sponsorship from a job location. Leave uncertain values as `unknown`; the assistant
will stop on them.

Visa-limited permission is not the same as unrestricted work authorisation. Record
the visa under `visa_status`, put the practical restriction in `limitations`, and
use:

- `limited` for permission restricted by hours, term dates, employer, occupation,
  or another condition.
- `program_specific` when work is allowed only within an approved programme or
  sponsor document.
- `unrestricted` only when you personally verified that the permission is not
  restricted for the job being considered.

For `limited` and `program_specific` profiles, the assistant may prepare and inspect
an application but will not auto-answer a broad work-authorisation question. The
exact job, form, hours, dates, and visa conditions must be reviewed first.

Official references: the US State Department says J-1 work is limited to the
activity on Form DS-2019 and the exchange category, with sponsor approval for work
outside the programme sponsor. UK Student rules generally limit eligible
degree-level students to their stated term-time hours and allow full-time work only
in permitted vacation periods; an eligible course placement must be integral and
assessed. Always verify the conditions shown on your own DS-2019, eVisa, and
university term/placement documents:

- https://j1visa.state.gov/participants/common-questions/
- https://www.gov.uk/guidance/immigration-rules/immigration-rules-appendix-student
- https://www.gov.uk/government/publications/right-to-work-checks-employers-guide/

`reviewed_answers` is for a required question you personally checked on a specific
job and form revision. Construct its key from the `form_hash`, `field_key`, and
exact `prompt` emitted by `inspect`, confirm the answer, then inspect again:

```yaml
reviewed_answers:
  exact-job-id:
    "exact-form-hash :: exact-field-key :: Exact prompt?": "Exact answer"
```

Never reuse an answer across jobs or form revisions, or by fuzzy prompt matching.

Country-specific work-authorisation and sponsorship choices are filled only from
the values you explicitly confirmed above. The following stay manual unless an
exact, job-bound reviewed answer is configured:

- Citizenship, export-control, and security-clearance questions.
- Legal declarations, consent, signatures, salary, and criminal-history questions.
- Disability, veteran, race/ethnicity, gender, and other protected EEO fields.
- Any unfamiliar custom question.

In `resume_facts.yaml`, include only evidence-backed facts. The local tailor selects
and reorders those facts for a role; it must not invent employers, dates, skills,
metrics, qualifications, or achievements. If no verified fact is relevant to the
role, `prepare` refuses to generate a CV until you add and review truthful evidence.

Never commit the completed YAML files, generated CVs, screenshots, browser profile,
or SQLite database.

## 3. Discover and import jobs

Refresh the tracker, then import supported postings into the private local database:

```bash
python3 internship_watcher.py
python -m autoapply import-tracker --tracker tracker.csv
python -m autoapply status
```

Use a job ID shown by `status` or the `id` column in `tracker.csv`.

Only open postings on supported Greenhouse, Lever, and Ashby hosts are eligible for
browser automation. Career hubs, stale rows, unsupported hosts, and unsafe URLs are
not submission targets.

## 4. Prepare, inspect, and fill without submitting

Set a job ID for the commands below:

```bash
JOB_ID="paste-the-exact-job-id-here"
python -m autoapply prepare "$JOB_ID"
python -m autoapply inspect "$JOB_ID" --headed
```

`prepare` fetches the public job description when available, checks eligibility,
and creates a role-specific PDF from the private fact bank. Review that PDF.

`inspect` opens the real form and produces a dry-run fill plan. It does not enter
answers or click Submit. Review:

- The company, role, location, and application URL.
- The complete job description and graduation/degree requirements.
- Work authorisation, sponsorship, citizenship, and export-control requirements.
- Every planned value and its profile source.
- The tailored CV, selected facts, and file hash.
- Every unresolved required field.

Personal planned values are redacted from terminal output by default. If you need
to inspect them in a private terminal, add `--show-values`; do not copy that output
into logs, issues, or chat.

Add only personally verified answers to the private profile, then rerun `inspect`.
When the plan is correct, the optional fill step can populate the form while leaving
submission untouched:

```bash
python -m autoapply fill "$JOB_ID" --headed --execute
```

Review the visible form and the saved screenshot. CAPTCHA challenges are not solved
or bypassed by the assistant.

## 5. Approve and submit once

Approval is deliberately separate:

```bash
python -m autoapply approve "$JOB_ID"
```

This succeeds only when eligibility is explicitly confirmed, the description is
still available, and the stored plan has no unresolved required fields or active
CAPTCHA. It writes a mode-0600 approval token file under the private data directory.
The token is bound to that exact job, application URL, form, answers, eligibility
facts, CV, initial field values, and exact visible submit control, and expires after
24 hours.

After one final review:

```bash
python -m autoapply submit "$JOB_ID"
```

Submission always runs in a visible Edge window; headless submission is prohibited.
Before the click, it rechecks the posting, form, answers, CV hash, browser validation,
and approval, then compares two post-fill snapshots for stable fields, values, URL,
and submit control. New conditional questions, changed or unobservable values, and
prefilled answers that were never approved all stop the click. If anything changed,
approval is rejected and you must inspect and approve again.

The private token file is consumed for the one click and removed after use or
expiry. It is never placed in shell history. An ambiguous browser response is
recorded as `unknown_outcome` and is never retried automatically; check the employer
portal or confirmation email yourself.

## Categories and position types

The dashboard has two filter rows:

**Category chips** (green) — AI / ML, Software Engineering, Quant / Finance,
Robotics & Embodied AI, Security, Data, Systems & Infra, Hardware / EE, HCI / XR,
Computational Science.

**Position type chips** (purple) — Internship, Co-op, Research Assistant,
New Grad, PhD Fellowship, Postdoc, Masters Research.

Academic sources (NSF REU, NIH, NASA, DOE, CERN, ESA, Turing Institute,
EURAXESS, jobs.ac.uk) feed the Research Assistant, PhD Fellowship, Postdoc,
and Masters Research chips.

Useful tracker columns are:

- `category` for the technical area.
- `role_type` for position type (intern, co-op, research-assistant, phd-fellowship, postdoc, new-grad).
- `company_type` for emerging startup, startup, private scaleup, established, or public.
- `region` and `work_mode` for geography.
- `equity_signal` as a reminder to verify the actual offer.

A company being private does not guarantee that an intern will receive equity,
that the equity will have value, or that the role fits your visa status. Verify
compensation, vesting, strike price, dilution, tax treatment, and work
authorisation before accepting any offer.

## Legacy basic userscript

`autofill.user.js` is a generic legacy template for basic contact and education text
fields. It contains no personal data and intentionally does not fill dropdowns,
radio buttons, checkboxes, work-authorisation, sponsorship, citizenship, legal, or
EEO answers.

To use it:

```bash
cp autofill.user.js autofill.local.user.js
```

Edit only the private `autofill.local.user.js`, install that copy in Tampermonkey,
and review every populated field. It cannot attach a CV or submit an application.
The local guarded assistant is preferred for supported ATS sites.

## Free daily watcher on GitHub

The tracked `.github/workflows/watch.yml` runs the discovery watcher on GitHub
Actions and commits generated tracker updates. For a personal repository:

1. Push the repository to GitHub.
2. Enable Actions and grant the workflow read/write contents permission.
3. Run “Daily internship watch” manually once.
4. Confirm that its generated commit contains only expected public tracker files.

Keep private profiles and application artifacts local. The GitHub workflow discovers
jobs; it must not receive personal application data or submit applications.

## Tests

Run the offline regression suite before changing watcher or application logic:

```bash
python3 -m unittest discover -s tests -v
```

Network-backed employer forms change frequently. Always perform a headed dry run and
manual review for the exact live form before creating approval.
