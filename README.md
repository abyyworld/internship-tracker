# 🎯 Universal Academic & Career Tracker — Internships · Research · PhD · New Grad

<p align="center">
  <a href="https://abyyworld.github.io/internship-tracker/"><img alt="Open the tracker — 4408 open postings" src="https://img.shields.io/badge/Open%20the%20tracker-4408%20open%20postings-1f6feb?style=for-the-badge&labelColor=0d1117"></a>
  <a href="https://abyyworld.github.io/internship-tracker/studio.html"><img alt="Tailor my CV — in the browser" src="https://img.shields.io/badge/Tailor%20my%20CV-in%20the%20browser-2ea043?style=for-the-badge&labelColor=0d1117"></a>
</p>

<p align="center"><b><a href="https://abyyworld.github.io/internship-tracker/">https://abyyworld.github.io/internship-tracker/</a></b><br>
Search and filter every posting, then tailor your CV for one — in the browser, on a phone, with nothing to install.</p>

> Last verified run: **2026-11-23** · **4408 verified-open postings** · **143 research / PhD / postdoc positions**

This tracker watches community internship boards and official Greenhouse, Ashby, and Lever feeds. Career hubs and forecast programmes are kept separate from real postings. Unknown work-authorisation or sponsorship data means **review required**, never assumed eligible.

## Filter jobs, generate a CV, then use Simplify

