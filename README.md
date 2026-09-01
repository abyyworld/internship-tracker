# 🎯 Universal Academic & Career Tracker — Internships · Research · PhD · New Grad

<p align="center">
  <a href="https://abyyworld.github.io/internship-tracker/"><img alt="Open the tracker — 1510 open postings" src="https://img.shields.io/badge/Open%20the%20tracker-1510%20open%20postings-1f6feb?style=for-the-badge&labelColor=0d1117"></a>
  <a href="https://abyyworld.github.io/internship-tracker/studio.html"><img alt="Tailor my CV — in the browser" src="https://img.shields.io/badge/Tailor%20my%20CV-in%20the%20browser-2ea043?style=for-the-badge&labelColor=0d1117"></a>
</p>

<p align="center"><b><a href="https://abyyworld.github.io/internship-tracker/">https://abyyworld.github.io/internship-tracker/</a></b><br>
Search and filter every posting, then tailor your CV for one — in the browser, on a phone, with nothing to install.</p>

> Last verified run: **2026-09-01** · **1510 verified-open postings** · **40 research / PhD / postdoc positions**

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

> ⚠️ **5 previously seen roles are stale because at least one source failed or was not checked. They were not marked closed.**

## At a glance

| Metric | Count |
|--|--:|
| Verified-open postings | 1510 |
| Roles discovered today | 159 |
| New verified postings | 159 |
| Research / PhD / postdoc positions | 40 |
| Elite tier | 217 |
| High tier | 191 |
| Eligibility still needs review | 1510 |
| Deadlines within 10 days | 0 |

**By category:** Software Engineering 780 · Quant / Finance 194 · AI / ML 134 · Robotics & Embodied AI 115 · Data 106 · Hardware / EE 68 · Security 54 · Systems & Infra 38 · Computational Science 21

**By region:** US 1273 · UK 77 · Canada 55 · Unknown 29 · Singapore 12 · Netherlands 9 · US / Canada 5 · Hong Kong 4 · Ireland 4 · Switzerland 4 · US / Austria 3 · Singapore / China / Hong Kong / Australia 2 · US / Australia 2 · UK / Ireland 2 · Australia 2 · China / Hong Kong 2 · France 2 · US / Global 2 · South Korea 2 · Serbia 2 · US / Italy 2 · US / UAE 2 · US / UK 2 · Spain 1 · US / India 1 · Singapore / China / Hong Kong 1 · US / France / Singapore / Hong Kong 1 · Remote 1 · Germany 1 · Poland 1 · India 1 · US / Canada / UK 1 · US / Europe 1 · UK / Australia 1

**By degree evidence:** Unknown 1267 · Advanced/unknown 144 · PhD 51 · Undergraduate eligible 39 · Masters 9

## Newly opened (159)

