# Setup and Safe Local Workflow

The watcher, cockpit, CV tailoring, and guarded application assistant can all run
locally without a paid service or API key. The watcher itself uses the Python
standard library. The application assistant uses free Python packages and an
installed copy of Microsoft Edge, and requires Python 3.11 or newer.
“Free” here means no software subscription or paid API is required; your normal
computer, internet, and any GitHub Actions quota still apply.

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

The daily watcher and cockpit do not require the extra packages:

```bash
python3 internship_watcher.py
python3 copilot.py
open apply_cockpit.html
```

`apply_cockpit.html` is generated locally and ignored by Git.

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
- Whether sponsorship is required now or in the future in each country.
- Your EEO preference: manual, or decline only when one exact decline option exists.

Do not infer citizenship from residence, work authorisation from citizenship, or
sponsorship from a job location. Leave uncertain values as `unknown`; the assistant
will stop on them.

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

## Worldwide robotics and emerging startups

The watcher has a dedicated `Robotics & Embodied AI` category spanning official
global ATS boards and a manual worldwide watchlist. It covers areas such as:

- Humanoid and general-purpose robotics.
- Robot learning, embodied AI, perception, planning, and autonomy.
- Industrial, warehouse, construction, agricultural, medical, and field robotics.
- Autonomous vehicles, drones, delivery systems, mechatronics, controls, and firmware.

Useful tracker columns are:

- `category` and `robotics_focus` for the technical area.
- `company_type` for emerging startup, startup, private scaleup, established, or public.
- `region` and `work_mode` for geography.
- `equity_signal` as a reminder to verify the actual offer.

Filter `category = Robotics & Embodied AI`, then prioritise
`company_type = emerging-startup`, `startup`, or `private-scaleup` if early-stage
companies are your goal. A company being private does not guarantee that an intern
will receive equity, that the equity will have value, or that the role fits your visa
status. Verify compensation, vesting, strike price, dilution, tax treatment, and
work authorisation before accepting any offer.

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