Say what you are looking for — “fully funded robotics PhD in the UK”, “summer 2027 internship that sponsors” — and [the tracker](https://abyyworld.github.io/internship-tracker/) matches it against every internship, new-grad role, PhD and research post, accelerator, scholarship and university it knows about, and says on each card which part of what you asked for it answers. Filters are there too, in light or dark.

The CV editor comes in two forms and the dashboard picks between them for you. [CV Studio in the browser](https://abyyworld.github.io/internship-tracker/studio.html) needs nothing installed: your CV, your API key and your edits stay in that browser, and the rewrite request goes straight from the page to the model provider you choose. Every **Edit CV for this job** button lands there by itself when no local helper is running, so it never leads to a dead end.

It keeps every CV you send — a robotics one, a research one — and each posting remembers which of them it was tailored from. Drop in a PDF or a Word file and it is read here, set as A4 at true size, and exported as a real PDF written by the page itself. Against a pasted advert it scores what your CV already answers and names the phrases it does not, without a key and without sending anything anywhere. Where the posting is on Greenhouse, Lever or Ashby it can read the advert from the board for you. Any line can be rewritten, moved or cut on its own, the page count comes from the PDF writer rather than a guess, and one control sets the whole CV tighter when it has to fit.

The helper that runs on your own machine stays the better editor: it reads the advert for you, checks every claim against your fact bank, keeps a library of tailored CVs, and exports a real PDF. It installs itself as a background service, keeps its own code up to date, and needs no window kept open. See [SETUP.md](SETUP.md), then:

```bash
./start-autoapply.command     # macOS
./start-autoapply.sh           # Linux
start-autoapply.bat            # Windows
python3 -m autoapply bridge    # run it in this window instead
```

Every dashboard card has a native **✦ Edit CV for this job** button; Tampermonkey is not required for the dashboard. It opens a private localhost editor containing the complete master CV and tailors it to the selected posting: sections and entries reordered to lead with the evidence that posting cares about, every line rewritten against its stated requirements, and a summary written for the role. Each proposal can be accepted, rejected, or edited before exporting a job-specific PDF; untouched content is preserved, and the employer application remains a separate button where Simplify can autofill.

Every proposal is checked before it is shown. A rewrite may not introduce a number, a named technology, an employer, a date, or a qualification the CV does not already evidence, and a metric earned on one project may not reappear as the result of another. Keyword coverage is counted against the CV rather than taken from the model, and requirements the CV genuinely cannot evidence are reported as gaps instead of being written around.

Any OpenAI-compatible endpoint drives it — OpenAI, Groq, OpenRouter, Cerebras, Together, GitHub Models, Google AI Studio, or a model running locally under Ollama for nothing. The provider and model are chosen in the editor, and each provider keeps its own key file and its own chosen model, so switching provider asks for that provider's key rather than sending the previous one to an account that never issued it. **Test this provider** sends one cheap request and reports the endpoint, the status, the provider's own words, the parameters it refused and the models it offers.

The dashboard carries three kinds of opportunity behind one switch — **Roles**, **Ventures** and **Funding**. Ventures is the accelerators, talent investors, founder fellowships, grants and studios that back a person rather than employ one: Y Combinator, Techstars, Entrepreneur First, Antler and a16z Speedrun alongside the ones a generic list misses — Conception X for UK PhD researchers, Creator Fund, Royal Academy of Engineering Enterprise Fellowships, Innovate UK Young Innovators. Half of them take no equity at all, and that is a filter. Cheque sizes and equity are shown only where the programme publishes them, and cohort dates are deliberately absent — they move every year, so every card links to the page that governs it.

Any job posting on any site can be tailored for: the `tailor-anywhere.user.js` userscript puts a **✦ Tailor my CV** button on pages that read like a job advert, reads the posting, and opens it in the same local editor — the tracker's own feeds are a starting point, not the limit.

The GitHub repository never receives the private profile, fact bank, API keys, drafts, or generated PDFs. The editor runs on `127.0.0.1`, stores each provider's key locally as a mode-0600 private file, requires review of every proposed change, and never submits an application.

Pressing **Generate suggestions** sends the selected job description and master CV text to the configured endpoint through the user's own account. Merely opening the editor, editing by hand, or exporting a PDF makes no network call. Pointing the editor at a local model means the CV never leaves the machine at all.

> ⚠️ **1462 previously seen roles are stale because at least one source failed or was not checked. They were not marked closed.**

## At a glance

| Metric | Count |
|--|--:|
| Verified-open postings | 4408 |
| Roles discovered today | 49 |
| New verified postings | 49 |
| Research / PhD / postdoc positions | 143 |
| Elite tier | 307 |
| High tier | 337 |
| Eligibility still needs review | 4407 |
| Deadlines within 10 days | 0 |

**By category:** Software Engineering 2247 · Robotics & Embodied AI 460 · Security 339 · AI / ML 298 · Data 270 · Quant / Finance 264 · Hardware / EE 213 · Systems & Infra 212 · Computational Science 95 · HCI / XR 10

**By region:** US 3593 · Canada 218 · UK 166 · Unknown 112 · Singapore 39 · Remote 35 · France 32 · Germany 30 · US / Canada 16 · Switzerland 15 · Netherlands 15 · Hong Kong 12 · US / Austria 11 · Ireland 10 · Brazil 10 · China 8 · US / Australia 8 · India 7 · Poland 6 · Taiwan 6 · Spain 6 · Belgium 5 · US / UK 4 · China / Hong Kong 4 · South Korea 4 · US / Mexico 4 · Australia 3 · Serbia 3 · Austria 3 · Italy 3 · US / Global 2 · Singapore / China / Hong Kong / Australia 2 · Denmark 2 · Global 2 · Mexico 2 · UK / Ireland 1 · Singapore / China / Hong Kong 1 · US / France / Singapore / Hong Kong 1 · Sweden 1 · Japan 1 · US / Belgium 1 · UK / Netherlands / Singapore 1 · Canada / UK 1 · UAE 1 · US / UK / Germany 1

**By degree evidence:** Unknown 3500 · Undergraduate eligible 486 · Advanced/unknown 190 · PhD 189 · Masters 43

## Newly opened (49)

| Company | Role | Category | Region | Term | Eligibility |
|--|--|--|--|--|--|
| **Sierra Space** | [Electrical Engineering Intern - Electrical Engineering](https://sierraspace.wd1.myworkdayjobs.com/en-US/Sierra_Space_External_Career_Site/job/Centennial-CO/XMLNAME-2027-Summer-Internship---Electrical-Engineering_R26563-1?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **Sierra Space** | [Software Engineering Intern - Software Engineering](https://sierraspace.wd1.myworkdayjobs.com/en-US/Sierra_Space_External_Career_Site/job/Centennial-CO/XMLNAME-2027-Summer-Internship---Software-Engineering_R26560-1?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **APEX Analytix** | [Software Engineer Intern - Platform Tooling](https://ats.rippling.com/apexanalytix-careers/jobs/0ab75bb7-08ee-403a-bbe5-3937bb948b19?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Aon** | [Early Careers Health Analytics Specialist](https://jobs.aon.com/jobs/113794?icims=1&lang=en-us&utm_source=Simplify&ref=Simplify) | Data | US | New Grad 2026 | review required |
| **Aon** | [IT / Cybersecurity Engineer Intern](https://go.vansh.nyc/1H4?s=y) | Security | US | Summer 2027 | review required |
| **Artefact** | [AI Engineer Intern](https://go.vansh.nyc/1Gz?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Artefactlinkedin** | [AI Adoption Intern](https://job-boards.greenhouse.io/artefactlinkedin/jobs/8958079002) | Software Engineering | US | None | review required |
| **Artefactlinkedin** | [AI Engineering Intern](https://job-boards.greenhouse.io/artefactlinkedin/jobs/8958074002) | Software Engineering | US | None | review required |
| **Artefactlinkedin** | [AI Strategy Intern](https://job-boards.greenhouse.io/artefactlinkedin/jobs/8958071002) | Software Engineering | US | None | review required |
| **Benchling** | [Software Engineer Intern](https://go.vansh.nyc/1GP?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Benchling** | [Software Engineer, Intern \(Summer 2027\)](https://jobs.ashbyhq.com/benchling/96370d1b-d35e-446b-8e26-dce088860099/application?embed=true&utm_source=Simplify&ref=Simplify) | Computational Science | US | Summer 2027 | review required |
| **CAS** | [Technology Intern, Development Operations](https://go.vansh.nyc/1GH?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Calyx Containers** | [Junior Software Developer - Print &amp; Packaging](https://calyxcontainers.applytojob.com/apply/HHSphZTCc2/Junior-Software-Developer-Print-Packaging?utm_source=Simplify&ref=Simplify) | Software Engineering | US | New Grad 2026 | review required |
| **First Resonance** | [Forward Deployed Engineering Intern \(Summer 2027\)](https://jobs.ashbyhq.com/first-resonance/465193ff-26d7-41d1-8202-2b4ecb22ad0a) | Robotics &amp; Embodied AI | US | Summer 2027 | review required |
| **First Resonance** | [Software Engineering Intern, Platform](https://go.vansh.nyc/1GE?s=y) | Software Engineering | US | Summer 2027 | review required |
| **First Resonance** | [Software Engineering Intern, Platform \(Summer 2027\)](https://jobs.ashbyhq.com/first-resonance/0c88b508-432d-442d-aa5f-486e08aaf5a7/application?embed=true&utm_source=Simplify&ref=Simplify) | Robotics &amp; Embodied AI | US | Summer 2027 | review required |
| **Garmin** | [Data Scientist Intern](https://go.vansh.nyc/1H1?s=y) | Data | US | Summer 2027 | review required |
| **Garmin** | [Software Engineer Intern, Automotive OEM](https://go.vansh.nyc/1H2?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Garmin** | [Software Engineer Intern, Aviation Web Development](https://go.vansh.nyc/1H0?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Garmin** | [Software Engineering Intern](https://go.vansh.nyc/1GY?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Garmin** | [Software Engineering Intern](https://go.vansh.nyc/1GZ?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Genentech** | [AI for Drug Discovery Intern - AI for Drug Discovery - AIDD](https://roche.wd3.myworkdayjobs.com/ROG-A2O-GENE/job/New-York-City/XMLNAME-2027-Summer-Intern---AI-for-Drug-Discovery--AIDD-_202611-129550-1?utm_source=Simplify&ref=Simplify) | Computational Science | US | Summer 2027 | review required |
| **General Dynamics Information Technology** | [AI and Estimation Intern - Interns](https://gdit.wd5.myworkdayjobs.com/gdit_earlytalent/job/USA-VA-Falls-Church/Summer-2027-AI-and-Estimation-Intern_RQ232867?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **GrayMatter Robotics** | [Robotics Engineering Intern: Systems &amp; Applications - Winter '27 - January Start](https://jobs.ashbyhq.com/graymatter-robotics/347cbb66-c542-4c41-bdfc-3f9fa242b20b) | Robotics &amp; Embodied AI | US | Winter | review required |
| **Harmattan Ai** | [Mechatronics Engineer Intern - Automated UAV Calibration](https://jobs.ashbyhq.com/harmattan-ai/e797faf2-88d4-48ff-8a8d-917b50ed207e) | Robotics &amp; Embodied AI | Switzerland | None | review required |
| **JP Morgan Chase** | [Machine Learning Intern - Time Series and Reinforcement Learning 🎓](https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/job/210806784?utm_source=Simplify&ref=Simplify) | AI / ML | UK | Ambiguous | review required |
| **LabCorp** | [Bioinformatics Intern](https://go.vansh.nyc/1GM?s=y) | Computational Science | US | Summer 2027 | review required |
| **MITRE** | [Cybersecurity and Information Security Intern](https://go.vansh.nyc/1GC?s=y) | Security | US | Summer 2027 | review required |
| **MITRE** | [Embedded Security Intern, Electronics Prototype](https://go.vansh.nyc/1GA?s=y) | Security | US | Summer 2027 | review required |
| **MITRE** | [Generative and Agentic AI Intern](https://go.vansh.nyc/1GB?s=y) | Software Engineering | US | Summer 2027 | review required |
| **ManTech** | [CNO Developer Intern](https://go.vansh.nyc/1H5?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Micron Technology** | [Advanced Modeling and AI Solutions Intern](https://go.vansh.nyc/1GW?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Neogen** | [Embedded Systems Engineer Intern](https://go.vansh.nyc/1Gp?s=y) | Systems &amp; Infra | US | Summer 2027 | review required |
| **Nintendo** | [IT Platform Engineer Intern](https://go.vansh.nyc/1GU?s=y) | Systems &amp; Infra | US | Summer 2027 | review required |
| **Northrop Grumman** | [AI/ML Engineering Intern 🇺🇸](https://go.vansh.nyc/1GD?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Playfly Sports** | [Research &amp; Insights Intern](https://www.playfly.com/careers?gh_jid=4486378009&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Sallie Mae** | [Software Engineer Intern](https://sallie-mae.wd5.myworkdayjobs.com/Careers/job/Newark-DE/Software-Engineering-Intern_R26_000688?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Shield AI** | [2027 Summer Intern - Software Engineering - 5815](https://jobs.ashbyhq.com/shield/f96617c2-a120-4b3b-844d-790fcda42503) | Robotics &amp; Embodied AI | US | Summer 2027 | review required |
| **Skynrg** | [Finance &amp; Risk Internship](https://jobs.ashbyhq.com/skynrg/85735acd-c176-46e0-a0c7-03bd8c4b3b25) | Computational Science | Netherlands | None | review required |
| **Stantec** | [Data Scientist Intern - Water](https://hdhl.fa.us6.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/1009005?utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **Stantec** | [Data Scientist Intern, Water](https://go.vansh.nyc/1GO?s=y) | Data | US | Summer 2027 | review required |
| **Strava** | [Software Engineering Intern, AI/ML Data Products](https://jobs.ashbyhq.com/Strava/e4e04f82-bc91-4bc1-b775-85b2b2549023) | AI / ML | US | None | review required |
| **Strava** | [Software Engineering Intern, Android, Subscriptions](https://jobs.ashbyhq.com/Strava/02999001-164a-45c2-a763-03dedf458f0c) | Hardware / EE | US | None | review required |
| **Strava** | [Software Engineering Intern, Server, Comms](https://jobs.ashbyhq.com/Strava/96968b02-dde9-4e0d-b6a8-d2363f550126) | Systems &amp; Infra | US | None | review required |
| **Strava** | [Software Engineering Intern, Server, Next Sports](https://jobs.ashbyhq.com/Strava/0a1c94e3-c19c-47a4-9974-5cc86b74e3e9) | Systems &amp; Infra | US | None | review required |
| **Strava** | [Software Engineering Intern, Server, Security](https://jobs.ashbyhq.com/Strava/924afc4f-b490-4716-a308-5e02fe56653b) | Security | US | None | review required |
| **Strava** | [Software Engineering Intern, Server, User Lifecycle](https://jobs.ashbyhq.com/Strava/12d85f67-5fac-4dfa-8fd7-a4f886b4a10a) | Data | US | None | review required |
| **T.D. Williamson** | [Engineering Intern](https://go.vansh.nyc/1Gy?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Zebra Technologies** | [WWAN Cellular Engineer Intern](https://go.vansh.nyc/1GV?s=y) | Software Engineering | US | Summer 2027 | review required |

## Browse by category

Every category is listed the same way. Live geography reflects what official feeds expose today; the worldwide career-hub and academic watchlists are kept separately in [manual_checks.md](manual_checks.md).

### Software Engineering (2247 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Software Engineer Intern \(Summer 2027, Python / C++ / Full Stack / C# .NET\)](https://akunacapital.com/careers/job/8018847/) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer Intern - Python, Summer 2027](https://www.akunacapital.com/careers/job/8018853/?gh_jid=8018853) | US |  | unknown | unknown |
| **Amazon** | [Software Development Engineer Intern](https://go.vansh.nyc/IN?s=y) | Canada |  | unknown | unknown |
| **Amazon** | [Software Development Engineer Intern](https://go.vansh.nyc/IL?s=y) | US |  | unknown | unknown |
| **Amazon** | [Software Development Engineer Intern, Amazon Leo 🇺🇸](https://go.vansh.nyc/hR?s=y) | US |  | unknown | unknown |
| **Amazon** | [Software Development Engineer Intern, Annapurna Labs](https://go.vansh.nyc/17u?s=y) | US |  | unknown | unknown |
| **Anthropic** | [Research Associate, Biology](https://job-boards.greenhouse.io/anthropic/jobs/5285248008) | US | research | unknown | unknown |
| **Apple** | [Applied Data Solutions Program Intern](https://go.vansh.nyc/17v?s=y) | US |  | unknown | unknown |
| **Apple** | [Hardware Engineering Intern](https://go.vansh.nyc/1tl?s=y) | US |  | unknown | unknown |
| **Apple** | [Hardware Technologies Engineering Intern](https://go.vansh.nyc/1tk?s=y) | US |  | unknown | unknown |
| **Apple** | [Software Engineer Intern, Undergrad](https://go.vansh.nyc/33?s=y) | US |  | unknown | unknown |
| **Apple** | [Software Engineering Intern, Masters](https://go.vansh.nyc/32?s=y) | US |  | unknown | unknown |
| **Citadel** | [Software Engineer Intern](https://go.vansh.nyc/3a?s=y) | US |  | unknown | unknown |
| **Citadel** | [Software Engineer – University Graduate](https://www.citadel.com/careers/details/software-engineer-university-graduate-us/?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Citadel Securities** | [Software Engineer – University Graduate](https://www.citadelsecurities.com/careers/details/software-engineer-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **DE Shaw** | [Software Developer Intern](https://www.deshaw.com/careers/software-developer-intern-new-york-summer-2027-5894) | US |  | unknown | unknown |
| **DRW** | [AI/ML Research Intern](https://go.vansh.nyc/5o?s=y) | Unknown | research | unknown | unknown |
| **DRW** | [Software Developer Intern](https://go.vansh.nyc/5t?s=y) | US |  | unknown | unknown |
| **DRW** | [Software Developer Intern](https://go.vansh.nyc/5s?s=y) | Unknown |  | unknown | unknown |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/7942281) | UK |  | unknown | unknown |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/8020364) | Netherlands |  | unknown | unknown |
| **DRW** | [Software Developer Intern - Industrial Placement](https://job-boards.greenhouse.io/drwuniversityjobs/jobs/7364884) | UK |  | unknown | unknown |
| **Five Rings** | [Software Developer Intern 🇺🇸](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349707008) | US |  | unknown | unknown |
| **Google** | [Software Engineering Intern, BS \(Summer 2027\)](https://www.google.com/about/careers/applications/jobs/results/85564713261245126-software-engineering-intern/) | US |  | unknown | unknown |
| **Jane Street** | [Fundamental Research Analyst Intern](https://go.vansh.nyc/43?s=y) | US | research | unknown | unknown |
| **Jane Street** | [Linux Engineer Intern](https://go.vansh.nyc/45?s=y) | US |  | unknown | unknown |
| **Jane Street** | [Software Engineer Intern](https://go.vansh.nyc/4c?s=y) | US |  | unknown | unknown |
| **Jane Street** | [Tools and Compilers Research and Development Intern](https://go.vansh.nyc/48?s=y) | US | research | unknown | unknown |
| **Jane Street** | [Windows Engineer Intern](https://go.vansh.nyc/4a?s=y) | US |  | unknown | unknown |
| **Microsoft** | [Applied Scientist Intern](https://go.vansh.nyc/FW?s=y) | US |  | unknown | unknown |
| **Microsoft** | [Applied Scientist Intern, Turing](https://go.vansh.nyc/Z4?s=y) | US |  | unknown | unknown |
| **Microsoft** | [First-Year Explore Program Engineering Intern](https://go.vansh.nyc/199?s=y) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern](https://go.vansh.nyc/19z?s=y) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Cloud &amp; Distributed Backend](https://go.vansh.nyc/5L?s=y) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, CoreAI](https://go.vansh.nyc/19t?s=y) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, CoreAI](https://go.vansh.nyc/5H?s=y) | US / Global |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Fullstack Product \(Web + Services\)](https://go.vansh.nyc/5M?s=y) | US / Global |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Teamwork Experiences](https://go.vansh.nyc/1dY?s=y) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineering Intern](https://go.vansh.nyc/17y?s=y) | US |  | unknown | unknown |
| **NVIDIA** | [AI Operations Intern, AI Clouds](https://go.vansh.nyc/1qq?s=y) | US |  | unknown | unknown |

_2207 more are in [tracker.csv](tracker.csv)._

### Robotics & Embodied AI (460 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Amazon** | [Frontier AI &amp; Robotics Intern](https://go.vansh.nyc/eL?s=y) | US |  | unknown | unknown |
| **Amazon** | [Software Development Engineer Intern, Robotics](https://go.vansh.nyc/Mg?s=y) | US |  | unknown | unknown |
| **Amazon** | [Software Development Engineer Intern, Robotics](https://go.vansh.nyc/17r?s=y) | Canada |  | unknown | unknown |
| **NVIDIA** | [Autonomous Vehicles and Robotics Intern](https://go.vansh.nyc/12h?s=y) | US | autonomy | unknown | unknown |
| **🔥 Amazon** | [Hardware Development Engineer Intern Co-op - Robotics](https://amazon.jobs/en/jobs/10535282/hardware-development-engineer-intern-co-op-robotics-2027?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Amazon** | [Robotics Applied Scientist 2 Intern - Robotics 🎓](https://amazon.jobs/en/jobs/10604778/2027-applied-science-internship-robotics-united-states?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [Research Intern - Robotic Perception and Learning 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-WA-Redmond/PhD-Research-Intern--Robotic-Perception-and-Learning---2027_JR2027089?utm_source=Simplify&ref=Simplify) | US | perception,research | unknown | unknown |
| **🔥 NVIDIA** | [Research Intern - World Models and Synthetic Data for Autonomous Driving 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Research-Intern--World-Models-and-Synthetic-Data-for-Autonomous-Driving---Summer-2027_JR2026839-1?utm_source=Simplify&ref=Simplify) | US | autonomy,research | unknown | unknown |
| **🔥 NVIDIA** | [Research Scientist New Grad - Robotics Research 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-WA-Seattle/Research-Scientist--Robotics-Research----PhD-New-College-Grad-2026_JR2011473?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **🔥 NVIDIA** | [Research Scientist PhD New Grad - Autonomous Systems and Physical AI Research 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Research-Scientist--Autonomous-Systems-and-Physical-AI-Research---PhD-New-College-Grad-2026_JR2027551?utm_source=Simplify&ref=Simplify) | US | autonomy,research,phd-position | unknown | unknown |
| **Cerebras Systems** | [Supplier Quality Engineer - New Grad](https://jobs.ashbyhq.com/cerebras/04ce4198-d9b6-4aae-ad11-97708033f94a) | US | controls,robot-software,hardware,research | unknown | unknown |
| **Nuro** | [Software Engineer, AI Platform - Intern](https://nuro.ai/careersitem?gh_jid=7351061) | US | autonomous vehicles | private-scaleup | private company; verify offer |
| **Nuro** | [Software Engineer, AI Platform - New Grad](https://nuro.ai/careersitem?gh_jid=7351066) | US | autonomous vehicles | private-scaleup | private company; verify offer |
| **Nuro** | [Systems Engineering, New Grad 2027](https://nuro.ai/careersitem?gh_jid=8360415) | US | autonomous vehicles | private-scaleup | private company; verify offer |
| **Palantir** | [American Tech Fellowship](https://jobs.lever.co/palantir/0ccbe620-a3ef-41d1-a5c4-68e56b3c91d0) | Unknown | controls,robot-software,hardware,funded | unknown | unknown |
| **Qualcomm** | [Deep Learning Research Intern - Embodied AI - Interim Engineering Intern - Systems](https://qualcomm.eightfold.ai/careers/job/446721858024?utm_source=Simplify&ref=Simplify) | Canada | embodied-ai,research | unknown | unknown |
| **Qualcomm** | [Deep Learning Research Intern, Embodied AI Systems](https://go.vansh.nyc/ZM?s=y) | Canada | embodied-ai,research | unknown | unknown |
| **The Allen Institute for AI** | [Research Intern - Robotics 🎓](https://job-boards.greenhouse.io/thealleninstitute/jobs/8293641?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Waymo** | [2027 Summer Intern, BS/MS, Software Engineer, RO Performance team, Release Evaluation \(Simulation\)](https://careers.withwaymo.com/jobs?gh_jid=8214729) | Poland | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, MS/PhD, Machine Learning Engineer](https://careers.withwaymo.com/jobs?gh_jid=8223735) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, MS/PhD, Machine Learning, Driver Refinement Foundations](https://careers.withwaymo.com/jobs?gh_jid=8304574) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, MS/PhD, Machine Learning, Driver Refinement Foundations](https://careers.withwaymo.com/jobs?gh_jid=8243556) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, MS/PhD, Software Engineer](https://careers.withwaymo.com/jobs?gh_jid=8224729) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, MS/PhD, Software Engineer, Simulation Evaluation ML Model](https://careers.withwaymo.com/jobs?gh_jid=8221795) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, MS/PhD, Software/ML Engineer, Simulation](https://careers.withwaymo.com/jobs?gh_jid=8221851) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, Machine Learning, MS/PhD, Simulation Realism \(World Model\)](https://careers.withwaymo.com/jobs?gh_jid=8358262) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Data Science](https://careers.withwaymo.com/jobs?gh_jid=8221956) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Machine Learning, Simulation Realism](https://careers.withwaymo.com/jobs?gh_jid=8265868) | UK | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Research Scientist, Foundation Models](https://careers.withwaymo.com/jobs?gh_jid=8227640) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Research Scientist, Visual Reasoning](https://careers.withwaymo.com/jobs?gh_jid=8292367) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Research, Behavior Post-training](https://careers.withwaymo.com/jobs?gh_jid=8289816) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Research, RSI for Autonomous Driving](https://careers.withwaymo.com/jobs?gh_jid=8306779) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Research, VLM Harnesses for AV Planning](https://careers.withwaymo.com/jobs?gh_jid=8301854) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Research, World Action Model](https://careers.withwaymo.com/jobs?gh_jid=8243732) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Research, World Modeling Evaluation](https://careers.withwaymo.com/jobs?gh_jid=8265173) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Safety Research, Human Behavior Analytics](https://careers.withwaymo.com/jobs?gh_jid=8197899) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [Software Engineer Intern, Multiverse](https://go.vansh.nyc/1qh?s=y) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [2027 Summer Intern - AI Foundations - Recipes 🎓](https://careers.withwaymo.com/jobs?gh_jid=8306841&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Agentic AI Intern 🎓](https://careers.withwaymo.com/jobs?gh_jid=8401116&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [MS/PhD, ML Systems &amp; Behavior Discovery Intern 🎓](https://careers.withwaymo.com/jobs?gh_jid=8257159&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |

_420 more are in [tracker.csv](tracker.csv)._

### Security (339 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Apple Bank** | [Information Security Intern 🛂](https://go.vansh.nyc/VV?s=y) | US | security | unknown | unknown |
| **Jane Street** | [Cybersecurity Analyst Intern](https://go.vansh.nyc/41?s=y) | US |  | unknown | unknown |
| **Microsoft** | [Research Intern, Firmware Security](https://go.vansh.nyc/1BR?s=y) | US | hardware,security,research | unknown | unknown |
| **Microsoft** | [Security Assurance Intern](https://go.vansh.nyc/15H?s=y) | US | security | unknown | unknown |
| **Microsoft** | [Security Research Intern](https://go.vansh.nyc/eB?s=y) | US | security,research | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Security &amp; Identity](https://go.vansh.nyc/hN?s=y) | US | security | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Security &amp; Identity](https://go.vansh.nyc/e6?s=y) | US | security | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Security &amp; Identity](https://go.vansh.nyc/5J?s=y) | US | security | unknown | unknown |
| **Mistral AI** | [Applied Scientist  \(Internship\)](https://jobs.ashbyhq.com/mistral.ai/de46ba8b-00cb-4618-83df-66e15a78434e) | France | multimodal,research,phd-position | unknown | unknown |
| **Qube Research and Technologies** | [Security Engineer Intern](https://go.vansh.nyc/QJ?s=y) | US | security,research | unknown | unknown |
| **🔥 Amazon** | [Software Developer Engineer 1 - Security Platform](https://amazon.jobs/en/jobs/10597112/software-dev-engineer-i-security-platform?utm_source=Simplify&ref=Simplify) | US | security | unknown | unknown |
| **Cohere** | [Machine Learning Intern/Co-op  \(Winter 2027\)](https://jobs.ashbyhq.com/cohere/36d1f52f-8270-4652-adf5-5303a0ff341b) | Canada | computer-vision,nlp,security,research,funded | unknown | unknown |
| **Figma** | [PhD Intern, Security Engineer \(2027\)](https://boards.greenhouse.io/figma/jobs/6238015004?gh_jid=6238015004) | US | security,phd-position | unknown | unknown |
| **Palantir** | [Forward Deployed Infrastructure Engineer, New Grad - UK Government](https://jobs.lever.co/palantir/cadc0eb2-2703-43e4-8e4f-41edf5b071c6) | UK | autonomy,llm,infra,distributed,security | unknown | unknown |
| **Palantir** | [Forward Deployed Infrastructure Engineer, New Grad - US Government](https://jobs.lever.co/palantir/33243fb5-6907-40c7-930c-968b25d825d0) | US | autonomy,llm,infra,distributed,security,funded | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - AUS Government](https://jobs.lever.co/palantir/395a4483-fc3d-4b77-a500-501923fd0976) | Australia | infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - UK Government](https://jobs.lever.co/palantir/26e23f5d-083b-45aa-b223-1a6e43d960bf) | UK | autonomy,llm,computer-vision,infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - UK Government](https://jobs.lever.co/palantir/b4aa51a2-bc43-4d67-bf55-12db7feefb3a/apply?utm_source=Simplify&ref=Simplify) | UK | autonomy,hardware,llm,computer-vision,infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - US Government](https://jobs.lever.co/palantir/cbe90327-3e6e-451c-a54c-1d3cbcef5aeb/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,infra,security,funded | unknown | unknown |
| **Palantir** | [Information Security Engineer, Internship](https://jobs.lever.co/palantir/ef725594-42dd-4f0d-ba8e-df8179dbc6cb) | US | autonomy,computer-vision,security | unknown | unknown |
| **Palantir** | [Meritocracy Fellowship](https://jobs.lever.co/palantir/7fa0ceca-c30e-48de-9b27-f98469c374f3) | US | autonomy,security,funded | unknown | unknown |
| **Palantir** | [Privacy &amp; Civil Liberties Engineer - New Grad](https://jobs.lever.co/palantir/95e0d2b0-437a-4096-a5c6-0f247f426c90) | US | security,funded | unknown | unknown |
| **Palantir** | [Privacy and Civil Liberties Software Engineer, Internship](https://jobs.lever.co/palantir/09846827-b931-4a9f-bd64-c3bb8860187b) | US | infra,security | unknown | unknown |
| **Palantir** | [Software Engineer, Internship](https://jobs.lever.co/palantir/e27af7ab-41fc-40c9-b31d-02c6cb1c505c) | US | computer-vision,data-eng,infra,security,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship](https://jobs.lever.co/palantir/373eb939-6f57-4836-8479-be79a5e07249) | US | computer-vision,data-eng,infra,security,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship](https://jobs.lever.co/palantir/bdcfb29f-4f27-42de-933f-7f83a359b9f0) | US | computer-vision,data-eng,infra,security,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Connectivity Platform and Product](https://jobs.lever.co/palantir/130ee501-bd22-4d44-b651-39581ef97743) | US | computer-vision,infra,distributed,security,phd-position | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Connectivity Platform and Product](https://jobs.lever.co/palantir/eb496d6a-a960-43d3-a09b-e3843052f54e) | US | computer-vision,infra,distributed,security,phd-position | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Data Connectors](https://jobs.lever.co/palantir/45e4617d-d658-4b30-8dc9-378ca84a027a) | US | computer-vision,infra,distributed,security,phd-position | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Defense Tech](https://jobs.lever.co/palantir/f17e98d0-046a-4e6e-9d65-ed0b12dd0ff7) | US | computer-vision,data-eng,infra,security | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Defense Tech](https://jobs.lever.co/palantir/8bcf4f33-0a79-4248-bbfd-49ac4be9dd8e) | US | computer-vision,data-eng,infra,security | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Defense Tech](https://jobs.lever.co/palantir/a483f41b-0da9-42ea-8ed6-cbf6eb93cc6d) | US | computer-vision,data-eng,infra,security | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Infrastructure](https://jobs.lever.co/palantir/b229baac-494b-4a0d-9a13-2e38806e06f3) | US | computer-vision,data-eng,infra,security | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Infrastructure](https://jobs.lever.co/palantir/f221738b-e97c-4ce3-a12a-17ada2b855e4) | US | computer-vision,data-eng,infra,security | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Production Infrastructure](https://jobs.lever.co/palantir/373367a9-3160-49d8-b7af-2efec062fad1) | US | computer-vision,infra,security,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Production Infrastructure](https://jobs.lever.co/palantir/3ab9e715-1ea9-4c6c-ad50-7340eac14e86) | US | computer-vision,infra,security,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Sovereign AI Systems](https://jobs.lever.co/palantir/40840cef-bbd7-4557-bb21-cbdcf4be616e) | UK | computer-vision,infra,distributed,security,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Sovereign AI Systems](https://jobs.lever.co/palantir/cd64bcd4-50bb-4aeb-a135-4e0487ffd312) | US | computer-vision,infra,distributed,security,research | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad](https://jobs.lever.co/palantir/94984771-0704-446c-88c6-91ce748f6d92/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,data-eng,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad](https://jobs.lever.co/palantir/c34b424e-caf2-455a-b104-ae1096ccca29/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,data-eng,infra,security,research,funded | unknown | unknown |

_299 more are in [tracker.csv](tracker.csv)._

### AI / ML (298 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Amazon** | [Machine Learning Systems Software Development Engineer Intern, Annapurna Labs](https://go.vansh.nyc/MP?s=y) | Canada |  | unknown | unknown |
| **Amazon** | [Software Development Engineer Intern, Machine Learning/Automated Reasoning](https://go.vansh.nyc/10y?s=y) | US |  | unknown | unknown |
| **Apple** | [Machine Learning and Artificial Intelligence Undergrad Intern](https://go.vansh.nyc/19Z?s=y) | US |  | unknown | unknown |
| **G-Research** | [Machine Learning Engineer Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Machine-Learning-Engineer-Intern_R3773?utm_source=Simplify&ref=Simplify) | UK | research | unknown | unknown |
| **Jane Street** | [Machine Learning Engineer Intern](https://go.vansh.nyc/3Z?s=y) | US |  | unknown | unknown |
| **Jane Street** | [Machine Learning Researcher Intern](https://go.vansh.nyc/40?s=y) | US |  | unknown | unknown |
| **Microsoft** | [Research Intern, AI/Machine Learning Numerics &amp; Efficiency](https://go.vansh.nyc/1Dx?s=y) | US | research | unknown | unknown |
| **Microsoft** | [Research Intern, Computer Vision and Deep Learning](https://go.vansh.nyc/1Cv?s=y) | US | perception,computer-vision,research | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, AI/ML &amp; LLM](https://go.vansh.nyc/5K?s=y) | US | llm | unknown | unknown |
| **Mistral AI** | [AI Scientist - \(Internship, Masters or Phd\)](https://jobs.ashbyhq.com/mistral.ai/f7245b49-92a0-4111-bba1-343183de7d97) | France | autonomy,controls,llm,nlp,infra,research,neuroscience,phd-position | unknown | unknown |
| **Mistral AI** | [AI Scientist Intern - \(Internship, Masters or Phd\)](https://jobs.ashbyhq.com/mistral.ai/7c401bbf-ee63-4fcd-a44a-a16b9b787697) | US | autonomy,controls,llm,nlp,infra,research,neuroscience,phd-position | unknown | unknown |
| **Mistral AI** | [Applied AI, Forward Deployed Machine Learning Engineer - \(Internship\)](https://jobs.ashbyhq.com/mistral.ai/fcdb8407-20b9-4179-81b6-f2ca2c79a39b) | France | controls,nlp | unknown | unknown |
| **NVIDIA** | [Deep Learning Computer Architecture Intern](https://go.vansh.nyc/Rn?s=y) | US |  | unknown | unknown |
| **NVIDIA** | [Deep Learning Intern](https://go.vansh.nyc/12j?s=y) | US |  | unknown | unknown |
| **Susquehanna International Group** | [Machine Learning Engineering Intern](https://go.vansh.nyc/RM?s=y) | US |  | unknown | unknown |
| **Tower Research Capital** | [Machine Learning Intern](https://go.vansh.nyc/9U?s=y) | Canada | research | unknown | unknown |
| **Tower Research Capital** | [Stagiaire en machine learning / Machine Learning Intern](https://www.tower-research.com/open-positions/?gh_jid=7077280) | Canada | research | unknown | unknown |
| **Two Sigma** | [AI Research Scientist Intern \(MS / PhD\)](https://careers.twosigma.com/careers/JobDetail/New-York-New-York-United-States-AI-Research-Scientist-Internship-2027-Summer/14022) | US | research,phd-position | unknown | unknown |
| **🔥 Amazon** | [Applied Science Intern - Gen AI &amp; Large Language Models 🎓](https://amazon.jobs/en/jobs/10564589/2027-applied-science-internship-gen-ai-large-language-models-united-states-phd-student-science-recruiting?utm_source=Simplify&ref=Simplify) | US | llm | unknown | unknown |
| **🔥 Amazon** | [Applied Science Intern - Natural Language Processing and Speech Technologies 🎓](https://amazon.jobs/en/jobs/10564593/2027-applied-science-internship-natural-language-processing-and-speech-technologies-united-states-phd-student-science-recruiting?utm_source=Simplify&ref=Simplify) | US | nlp | unknown | unknown |
| **🔥 Amazon** | [Applied Scientist Intern - Reinforcement Learning &amp; Optimization - Machine Learning 🎓](https://amazon.jobs/en/jobs/10564597/2027-applied-science-internship-reinforcement-learning-optimization-machine-learning-united-states-phd-student-science-recruiting?utm_source=Simplify&ref=Simplify) | US | rl | unknown | unknown |
| **🔥 Amazon** | [Software Engineer Intern - Machine Learning/Automated Reasoning](https://amazon.jobs/en/jobs/10593521/software-development-engineer-intern-machine-learning-automated-reasoning-summer-2027?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Microsoft** | [Research Intern - Deep Learning Group 🎓](https://apply.careers.microsoft.com/careers/job/1970393557076095?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **🔥 NVIDIA** | [Applied Research Scientist Intern - Agentic Biology 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Applied-Research-Scientist-Intern--Agentic-Biology---Summer-2027_JR2029307?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **🔥 NVIDIA** | [Deep Learning Scientist Intern - LLM, Multimodal and Agentic AI 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Deep-Learning-Scientist-Intern--LLM--Multimodal-and-Agentic-AI---Summer-2027_JR2027548?utm_source=Simplify&ref=Simplify) | US / Canada | llm,multimodal | unknown | unknown |
| **🔥 NVIDIA** | [Research Scientist New Grad - Electronic Design Automation 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Research-Scientist--Electronic-Design-Automation---New-College-Grad-2026_JR2012979?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **🔥 NVIDIA** | [Research Scientist – PhD New College Grad - Generative AI for Physical AI 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Research-Scientist--Generative-AI-for-Physical-AI---PhD-New-College-Grad-2026_JR2016032?utm_source=Simplify&ref=Simplify) | US | research,phd-position | unknown | unknown |
| **Cerebras Systems** | [Kernel Engineer - New Grad](https://jobs.ashbyhq.com/cerebras/9c7da4b8-446b-4bf2-8d07-23241590bf2e) | US | hardware,research,neuroscience,phd-position | unknown | unknown |
| **Coinbase** | [Machine Learning Engineer Intern](https://www.coinbase.com/careers/positions/8175441?gh_jid=8175441) | US |  | unknown | unknown |
| **Databricks** | [PhD GenAI Research Scientist Intern](https://databricks.com/company/careers/open-positions/job?gh_jid=7011263002) | US | research,phd-position | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - Commercial](https://jobs.lever.co/palantir/2ad0ab10-34c3-410d-883b-8052864a95cd) | South Korea | autonomy,hardware,llm,computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - Commercial](https://jobs.lever.co/palantir/e500bcf3-19d8-4d3c-b340-4d76e4a55b40/apply?utm_source=Simplify&ref=Simplify) | US | autonomy,hardware,llm,computer-vision,infra,funded | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - Commercial](https://jobs.lever.co/palantir/2e6b0ac8-83e9-4be5-a3aa-cf319f751728/apply?utm_source=Simplify&ref=Simplify) | US | autonomy,hardware,llm,computer-vision,infra,funded | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - Commercial](https://jobs.lever.co/palantir/341d5cae-a473-4813-9a6c-0f67fcc1b253) | South Korea | autonomy,hardware,llm,computer-vision,infra | unknown | unknown |
| **Palantir** | [Neurodivergent Fellowship](https://jobs.lever.co/palantir/61eaa54c-e1b7-4064-afad-f7df3d48d652) | US | llm,funded | unknown | unknown |
| **Palantir** | [Neurodivergent Fellowship](https://jobs.lever.co/palantir/fd952b52-7b9c-4056-a3dd-0bc41fcfe603) | US | llm,funded | unknown | unknown |
| **Perplexity** | [Internship - Search Machine Learning Engineer](https://jobs.ashbyhq.com/Perplexity/9246cf02-26fd-4ae8-90c5-639c6e85e9e2) | Serbia | llm,nlp,infra,research,phd-position | unknown | unknown |
| **Perplexity** | [Internship - Search Machine Learning Engineer](https://jobs.ashbyhq.com/Perplexity/71168628-1998-47d3-87a9-be7bc56a430d) | UK | llm,nlp,infra,research | unknown | unknown |
| **Qualcomm** | [AI/Machine Learning Intern](https://go.vansh.nyc/1Bt?s=y) | Canada |  | unknown | unknown |
| **Qualcomm** | [AI/Machine Learning Intern - Interim Engineering Intern - SW](https://qualcomm.eightfold.ai/careers/job/446722176432?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |

_258 more are in [tracker.csv](tracker.csv)._

### Data (270 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Apple Bank** | [IT Data Intern - Analytics, &amp; Automation](https://applebank.wd5.myworkdayjobs.com/applebankcareers/job/New-York-NY/XMLNAME-2027-Summer-Intern--IT-Data--Analytics----Automation_2026-1414?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Jane Street** | [Data Engineer Intern](https://go.vansh.nyc/42?s=y) | US | data-eng | unknown | unknown |
| **Microsoft** | [Data Scientist Intern, CoreAI](https://go.vansh.nyc/1wj?s=y) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Data Platform/Analytics](https://go.vansh.nyc/5I?s=y) | US |  | unknown | unknown |
| **Point72** | [Data Scientist Intern 🎓](https://boards.greenhouse.io/point72/jobs/8885299002?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Qube Research &amp; Technologies** | [Business Data Analytics Intern](https://job-boards.greenhouse.io/quberesearchandtechnologies/jobs/8926633002?utm_source=Simplify&ref=Simplify) | UK | research | unknown | unknown |
| **🔥 Amazon** | [Business Intelligence Engineer Intern](https://amazon.jobs/en/jobs/10553765/business-intelligence-engineer-internship-2027-us?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Amazon** | [Data Engineer Early Career](https://amazon.jobs/en/jobs/10559101/data-engineer-early-career-2026-can?utm_source=Simplify&ref=Simplify) | Canada | data-eng | unknown | unknown |
| **🔥 Amazon** | [Data Engineer Intern](https://amazon.jobs/en/jobs/10553907/data-engineer-internship-2027-us?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **🔥 Google** | [People Analytics Intern 🎓](https://www.google.com/about/careers/applications/jobs/results/81809776362562246?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Meta** | [Data Scientist Intern - Product Analytics](https://www.metacareers.com/jobs/1633096478817942?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Coinbase** | [Analytics Engineer Intern](https://go.vansh.nyc/Mt?s=y) | US |  | unknown | unknown |
| **Coinbase** | [Analytics Engineer Intern](https://www.coinbase.com/careers/positions/8175471?gh_jid=8175471) | US |  | unknown | unknown |
| **Coinbase** | [Internal Audit Analytics Intern](https://www.coinbase.com/careers/positions/8221238?gh_jid=8221238) | US |  | unknown | unknown |
| **Coinbase** | [People Analytics Intern](https://www.coinbase.com/careers/positions/8175517?gh_jid=8175517) | US |  | unknown | unknown |
| **Figma** | [Data Engineer Intern \(2027\)](https://boards.greenhouse.io/figma/jobs/6178851004?gh_jid=6178851004) | US | data-eng | unknown | unknown |
| **Notion** | [Software Engineer, Growth \(Early Career\)](https://jobs.ashbyhq.com/notion/297b4ece-765f-4eea-b1b8-46057cb6501f) | US | autonomy,infra,distributed,research | unknown | posting mentions equity |
| **Snowflake** | [Software Engineer Intern AI/ML - Warsaw \(2027\)](https://jobs.ashbyhq.com/snowflake/418a8f32-1658-47d9-9450-ed3a6e947215) | Poland | data-eng,infra,distributed,research | unknown | unknown |
| **Snowflake** | [Software Engineering Intern – Data Ingestion &amp; Platform Infrastructure \(Warsaw, Summer 2027\)](https://jobs.ashbyhq.com/snowflake/aada80b0-a940-4441-89c0-08d929db38a7) | Poland | manipulation,data-eng,infra,distributed | unknown | unknown |
| **Stripe** | [PhD Data Scientist, Intern](https://stripe.com/jobs/search?gh_jid=8194285) | Canada | phd-position | unknown | unknown |
| **Stripe** | [PhD Data Scientist, Intern](https://stripe.com/jobs/search?gh_jid=8194283) | US | phd-position | unknown | unknown |
| **🔥 Tesla** | [Data Engineer Intern - Energy](https://www.tesla.com/careers/search/job/287982?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **ADT** | [Data, Analytics &amp; AI Intern 🛂](https://go.vansh.nyc/CW?s=y) | US |  | unknown | unknown |
| **ASML** | [Data Scientist Intern](https://asml.wd3.myworkdayjobs.com/asmlext1/job/Wilton-CT-USA/Internship---Data-Scientist_J-00356462?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **ASML** | [EUV Data Science and Analytics Intern](https://go.vansh.nyc/1yZ?s=y) | US |  | unknown | unknown |
| **AXA** | [Underwriting Data &amp; Analytics Intern](https://careers.axa.com/jobs/25498?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Acluinternships** | [Spring 2027 Graduate Intern, Product Design- Technology and Analytics Department](https://job-boards.greenhouse.io/acluinternships/jobs/8919915002) | US |  | unknown | unknown |
| **Acluinternships** | [Spring 2027 Undergraduate Intern, Technology and Analytics Department- Educate Pod](https://job-boards.greenhouse.io/acluinternships/jobs/8919540002) | US |  | unknown | unknown |
| **Acuity Insurance** | [Data Analytics Intern - Data Science](https://recruiting2.ultipro.com/her1001acfin/JobBoard/ab33798a-3521-417b-8db8-a8e435c475fa/OpportunityDetail?opportunityId=3d8a72b0-b464-4ff8-bd58-555a1e640ef7&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Addepar** | [Data Engineer Intern](https://job-boards.greenhouse.io/addepar1/jobs/8910327002?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **Affinius Capital** | [Data Scientist Intern](https://careers-affiniuscapital.icims.com/jobs/2284/summer-2027-data-scientist-intern/job) | US |  | unknown | unknown |
| **Agave** | [Full-Stack Software Engineer \(New Grad\)](https://jobs.ashbyhq.com/agave/73bd2c98-bf87-4eaa-aea8-35e7b6131d0e/application?embed=true&utm_source=Simplify&ref=Simplify) | US | research | unknown | posting mentions equity |
| **Agoda** | [Associate Data Analyst \(New Graduate, Thai Speaking\) \(Marketing Analytics, Bangkok Based\)](https://job-boards.greenhouse.io/agoda/jobs/8194692) | Unknown |  | unknown | unknown |
| **Agoda** | [\[Cooperative Internship 2027\] Data Pipeline Intern BKK](https://job-boards.greenhouse.io/agoda/jobs/8358205) | Unknown | data-eng | unknown | unknown |
| **Agoda** | [\[Summer Internship 2027\] CEG Data Analytics Intern \(Bangkok Based\)](https://job-boards.greenhouse.io/agoda/jobs/8335899) | Unknown |  | unknown | unknown |
| **Agoda** | [\[Summer Internship 2027\] Supply Analytics Intern](https://job-boards.greenhouse.io/agoda/jobs/8358027) | Unknown |  | unknown | unknown |
| **Allstate** | [Data Analytics Engineer Intern](https://allstate.wd5.myworkdayjobs.com/sourcing_event/job/USA---IL-Remote/Arity---Data-Analytics-Engineer-Intern_R36286?utm_source=Simplify&ref=Simplify) | Unknown |  | unknown | unknown |
| **Allstate** | [Data Analytics Engineer Intern](https://go.vansh.nyc/fe?s=y) | US |  | unknown | unknown |
| **American Family Insurance Group** | [Business Intelligence Enablement Intern](https://go.vansh.nyc/fc?s=y) | US |  | unknown | unknown |
| **Amgen** | [AI-Enabled Knowledge Graphs for Patient Journey Analytics Intern 🎓](https://amgen.wd1.myworkdayjobs.com/careers/job/United-States---Remote/Grad-Intern---Knowledge-Graph-Applications--Summer-2027-_R-260625?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |

_230 more are in [tracker.csv](tracker.csv)._

### Quant / Finance (264 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Junior Quantitative Developer &amp; Strategist](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8065007?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Akuna Capital** | [Junior Quantitative Researcher](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8065206?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Akuna Capital** | [Junior Quantitative Researcher - Harvard](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8065211?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Akuna Capital** | [Quantitative Development &amp; Strategy Intern, Summer 2027 \| Harvard](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8066880) | US |  | unknown | unknown |
| **Akuna Capital** | [Quantitative Development &amp; Strategy Intern, Summer 2027 \| Massachusetts Institute of Technology](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8066884) | US |  | unknown | unknown |
| **Akuna Capital** | [Quantitative Research Intern 🇺🇸](https://www.akunacapital.com/careers/job/8036614/?gh_jid=8036614) | US | research | unknown | unknown |
| **Akuna Capital** | [Quantitative Research Intern, Summer 2027 \| Columbia University](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8065680) | US | research | unknown | unknown |
| **Akuna Capital** | [Quantitative Research Intern, Summer 2027 \| Georgia Institute of Technology](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8065656) | US | research | unknown | unknown |
| **Akuna Capital** | [Quantitative Research Intern, Summer 2027 \| Massachusetts Institute of Technology](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8065670) | US | research | unknown | unknown |
| **Akuna Capital University** | [Junior Quantitative Developer &amp; Strategist](https://www.akunacapital.com/careers/job/8016687/?gh_jid=8016687&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Akuna Capital University** | [Junior Quantitative Researcher](https://www.akunacapital.com/careers/job/8036541/?gh_jid=8036541&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Citadel** | [Quantitative Research Analyst University Graduate](https://www.citadel.com/careers/details/quantitative-research-analyst-university-graduate-us/?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Citadel** | [Quantitative Trader: Equity Quantitative Research – University Graduate](https://www.citadel.com/careers/details/quantitative-trader-equity-quantitative-research-university-graduate-us/?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Citadel Securities** | [Quantitative Research Analyst – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-research-analyst-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | UK / Ireland | research | unknown | unknown |
| **Citadel Securities** | [Quantitative Trader – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-us-miami/?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Citadel Securities** | [Quantitative Trader – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-us-new-york/?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Cubist Systematic Strategies** | [Quantitative Developer Intern](https://job-boards.greenhouse.io/point72/jobs/7297613002) | US |  | unknown | unknown |
| **DRW** | [Quantitative Research Intern](https://job-boards.greenhouse.io/drweng/jobs/7818540) | US | research | unknown | unknown |
| **DRW** | [Quantitative Research Intern](https://job-boards.greenhouse.io/drweng/jobs/7957756) | UK | research | unknown | unknown |
| **DRW** | [Quantitative Research Intern](https://job-boards.greenhouse.io/drweng/jobs/8014915) | Singapore | research | unknown | unknown |
| **DRW** | [Quantitative Trading Analyst Intern](https://job-boards.greenhouse.io/drweng/jobs/7668776) | US |  | unknown | unknown |
| **DRW** | [Quantitative Trading Analyst Intern](https://job-boards.greenhouse.io/drweng/jobs/7957243) | UK |  | unknown | unknown |
| **Five Rings** | [Quantitative Trader Intern \(Summer 2027\)](https://job-boards.greenhouse.io/fiveringsllc/jobs/5139668008) | US |  | unknown | unknown |
| **Hudson River Trading** | [Algorithm Developer New Grad - Quant Researcher](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8052050&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Hudson River Trading** | [Data Scientist Intern](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8257369&utm_source=Simplify&ref=Simplify) | US / UK |  | unknown | unknown |
| **Hudson River Trading** | [Data Scientist Intern](https://go.vansh.nyc/1A5?s=y) | US |  | unknown | unknown |
| **Hudson River Trading** | [FPGA Verification and Developer Intern](https://go.vansh.nyc/QI?s=y) | US | hardware | unknown | unknown |
| **Hudson River Trading** | [Software Engineer Intern](https://go.vansh.nyc/3F?s=y) | US |  | unknown | unknown |
| **Hudson River Trading** | [Software Engineering Intern \(Summer 2027, C++ / Python\)](https://www.hudsonrivertrading.com/hrt-job/software-engineering-internship-c-or-python-summer-2027/) | US |  | unknown | unknown |
| **IMC Trading** | [Deep Learning Research Intern - 2027 - Sydney](https://job-boards.eu.greenhouse.io/imc/jobs/4956547101) | Australia | research | unknown | unknown |
| **IMC Trading** | [Deep Learning Research Intern - Summer 2027 - Amsterdam](https://job-boards.eu.greenhouse.io/imc/jobs/4912874101) | Netherlands | research | unknown | unknown |
| **IMC Trading** | [Graduate Quantitative Researcher \(PhD\)](https://job-boards.eu.greenhouse.io/imc/jobs/4912325101) | US | phd-position | unknown | unknown |
| **IMC Trading** | [Hardware Engineer Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4823945101) | US |  | unknown | unknown |
| **IMC Trading** | [Hardware Machine Learning PhD Research Internship](https://job-boards.eu.greenhouse.io/imc/jobs/4975945101) | US | research,phd-position | unknown | unknown |
| **IMC Trading** | [Machine Learning Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4962456101?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **IMC Trading** | [Machine Learning Engineer Intern](https://go.vansh.nyc/1nv?s=y) | US |  | unknown | unknown |
| **IMC Trading** | [Machine Learning Research Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4907430101) | US | research | unknown | unknown |
| **IMC Trading** | [Quant Performance Engineer Intern - Summer 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4842595101) | US |  | unknown | unknown |
| **IMC Trading** | [Quantitative Research Intern \(Summer 2027, BS / MS\)](https://job-boards.eu.greenhouse.io/imc/jobs/4907399101) | US | research | unknown | unknown |
| **IMC Trading** | [Quantitative Research Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941208101) | Hong Kong | research | unknown | unknown |

_224 more are in [tracker.csv](tracker.csv)._

### Hardware / EE (213 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Amazon** | [ASIC Engineer Intern](https://go.vansh.nyc/hA?s=y) | US |  | unknown | unknown |
| **Amazon** | [Software Development Engineer Intern, Amazon Leo, Embedded Systems 🇺🇸](https://go.vansh.nyc/g6?s=y) | US | hardware | unknown | unknown |
| **Amazon** | [Software Development Engineer Intern, Embedded Systems](https://go.vansh.nyc/g0?s=y) | US | hardware | unknown | unknown |
| **DRW** | [FPGA Intern](https://go.vansh.nyc/5n?s=y) | US | hardware | unknown | unknown |
| **Virtu Financial** | [2027 Internship- Hardware Engineer \(FPGA\)](https://job-boards.greenhouse.io/virtu/jobs/8657286002) | US | hardware | unknown | unknown |
| **🔥 Amazon** | [ASIC Engineer Early Career](https://amazon.jobs/en/jobs/10576621/asic-engineer-early-career-2027-project-leo?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Amazon** | [ASIC Engineer Intern](https://amazon.jobs/en/jobs/10576619/asic-engineer-intern-summer-2027?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Amazon** | [ASIC Formal Verification Engineer 1](https://amazon.jobs/en/jobs/10597433/asic-formal-verification-engineer-i-annapurna-labs?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Amazon** | [Software Development Engineer – Early Career - Embedded Systems](https://amazon.jobs/en/jobs/10598021/software-development-engineer-embedded-systems-amazon-leo-early-career-2027-us?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 Amazon** | [Software Development Engineer – Early Career - Embedded Systems](https://amazon.jobs/en/jobs/10595839/software-development-engineer-embedded-systems-early-career-2027-us?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 Amazon** | [Software Engineer Intern - Embedded Systems](https://amazon.jobs/en/jobs/10567914/software-development-engineer-intern-embedded-systems-summer-2027-usa?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 Amazon** | [Software Engineer Intern - Embedded Systems](https://amazon.jobs/en/jobs/10571374/software-development-engineer-embedded-systems-intern-amazon-leo-summer-2027-usa?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 Meta** | [ASIC Engineer New Grad - Performance Architecture and Modeling](https://www.metacareers.com/jobs/4596319193960098?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Clocks Verification Engineer New Grad 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Clocks-Verification-Engineer---New-College-Grad-2026_JR2027579?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Design Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Design-Engineer---New-College-Grad-2026_JR2020309?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Floorplan Design Engineer New Grad 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Floorplan-Design-Engineer---New-College-Grad-2026_JR2024651?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Physical Design Engineer New Grad - Netlisting 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Physical-Design-Engineer--Netlisting---New-College-Grad-2026_JR2017681?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Physical Design and Timing Engineer – New College Grad 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Timing-Engineer---New-College-Grad-2026_JR2013177?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Verification Intern](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/Canada-Toronto/ASIC-Verification-Intern---Summer-2027_JR2027982?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **🔥 NVIDIA** | [Low Power ASIC Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Low-Power-ASIC-Engineer---New-College-Grad-2027_JR2027850?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [VLSI CAD Timing Intern - Applied AI 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/VLSI-CAD-Timing-Intern--Applied-AI---Summer-2027_JR2026799?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 NVIDIA** | [VLSI Timing Methodology Intern 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/VLSI-Timing-Methodology-Intern---Summer-2027_JR2026798?utm_source=Simplify&ref=Simplify) | US / Canada | hardware | unknown | unknown |
| **Graphcore** | [Firmware Engineer Intern](https://job-boards.greenhouse.io/graphcore-early-careers/jobs/8902588002?utm_source=Simplify&ref=Simplify) | UK | hardware | unknown | unknown |
| **Graphcore** | [Firmware Intern](https://job-boards.greenhouse.io/graphcore/jobs/8894770002?utm_source=Simplify&ref=Simplify) | UK | hardware | unknown | unknown |
| **Qualcomm** | [AI and DSP Applications Engineer Intern](https://qualcomm.eightfold.ai/careers/job/446721686396?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Qualcomm** | [Camera HW ASIC Verification Intern](https://qualcomm.eightfold.ai/careers/job/446721829462?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Qualcomm** | [Display IP FPGA Emulation Intern](https://qualcomm.eightfold.ai/careers/job/446721972361?utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **Qualcomm** | [Driver and Tools Developer Intern - Telemetry Firmware](https://qualcomm.eightfold.ai/careers/job/446721989047?utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **Qualcomm** | [Embedded Engineering Intern](https://go.vansh.nyc/Rq?s=y) | US | hardware | unknown | unknown |
| **Qualcomm** | [Firmware Development Intern, PAL](https://go.vansh.nyc/Jq?s=y) | Canada | hardware | unknown | unknown |
| **Qualcomm** | [Firmware Engineer Intern, Embedded Software Engineering, Embedded Firmware and SDK Development](https://go.vansh.nyc/II?s=y) | Canada | hardware | unknown | unknown |
| **Qualcomm** | [Firmware Engineering Intern](https://qualcomm.eightfold.ai/careers/job/446722038614?utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **Qualcomm** | [Soft IP ASIC Engineer Intern](https://go.vansh.nyc/DS?s=y) | Canada |  | unknown | unknown |
| **Qualcomm** | [Telemetry Firmware, Driver and Tools Developer Intern](https://go.vansh.nyc/1jr?s=y) | Canada | hardware | unknown | unknown |
| **Verkada** | [Embedded Software Engineering Intern 2027](https://job-boards.greenhouse.io/verkada/jobs/5211595007) | US | hardware | unknown | unknown |
| **AGCO** | [Embedded Software Engineer Intern](https://careers.agcocorp.com/job/Hesston-Embedded-Software-Engineering-Intern-Summer-2027-KS-67062/1440993300/?ats=successfactors&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Acron Aviation** | [Electrical Engineer Intern - St. Pete Site](https://jobs.lever.co/acronaviation/0cd327f1-0f91-41d0-8b88-093a084fb082) | US | controls,hardware,research | unknown | unknown |
| **Acron Aviation** | [Software Engineer Intern - St. Pete Site](https://jobs.lever.co/acronaviation/19dbac7d-b4fb-4d21-9247-dc610bf55fed) | US | controls,hardware,research | unknown | unknown |
| **Acron Aviation** | [Sustaining Engineer Intern - Grand Rapids Site](https://jobs.lever.co/acronaviation/e2c8a9f9-3b23-4ab9-bbc6-f37401892770) | US | controls,hardware,research | unknown | unknown |
| **AeroVironment** | [Embedded Software Engineer Intern](https://go.vansh.nyc/Ly?s=y) | US / Australia | hardware | unknown | unknown |

_173 more are in [tracker.csv](tracker.csv)._

### Systems & Infra (212 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **DRW** | [Platform Engineer Intern](https://go.vansh.nyc/5p?s=y) | US |  | unknown | unknown |
| **NVIDIA** | [AI Compiler and Kernel Intern](https://go.vansh.nyc/1bR?s=y) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [Compiler Software Engineer Intern](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-WA-Redmond/Compiler-Software-Engineering-Intern---Summer-2027_JR2028607?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Cerebras Systems** | [DevOps Engineer - New Grad 2026](https://jobs.ashbyhq.com/cerebras/40e0d3ee-8f0a-4b19-9bf9-79410b1c7735) | Remote | infra,distributed,research | unknown | unknown |
| **Cerebras Systems** | [Software Engineer - New Grad 2026](https://jobs.ashbyhq.com/cerebras/99c289fa-8fc6-49f7-b7e8-78ac4e9d99ac/application?utm_source=Simplify&ref=Simplify) | US / Canada | hardware,infra,distributed,research | unknown | unknown |
| **Intel** | [Compiler Engineering Intern](https://go.vansh.nyc/9M?s=y) | Canada |  | unknown | unknown |
| **Notion** | [Software Engineer, Early Career \(AI\)](https://jobs.ashbyhq.com/notion/85947779-6b87-466a-98bc-30a640448c28/application?utm_source=Simplify&ref=Simplify) | US | autonomy,infra,distributed | unknown | posting mentions equity |
| **Palantir Technologies** | [Software Engineer Intern, Infrastructure](https://go.vansh.nyc/4q?s=y) | US | infra | unknown | unknown |
| **Palantir Technologies** | [Software Engineer Intern, Production Infrastructure](https://go.vansh.nyc/4t?s=y) | US | infra | unknown | unknown |
| **Perplexity** | [Internship - Search Backend Infra Engineer](https://jobs.ashbyhq.com/Perplexity/be94e89b-89d5-4f2a-a58b-7929c8d97f92) | Serbia | infra,distributed,phd-position | unknown | unknown |
| **Qualcomm** | [Display Systems Engineer Intern](https://go.vansh.nyc/dX?s=y) | Canada |  | unknown | unknown |
| **Qualcomm** | [GPU Compiler Development Intern - Interim Engineering Intern - HW](https://qualcomm.eightfold.ai/careers/job/446722198182?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Qualcomm** | [IT Infrastructure &amp; Cloud Engineering Intern](https://go.vansh.nyc/Rv?s=y) | US | infra | unknown | unknown |
| **Ramp** | [Software Engineering Intern, Android](https://jobs.ashbyhq.com/ramp/fcf118cc-521a-4a62-9d13-945e5b6e3cb8) | US | hardware,infra,funded | unknown | unknown |
| **Ramp** | [Software Engineering Intern, Backend](https://jobs.ashbyhq.com/ramp/acf6b28d-767f-483f-8ff2-114620cd7e04) | US | hardware,infra,funded | unknown | unknown |
| **Ramp** | [Software Engineering Intern, Frontend](https://jobs.ashbyhq.com/ramp/a13ae586-f4cb-4385-8822-c42b9b54ed74) | US | hardware,infra,funded | unknown | unknown |
| **Ramp** | [Software Engineering Intern, iOS](https://jobs.ashbyhq.com/ramp/b66be397-240b-41a6-9b05-493299b270a9) | US | hardware,infra,funded | unknown | unknown |
| **Sierra Nevada Corporation** | [DevOps Engineer Intern 🇺🇸](https://go.vansh.nyc/19u?s=y) | US | infra | unknown | unknown |
| **Snowflake** | [Software Engineering Intern – Developer Platform \(Warsaw, Summer 2027\)](https://jobs.ashbyhq.com/snowflake/a1d72623-8c75-41ce-8980-760ffcbc050c) | Poland | controls,infra | unknown | unknown |
| **APEX Analytix** | [Product Management Intern - DevOps](https://ats.rippling.com/apexanalytix-careers/jobs/101ae05c-1f3c-4d80-9f71-216aa078c164?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **Acron Aviation** | [Systems Engineer Intern - St. Pete Site](https://jobs.lever.co/acronaviation/eaebe6c7-a38f-404f-ba93-210861faf184) | US | controls,hardware | unknown | unknown |
| **Agentis Capital Advisors** | [Investment Banking Summer Analyst - Infrastructure M&amp;A Advisory - Summer 2027](https://jobs.ashbyhq.com/Agentis-Capital-Advisors/af7e9253-cea8-4287-baf9-838a900546b3) | Canada | infra,research | unknown | posting mentions equity |
| **Agoda** | [\[Cooperative Internship 2027\] Data Platform Intern, Devops](https://job-boards.greenhouse.io/agoda/jobs/8358246) | Unknown | infra | unknown | unknown |
| **Agoda** | [\[Cooperative Internship 2027\] Infrastructure Internship BKK](https://job-boards.greenhouse.io/agoda/jobs/8335941) | Unknown | infra | unknown | unknown |
| **Amplify** | [Summer 2027: Software Engineering Intern](https://jobs.ashbyhq.com/amplify/855d22a3-f15e-49f6-854c-29e505653efa/application?embed=true&utm_source=Simplify&ref=Simplify) | US | controls,infra,distributed,research | unknown | unknown |
| **Arcesium** | [Infrastructure Engineer Intern](https://go.vansh.nyc/ga?s=y) | US | infra | unknown | unknown |
| **Arcesiumllc** | [Infrastructure Engineer Intern](https://job-boards.greenhouse.io/arcesiumllc/jobs/5257199007) | US | infra | unknown | unknown |
| **Astreya** | [AI Infrastructure DC Design Intern](https://go.vansh.nyc/8Z?s=y) | US | infra | unknown | unknown |
| **Astro Mechanica** | [Airframe/Structures Engineering Intern](https://jobs.ashbyhq.com/Astro-Mechanica/746a6647-a07d-41ef-91e4-0dfe3a10800b) | US | controls,hardware,infra,research,phd-position,funded | unknown | unknown |
| **Astro Mechanica** | [Electrical/Avionics Engineering Intern](https://jobs.ashbyhq.com/Astro-Mechanica/0916ad59-846f-4635-a68a-276da216a906) | US | hardware,infra,research,phd-position,funded | unknown | unknown |
| **Astro Mechanica** | [Propulsion Engineering Intern](https://jobs.ashbyhq.com/Astro-Mechanica/8406a0b9-d8d6-40ff-b3e1-081a3e68968f) | US | hardware,infra,research,phd-position,funded | unknown | unknown |
| **Astro Mechanica** | [Software Engineering Intern](https://jobs.ashbyhq.com/astro-mechanica/740cedb6-3c69-49c2-8662-7997799b8c87/application?embed=true&utm_source=Simplify&ref=Simplify) | US | controls,hardware,infra,research,phd-position,funded | unknown | unknown |
| **Astro Mechanica** | [Test Engineering Intern](https://jobs.ashbyhq.com/Astro-Mechanica/06ecc8a2-5153-4257-8e54-eb9326a31982) | US | hardware,infra,research,phd-position,funded | unknown | unknown |
| **Atlys** | [Launchpad Fellowship](https://jobs.ashbyhq.com/atlys/53dcce66-f865-4d1e-a6b0-31433d844723) | Unknown | infra,research,funded | unknown | posting mentions equity |
| **Augustus** | [Engineering Fellowship](https://jobs.ashbyhq.com/Augustus/cfdae9c7-93de-482a-9006-68b4c35e0587) | Germany | infra,funded | unknown | unknown |
| **Axelera** | [Hardware Lab Engineer - Internship](https://jobs.ashbyhq.com/axelera/cac5f1c7-2eb7-4bfe-b67f-dfc23dc59c16) | Remote | controls,hardware,infra | unknown | unknown |
| **Backmarket** | [Software Engineer Intern](https://jobs.ashbyhq.com/backmarket/154e6aa0-dbeb-4521-8135-3304118c822b) | France | hardware,infra,climate | unknown | posting mentions equity |
| **Backmarket** | [Software Engineer Intern](https://jobs.ashbyhq.com/backmarket/09ecb805-3072-4e44-a66b-17c4bdb738f5) | Spain | hardware,infra,climate | unknown | posting mentions equity |
| **Base Power** | [Supply Chain Tooling Engineer Intern](https://jobs.ashbyhq.com/base-power/7fce3b16-c132-453b-a836-a3bcbd21abd2) | US | data-eng,research | unknown | unknown |
| **Blue Energy** | [Mechanical Engineering Intern - Summer 27'](https://jobs.ashbyhq.com/blue-energy/8c2d0a73-dc6e-417c-8585-2482d0df2791) | US | hardware,infra,research,climate | unknown | unknown |

_172 more are in [tracker.csv](tracker.csv)._

### Computational Science (95 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **🔥 NVIDIA** | [Technical Marketing Engineer Intern - Digital Biology and Scientific Computing](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Technical-Marketing-Engineering-Intern--Digital-Biology-and-Scientific-Computing---Summer-2027_JR2029793?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship](https://jobs.lever.co/palantir/1b6f1d82-d459-4dea-8bc2-8d2ffe6f881a) | France | autonomy,computer-vision,infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - France](https://jobs.lever.co/palantir/ac0dc094-2480-43c2-8495-26ade227ff4f) | US | infra,funded | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - US Government](https://jobs.lever.co/palantir/315f695d-04d1-4a9a-848e-cb2bec7a997e) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - US Government](https://jobs.lever.co/palantir/e0010393-c300-446f-bf67-fa2ef067f16f) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - US Government](https://jobs.lever.co/palantir/e6ff8bf2-135e-474d-ad37-24f490ae1dd2) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - Warp Speed](https://jobs.lever.co/palantir/b3d81928-6c26-432f-8a0a-36602c2eefcb) | US | autonomy,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - Warp Speed](https://jobs.lever.co/palantir/66b495eb-aaf9-4bf9-a759-41854534add7/apply?utm_source=Simplify&ref=Simplify) | US | autonomy,infra,funded | unknown | unknown |
| **Palantir** | [Software Engineer, Internship](https://jobs.lever.co/palantir/3531977a-9b2f-40a0-a486-4eeb38e75fc1) | Singapore | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship](https://jobs.lever.co/palantir/76a60923-bb49-40f5-b061-7c7eb1299602) | UK | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Infrastructure](https://jobs.lever.co/palantir/fd3603a9-7016-45c6-9c8d-04c9279ab85e) | UK | computer-vision,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Query Engines](https://jobs.lever.co/palantir/da774f81-c98c-4dcf-9b9c-949fd7d90a13) | US | data-eng,infra,distributed,phd-position | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Query Engines](https://jobs.lever.co/palantir/3e59369e-1392-42f2-8d03-86648e87e963) | UK | data-eng,infra,distributed,phd-position | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad](https://jobs.lever.co/palantir/d372c805-d0cd-4a10-9522-fbecc78d6f3e/apply?utm_source=Simplify&ref=Simplify) | UK | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad](https://jobs.lever.co/palantir/2458ba08-de79-4e8f-b553-060f9568727e) | Singapore | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Infrastructure](https://jobs.lever.co/palantir/9265acce-12cd-4179-8c50-55d15963532b) | UK | computer-vision,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Query Engines](https://jobs.lever.co/palantir/0f7d1e01-1f74-4786-944d-910208d390fa/apply?utm_source=Simplify&ref=Simplify) | UK | data-eng,infra,distributed,phd-position | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Query Engines](https://jobs.lever.co/palantir/90329118-d9b7-4b96-acdf-13377e3196ac/apply?utm_source=Simplify&ref=Simplify) | US | data-eng,infra,distributed,phd-position,funded | unknown | unknown |
| **Snowflake** | [Software Engineer Intern - Berlin \(2027\)](https://jobs.ashbyhq.com/snowflake/ab028e3c-c1cf-4455-8915-8e4e6b0cc9e8) | Germany | data-eng,infra,distributed,research,phd-position | unknown | unknown |
| **Snowflake** | [Software Engineer Intern - Zurich \(2027\)](https://jobs.ashbyhq.com/snowflake/26a0ae52-97a6-4a46-9216-3c382570d89b) | Switzerland | controls,hardware,data-eng,infra,distributed,research,phd-position | unknown | unknown |
| **Tesla** | [Physics Engine Development Engineer Intern, Optimus](https://go.vansh.nyc/1aT?s=y) | US |  | unknown | unknown |
| **The Allen Institute for AI** | [Research Intern - Climate Modeling 🎓](https://job-boards.greenhouse.io/thealleninstitute/jobs/8404052?utm_source=Simplify&ref=Simplify) | US | research,climate | unknown | unknown |
| **Americanpublichealthassociation** | [Climate, Health and Equity Internship: 2027 spring term](https://job-boards.greenhouse.io/americanpublichealthassociation/jobs/4434254009) | US | climate | unknown | unknown |
| **Antares Nuclear** | [Multiphysics Software Intern - Summer 2027](https://jobs.ashbyhq.com/Antares/922a527d-9826-446d-9aba-ffc611995830) | US | infra,research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Nuclear Engineering Intern - Summer 2027](https://jobs.ashbyhq.com/Antares/e92ae489-1b1a-4616-a9c8-7c2390698af8) | US | research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Nuclear Operations &amp; Licensing Engineering Intern - Summer 2027](https://jobs.ashbyhq.com/Antares/ec96a761-509f-44e9-90aa-e1fee5388aa1) | Unknown | research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Quality Engineering Intern - Summer 2027](https://jobs.ashbyhq.com/Antares/9335fe9a-a994-4209-bd97-9a6070f4e94f) | US | hardware,research,climate,funded | unknown | unknown |
| **Base Power** | [Electrical Engineering Intern](https://jobs.ashbyhq.com/base-power/7284737d-7e04-43e0-af1f-858103f64e97) | US | hardware | unknown | unknown |
| **Base Power** | [Hardware Engineering Intern](https://jobs.ashbyhq.com/base-power/f22cee0e-55d9-42cd-806e-1c1fc7217770) | US | hardware | unknown | unknown |
| **Base Power** | [Mechanical Engineering Intern](https://jobs.ashbyhq.com/base-power/717274d7-09dc-4176-b307-07301074b87f) | US | hardware | unknown | unknown |
| **Benchling** | [Software Engineer, Intern \(Summer 2027\)](https://jobs.ashbyhq.com/benchling/96370d1b-d35e-446b-8e26-dce088860099/application?embed=true&utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **Biohub** | [Post-Doctoral Fellow, High-Throughput Functional Genomics](https://job-boards.greenhouse.io/biohub/jobs/8393790) | US | bioinformatics,phd-position | unknown | unknown |
| **Blue Cross Blue Shield of Michigan** | [Epidemiology / Biostatistics Intern](https://ejko.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_3/job/14949?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen Hamilton** | [Quantum Computing Research Intern](https://go.vansh.nyc/1qt?s=y) | US | research | unknown | unknown |
| **CAS** | [Cheminformatics Scientist Intern](https://recruiting.ultipro.com/AME1095ACHM/JobBoard/c06ddd6c-8fd2-42b0-96f5-4d70bdc7655a/OpportunityDetail?opportunityId=2225e962-d694-4585-a937-82c9c01b6337&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **CAS** | [Product Management in AI for Chemistry Fellow](https://recruiting.ultipro.com/AME1095ACHM/JobBoard/c06ddd6c-8fd2-42b0-96f5-4d70bdc7655a/OpportunityDetail?opportunityId=f0600bf5-5242-4565-9d1a-021544b8fca1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Commonwealth Fusion Systems** | [Intern - Cryogenics Engineer - Spring 2027](https://jobs.lever.co/cfsenergy/12638cfd-8bad-40b5-88b4-1fe3b21aec8f) | US | controls,hardware,research,phd-position | unknown | unknown |
| **Commonwealth Fusion Systems** | [Intern - EHS Engineer - Spring or Summer 2027](https://jobs.lever.co/cfsenergy/3e88978c-ff6e-461a-997a-2a7a6ffb3fea) | US | controls,research,phd-position | unknown | unknown |
| **Commonwealth Fusion Systems** | [Intern - Electrical Engineer, RF Heating Systems - Spring 2027](https://jobs.lever.co/cfsenergy/a3a36962-1f34-40d3-b138-401b4e0c24e0) | US | controls,hardware,research,phd-position | unknown | unknown |
| **Commonwealth Fusion Systems** | [Intern - Fusion Fuel Systems - Spring or Summer 2027](https://jobs.lever.co/cfsenergy/b464985c-bfc2-4efb-91db-7dd1a92f8f4b) | US | controls,hardware,research,phd-position | unknown | unknown |

_55 more are in [tracker.csv](tracker.csv)._

### HCI / XR (10 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **🔥 Figma** | [PhD Intern - Software Engineer - Interaction Design 🎓](https://boards.greenhouse.io/figma/jobs/6241542004?utm_source=Simplify&ref=Simplify) | US | phd-position | unknown | unknown |
| **OpenArt AI** | [Early Adopter &amp; Product Builder Intern, Creative AI](https://jobs.ashbyhq.com/openart/8dd52ba6-a5b6-40b1-95fe-50de352fa254) | US | research | unknown | unknown |
| **Simular** | [Design Engineer Intern](https://jobs.ashbyhq.com/simular/3c53a046-4fc0-4b67-9295-1912abf16262) | Singapore | autonomy,controls | unknown | unknown |
| **Tacit** | [Antenna Engineering Intern \(Fall 2026\)](https://jobs.ashbyhq.com/tacit/9d8cf04c-4033-40ff-9af4-91dd8e4f02c6) | US | hardware,neuroscience,phd-position | unknown | unknown |
| **Tacit** | [RF Hardware Intern \(Fall 2026\)](https://jobs.ashbyhq.com/tacit/d001e2d9-90af-4d0b-bc97-fd6fa149ad19) | US | controls,hardware,infra,neuroscience,phd-position | unknown | unknown |
| **Tacit** | [System Electrical Engineer Intern](https://jobs.ashbyhq.com/tacit/cadc8b71-ee79-4b44-951b-da7c5a0142eb) | US | manipulation,hardware,neuroscience,phd-position | unknown | unknown |
| **Toyota Research Institute** | [Future Product Innovation Research Intern, Computational Cognitive Science](https://jobs.lever.co/tri/0d74ff26-05cc-4616-bda0-97d821c9452b) | US | autonomy,rl,multimodal,research,neuroscience,phd-position | unknown | unknown |
| **Toyota Research Institute** | [Human-Centered AI Research Intern, Human Language Models](https://jobs.lever.co/tri/d4184c04-b963-489a-9a0b-91bc57d6267e/apply?utm_source=Simplify&ref=Simplify) | US | llm,computer-vision,research,phd-position | unknown | unknown |
| **Toyota Research Institute** | [Robotics Intern, Teleoperation and Spatial Computing](https://jobs.lever.co/tri/4ea8d663-1060-4c55-aede-91fd8f945871) | US | perception,controls,manipulation,robot-software,hardware,research | unknown | unknown |
| **Toyota Research Institute** | [Robotics Intern, UX Design](https://jobs.lever.co/tri/2d9833d5-a940-4862-b13b-a1ecc9378fea) | US | controls,robot-software,hardware,research | unknown | unknown |

### Early-company / equity reality check

The company signal is a discovery aid, not a prediction. Private-company options can become valuable, but can also expire, dilute, remain illiquid, or end up worth zero. `private company; verify offer` means the posting does not prove that equity is included. Ask for the option count **and fully diluted percentage**, strike price, vesting/cliff, exercise window, latest common valuation, and liquidation preferences.

## Elite and high-tier live postings (644)

| Company | Role | Category | Region | Term | Eligibility |
|--|--|--|--|--|--|
| **Akuna Capital** | [Junior Quantitative Developer &amp; Strategist](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8065007?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Akuna Capital** | [Junior Quantitative Researcher](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8065206?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Akuna Capital** | [Junior Quantitative Researcher - Harvard](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8065211?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Akuna Capital** | [Quantitative Development &amp; Strategy Intern, Summer 2027 \| Harvard](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8066880) | Quant / Finance | US | Summer 2027 | review required |
| **Akuna Capital** | [Quantitative Development &amp; Strategy Intern, Summer 2027 \| Massachusetts Institute of Technology](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8066884) | Quant / Finance | US | Summer 2027 | review required |
| **Akuna Capital** | [Quantitative Research Intern 🇺🇸](https://www.akunacapital.com/careers/job/8036614/?gh_jid=8036614) | Quant / Finance | US | Summer 2027 | review required |
| **Akuna Capital** | [Quantitative Research Intern, Summer 2027 \| Columbia University](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8065680) | Quant / Finance | US | Summer 2027 | review required |
| **Akuna Capital** | [Quantitative Research Intern, Summer 2027 \| Georgia Institute of Technology](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8065656) | Quant / Finance | US | Summer 2027 | review required |
| **Akuna Capital** | [Quantitative Research Intern, Summer 2027 \| Massachusetts Institute of Technology](https://job-boards.greenhouse.io/akunacapitaloci/jobs/8065670) | Quant / Finance | US | Summer 2027 | review required |
| **Akuna Capital** | [Software Engineer Intern \(Summer 2027, Python / C++ / Full Stack / C# .NET\)](https://akunacapital.com/careers/job/8018847/) | Software Engineering | US | Summer 2027 | review required |
| **Akuna Capital** | [Software Engineer Intern - Python, Summer 2027](https://www.akunacapital.com/careers/job/8018853/?gh_jid=8018853) | Software Engineering | US | Summer 2027 | review required |
| **Akuna Capital University** | [Junior Quantitative Developer &amp; Strategist](https://www.akunacapital.com/careers/job/8016687/?gh_jid=8016687&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Akuna Capital University** | [Junior Quantitative Researcher](https://www.akunacapital.com/careers/job/8036541/?gh_jid=8036541&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Amazon** | [ASIC Engineer Intern](https://go.vansh.nyc/hA?s=y) | Hardware / EE | US | Summer 2027 | review required |
| **Amazon** | [Frontier AI &amp; Robotics Intern](https://go.vansh.nyc/eL?s=y) | Robotics &amp; Embodied AI | US | Summer 2027 | review required |
| **Amazon** | [Machine Learning Systems Software Development Engineer Intern, Annapurna Labs](https://go.vansh.nyc/MP?s=y) | AI / ML | Canada | Summer 2027 | review required |
| **Amazon** | [Software Development Engineer Intern](https://go.vansh.nyc/IN?s=y) | Software Engineering | Canada | Summer 2027 | review required |
| **Amazon** | [Software Development Engineer Intern](https://go.vansh.nyc/IL?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Amazon** | [Software Development Engineer Intern, Amazon Leo 🇺🇸](https://go.vansh.nyc/hR?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Amazon** | [Software Development Engineer Intern, Amazon Leo, Embedded Systems 🇺🇸](https://go.vansh.nyc/g6?s=y) | Hardware / EE | US | Summer 2027 | review required |
| **Amazon** | [Software Development Engineer Intern, Annapurna Labs](https://go.vansh.nyc/17u?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Amazon** | [Software Development Engineer Intern, Embedded Systems](https://go.vansh.nyc/g0?s=y) | Hardware / EE | US | Summer 2027 | review required |
| **Amazon** | [Software Development Engineer Intern, Machine Learning/Automated Reasoning](https://go.vansh.nyc/10y?s=y) | AI / ML | US | Summer 2027 | review required |
| **Amazon** | [Software Development Engineer Intern, Robotics](https://go.vansh.nyc/Mg?s=y) | Robotics &amp; Embodied AI | US | Summer 2027 | review required |
| **Amazon** | [Software Development Engineer Intern, Robotics](https://go.vansh.nyc/17r?s=y) | Robotics &amp; Embodied AI | Canada | Summer 2027 | review required |
| **Anthropic** | [Research Associate, Biology](https://job-boards.greenhouse.io/anthropic/jobs/5285248008) | Software Engineering | US | Unknown | review required |
| **Apple** | [Applied Data Solutions Program Intern](https://go.vansh.nyc/17v?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Apple** | [Hardware Engineering Intern](https://go.vansh.nyc/1tl?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Apple** | [Hardware Technologies Engineering Intern](https://go.vansh.nyc/1tk?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Apple** | [Machine Learning and Artificial Intelligence Undergrad Intern](https://go.vansh.nyc/19Z?s=y) | AI / ML | US | Summer 2027 | review required |
| **Apple** | [Software Engineer Intern, Undergrad](https://go.vansh.nyc/33?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Apple** | [Software Engineering Intern, Masters](https://go.vansh.nyc/32?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Apple Bank** | [IT Data Intern - Analytics, &amp; Automation](https://applebank.wd5.myworkdayjobs.com/applebankcareers/job/New-York-NY/XMLNAME-2027-Summer-Intern--IT-Data--Analytics----Automation_2026-1414?utm_source=Simplify&ref=Simplify) | Data | US | Summer 2027 | review required |
| **Apple Bank** | [Information Security Intern 🛂](https://go.vansh.nyc/VV?s=y) | Security | US | Summer 2027 | work-rights review |
| **Citadel** | [Quantitative Research Analyst University Graduate](https://www.citadel.com/careers/details/quantitative-research-analyst-university-graduate-us/?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Citadel** | [Quantitative Trader: Equity Quantitative Research – University Graduate](https://www.citadel.com/careers/details/quantitative-trader-equity-quantitative-research-university-graduate-us/?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Citadel** | [Software Engineer Intern](https://go.vansh.nyc/3a?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Citadel** | [Software Engineer – University Graduate](https://www.citadel.com/careers/details/software-engineer-university-graduate-us/?utm_source=Simplify&ref=Simplify) | Software Engineering | US | New Grad 2026 | review required |
| **Citadel Securities** | [Quantitative Research Analyst – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-research-analyst-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | Quant / Finance | UK / Ireland | New Grad 2026 | review required |
| **Citadel Securities** | [Quantitative Trader – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-us-miami/?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Citadel Securities** | [Quantitative Trader – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-us-new-york/?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Citadel Securities** | [Software Engineer – University Graduate](https://www.citadelsecurities.com/careers/details/software-engineer-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | Software Engineering | UK | New Grad 2026 | review required |
| **Cubist Systematic Strategies** | [Quantitative Developer Intern](https://job-boards.greenhouse.io/point72/jobs/7297613002) | Quant / Finance | US | Summer 2027 | review required |
| **DE Shaw** | [Software Developer Intern](https://www.deshaw.com/careers/software-developer-intern-new-york-summer-2027-5894) | Software Engineering | US | Summer 2027 | review required |
| **DRW** | [AI/ML Research Intern](https://go.vansh.nyc/5o?s=y) | Software Engineering | Unknown | Summer 2027 | review required |
| **DRW** | [FPGA Intern](https://go.vansh.nyc/5n?s=y) | Hardware / EE | US | Summer 2027 | review required |
| **DRW** | [Platform Engineer Intern](https://go.vansh.nyc/5p?s=y) | Systems &amp; Infra | US | Summer 2027 | review required |
| **DRW** | [Quantitative Research Intern](https://job-boards.greenhouse.io/drweng/jobs/7818540) | Quant / Finance | US | Ambiguous | review required |
| **DRW** | [Quantitative Research Intern](https://job-boards.greenhouse.io/drweng/jobs/7957756) | Quant / Finance | UK | None | review required |
| **DRW** | [Quantitative Research Intern](https://job-boards.greenhouse.io/drweng/jobs/8014915) | Quant / Finance | Singapore | None | review required |
| **DRW** | [Quantitative Trading Analyst Intern](https://job-boards.greenhouse.io/drweng/jobs/7668776) | Quant / Finance | US | Ambiguous | review required |
| **DRW** | [Quantitative Trading Analyst Intern](https://job-boards.greenhouse.io/drweng/jobs/7957243) | Quant / Finance | UK | None | review required |
| **DRW** | [Software Developer Intern](https://go.vansh.nyc/5t?s=y) | Software Engineering | US | Summer 2027 | review required |
| **DRW** | [Software Developer Intern](https://go.vansh.nyc/5s?s=y) | Software Engineering | Unknown | Summer 2027 | review required |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/7942281) | Software Engineering | UK | None | review required |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/8020364) | Software Engineering | Netherlands | None | review required |
| **DRW** | [Software Developer Intern - Industrial Placement](https://job-boards.greenhouse.io/drwuniversityjobs/jobs/7364884) | Software Engineering | UK | None | review required |
| **Five Rings** | [Quantitative Trader Intern \(Summer 2027\)](https://job-boards.greenhouse.io/fiveringsllc/jobs/5139668008) | Quant / Finance | US | Summer 2027 | review required |
| **Five Rings** | [Software Developer Intern 🇺🇸](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349707008) | Software Engineering | US | Summer 2027 | review required |
| **G-Research** | [Machine Learning Engineer Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Machine-Learning-Engineer-Intern_R3773?utm_source=Simplify&ref=Simplify) | AI / ML | UK | Ambiguous | review required |
| **Google** | [Software Engineering Intern, BS \(Summer 2027\)](https://www.google.com/about/careers/applications/jobs/results/85564713261245126-software-engineering-intern/) | Software Engineering | US | Summer 2027 | review required |
| **Hudson River Trading** | [Algorithm Developer New Grad - Quant Researcher](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8052050&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Hudson River Trading** | [Data Scientist Intern](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8257369&utm_source=Simplify&ref=Simplify) | Quant / Finance | US / UK | Ambiguous | review required |
| **Hudson River Trading** | [Data Scientist Intern](https://go.vansh.nyc/1A5?s=y) | Quant / Finance | US | Summer 2027 | review required |
| **Hudson River Trading** | [FPGA Verification and Developer Intern](https://go.vansh.nyc/QI?s=y) | Quant / Finance | US | Summer 2027 | review required |
| **Hudson River Trading** | [Software Engineer Intern](https://go.vansh.nyc/3F?s=y) | Quant / Finance | US | Summer 2027 | review required |
| **Hudson River Trading** | [Software Engineering Intern \(Summer 2027, C++ / Python\)](https://www.hudsonrivertrading.com/hrt-job/software-engineering-internship-c-or-python-summer-2027/) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Deep Learning Research Intern - 2027 - Sydney](https://job-boards.eu.greenhouse.io/imc/jobs/4956547101) | Quant / Finance | Australia | 2027 | review required |
| **IMC Trading** | [Deep Learning Research Intern - Summer 2027 - Amsterdam](https://job-boards.eu.greenhouse.io/imc/jobs/4912874101) | Quant / Finance | Netherlands | Summer 2027 | review required |
| **IMC Trading** | [Graduate Quantitative Researcher \(PhD\)](https://job-boards.eu.greenhouse.io/imc/jobs/4912325101) | Quant / Finance | US | Unknown | review required |
| **IMC Trading** | [Hardware Engineer Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4823945101) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Hardware Machine Learning PhD Research Internship](https://job-boards.eu.greenhouse.io/imc/jobs/4975945101) | Quant / Finance | US | Unknown | review required |
| **IMC Trading** | [Machine Learning Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4962456101?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Machine Learning Engineer Intern](https://go.vansh.nyc/1nv?s=y) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Machine Learning Research Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4907430101) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Quant Performance Engineer Intern - Summer 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4842595101) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Quantitative Research Intern \(Summer 2027, BS / MS\)](https://job-boards.eu.greenhouse.io/imc/jobs/4907399101) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Quantitative Research Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941208101) | Quant / Finance | Hong Kong | 2027 | review required |
| **IMC Trading** | [Quantitative Trader Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4936262101) | Quant / Finance | Netherlands | Unknown | review required |
| **IMC Trading** | [Quantitative Trader Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4823923101) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Quantitative Trader Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941205101) | Quant / Finance | Hong Kong | 2027 | review required |
| **IMC Trading** | [Research Analyst Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823946101?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Software Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4667854101) | Quant / Finance | Netherlands | Unknown | review required |
| **IMC Trading** | [Software Engineer Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4823924101) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Software Engineer Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941206101) | Quant / Finance | Hong Kong | 2027 | review required |
| **IMC Trading** | [Software Engineer, Early Career](https://job-boards.eu.greenhouse.io/imc/jobs/4796143101) | Quant / Finance | US | Unknown | review required |
| **IMC Trading** | [Trader Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4939846101) | Quant / Finance | Netherlands | Unknown | review required |
| **Jane Street** | [Cybersecurity Analyst Intern](https://go.vansh.nyc/41?s=y) | Security | US | Summer 2027 | review required |
| **Jane Street** | [Data Engineer Intern](https://go.vansh.nyc/42?s=y) | Data | US | Summer 2027 | review required |
| **Jane Street** | [Fundamental Research Analyst Intern](https://go.vansh.nyc/43?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Jane Street** | [Linux Engineer Intern](https://go.vansh.nyc/45?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Jane Street** | [Machine Learning Engineer Intern](https://go.vansh.nyc/3Z?s=y) | AI / ML | US | Summer 2027 | review required |
| **Jane Street** | [Machine Learning Researcher Intern](https://go.vansh.nyc/40?s=y) | AI / ML | US | Summer 2027 | review required |
| **Jane Street** | [Quantitative Researcher Intern](https://go.vansh.nyc/3Y?s=y) | Quant / Finance | US | Summer 2027 | review required |
| **Jane Street** | [Quantitative Trader Intern](https://go.vansh.nyc/3X?s=y) | Quant / Finance | US | Summer 2027 | review required |
| **Jane Street** | [Sales and Trading Intern](https://go.vansh.nyc/47?s=y) | Quant / Finance | US | Summer 2027 | review required |
| **Jane Street** | [Software Engineer Intern](https://go.vansh.nyc/4c?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Jane Street** | [Tools and Compilers Research and Development Intern](https://go.vansh.nyc/48?s=y) | Software Engineering | US | Summer 2027 | review required |
| **Jane Street** | [Trading Desk Operations Engineer Intern](https://go.vansh.nyc/49?s=y) | Quant / Finance | US | Summer 2027 | review required |
| **Jane Street** | [Windows Engineer Intern](https://go.vansh.nyc/4a?s=y) | Software Engineering | US | Summer 2027 | review required |

_544 more are in [tracker.csv](tracker.csv)._

## Planned spring / insight programmes

These are expected programme windows, not verified-open applications.

| Company | Programme | Window | Link |
|--|--|--|--|
| **Barclays** | Technology Spring Intern \(UK\) | Nov–Jan 2027 | [Check official page](https://home.barclays/careers/) |
| **Citadel** | Discover Citadel \(Spring Week\) | Oct–Nov 2026 | [Check official page](https://www.citadel.com/careers/) |
| **Five Rings** | Summer Smash / Insight Event | Rolling | [Check official page](https://fiverings.com/careers/) |
| **Goldman Sachs** | Engineering Spring Insight \(UK\) | Oct–Dec 2026 | [Check official page](https://www.goldmansachs.com/careers/) |
| **Hudson River Trading** | Insight Day / Campus Event | Rolling | [Check official page](https://www.hudsonrivertrading.com/careers/) |
| **IMC Trading** | Insight Day | Rolling Oct–Feb | [Check official page](https://www.imc.com/eu/careers/) |
| **JP Morgan** | Technology Spring Week \(UK\) | Oct–Nov 2026 | [Check official page](https://careers.jpmorgan.com/) |
| **Jane Street** | FOCUS \(First-Year Insight\) | Oct–Nov 2026 | [Check official page](https://www.janestreet.com/join-jane-street/open-roles/) |
| **Morgan Stanley** | Technology Spring Insight \(UK\) | Oct–Dec 2026 | [Check official page](https://www.morganstanley.com/people-opportunities/) |
| **Optiver** | Insight Day / Spring Program | Rolling Oct–Feb | [Check official page](https://optiver.com/working-at-optiver/career-opportunities/) |
| **Susquehanna \(SIG\)** | Quant Finance Insight Days | Rolling | [Check official page](https://careers.sig.com/) |
| **Two Sigma** | Discovery Program | Oct–Jan 2027 | [Check official page](https://careers.twosigma.com/careers/jobListings) |

## Filtering and application workflow

Open [tracker.csv](tracker.csv) in a spreadsheet. Useful columns include `category`, `focus_tags`, `company_type`, `region`, `work_mode`, `term`, `level`, `eligibility`, `source_status`, and `equity_signal`.

- `source_status=open` means the individual posting was returned by a live source.
- `watchlist` or `planned` is a career hub, not proof of an opening.
- `stale/source-error` is protected during an outage; it is not closed.
- A role closes only after two consecutive healthy runs do not see it.
- Run `python3 copilot.py` for local triage, or `python3 -m autoapply doctor` for the guarded local application pipeline.

See [manual_checks.md](manual_checks.md) for official robotics and elite career pages that need a browser check.

---

The watcher is free and uses public job feeds. Always verify the posting and every application answer before approval.