| Company | Role | Category | Region | Term | Eligibility |
|--|--|--|--|--|--|
| **Hudson River Trading** | [Hardware Engineer Intern](https://www.hudsonrivertrading.com/careers/job/?gh_jid=7899574&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Ambiguous | review required |
| **Tower Research Capital** | [Quantitative Researcher Intern, Bachelor or Master](https://www.tower-research.com/open-positions/?gh_jid=8168750) | Quant / Finance | Singapore / China / Hong Kong / Australia | Unknown | review required |
| **Tower Research Capital** | [Quantitative Researcher Intern, PhD or Postdoc](https://www.tower-research.com/open-positions/?gh_jid=8168634) | Quant / Finance | Singapore / China / Hong Kong / Australia | Unknown | review required |
| **🔥 Google** | [Software Engineer Intern - Multiple Teams](https://www.google.com/about/careers/applications/jobs/results/94172495052972742?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **🔥 Google** | [Software Engineer Intern - Multiple Teams](https://www.google.com/about/careers/applications/jobs/results/100648618540573382?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Sierra** | [Software Engineer Intern](https://jobs.ashbyhq.com/Sierra/34b31b67-268c-4270-b48f-72e59064c96e/application?embed=true&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Sierra** | [Software Engineer, Agent \(New Grad 2027\)](https://jobs.ashbyhq.com/Sierra/149f368c-52d5-408f-ba26-ad888f318a00/application?embed=true&utm_source=Simplify&ref=Simplify) | AI / ML | US | 2027 | review required |
| **Stripe** | [Software Engineer, Intern](https://stripe.com/jobs/search?gh_jid=8130867) | Software Engineering | UK | Unknown | review required |
| **Stripe** | [Software Engineer, Intern](https://stripe.com/jobs/search?gh_jid=8130807) | Software Engineering | Unknown | Unknown | review required |
| **Stripe** | [Software Engineer, Intern \(Summer or Winter\)](https://stripe.com/jobs/search?gh_jid=8130805) | Software Engineering | Canada | Summer | review required |
| **Stripe** | [Software Engineer, Intern \(Summer or Winter\)](https://stripe.com/jobs/search?gh_jid=8128745) | Software Engineering | US | Summer | review required |
| **Stripe** | [Software Engineer, New Grad](https://stripe.com/jobs/search?gh_jid=8130922) | Software Engineering | Unknown | Unknown | review required |
| **Stripe** | [Software Engineer, New Grad](https://stripe.com/jobs/search?gh_jid=8130881) | Software Engineering | Unknown | Unknown | review required |
| **Stripe** | [Software Engineer, New Grad - Frontend](https://stripe.com/jobs/search?gh_jid=8130927) | Software Engineering | Spain | Unknown | review required |
| **🔥 AMD** | [Diagnostics Design Engineer Intern/Co-op](https://careers.amd.com/jobs/90435?icims=1&utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | Ambiguous | review required |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op](https://careers.amd.com/jobs/91320?icims=1&utm_source=Simplify&ref=Simplify) | Hardware / EE | Canada | Ambiguous | review required |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op](https://careers.amd.com/jobs/91313?icims=1&utm_source=Simplify&ref=Simplify) | Hardware / EE | Canada | Ambiguous | review required |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op - Long Term](https://careers.amd.com/jobs/90297?icims=1&utm_source=Simplify&ref=Simplify) | Hardware / EE | Canada | Ambiguous | review required |
| **🔥 AMD** | [Graphics Software Engineer Intern/Co-op](https://careers.amd.com/jobs/90305?icims=1&utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | Ambiguous | review required |
| **🔥 AMD** | [Hardware Design Engineer Intern/Co-op](https://careers.amd.com/jobs/91360?icims=1&utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | Ambiguous | review required |
| **🔥 AMD** | [Hardware Design Engineer Intern/Co-op](https://careers.amd.com/jobs/90372?icims=1&utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | Ambiguous | review required |
| **🔥 AMD** | [Hardware Design Engineer Intern/Co-op - Long Term](https://careers.amd.com/jobs/90367?icims=1&utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | Ambiguous | review required |
| **🔥 AMD** | [Hardware Design Verification Engineer Intern/Co-op](https://careers.amd.com/jobs/90379?icims=1&utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | Ambiguous | review required |
| **🔥 AMD** | [Hardware Design Verification Engineer Intern/Co-op](https://careers.amd.com/jobs/91362?icims=1&utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | Ambiguous | review required |
| **🔥 AMD** | [Machine Learning/Artificial Intelligence Intern/Co-op](https://careers.amd.com/jobs/91363?icims=1&utm_source=Simplify&ref=Simplify) | AI / ML | Canada | Ambiguous | review required |
| **🔥 AMD** | [Software Engineer Intern/Co-op](https://careers.amd.com/jobs/91366?icims=1&utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | Ambiguous | review required |
| **🔥 AMD** | [Software Engineer Intern/Co-op](https://careers.amd.com/jobs/91367?icims=1&utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | Ambiguous | review required |
| **🔥 AMD** | [Software Engineer Intern/Co-op](https://careers.amd.com/jobs/91368?icims=1&utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | Ambiguous | review required |
| **🔥 Stripe** | [Software Engineer New Grad](https://stripe.com/jobs/search?gh_jid=8128744&utm_source=Simplify&ref=Simplify) | Software Engineering | US | New Grad 2026 | review required |
| **🔥 Stripe** | [Software Engineer New Grad](https://stripe.com/jobs/search?gh_jid=8130930&utm_source=Simplify&ref=Simplify) | Software Engineering | UK | New Grad 2026 | review required |
| **🔥 Waymo** | [Data Science Intern - Commercialization Testing 🎓](https://careers.withwaymo.com/jobs?gh_jid=8167323&utm_source=Simplify&ref=Simplify) | Robotics &amp; Embodied AI | US | Summer 2027 | review required |
| **Aerotech** | [Electrical/Computer Engineering Intern Co-op](https://aerotech.applytojob.com/apply/FrPUDToawu/ElectricalComputer-Engineering-Internship-Or-Coop-2027?utm_source=Simplify&ref=Simplify) | Software Engineering | US | 2027 | review required |
| **Aerotech** | [Software Engineering Intern Co-op - Enterprise Development Team - Application Development Team](https://aerotech.applytojob.com/apply/OFIYSpO0HW/Software-Engineering-Internship-Or-Coop-2027?utm_source=Simplify&ref=Simplify) | Software Engineering | US | 2027 | review required |
| **Alation** | [UX Software Engineer 1 - Contractor](https://alation.wd503.myworkdayjobs.com/ExternalSite/job/USA-CA-REDWOOD-CITY/UX-Software-Engineer-I--Contractor-_R10000770?utm_source=Simplify&ref=Simplify) | Software Engineering | US | New Grad 2026 | review required |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012703?utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012782?utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012784?utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012783?utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **American Express** | [Data Analytics Intern - US Consumer Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26011607?utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **American Express** | [Data Engineer Intern - Enterprise Technology Services](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012333?utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **American Express** | [Data Engineer Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012781?utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **American Express** | [Data Engineer Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012764?utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **American Express** | [Data Management Intern - Global Merchant &amp; Network Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012668?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **American Express** | [Data Science Intern - Finance](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26013190?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **American Express** | [Digital Product Management Intern - Enterprise Technology Services](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26011143?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Arch Capital Group** | [Data and Analytics Intern](https://archgroup.wd1.myworkdayjobs.com/careers/job/Farmington-CT-United-States-of-America/Data-and-Analytics-Intern_R26_845?utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **BP** | [Finance &amp; Risk Intern - Supply, Trading, &amp; Shipping](https://bpinternational.wd3.myworkdayjobs.com/bpPrivateExternalCareersSite/job/United-States-of-America---Illinois---Chicago/Summer-Internship---Supply--Trading----Shipping-Finance---Risk---Chicago--IL_RQ115370?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer | review required |
| **BP** | [Finance &amp; Risk Intern - Supply, Trading, &amp; Shipping](https://bpinternational.wd3.myworkdayjobs.com/bpPrivateExternalCareersSite/job/United-States-of-America---Texas---Houston/Summer-Internship---Supply--Trading----Shipping-Finance---Risk---Houston--TX_RQ115372?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer | review required |
| **Blackhawk Network Holdings** | [Technology Intern](https://careers-blackhawknetwork.icims.com/jobs/26867/job?mobile=true&needsRedirect=false&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Blue Origin** | [Avionics / Embedded Software Engineer 1 - 2027 Starts](https://blueorigin.wd5.myworkdayjobs.com/blueorigin/job/Greater-Seattle-Area/Avionics---Embedded-Software-Engineer-I---Early-Career--2027-Starts-_R71324?utm_source=Simplify&ref=Simplify) | Hardware / EE | US | 2027 | review required |
| **Blue Origin** | [Software Development Engineer 1 - Early Career - 2027 Starts](https://blueorigin.wd5.myworkdayjobs.com/blueorigin/job/Greater-Seattle-Area/Software-Development-Engineer-I---Early-Career--2027-Starts-_R71326?utm_source=Simplify&ref=Simplify) | Software Engineering | US | 2027 | review required |
| **BlueCross BlueShield of Nebraska** | [Data Intern - Data Science - Data Analytics](https://nebraskablue.wd1.myworkdayjobs.com/BCBSNE/job/Omaha-NE/Data-Intern--Summer-2027_JR101406?utm_source=Simplify&ref=Simplify) | Data | US | Summer 2027 | review required |
| **BlueCross BlueShield of Nebraska** | [Digital Experience Information Systems Intern](https://nebraskablue.wd1.myworkdayjobs.com/BCBSNE/job/Omaha-NE/IS-Intern--Summer-2027_JR101404?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **Bosch Home Comfort** | [AI Application Intern](https://jobs.smartrecruiters.com/BoschGroup/744000146547599?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Bosch Home Comfort** | [Calibration Process Optimization Intern](https://jobs.smartrecruiters.com/BoschGroup/744000146526409?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Bosch Home Comfort** | [Software Engineer Intern](https://jobs.smartrecruiters.com/BoschGroup/744000146546849?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Brunswick** | [Software Controls Engineer Intern](https://brunswick.wd1.myworkdayjobs.com/en-US/search/job/Fond-du-Lac-WI/Mercury-Marine--Software-Controls-Engineering-Intern_JR-051436?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **C3.ai** | [Data Scientist Intern - Summer 2027 🎓](https://c3.ai/job-description/8738918002?gh_jid=8738918002&utm_source=Simplify&ref=Simplify) | Data | US | Summer 2027 | review required |
| **C3.ai** | [Software Engineer Intern](https://c3.ai/job-description/8739037002?gh_jid=8739037002&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **CACI** | [Software Engineer Co-op - Spring &amp; Summer 2027](https://caci.wd1.myworkdayjobs.com/external/job/Danbury-CT-US/Software-Engineering-Co-op---Spring---Summer-2027_331356-1?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Spring/Summer 2027 | review required |

_99 more are in [tracker.csv](tracker.csv)._

## Browse by category

Every category is listed the same way. Live geography reflects what official feeds expose today; the worldwide career-hub and academic watchlists are kept separately in [manual_checks.md](manual_checks.md).

### Software Engineering (780 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Python Software Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018853/?gh_jid=8018853&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer \(Entry-Level\) - Python](https://www.akunacapital.com/careers/job/8013230/?gh_jid=8013230) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer Intern \(Summer 2027, Python / C++ / Full Stack / C# .NET\)](https://akunacapital.com/careers/job/8018847/) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer Intern, C# .NET Desktop](https://akunacapital.com/careers/job/8018886/?gh_jid=8018886&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer Intern, C++ 🇺🇸](https://akunacapital.com/careers/job/8018847/?gh_jid=8018847&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer Intern, Full Stack Web 🇺🇸](https://akunacapital.com/careers/job/8018893/?gh_jid=8018893&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Apple** | [Software Engineer Intern, Undergrad](https://jobs.apple.com/en-us/details/200664785/software-undergrad-engineering-internships?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Apple** | [Software Engineering Intern, Masters](https://jobs.apple.com/en-us/details/200664320/software-engineering-masters-internships?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Citadel** | [Software Engineer Intern](https://www.citadel.com/careers/details/software-engineer-intern-us/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Citadel** | [Software Engineer – University Graduate](https://www.citadel.com/careers/details/software-engineer-university-graduate-us/?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Citadel Securities** | [Software Engineer – University Graduate](https://www.citadelsecurities.com/careers/details/software-engineer-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **DE Shaw** | [Software Developer Intern](https://www.deshaw.com/careers/software-developer-intern-new-york-summer-2027-5894?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **DRW** | [AI/ML Research Intern](https://www.drw.com/work-at-drw/listings/aiml-research-intern-3466679?utm_source=github-vansh-ouckah) | Unknown | research | unknown | unknown |
| **DRW** | [Software Developer Intern](https://www.drw.com/work-at-drw/listings/software-developer-intern-3467328?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **DRW** | [Software Developer Intern](https://www.drw.com/work-at-drw/listings/software-developer-intern-3466687?utm_source=github-vansh-ouckah) | Unknown |  | unknown | unknown |
| **Five Rings** | [Software Developer Intern 🇺🇸](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349707008?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **G-Research** | [Data Science Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Data-Science-Internship_R3679?utm_source=Simplify&ref=Simplify) | UK | research | unknown | unknown |
| **Google** | [Software Engineering Intern](https://www.google.com/about/careers/applications/jobs/results/85564713261245126-software-engineering-intern-bs-summer-2027?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **IMC** | [Software Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823924101) | US |  | unknown | unknown |
| **Jane Street** | [Fundamental Research Analyst Intern](https://www.janestreet.com/join-jane-street/position/8347286002/?utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **Jane Street** | [Linux Engineer Intern](https://www.janestreet.com/join-jane-street/position/8626260002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Network Engineer Intern](https://www.janestreet.com/join-jane-street/position/8620793002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Software Engineer Intern](https://www.janestreet.com/join-jane-street/position/8599644002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Tools and Compilers Research and Development Intern](https://www.janestreet.com/join-jane-street/position/5869205002/?utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **Jane Street** | [Windows Engineer Intern](https://www.janestreet.com/join-jane-street/position/8628843002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Marshall Wace** | [Technology Intern](https://job-boards.greenhouse.io/mwinternshipprogram/jobs/8598324002?utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **Marshall Wace** | [Technology Intern](https://job-boards.greenhouse.io/mwinternshipprogram/jobs/8606238002?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Cloud &amp; Distributed Backend](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922923&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, CoreAI](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&utm_source=github-vansh-ouckah) | US / Global |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Fullstack Product \(Web + Services\)](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922922&utm_source=github-vansh-ouckah) | US / Global |  | unknown | unknown |
| **Optiver** | [Software Engineer Intern](https://www.optiver.com/join-us/jobs/8713435002/?gh_jid=8713435002&utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **Optiver** | [Software Engineer Intern](https://www.optiver.com/join-us/jobs/technology/chicago/software-engineer-intern-summer-2027-chicago/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Optiver** | [Software Engineer Intern](https://www.optiver.com/join-us/jobs/technology/austin/software-engineer-intern-summer-2027-austin/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Squarepoint Capital** | [Intern Software Developer - London - 2027](https://www.squarepoint-capital.com/open-opportunities?id=7231006&gh_jid=7231006) | UK |  | unknown | unknown |
| **Squarepoint Capital** | [Intern Software Developer - Montreal - 2027](https://www.squarepoint-capital.com/open-opportunities?id=7905463&gh_jid=7905463) | Canada |  | unknown | unknown |
| **Squarepoint Capital** | [Intern Software Developer - Singapore - 2027](https://www.squarepoint-capital.com/open-opportunities?id=6201998&gh_jid=6201998) | Singapore |  | unknown | unknown |
| **Tower Research Capital** | [Intern - AI/ML](https://www.tower-research.com/open-positions/?gh_jid=8143756) | Unknown | research | unknown | unknown |
| **Virtu Financial** | [2027 Internship - Software Engineer](https://job-boards.greenhouse.io/virtu/jobs/8551566002) | Ireland |  | unknown | unknown |
| **Virtu Financial** | [2027 Internship – Core Operations Engineer](https://job-boards.greenhouse.io/virtu/jobs/6329460002) | Singapore |  | unknown | unknown |
| **Virtu Financial** | [2027 Internship – Software Engineer](https://job-boards.greenhouse.io/virtu/jobs/5513756002) | Singapore |  | unknown | unknown |

_740 more are in [tracker.csv](tracker.csv)._

### Quant / Finance (194 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Quantitative Development &amp; Strategy Intern 🇺🇸](https://akunacapital.com/careers/job/8021481/?gh_jid=8021481&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Akuna Capital** | [Quantitative Research Intern 🇺🇸](https://akunacapital.com/careers/job/8036614/?gh_jid=8036614&utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **Citadel** | [Quantitative Research Analyst University Graduate](https://www.citadel.com/careers/details/quantitative-research-analyst-university-graduate-us/?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Citadel** | [Quantitative Trader: Equity Quantitative Research – University Graduate](https://www.citadel.com/careers/details/quantitative-trader-equity-quantitative-research-university-graduate-us/?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Citadel Securities** | [Quantitative Research Analyst – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-research-analyst-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | UK / Ireland | research | unknown | unknown |
| **Citadel Securities** | [Quantitative Trader New Grad](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **Cubist Systematic Strategies** | [Quantitative Developer Intern](https://job-boards.greenhouse.io/point72/jobs/7297613002) | US |  | unknown | unknown |
| **DRW** | [Quantitative Research Intern](https://www.drw.com/work-at-drw/listings/quantitative-research-intern-3413670?utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **DRW** | [Quantitative Trading Analyst Intern](https://job-boards.greenhouse.io/drweng/jobs/7957243?utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **DRW** | [Quantitative Trading Analyst Intern](https://www.drw.com/work-at-drw/listings/quantitative-trading-analyst-intern-3375090?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Five Rings** | [Quantitative Trader Intern \(Summer 2027\)](https://job-boards.greenhouse.io/fiveringsllc/jobs/5139668008) | US |  | unknown | unknown |
| **G-Research** | [Quantitative Research Internship 🎓](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Quant-Research-Internship_R3691?utm_source=Simplify&ref=Simplify) | UK | research | unknown | unknown |
| **Hudson River Trading** | [Algorithm Developer New Grad - Quant Researcher](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8052050&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Hudson River Trading** | [Algorithm Development Intern - Quant Research 🎓](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8059837&utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Hudson River Trading** | [Hardware Engineer Intern](https://www.hudsonrivertrading.com/careers/job/?gh_jid=7899574&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Hudson River Trading** | [Software Engineer Intern](https://www.hudsonrivertrading.com/hrt-job/software-engineering-internship-c-or-python-summer-2027/?gh_src=&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Hudson River Trading** | [Software Engineer Intern - C++ or Python](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8052083&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **IMC** | [Quantitative Research Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4907399101) | US | research | unknown | unknown |
| **IMC Trading** | [Graduate Quantitative Researcher \(PhD\)](https://job-boards.eu.greenhouse.io/imc/jobs/4912325101) | US | phd-position | unknown | unknown |
| **IMC Trading** | [Hardware Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4927149101) | Netherlands |  | unknown | unknown |
| **IMC Trading** | [Machine Learning Research Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4907430101) | US | research | unknown | unknown |
| **IMC Trading** | [Machine Learning Research Intern - Summer 2027 - Sydney](https://job-boards.eu.greenhouse.io/imc/jobs/4956547101) | Australia | research | unknown | unknown |
| **IMC Trading** | [Machine Learning Research Intern 🎓](https://job-boards.eu.greenhouse.io/imc/jobs/4912874101?utm_source=Simplify&ref=Simplify) | Netherlands | research | unknown | unknown |
| **IMC Trading** | [Performance Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4842595101?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **IMC Trading** | [Quantitative Research Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941208101) | Hong Kong | research | unknown | unknown |
| **IMC Trading** | [Quantitative Trader Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4936262101) | Netherlands |  | unknown | unknown |
| **IMC Trading** | [Quantitative Trader Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4823923101) | US |  | unknown | unknown |
| **IMC Trading** | [Quantitative Trader Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941205101) | Hong Kong |  | unknown | unknown |
| **IMC Trading** | [Software Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4667854101) | Netherlands |  | unknown | unknown |
| **IMC Trading** | [Software Engineer Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941206101) | Hong Kong |  | unknown | unknown |
| **IMC Trading** | [Software Engineer, Early Career](https://job-boards.eu.greenhouse.io/imc/jobs/4577504101) | US |  | unknown | unknown |
| **IMC Trading** | [Trader Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4939846101) | Netherlands |  | unknown | unknown |
| **Jane Street** | [Quantitative Researcher Intern](https://www.janestreet.com/join-jane-street/position/8498547002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Quantitative Trader Intern](https://www.janestreet.com/join-jane-street/position/8617344002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Sales and Trading Intern](https://www.janestreet.com/join-jane-street/apply/8537797002?gh_jid=8537797002&utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **Jane Street** | [Sales and Trading Intern](https://www.janestreet.com/join-jane-street/position/8347385002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Trading Desk Operations Engineer Intern](https://www.janestreet.com/join-jane-street/position/8621450002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jump Trading** | [Campus AI Research Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8052281) | US | research | unknown | unknown |
| **Jump Trading** | [Campus AI Research Engineer - Deep Learning \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8052338) | US | research | unknown | unknown |
| **Jump Trading** | [Campus AI Research Engineer – Research Automation \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8052351) | US | research | unknown | unknown |

_154 more are in [tracker.csv](tracker.csv)._

### AI / ML (134 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **G-Research** | [Machine Learning Research Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Machine-Learning-Research-Internship_R3682?utm_source=Simplify&ref=Simplify) | UK | research | unknown | unknown |
| **G-Research** | [Natural Language Processing Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Natural-Language-Processing-Internship_R3686?utm_source=Simplify&ref=Simplify) | UK | nlp,research | unknown | unknown |
| **Jane Street** | [Machine Learning Engineer Intern](https://www.janestreet.com/join-jane-street/position/8611307002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Machine Learning Researcher Intern](https://www.janestreet.com/join-jane-street/position/8384490002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, AI/ML &amp; LLM](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922929&utm_source=github-vansh-ouckah) | US | llm | unknown | unknown |
| **Two Sigma** | [AI Research Scientist Intern \(MS / PhD\)](https://careers.twosigma.com/careers/JobDetail/New-York-New-York-United-States-AI-Research-Scientist-Internship-2027-Summer/14022) | US | research,phd-position | unknown | unknown |
| **Two Sigma** | [AI Research Scientist Intern - 2027 Summer](https://twosigma.avature.net/careers/JobDetail/14096?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **🔥 Google** | [Research Scientist PhD Intern 🎓](https://www.google.com/about/careers/applications/jobs/results/134795423167455942?utm_source=Simplify&ref=Simplify) | UK | research,phd-position | unknown | unknown |
| **🔥 NVIDIA** | [Applied Machine Learning Engineer – New College Grad 2026 - Circuit Design 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Applied-Machine-Learning-Engineer--Circuit-Design---New-College-Grad-2026_JR2011517?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [Computer Vision and Deep Learning Intern 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/NVIDIA-2027-Internships--PhD-Research-Computer-Vision-and-Deep-Learning_JR2023833?utm_source=Simplify&ref=Simplify) | US | perception,computer-vision | unknown | unknown |
| **🔥 NVIDIA** | [Deep Learning Computer Architecture Intern](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/NVIDIA-2027-Internships--Deep-Learning-Computer-Architecture_JR2023491?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [Generative AI Ph.D. Research Intern 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/NVIDIA-2027-Internships--PhD-Research-Generative-AI_JR2023475?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **🔥 NVIDIA** | [Large Language Models Intern - Research 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/NVIDIA-2027-Internships--PhD-Research-Large-Language-Models_JR2023837?utm_source=Simplify&ref=Simplify) | US | llm,research | unknown | unknown |
| **🔥 NVIDIA** | [Research Scientist New Grad - Efficient Deep Learning 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Research-Scientist--Efficient-Deep-Learning---New-College-Grad-2026_JR2019729-1?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **🔥 NVIDIA** | [Research Scientist – PhD New College Grad - Generative AI for Physical AI 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Research-Scientist--Generative-AI-for-Physical-AI---PhD-New-College-Grad-2026_JR2016032?utm_source=Simplify&ref=Simplify) | US | research,phd-position | unknown | unknown |
| **Cerebras Systems** | [Kernel Engineer - New Grad](https://jobs.ashbyhq.com/cerebras/9c7da4b8-446b-4bf2-8d07-23241590bf2e) | US | hardware,research,neuroscience,phd-position | unknown | unknown |
| **Databricks** | [PhD GenAI Research Scientist Intern](https://databricks.com/company/careers/open-positions/job?gh_jid=7011263002) | US | research,phd-position | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - Commercial](https://jobs.lever.co/palantir/d5486403-c050-4920-b2e0-91b69b61ebb2) | US | autonomy,hardware,llm,computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - Commercial](https://jobs.lever.co/palantir/2ad0ab10-34c3-410d-883b-8052864a95cd) | South Korea | autonomy,hardware,llm,computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - Commercial](https://jobs.lever.co/palantir/599b1907-aba1-4303-837b-66e69a521636) | UK | autonomy,llm,computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - Commercial](https://jobs.lever.co/palantir/2aa14e4f-d406-486e-9aa8-6ff3358d70a0/apply?utm_source=Simplify&ref=Simplify) | UK | autonomy,hardware,llm,computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - Commercial](https://jobs.lever.co/palantir/e500bcf3-19d8-4d3c-b340-4d76e4a55b40/apply?utm_source=Simplify&ref=Simplify) | US | autonomy,hardware,llm,computer-vision,infra,funded | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - Commercial](https://jobs.lever.co/palantir/2e6b0ac8-83e9-4be5-a3aa-cf319f751728/apply?utm_source=Simplify&ref=Simplify) | US | autonomy,hardware,llm,computer-vision,infra,funded | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - Commercial](https://jobs.lever.co/palantir/341d5cae-a473-4813-9a6c-0f67fcc1b253) | South Korea | autonomy,hardware,llm,computer-vision,infra | unknown | unknown |
| **Palantir** | [Neurodivergent Fellowship](https://jobs.lever.co/palantir/61eaa54c-e1b7-4064-afad-f7df3d48d652) | US | llm,funded | unknown | unknown |
| **Palantir** | [Neurodivergent Fellowship](https://jobs.lever.co/palantir/fd952b52-7b9c-4056-a3dd-0bc41fcfe603) | US | llm,funded | unknown | unknown |
| **Perplexity** | [Internship - Search Machine Learning Engineer](https://jobs.ashbyhq.com/perplexity/9246cf02-26fd-4ae8-90c5-639c6e85e9e2) | Serbia | llm,nlp,infra,research | unknown | unknown |
| **Perplexity** | [Internship - Search Machine Learning Engineer](https://jobs.ashbyhq.com/perplexity/71168628-1998-47d3-87a9-be7bc56a430d) | UK | llm,nlp,infra,research | unknown | unknown |
| **Sierra** | [Software Engineer, Agent \(New Grad 2027\)](https://jobs.ashbyhq.com/Sierra/149f368c-52d5-408f-ba26-ad888f318a00/application?embed=true&utm_source=Simplify&ref=Simplify) | US | autonomy,llm,research,funded | unknown | posting mentions equity |
| **Snowflake** | [AI Research Scientist, New Grad – Agents &amp; Reinforcement Learning](https://jobs.ashbyhq.com/snowflake/1bad12df-f443-426f-9d09-e96fc780d698/application?utm_source=Simplify&ref=Simplify) | US | autonomy,llm,rl,data-eng,infra,research,phd-position | unknown | unknown |
| **🔥 AMD** | [Machine Learning Intern/Co-op - Artificial Intelligence 🎓](https://careers.amd.com/jobs/91181?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Machine Learning Intern/Co-op - Machine Learning - Artificial Intelligence](https://careers.amd.com/jobs/90892?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Machine Learning Intern/Co-op - Multiple Teams](https://careers.amd.com/jobs/91170?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Machine Learning/Artificial Intelligence Intern/Co-op](https://careers.amd.com/jobs/91363?icims=1&utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Allen Control Systems** | [Junior Computer Vision &amp; Machine Learning Engineer](https://jobs.ashbyhq.com/allen-control-systems/cfb348d0-ab31-4fa5-9bd5-def1de764ca9/application?embed=true&utm_source=Simplify&ref=Simplify) | US | perception,controls,computer-vision | unknown | unknown |
| **Atoms** | [Machine Learning PhD Software Engineer Intern 🎓](https://job-boards.greenhouse.io/cssmerge/jobs/8693034002?utm_source=Simplify&ref=Simplify) | US | phd-position | unknown | unknown |
| **Brunswick** | [Reinforcement Learning Intern - Boating Intelligence Design Lab](https://brunswick.wd1.myworkdayjobs.com/en-US/search/job/Champaign-IL/Software-Engineering-Intern_JR-051449?utm_source=Simplify&ref=Simplify) | US | rl | unknown | unknown |
| **ByteDance** | [Applied Machine Learning Production Engineer Intern](https://joinbytedance.com/search/7670009669494704437?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **ByteDance** | [Student Researcher, Multimodal Interaction &amp; World Model \(Seed\)](https://joinbytedance.com/search/7623548747208739077) | US | multimodal | unknown | unknown |
| **ByteDance** | [Student Researcher, Vision Foundation Model \(Seed\)](https://joinbytedance.com/search/7623544831999346997) | US | embodied-ai | unknown | unknown |

_94 more are in [tracker.csv](tracker.csv)._

### Robotics & Embodied AI (115 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Amazon** | [Robotics - Software Development Engineer Intern/Co-op](https://www.amazon.jobs/en/jobs/3136266/robotics-software-development-engineer-intern-co-op-2026?no_int_redir=1&utm_source=github-vansh-ouckah) | US | robot-software | unknown | unknown |
| **Nuro** | [Software Engineer, AI Platform - Intern](https://nuro.ai/careersitem?gh_jid=7351061) | US | autonomous vehicles | private-scaleup | private company; verify offer |
| **Nuro** | [Software Engineer, AI Platform - New Grad](https://nuro.ai/careersitem?gh_jid=7351066) | US | autonomous vehicles | private-scaleup | private company; verify offer |
| **Palantir** | [American Tech Fellowship](https://jobs.lever.co/palantir/0ccbe620-a3ef-41d1-a5c4-68e56b3c91d0) | Unknown | controls,robot-software,hardware,funded | unknown | unknown |
| **🔥 Waymo** | [Applied Research Scientist – New Grad - Perception Large Language Model/Vision-Language Model - PhD 🎓](https://careers.withwaymo.com/jobs?gh_jid=7488508&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Data Science Intern - Commercialization Testing 🎓](https://careers.withwaymo.com/jobs?gh_jid=8167323&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **Deft Robotics** | [Electrical Engineer Intern \(Spring-Summer 2026\)](https://jobs.ashbyhq.com/deft-ai/0d16afe8-30a9-43df-90d5-ccba1cb97b69) | US | humanoid robotics | emerging-startup | private company; verify offer |
| **Deft Robotics** | [Mechanical Engineer Intern \(Spring-Summer 2026\)](https://jobs.ashbyhq.com/deft-ai/1bef1405-cd24-4da7-b1e7-0ca02e8f5eb2) | US | humanoid robotics | emerging-startup | private company; verify offer |
| **Dyna Robotics** | [Research Internship](https://jobs.ashbyhq.com/dyna-robotics/5a431519-ee6b-4cb7-8a3a-422727053a09) | US | robot learning | emerging-startup | private company; verify offer |
| **Generalist AI** | [Research Assistant](https://jobs.ashbyhq.com/generalist/fc7c7b49-248a-4849-a473-a0bd246e5486) | US | general-purpose robotics | emerging-startup | private company; verify offer |
| **Lightwheel** | [Developer Advocate / Research Community Intern](https://jobs.ashbyhq.com/lightwheel/e22363b9-9c4f-4991-8de3-339b8e9399df) | US | robot learning | emerging-startup | private company; verify offer |
| **Physical Intelligence** | [Research Internships](https://jobs.ashbyhq.com/physicalintelligence/f020ff1a-4b4c-4415-8434-2da5010a7076) | US | embodied AI | emerging-startup | private company; verify offer |
| **RoboForce** | [Robotics Electrical Engineering Intern](https://job-boards.greenhouse.io/roboforce/jobs/5181214008) | US | industrial robotics | emerging-startup | private company; verify offer |
| **1X** | [AI Residency](https://jobs.ashbyhq.com/1x/5b2b4c73-13b5-46ca-8467-8024741a4b57) | US | humanoid robotics | private-scaleup | private company; verify offer |
| **1X** | [Internship - Manufacturing Engineering \(Fall\)](https://jobs.ashbyhq.com/1x/7d93444c-01f5-485c-89ef-24164f30441d) | US | humanoid robotics | private-scaleup | private company; verify offer |
| **ANYbotics** | [Product Data Management Internship](https://jobs.lever.co/anybotics/74b68707-86aa-4efc-9efb-94ca5ad82698) | Switzerland | legged robots | private-scaleup | private company; verify offer |
| **ANYbotics** | [Robotics Lab Technician Intern](https://jobs.lever.co/anybotics/9755ae0f-f740-40bc-bc13-be52c505748b) | Switzerland | legged robots | private-scaleup | private company; verify offer |
| **ANYbotics** | [Software Engineering Internship - AI Platform](https://jobs.lever.co/anybotics/7e305a48-4628-4a6a-b054-0367b6f6e586) | Switzerland | legged robots | private-scaleup | private company; verify offer |
| **Anduril** | [2026 Early Career Electrical Engineer](https://boards.greenhouse.io/andurilindustries/jobs/4802172007?gh_jid=4802172007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2026 Early Career Flight Test Engineer, Mission Autonomy](https://boards.greenhouse.io/andurilindustries/jobs/5185089007?gh_jid=5185089007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2026 Early Career Manufacturing Engineer](https://boards.greenhouse.io/andurilindustries/jobs/5176254007?gh_jid=5176254007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2026 Early Career Mechanical Engineer](https://boards.greenhouse.io/andurilindustries/jobs/4802167007?gh_jid=4802167007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2026 Early Career Test &amp; Evaluation Systems Integrator](https://boards.greenhouse.io/andurilindustries/jobs/5185888007?gh_jid=5185888007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2027 Early Career Electrical Engineer](https://boards.greenhouse.io/andurilindustries/jobs/5136925007?gh_jid=5136925007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2027 Early Career Manufacturing Engineer](https://boards.greenhouse.io/andurilindustries/jobs/5136970007?gh_jid=5136970007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2027 Early Career Mechanical Engineer](https://boards.greenhouse.io/andurilindustries/jobs/5136984007?gh_jid=5136984007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2027 Electrical Engineer Intern](https://boards.greenhouse.io/andurilindustries/jobs/5148101007?gh_jid=5148101007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2027 Manufacturing Engineer Intern](https://boards.greenhouse.io/andurilindustries/jobs/5153218007?gh_jid=5153218007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2027 Mechanical Engineer Intern](https://boards.greenhouse.io/andurilindustries/jobs/5153187007?gh_jid=5153187007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [Early Career Software Engineer](https://boards.greenhouse.io/andurilindustries/jobs/4802146007?utm_source=Simplify&ref=Simplify) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [Mission Engineer, Air Dominance &amp; Strike, Early Career](https://boards.greenhouse.io/andurilindustries/jobs/5174562007?gh_jid=5174562007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [Software Engineer Intern](https://job-boards.greenhouse.io/andurilindustries/jobs/5148079007?gh_jid=5148079007&utm_source=github-vansh-ouckah) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Applied Intuition** | [Build &amp; Release Engineer - New Grad \(December 2026\)](https://jobs.ashbyhq.com/applied/9534b49a-9feb-4063-ac33-a9c4d94a1352) | US | autonomy tooling | private-scaleup | private company; verify offer |
| **Applied Intuition** | [Embedded Software Engineer - New Grad \(2027\)](https://jobs.ashbyhq.com/applied/6971d533-1536-448b-96b8-544ad5383f44/application?embed=true&utm_source=Simplify&ref=Simplify) | US | autonomy tooling | private-scaleup | private company; verify offer |
| **Applied Intuition** | [Embedded Test Engineer - New Grad \(December 2026\)](https://jobs.ashbyhq.com/applied/0695a5b7-6823-4da5-b918-3b580d49662c) | US | autonomy tooling | private-scaleup | private company; verify offer |
| **Applied Intuition** | [Hardware Integration Engineer - New Grad \(December 2026\)](https://jobs.ashbyhq.com/applied/4c3cd892-2ef0-40b6-877a-39540a224a5c) | US | autonomy tooling | private-scaleup | private company; verify offer |
| **Applied Intuition** | [OTA/Cloud Validation Engineer - New Grad \(December 2026\)](https://jobs.ashbyhq.com/applied/e5ec6599-5ae4-4f0f-b0fd-cd6f4cad8d95) | US | autonomy tooling | private-scaleup | private company; verify offer |
| **Applied Intuition** | [Research Engineer - New Grad \(2027\)](https://jobs.ashbyhq.com/applied/45fc41cd-8280-4010-ba1f-def6114b3e39/application?embed=true&utm_source=Simplify&ref=Simplify) | US | autonomy tooling | private-scaleup | private company; verify offer |
| **Applied Intuition** | [Research Intern - 3D Vision and Generation, Self-Driving](https://jobs.ashbyhq.com/applied/91e0686e-272a-4780-b33d-d7860b94a7b4) | US | autonomy tooling | private-scaleup | private company; verify offer |
| **Applied Intuition** | [Research Intern - Reinforcement Learning, Robotics](https://jobs.ashbyhq.com/applied/bb953f29-0059-4a40-aa9e-3a8c88733902) | US | autonomy tooling | private-scaleup | private company; verify offer |

_75 more are in [tracker.csv](tracker.csv)._

### Data (106 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Citadel** | [Sector Data Scientist Intern](https://www.citadel.com/careers/details/sector-data-scientist-2027-intern-us/?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Jane Street** | [Data Engineer Intern](https://www.janestreet.com/join-jane-street/position/8631973002/?utm_source=github-vansh-ouckah) | US | data-eng | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Data Platform/Analytics](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922931&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Tower Research Capital** | [Business Analytics Intern - 6 Month Internship Opportunity](https://www.tower-research.com/open-positions/?gh_jid=8041512) | Netherlands | research | unknown | unknown |
| **Figma** | [Data Scientist, Core Data -  PhD \(2026\)](https://boards.greenhouse.io/figma/jobs/5976930004?gh_jid=5976930004) | US | phd-position | unknown | unknown |
| **AMERICAN SYSTEMS** | [Data Engineer - Junior](https://careers-americansystems.icims.com/jobs/4391/job?mobile=true&needsRedirect=false&utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **Affinius Capital** | [Data Scientist Intern](https://careers-affiniuscapital.icims.com/jobs/2284/summer-2027-data-scientist-intern/job) | US |  | unknown | unknown |
| **AlixPartners** | [Data Scientist Intern 🎓](https://www.alixpartners.com/careers/7725335003?gh_jid=7725335003&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Allegheny County** | [Business Analytics Intern](https://alleghenycounty.bamboohr.com/careers/663/?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Campus Undergraduate Summer Internship - Strategy &amp; Analytics - Credit &amp; Fraud Risk](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26011984?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012703?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012782?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012784?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012783?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - Global Servicing - Financial Crimes Risk &amp; Controls](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012627?utm_source=Simplify&ref=Simplify) | US | controls | unknown | unknown |
| **American Express** | [Data Analytics Intern - US Consumer Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26011607?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Engineer 1 - Global Servicing Technology](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26011091?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **American Express** | [Data Engineer Intern - Enterprise Technology Services](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012333?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **American Express** | [Data Engineer Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012781?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **American Express** | [Data Engineer Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012764?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **American Express** | [Undergraduate Intern - Strategy &amp; Analytics](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26011990?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Aon** | [Data &amp; Analytics Associate - Early Careers](https://jobs.aon.com/jobs/105952?icims=1&utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Arch Capital Group** | [Data and Analytics Intern](https://archgroup.wd1.myworkdayjobs.com/careers/job/Farmington-CT-United-States-of-America/Data-and-Analytics-Intern_R26_845?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Arthur J. Gallagher &amp; Co.** | [Data Analytics Intern](https://jobs.ajg.com/jobs/57701?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Blackstone** | [Data Engineer Summer Analyst - Blackstone Technology &amp; Innovations](https://blackstone.wd1.myworkdayjobs.com/zh-CN/Blackstone_Campus_Careers/job/Miami/XMLNAME-2027-Blackstone-Technology-and-Innovations--Data-Engineer-Summer-Analyst_45022?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **BlueCross BlueShield of Nebraska** | [Data Intern - Data Science - Data Analytics](https://nebraskablue.wd1.myworkdayjobs.com/BCBSNE/job/Omaha-NE/Data-Intern--Summer-2027_JR101406?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Rome-NY/University--2027-Summer-Games-Data-Scientist-Intern_R0248143?utm_source=Simplify&ref=Simplify) | US / Italy |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Colorado-Springs-CO/University--2027-Summer-Games-Data-Scientist-Intern_R0248132?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern - University](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Charleston-SC/University---2027-Summer-Games-Data-Scientist-Intern_R0248137?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern - University](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Atlanta-GA/University--2027-Summer-Games-Data-Scientist-Intern_R0248140?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern - University](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/McLean-VA/University---2027-Summer-Games-Data-Scientist-Intern---McLean--VA_R0248037?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern - University](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/San-Diego-CA/University---2027-Summer-Games-Data-Scientist-Intern---San-Diego--CA_R0248045?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern - University - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/El-Segundo-CA/University--2027-Summer-Games-Data-Scientist-Intern_R0248050?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Brunswick** | [Advanced Manufacturing/Operations Analytics Engineering Co-op - Global Operations Excellence](https://brunswick.wd1.myworkdayjobs.com/en-US/search/job/Fond-du-Lac-WI/Mercury-Marine--Advanced-Manufacturing-Operations-Analytics-Engineering-Co-op_JR-051238?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **C3.ai** | [Data Scientist Intern - Summer 2027 🎓](https://c3.ai/job-description/8738918002?gh_jid=8738918002&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **CACI** | [Software Developer/Data Scientist Intern - Summer 2027](https://caci.wd1.myworkdayjobs.com/external/job/Denver-CO-US/Software-Developer-Data-Scientist-Intern---Summer-2027_331120?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **CarbonChain** | [Junior Data Engineer](https://job-boards.greenhouse.io/carbonchain/jobs/6121104004?utm_source=Simplify&ref=Simplify) | UK | data-eng,climate | unknown | unknown |
| **Cardinal Health** | [Data and Analytics Intern - Summer 2027](https://cardinalhealth.wd1.myworkdayjobs.com/EXT/job/OH-Dublin-Cardinal-Place/Data---Analytics-Internship--Summer-2027-_20185913?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Cigna Group** | [Legal Operations Financial Data &amp; AI Analytics Intern](https://cigna.wd5.myworkdayjobs.com/cignacareers/job/St-Louis-MO/Legal-Operations-Financial--Data---AI-Analytics-Intern_25016386?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Compeer Financial** | [Data Analytics Intern](https://job-boards.greenhouse.io/compeerfinancial/jobs/5409874008?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |

_66 more are in [tracker.csv](tracker.csv)._

### Hardware / EE (68 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Hardware Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018880/?gh_jid=8018880&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **DRW** | [FPGA Intern](https://www.drw.com/work-at-drw/listings/fpga-intern-3484423?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **IMC** | [Hardware Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823945101) | US |  | unknown | unknown |
| **Jane Street** | [Hardware Engineer \(FPGA/ASIC\) Intern](https://www.janestreet.com/join-jane-street/position/8624440002/?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **Optiver** | [FPGA Engineer Intern](https://www.optiver.com/join-us/jobs/8402114002/?gh_jid=8402114002&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Optiver** | [FPGA Engineer Intern](https://www.optiver.com/join-us/jobs/8641352002/?gh_jid=8641352002&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Virtu Financial** | [2027 Internship - FPGA Engineer](https://job-boards.greenhouse.io/virtu/jobs/8638124002) | Ireland | hardware | unknown | unknown |
| **Virtu Financial** | [Hardware Engineer Intern - FPGA 🎓](https://job-boards.greenhouse.io/virtu/jobs/8657286002?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Design Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Design-Engineer---New-College-Grad-2026_JR2021534?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Floorplan Design Engineer New Grad 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Floorplan-Design-Engineer---New-College-Grad-2026_JR2024651?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Physical Design Engineer New Grad - Netlisting 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Physical-Design-Engineer--Netlisting---New-College-Grad-2026_JR2017681?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Physical Design and Timing Engineer – New College Grad 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Timing-Engineer---New-College-Grad-2026_JR2013177?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Verification Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Verification-Engineer---New-College-Grad-2026_JR2020640?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [Hardware ASIC Design Intern - Hardware](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/NVIDIA-2027-Internships--Hardware-ASIC-Design_JR2023486?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [Hardware Physical Design / VLSI Intern](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/NVIDIA-2027-Internships--Hardware-Physical-Design---VLSI_JR2023501?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 NVIDIA** | [Low Power ASIC Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Low-Power-ASIC-Engineer---New-College-Grad-2026_JR2017005?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Verkada** | [Embedded Software Engineer Intern](https://job-boards.greenhouse.io/verkada/jobs/5211595007?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 AMD** | [ASIC Package Engineer Intern Co-op 🎓](https://careers.amd.com/jobs/91469?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [ASIC Package Engineering Intern Co-op 🎓](https://careers.amd.com/jobs/91471?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Co-op/Intern 🎓](https://careers.amd.com/jobs/90809?icims=1&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op](https://careers.amd.com/jobs/91320?icims=1&utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op](https://careers.amd.com/jobs/91313?icims=1&utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op - Long Term](https://careers.amd.com/jobs/90297?icims=1&utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op 🎓](https://careers.amd.com/jobs/90805?icims=1&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineering Intern Co-op - Undergrad](https://careers.amd.com/jobs/90807?icims=1&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 AMD** | [Hardware Engineer Intern/Co-op](https://careers.amd.com/jobs/90894?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Hardware Engineer Intern/Co-op - Hardware Engineering 🎓](https://careers.amd.com/jobs/91182?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Alarm.com** | [Embedded Software Engineer 1](https://job-boards.greenhouse.io/alarmcom/jobs/8622530002?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Apex Technology, Inc.** | [Software Engineering Intern, Embedded Systems](https://jobs.ashbyhq.com/apex-technology-inc/5ec2dfa9-724d-4ce4-ab97-5067ec747f11?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **Axon** | [Embedded Engineer Intern](https://job-boards.greenhouse.io/axontalentcommunity/jobs/7800627003?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Blue Origin** | [ASIC Engineer - Early Career](https://blueorigin.wd5.myworkdayjobs.com/blueorigin/job/Greater-Seattle-Area/ASIC-Engineer---Early-Career_R70802?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Blue Origin** | [Avionics / Embedded Software Engineer 1 - 2027 Starts](https://blueorigin.wd5.myworkdayjobs.com/blueorigin/job/Greater-Seattle-Area/Avionics---Embedded-Software-Engineer-I---Early-Career--2027-Starts-_R71324?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Blue Origin** | [Avionics / Embedded Software Engineer 1 - Early Career](https://blueorigin.wd5.myworkdayjobs.com/blueorigin/job/Greater-Seattle-Area/Avionics---Embedded-Software-Engineer-I---Early-Career--2026-Starts-_R70055?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Boeing** | [Entry Level ASIC/FPGA Design Engineer - Space Electronics](https://boeing.wd1.myworkdayjobs.com/external_subsidiary/job/USA---Mountain-View-CA/Entry-Level-ASIC-FPGA-Design-Engineer---Space-Electronics---MTV_JR2026520433?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Boeing** | [Entry Level ASIC/FPGA Verification Engineer - Space Electronics](https://boeing.wd1.myworkdayjobs.com/external_subsidiary/job/USA---Mountain-View-CA/Entry-Level-ASIC-FPGA-Verification-Engineer---Space-Electronics---MTV_JR2026520435-2?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Ciena** | [ASIC Synthesis and STA Engineer New Grad](https://ciena.wd5.myworkdayjobs.com/Careers/job/Ottawa/ASIC-Synthesis-and-STA-Engineer---New-Grad_R030893?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Ciena** | [Embedded Software Engineer New Grad](https://ciena.wd5.myworkdayjobs.com/Careers/job/Ottawa/Embedded-Software-Developer--New-Grad-_R031481?utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **Daktronics** | [Hardware Design Co-op Intern - Firmware](https://careers-daktronics.icims.com/jobs/7518/job?mobile=true&needsRedirect=false&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Dell Technologies** | [Hardware Engineer 1 - Client Solutions Group](https://iawmqy.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/careers/job/298141?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Eaton** | [Firmware Engineer Intern/Co-op - Research &amp; Development Engineering](https://eaton.eightfold.ai/careers/job/687238596754?utm_source=Simplify&ref=Simplify) | US | hardware,research | unknown | unknown |

_28 more are in [tracker.csv](tracker.csv)._

### Security (54 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Jane Street** | [Cybersecurity Analyst Intern](https://www.janestreet.com/join-jane-street/position/8632723002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Security &amp; Identity](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922930&utm_source=github-vansh-ouckah) | US | security | unknown | unknown |
| **Cohere** | [Machine Learning Intern/Co-op  \(Winter 2027\)](https://jobs.ashbyhq.com/cohere/36d1f52f-8270-4652-adf5-5303a0ff341b) | Canada | computer-vision,nlp,security,research,funded | unknown | unknown |
| **Cohere** | [Software Engineer Intern \(Winter 2027\)](https://jobs.ashbyhq.com/cohere/8c035d3d-081d-4c8a-914a-72f4efaad254) | Canada | autonomy,computer-vision,nlp,data-eng,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Forward Deployed Infrastructure Engineer, New Grad - UK Government](https://jobs.lever.co/palantir/cadc0eb2-2703-43e4-8e4f-41edf5b071c6) | UK | autonomy,llm,infra,distributed,security | unknown | unknown |
| **Palantir** | [Forward Deployed Infrastructure Engineer, New Grad - US Government](https://jobs.lever.co/palantir/33243fb5-6907-40c7-930c-968b25d825d0) | US | autonomy,llm,infra,distributed,security,funded | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - AUS Government](https://jobs.lever.co/palantir/395a4483-fc3d-4b77-a500-501923fd0976) | Australia | infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - Defense Tech](https://jobs.lever.co/palantir/cccfe1bd-f15b-4fe5-b044-c793e7961c1b) | US | computer-vision,infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - UK Government](https://jobs.lever.co/palantir/26e23f5d-083b-45aa-b223-1a6e43d960bf) | UK | autonomy,llm,computer-vision,infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - UK Government](https://jobs.lever.co/palantir/b4aa51a2-bc43-4d67-bf55-12db7feefb3a/apply?utm_source=Simplify&ref=Simplify) | UK | autonomy,hardware,llm,computer-vision,infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - US Government](https://jobs.lever.co/palantir/cbe90327-3e6e-451c-a54c-1d3cbcef5aeb/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,infra,security,funded | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - US Government](https://jobs.lever.co/palantir/d1ac83d0-e923-42a5-8e6d-58dd0cab25ca/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,infra,security,funded | unknown | unknown |
| **Palantir** | [Information Security Engineer, Internship](https://jobs.lever.co/palantir/ef725594-42dd-4f0d-ba8e-df8179dbc6cb) | US | autonomy,computer-vision,security | unknown | unknown |
| **Palantir** | [Privacy &amp; Civil Liberties Engineer - New Grad](https://jobs.lever.co/palantir/95e0d2b0-437a-4096-a5c6-0f247f426c90) | US | security,funded | unknown | unknown |
| **Palantir** | [Privacy and Civil Liberties Software Engineer, Internship](https://jobs.lever.co/palantir/09846827-b931-4a9f-bd64-c3bb8860187b) | US | infra,security | unknown | unknown |
| **Palantir** | [Software Engineer, Internship](https://jobs.lever.co/palantir/7d69cf8a-06fd-4f05-bd84-27149db29c4d?utm_source=github-vansh-ouckah) | US | computer-vision,data-eng,infra,security,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship](https://jobs.lever.co/palantir/bdcfb29f-4f27-42de-933f-7f83a359b9f0?utm_source=github-vansh-ouckah) | US | computer-vision,data-eng,infra,security,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship](https://jobs.lever.co/palantir/e27af7ab-41fc-40c9-b31d-02c6cb1c505c?utm_source=github-vansh-ouckah) | US | computer-vision,data-eng,infra,security,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship](https://jobs.lever.co/palantir/373eb939-6f57-4836-8479-be79a5e07249) | US | computer-vision,data-eng,infra,security,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Defense Tech](https://jobs.lever.co/palantir/f17e98d0-046a-4e6e-9d65-ed0b12dd0ff7) | US | computer-vision,data-eng,infra,security | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Defense Tech](https://jobs.lever.co/palantir/8bcf4f33-0a79-4248-bbfd-49ac4be9dd8e) | US | computer-vision,data-eng,infra,security | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Defense Tech](https://jobs.lever.co/palantir/a483f41b-0da9-42ea-8ed6-cbf6eb93cc6d) | US | computer-vision,data-eng,infra,security | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Infrastructure](https://jobs.lever.co/palantir/b229baac-494b-4a0d-9a13-2e38806e06f3?utm_source=github-vansh-ouckah) | US | computer-vision,data-eng,infra,security | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Infrastructure](https://jobs.lever.co/palantir/f221738b-e97c-4ce3-a12a-17ada2b855e4) | US | computer-vision,data-eng,infra,security | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Production Infrastructure](https://jobs.lever.co/palantir/373367a9-3160-49d8-b7af-2efec062fad1?utm_source=github-vansh-ouckah) | US | computer-vision,infra,security,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Production Infrastructure](https://jobs.lever.co/palantir/3ab9e715-1ea9-4c6c-ad50-7340eac14e86) | US | computer-vision,infra,security,research | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad](https://jobs.lever.co/palantir/c34b424e-caf2-455a-b104-ae1096ccca29/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,data-eng,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad](https://jobs.lever.co/palantir/94984771-0704-446c-88c6-91ce748f6d92) | US | computer-vision,data-eng,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Defense](https://jobs.lever.co/palantir/18d901fc-93bb-4d18-9f04-c72031e20d79/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,data-eng,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Defense](https://jobs.lever.co/palantir/0a838e66-1ab0-4fc4-b4d3-4671c0352278/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,data-eng,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Defense](https://jobs.lever.co/palantir/f362d7aa-360d-4059-ab38-f482742693b3/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,data-eng,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Infrastructure](https://jobs.lever.co/palantir/4abf26b4-795c-420a-bf22-1ab98db268b4) | US | computer-vision,data-eng,infra,security,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Infrastructure](https://jobs.lever.co/palantir/7d75bed5-45d8-4876-840a-2d92ea79c98d) | US | computer-vision,data-eng,infra,security,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Production Infrastructure](https://jobs.lever.co/palantir/15844944-fb69-4b57-9531-e988650b20c6/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Production Infrastructure](https://jobs.lever.co/palantir/4d5a144e-87ea-45e2-a68c-3fad590629af) | US | computer-vision,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Production Infrastructure](https://jobs.lever.co/palantir/e1a6c138-98bf-45e2-97f7-2c70371cc38a) | US | computer-vision,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Year at Palantir - Forward Deployed Software Engineer, Internship - Commercial](https://jobs.lever.co/palantir/75cc1c09-8ebd-44c8-b3bc-d122cd1fecb3) | US | autonomy,infra,security,research | unknown | unknown |
| **Palantir** | [Year at Palantir - Forward Deployed Software Engineer, Internship - USG](https://jobs.lever.co/palantir/5c4c65c5-77da-4d36-856c-4ade87631019) | US | autonomy,infra,security,research | unknown | unknown |
| **Palantir** | [Year at Palantir - Forward Deployed Software Engineer, Internship - USG](https://jobs.lever.co/palantir/5c7bb70c-83ea-43e7-8055-0c8f319f4333) | US | autonomy,infra,security,research | unknown | unknown |
| **Palantir** | [Year at Palantir - Software Engineer, Internship](https://jobs.lever.co/palantir/655f9937-a4ce-4e7d-80e2-a6659af07329) | US | autonomy,infra,security,research | unknown | unknown |

_14 more are in [tracker.csv](tracker.csv)._

### Systems & Infra (38 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Platform Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018856/?gh_jid=8018856&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **DRW** | [Platform Engineer Intern](https://www.drw.com/work-at-drw/listings/platform-engineer-intern-3468737?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [Backend Compiler Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Backend-Compiler-Engineer---New-College-Grad-2026_JR2021242?utm_source=Simplify&ref=Simplify) | US / Canada |  | unknown | unknown |
| **🔥 NVIDIA** | [Compiler Engineer – Backend-New College Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Compiler-Engineer--Backend--New-College-Grad-2026_JR2017290?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Cerebras Systems** | [DevOps Engineer - New Grad 2026](https://jobs.ashbyhq.com/cerebras/40e0d3ee-8f0a-4b19-9bf9-79410b1c7735) | Remote | infra,distributed,research | unknown | unknown |
| **Cerebras Systems** | [Software Engineer - New Grad 2026](https://jobs.ashbyhq.com/cerebras/99c289fa-8fc6-49f7-b7e8-78ac4e9d99ac/application?utm_source=Simplify&ref=Simplify) | US / Canada | hardware,infra,distributed,research | unknown | unknown |
| **Cloudflare** | [Systems Engineer - Global Resource Management \(Data Residency\)](https://boards.greenhouse.io/cloudflare/jobs/8015230?gh_jid=8015230) | Unknown |  | unknown | unknown |
| **Notion** | [Software Engineer, Early Career](https://jobs.ashbyhq.com/notion/297b4ece-765f-4eea-b1b8-46057cb6501f/application?utm_source=Simplify&ref=Simplify) | US | autonomy,infra,distributed,research | unknown | posting mentions equity |
| **Notion** | [Software Engineer, Early Career \(AI\)](https://jobs.ashbyhq.com/notion/85947779-6b87-466a-98bc-30a640448c28/application?utm_source=Simplify&ref=Simplify) | US | autonomy,infra,distributed | unknown | posting mentions equity |
| **Perplexity** | [Internship - Search Backend Infra Engineer](https://jobs.ashbyhq.com/perplexity/be94e89b-89d5-4f2a-a58b-7929c8d97f92) | Serbia | infra,distributed | unknown | unknown |
| **Air Products** | [Information Technology/Digital Technology Intern - Infrastructure Services](https://airproducts.wd5.myworkdayjobs.com/en-US/AP0001/job/Allentown-Pennsylvania/Summer-Intern--IT-Digital-Technology--2027-_JR-2026-21953?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **Blissway** | [Embedded Systems Engineer New Grad](https://jobs.ashbyhq.com/blissway/51d6d839-9801-4436-bfc2-918bae428ed8/application?embed=true&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Brunswick** | [Systems Engineer Co-op - Software Engineering](https://brunswick.wd1.myworkdayjobs.com/en-US/search/job/Fond-du-Lac-WI/Mercury-Marine---Systems-Software-Engineering-Co-op_JR-051212?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Crusoe** | [Software Engineer 1 - Storage](https://jobs.ashbyhq.com/Crusoe/4f5d34ed-0c05-4eec-b8f8-14663e114b02/application?embed=true&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Dedalus Labs** | [Systems Engineer / Product Manager Intern \(Summer 2027\)](https://www.ycombinator.com/companies/dedalus-labs/jobs/YtbvXM8-systems-engineer-summer-2027-intern) | US |  | unknown | unknown |
| **Etched** | [Infrastructure Intern](https://jobs.ashbyhq.com/Etched/80926a71-0a62-4bf8-a877-b6d96df279b7?utm_source=github-vansh-ouckah) | US | infra | unknown | unknown |
| **Etched AI** | [Chip Simulation Software Intern](https://jobs.ashbyhq.com/etched/27e5bd6b-9357-45f0-9e79-cfa2bf4eeba8) | Unknown | hardware,infra,research,phd-position | unknown | unknown |
| **Etched AI** | [Electrical Platform Intern](https://jobs.ashbyhq.com/etched/904ddf46-55fc-4a8f-8b49-f32cfe88116a) | Unknown | hardware,infra,research | unknown | unknown |
| **Etched AI** | [Firmware Intern](https://jobs.ashbyhq.com/etched/699f3ab2-07e4-466c-9d76-3d4a3abb4ebc) | Unknown | hardware,infra,research,phd-position | unknown | unknown |
| **Etched AI** | [Performance Tools Intern](https://jobs.ashbyhq.com/etched/f02e8035-7dc9-4b0c-aab7-75bbb4e975b8) | Unknown | hardware,infra,research | unknown | unknown |
| **Everfox** | [Embedded Systems Engineer 1](https://evergreenix.wd1.myworkdayjobs.com/external-careers2/job/UK---London/Embedded-Systems-Engineer-I_JR500701?utm_source=Simplify&ref=Simplify) | UK | hardware | unknown | unknown |
| **General Dynamics Information Technology** | [Systems Engineer Intern](https://www.gd.com/careers/systems-engineer-intern-albany-ny-us-rq225289-gdit-opportunity?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Lightfield** | [Early Career Infrastructure Software Engineer](https://jobs.ashbyhq.com/Lightfield/9a7ef2f9-577a-4242-b884-719e3cdf4420/application?embed=true&utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **Poshmark** | [Cloud Platform Engineer Intern, Growth 🛂](https://jobs.ashbyhq.com/poshmark/062b84e6-1633-43ae-870b-83cb62893caa?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **QTS** | [Data Center Infrastructure Management Intern - DCIM](https://qtsdatacenters.wd5.myworkdayjobs.com/qts/job/Suwanee-GA/Summer-2027-Internship--Data-Center-Infrastructure-Management--DCIM-_R2026-1892?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **StepStone Group** | [Private Equity Infrastructure &amp; Real Assets Summer Analyst 🛂](https://www.stepstonegroup.com/current-opportunities/?gh_jid=7872890) | US | infra | unknown | unknown |
| **🔥 ByteDance** | [AI Network Automation Engineer Intern - Global Physical Network Infrastructure](https://jobs.bytedance.com/en/position/7670690923748870405/detail?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 ByteDance** | [Backend and Infrastructure Software Engineer New Grad - Dev Infra](https://jobs.bytedance.com/en/position/7667894766036322565/detail?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 ByteDance** | [Software Engineer Intern - AI Infrastructure Compute 🎓](https://jobs.bytedance.com/en/position/7667377525182662965/detail?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 ByteDance** | [Software Engineer Intern - Traffic Infrastructure](https://jobs.bytedance.com/en/position/7672626707586746629/detail?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 ByteDance** | [Software Engineer New Grad - AI Infrastructure-Compute Efficiency &amp; Scheduling](https://jobs.bytedance.com/en/position/7668799020705679669/detail?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 ByteDance** | [Software Engineer New Grad - Traffic Infrastructure](https://jobs.bytedance.com/en/position/7665849950984194309/detail?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 TikTok** | [AI Agent Product Manager Intern - Product Infrastructure-Customer Service Platform](https://lifeattiktok.com/search/7670010726514493749?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 TikTok** | [Backend Software Engineer Intern - Product Infrastructure](https://lifeattiktok.com/search/7667935633764370741?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 TikTok** | [Product Manager Intern - Product Infrastructure - Account](https://lifeattiktok.com/search/7670009830602721589?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 TikTok** | [Research Engineer Intern - Agentic Systems &amp; AI Infrastructure - Generalized Architecture](https://lifeattiktok.com/search/7667934792727906565?utm_source=Simplify&ref=Simplify) | US | infra,research | unknown | unknown |
| **🔥 TikTok** | [Software Engineer Intern - Recommendation Architecture - Feeds Infrastructure](https://lifeattiktok.com/search/7672926068681951493?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 TikTok** | [Software Engineer New Grad - Ads Infrastructure](https://lifeattiktok.com/search/7668879883938203957?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |

### Computational Science (21 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Palantir** | [Forward Deployed Software Engineer, Internship](https://jobs.lever.co/palantir/1b6f1d82-d459-4dea-8bc2-8d2ffe6f881a) | France | autonomy,computer-vision,infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - France](https://jobs.lever.co/palantir/ac0dc094-2480-43c2-8495-26ade227ff4f) | US | infra,funded | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - Intel](https://jobs.lever.co/palantir/9e40d77f-b07c-437b-98e7-def9b0184d89) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - US Government](https://jobs.lever.co/palantir/315f695d-04d1-4a9a-848e-cb2bec7a997e) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - US Government](https://jobs.lever.co/palantir/e0010393-c300-446f-bf67-fa2ef067f16f) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - US Government](https://jobs.lever.co/palantir/e6ff8bf2-135e-474d-ad37-24f490ae1dd2) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Software Engineer, Internship](https://jobs.lever.co/palantir/76a60923-bb49-40f5-b061-7c7eb1299602) | UK | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Infrastructure](https://jobs.lever.co/palantir/fd3603a9-7016-45c6-9c8d-04c9279ab85e) | UK | computer-vision,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad](https://jobs.lever.co/palantir/d372c805-d0cd-4a10-9522-fbecc78d6f3e/apply?utm_source=Simplify&ref=Simplify) | UK | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Infrastructure](https://jobs.lever.co/palantir/9265acce-12cd-4179-8c50-55d15963532b/apply?utm_source=Simplify&ref=Simplify) | UK | computer-vision,infra,research | unknown | unknown |
| **Snowflake** | [Software Engineer Intern - Berlin \(2026\)](https://jobs.ashbyhq.com/snowflake/41e65c6c-a01e-4f40-af14-ae75d3b95e27) | Germany | hardware,data-eng,infra,distributed,research,phd-position | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [AI/ML Data Scientist/Engineer New Grad - Analytic Capabilities 🎓](https://careers.jhuapl.edu/jobs/57801?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Data Scientist/Engineer New Grad - Analytic Capabilities 🎓](https://careers.jhuapl.edu/jobs/59818?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Modeler and Data Analyst New Grad 🎓](https://careers.jhuapl.edu/jobs/59858?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Sensor Systems/Data Analytics New Grad](https://careers.jhuapl.edu/jobs/59770?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Signal Processing Intern - Multiple Teams](https://careers.jhuapl.edu/jobs/59875?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Software Engineering/ML/Data Scientist New Grad - Intelligence Systems 🎓](https://careers.jhuapl.edu/jobs/59654?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Systems Engineer/Analyst New Grad - Multi-Mission Planning Development 🎓](https://careers.jhuapl.edu/jobs/58164?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Lawrence Livermore National Laboratory \(LLNL\)** | [Computational Engineering Graduate Intern](https://jobs.smartrecruiters.com/LLNL/3743990014730886?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **University Corporation for Atmospheric Research** | [CESM Software Engineer 1 - Computer Engineering](https://ucar.wd5.myworkdayjobs.com/UCAR_Careers/job/Boulder-CO/CESM-Software-Engineer-I_REQ-2026-117-1?utm_source=Simplify&ref=Simplify) | US | research,climate | unknown | unknown |
| **Wells Fargo** | [Applied Computational Intelligence Intern - ACI Masters - Early Careers 🎓](https://wd1.myworkdaysite.com/recruiting/wf/WellsFargoJobs/job/CHARLOTTE-NC/XMLNAME-2027-Quantitative-Analytics-Summer-Internship-Applied-Computational-Intelligence--ACI-Masters----Early-Careers_R-571698?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |

### Early-company / equity reality check

The company signal is a discovery aid, not a prediction. Private-company options can become valuable, but can also expire, dilute, remain illiquid, or end up worth zero. `private company; verify offer` means the posting does not prove that equity is included. Ask for the option count **and fully diluted percentage**, strike price, vesting/cliff, exercise window, latest common valuation, and liquidation preferences.

## Elite and high-tier live postings (408)

| Company | Role | Category | Region | Term | Eligibility |
|--|--|--|--|--|--|
| **Akuna Capital** | [Hardware Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018880/?gh_jid=8018880&utm_source=github-vansh-ouckah) | Hardware / EE | US | Summer 2027 | review required |
| **Akuna Capital** | [Platform Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018856/?gh_jid=8018856&utm_source=github-vansh-ouckah) | Systems &amp; Infra | US | Summer 2027 | review required |
| **Akuna Capital** | [Python Software Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018853/?gh_jid=8018853&utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Akuna Capital** | [Quantitative Development &amp; Strategy Intern 🇺🇸](https://akunacapital.com/careers/job/8021481/?gh_jid=8021481&utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
| **Akuna Capital** | [Quantitative Research Intern 🇺🇸](https://akunacapital.com/careers/job/8036614/?gh_jid=8036614&utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
| **Akuna Capital** | [Software Engineer \(Entry-Level\) - Python](https://www.akunacapital.com/careers/job/8013230/?gh_jid=8013230) | Software Engineering | US | Unknown | review required |
| **Akuna Capital** | [Software Engineer Intern \(Summer 2027, Python / C++ / Full Stack / C# .NET\)](https://akunacapital.com/careers/job/8018847/) | Software Engineering | US | Summer 2027 | review required |
| **Akuna Capital** | [Software Engineer Intern, C# .NET Desktop](https://akunacapital.com/careers/job/8018886/?gh_jid=8018886&utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Akuna Capital** | [Software Engineer Intern, C++ 🇺🇸](https://akunacapital.com/careers/job/8018847/?gh_jid=8018847&utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Akuna Capital** | [Software Engineer Intern, Full Stack Web 🇺🇸](https://akunacapital.com/careers/job/8018893/?gh_jid=8018893&utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Amazon** | [Robotics - Software Development Engineer Intern/Co-op](https://www.amazon.jobs/en/jobs/3136266/robotics-software-development-engineer-intern-co-op-2026?no_int_redir=1&utm_source=github-vansh-ouckah) | Robotics &amp; Embodied AI | US | 2026 | review required |
| **Apple** | [Software Engineer Intern, Undergrad](https://jobs.apple.com/en-us/details/200664785/software-undergrad-engineering-internships?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Apple** | [Software Engineering Intern, Masters](https://jobs.apple.com/en-us/details/200664320/software-engineering-masters-internships?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Citadel** | [Quantitative Research Analyst University Graduate](https://www.citadel.com/careers/details/quantitative-research-analyst-university-graduate-us/?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Citadel** | [Quantitative Trader: Equity Quantitative Research – University Graduate](https://www.citadel.com/careers/details/quantitative-trader-equity-quantitative-research-university-graduate-us/?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Citadel** | [Sector Data Scientist Intern](https://www.citadel.com/careers/details/sector-data-scientist-2027-intern-us/?utm_source=Simplify&ref=Simplify) | Data | US | 2027 | review required |
| **Citadel** | [Software Engineer Intern](https://www.citadel.com/careers/details/software-engineer-intern-us/?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Citadel** | [Software Engineer – University Graduate](https://www.citadel.com/careers/details/software-engineer-university-graduate-us/?utm_source=Simplify&ref=Simplify) | Software Engineering | US | New Grad 2026 | review required |
| **Citadel Securities** | [Quantitative Research Analyst – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-research-analyst-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | Quant / Finance | UK / Ireland | New Grad 2026 | review required |
| **Citadel Securities** | [Quantitative Trader New Grad](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | Quant / Finance | UK | New Grad 2026 | review required |
| **Citadel Securities** | [Software Engineer – University Graduate](https://www.citadelsecurities.com/careers/details/software-engineer-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | Software Engineering | UK | New Grad 2026 | review required |
| **Cubist Systematic Strategies** | [Quantitative Developer Intern](https://job-boards.greenhouse.io/point72/jobs/7297613002) | Quant / Finance | US | Summer 2027 | review required |
| **DE Shaw** | [Software Developer Intern](https://www.deshaw.com/careers/software-developer-intern-new-york-summer-2027-5894?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **DRW** | [AI/ML Research Intern](https://www.drw.com/work-at-drw/listings/aiml-research-intern-3466679?utm_source=github-vansh-ouckah) | Software Engineering | Unknown | Summer 2027 | review required |
| **DRW** | [FPGA Intern](https://www.drw.com/work-at-drw/listings/fpga-intern-3484423?utm_source=github-vansh-ouckah) | Hardware / EE | US | Summer 2027 | review required |
| **DRW** | [Platform Engineer Intern](https://www.drw.com/work-at-drw/listings/platform-engineer-intern-3468737?utm_source=github-vansh-ouckah) | Systems &amp; Infra | US | Summer 2027 | review required |
| **DRW** | [Quantitative Research Intern](https://www.drw.com/work-at-drw/listings/quantitative-research-intern-3413670?utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
| **DRW** | [Quantitative Trading Analyst Intern](https://job-boards.greenhouse.io/drweng/jobs/7957243?utm_source=Simplify&ref=Simplify) | Quant / Finance | UK | Ambiguous | review required |
| **DRW** | [Quantitative Trading Analyst Intern](https://www.drw.com/work-at-drw/listings/quantitative-trading-analyst-intern-3375090?utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
| **DRW** | [Software Developer Intern](https://www.drw.com/work-at-drw/listings/software-developer-intern-3467328?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **DRW** | [Software Developer Intern](https://www.drw.com/work-at-drw/listings/software-developer-intern-3466687?utm_source=github-vansh-ouckah) | Software Engineering | Unknown | Summer 2027 | review required |
| **Five Rings** | [Quantitative Trader Intern \(Summer 2027\)](https://job-boards.greenhouse.io/fiveringsllc/jobs/5139668008) | Quant / Finance | US | Summer 2027 | review required |
| **Five Rings** | [Software Developer Intern 🇺🇸](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349707008?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **G-Research** | [Data Science Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Data-Science-Internship_R3679?utm_source=Simplify&ref=Simplify) | Software Engineering | UK | Ambiguous | review required |
| **G-Research** | [Machine Learning Research Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Machine-Learning-Research-Internship_R3682?utm_source=Simplify&ref=Simplify) | AI / ML | UK | Ambiguous | review required |
| **G-Research** | [Natural Language Processing Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Natural-Language-Processing-Internship_R3686?utm_source=Simplify&ref=Simplify) | AI / ML | UK | Ambiguous | review required |
| **G-Research** | [Quantitative Research Internship 🎓](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Quant-Research-Internship_R3691?utm_source=Simplify&ref=Simplify) | Quant / Finance | UK | Ambiguous | review required |
| **Google** | [Software Engineering Intern](https://www.google.com/about/careers/applications/jobs/results/85564713261245126-software-engineering-intern-bs-summer-2027?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Hudson River Trading** | [Algorithm Developer New Grad - Quant Researcher](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8052050&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Hudson River Trading** | [Algorithm Development Intern - Quant Research 🎓](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8059837&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Ambiguous | review required |
| **Hudson River Trading** | [Hardware Engineer Intern](https://www.hudsonrivertrading.com/careers/job/?gh_jid=7899574&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Ambiguous | review required |
| **Hudson River Trading** | [Software Engineer Intern](https://www.hudsonrivertrading.com/hrt-job/software-engineering-internship-c-or-python-summer-2027/?gh_src=&utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
| **Hudson River Trading** | [Software Engineer Intern - C++ or Python](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8052083&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Ambiguous | review required |
| **IMC** | [Hardware Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823945101) | Hardware / EE | US | Summer 2027 | review required |
| **IMC** | [Quantitative Research Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4907399101) | Quant / Finance | US | Summer 2027 | review required |
| **IMC** | [Software Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823924101) | Software Engineering | US | Summer 2027 | review required |
| **IMC Trading** | [Graduate Quantitative Researcher \(PhD\)](https://job-boards.eu.greenhouse.io/imc/jobs/4912325101) | Quant / Finance | US | Unknown | review required |
| **IMC Trading** | [Hardware Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4927149101) | Quant / Finance | Netherlands | Unknown | review required |
| **IMC Trading** | [Machine Learning Research Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4907430101) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Machine Learning Research Intern - Summer 2027 - Sydney](https://job-boards.eu.greenhouse.io/imc/jobs/4956547101) | Quant / Finance | Australia | Summer 2027 | review required |
| **IMC Trading** | [Machine Learning Research Intern 🎓](https://job-boards.eu.greenhouse.io/imc/jobs/4912874101?utm_source=Simplify&ref=Simplify) | Quant / Finance | Netherlands | Summer 2027 | review required |
| **IMC Trading** | [Performance Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4842595101?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Quantitative Research Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941208101) | Quant / Finance | Hong Kong | 2027 | review required |
| **IMC Trading** | [Quantitative Trader Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4936262101) | Quant / Finance | Netherlands | Unknown | review required |
| **IMC Trading** | [Quantitative Trader Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4823923101) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Quantitative Trader Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941205101) | Quant / Finance | Hong Kong | 2027 | review required |
| **IMC Trading** | [Software Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4667854101) | Quant / Finance | Netherlands | Unknown | review required |
| **IMC Trading** | [Software Engineer Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941206101) | Quant / Finance | Hong Kong | 2027 | review required |
| **IMC Trading** | [Software Engineer, Early Career](https://job-boards.eu.greenhouse.io/imc/jobs/4577504101) | Quant / Finance | US | Unknown | review required |
| **IMC Trading** | [Trader Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4939846101) | Quant / Finance | Netherlands | Unknown | review required |
| **Jane Street** | [Cybersecurity Analyst Intern](https://www.janestreet.com/join-jane-street/position/8632723002/?utm_source=github-vansh-ouckah) | Security | US | Summer 2027 | review required |
| **Jane Street** | [Data Engineer Intern](https://www.janestreet.com/join-jane-street/position/8631973002/?utm_source=github-vansh-ouckah) | Data | US | Summer 2027 | review required |
| **Jane Street** | [Fundamental Research Analyst Intern](https://www.janestreet.com/join-jane-street/position/8347286002/?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Jane Street** | [Hardware Engineer \(FPGA/ASIC\) Intern](https://www.janestreet.com/join-jane-street/position/8624440002/?utm_source=github-vansh-ouckah) | Hardware / EE | US | Summer 2027 | review required |
| **Jane Street** | [Linux Engineer Intern](https://www.janestreet.com/join-jane-street/position/8626260002/?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Jane Street** | [Machine Learning Engineer Intern](https://www.janestreet.com/join-jane-street/position/8611307002/?utm_source=github-vansh-ouckah) | AI / ML | US | Summer 2027 | review required |
| **Jane Street** | [Machine Learning Researcher Intern](https://www.janestreet.com/join-jane-street/position/8384490002/?utm_source=github-vansh-ouckah) | AI / ML | US | Summer 2027 | review required |
| **Jane Street** | [Network Engineer Intern](https://www.janestreet.com/join-jane-street/position/8620793002/?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Jane Street** | [Quantitative Researcher Intern](https://www.janestreet.com/join-jane-street/position/8498547002/?utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
| **Jane Street** | [Quantitative Trader Intern](https://www.janestreet.com/join-jane-street/position/8617344002/?utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
| **Jane Street** | [Sales and Trading Intern](https://www.janestreet.com/join-jane-street/apply/8537797002?gh_jid=8537797002&utm_source=Simplify&ref=Simplify) | Quant / Finance | UK | Ambiguous | review required |
| **Jane Street** | [Sales and Trading Intern](https://www.janestreet.com/join-jane-street/position/8347385002/?utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
| **Jane Street** | [Software Engineer Intern](https://www.janestreet.com/join-jane-street/position/8599644002/?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Jane Street** | [Tools and Compilers Research and Development Intern](https://www.janestreet.com/join-jane-street/position/5869205002/?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Jane Street** | [Trading Desk Operations Engineer Intern](https://www.janestreet.com/join-jane-street/position/8621450002/?utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
| **Jane Street** | [Windows Engineer Intern](https://www.janestreet.com/join-jane-street/position/8628843002/?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Jump Trading** | [Campus AI Research Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8052281) | Quant / Finance | US | Unknown | review required |
| **Jump Trading** | [Campus AI Research Engineer - Deep Learning \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8052338) | Quant / Finance | US | Unknown | review required |
| **Jump Trading** | [Campus AI Research Engineer – Research Automation \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8052351) | Quant / Finance | US | Unknown | review required |
| **Jump Trading** | [Campus AI Researcher, PhD/Postdoc \(Full-Time\)](https://www.jumptrading.com/hr/job?gh_jid=7976923) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus AI/ML Researcher \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027938) | Quant / Finance | Singapore / China / Hong Kong | Unknown | review required |
| **Jump Trading** | [Campus ASIC Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7974837) | Quant / Finance | Unknown | Unknown | review required |
| **Jump Trading** | [Campus C++ Software Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027946) | Quant / Finance | Singapore | Unknown | review required |
| **Jump Trading** | [Campus Crypto Researcher \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7362318) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus Data Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8002998) | Quant / Finance | US | Unknown | review required |
| **Jump Trading** | [Campus Data Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7975008) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus FPGA Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7974391) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus FPGA Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8003013) | Quant / Finance | US | Unknown | review required |
| **Jump Trading** | [Campus ML Research Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7977145) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus Python Software Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027955) | Quant / Finance | Singapore | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Researcher \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8010307) | Quant / Finance | Netherlands | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Researcher \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027939) | Quant / Finance | Singapore | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Researcher \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027900) | Quant / Finance | China / Hong Kong | Winter/Spring 2027 | review required |
| **Jump Trading** | [Campus Quantitative Researcher \(M1/M2 Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8059384) | Quant / Finance | France | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Researcher Intern - PhD 🎓](https://boards.greenhouse.io/embed/job_app?token=8049938&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Ambiguous | review required |
| **Jump Trading** | [Campus Quantitative Researcher, PhD \(Full-Time\)](https://www.jumptrading.com/hr/job?gh_jid=8125888) | Quant / Finance | US | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Researcher, UG/MS \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7982648) | Quant / Finance | US | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Trader \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027941) | Quant / Finance | Singapore | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Trader \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027922) | Quant / Finance | China / Hong Kong | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Trader \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8050772) | Quant / Finance | Netherlands | Unknown | review required |

_308 more are in [tracker.csv](tracker.csv)._

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
