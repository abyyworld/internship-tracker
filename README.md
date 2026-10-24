# 🎯 Universal Academic & Career Tracker — Internships · Research · PhD · New Grad

<p align="center">
  <a href="https://abyyworld.github.io/internship-tracker/"><img alt="Open the tracker — 4401 open postings" src="https://img.shields.io/badge/Open%20the%20tracker-4401%20open%20postings-1f6feb?style=for-the-badge&labelColor=0d1117"></a>
  <a href="https://abyyworld.github.io/internship-tracker/studio.html"><img alt="Tailor my CV — in the browser" src="https://img.shields.io/badge/Tailor%20my%20CV-in%20the%20browser-2ea043?style=for-the-badge&labelColor=0d1117"></a>
</p>

<p align="center"><b><a href="https://abyyworld.github.io/internship-tracker/">https://abyyworld.github.io/internship-tracker/</a></b><br>
Search and filter every posting, then tailor your CV for one — in the browser, on a phone, with nothing to install.</p>

> Last verified run: **2026-10-24** · **4401 verified-open postings** · **192 research / PhD / postdoc positions**

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

> ⚠️ **35 previously seen roles are stale because at least one source failed or was not checked. They were not marked closed.**

## At a glance

| Metric | Count |
|--|--:|
| Verified-open postings | 4401 |
| Roles discovered today | 180 |
| New verified postings | 180 |
| Research / PhD / postdoc positions | 192 |
| Elite tier | 295 |
| High tier | 360 |
| Eligibility still needs review | 4396 |
| Deadlines within 10 days | 5 |

**By category:** Software Engineering 2503 · Robotics & Embodied AI 391 · Quant / Finance 302 · Data 269 · AI / ML 246 · Security 223 · Hardware / EE 197 · Systems & Infra 183 · Computational Science 85 · HCI / XR 2

**By region:** US 3375 · UK 204 · Canada 198 · Unknown 178 · Singapore 53 · Remote 53 · Germany 39 · France 37 · US / Austria 24 · Hong Kong 24 · South Korea 21 · Netherlands 16 · Brazil 11 · US / Canada 10 · India 10 · China 9 · Ireland 9 · Spain 9 · Switzerland 8 · Italy 8 · US / Australia 7 · Poland 6 · Taiwan 6 · Mexico 6 · US / UK 5 · Australia 5 · China / Hong Kong 4 · US / Netherlands 4 · Global 4 · Austria 4 · UK / Global 4 · Singapore / Hong Kong 4 · New Zealand 4 · Singapore / China / Hong Kong 3 · US / France 3 · Serbia 3 · US / Italy 3 · US / Mexico 3 · US / Global 2 · Singapore / China / Hong Kong / Australia 2 · Sweden 2 · Belgium 2 · Canada / UK 1 · UK / Portugal / Poland 1 · UK / Ireland 1 · France / Japan / Hong Kong 1 · US / France / Singapore / Hong Kong 1 · Denmark 1 · Japan 1 · UK / Netherlands 1 · US / Belgium 1 · US / UK / Netherlands / Singapore 1 · UK / Netherlands / Singapore 1 · US / Singapore 1 · UAE 1 · US / Europe 1 · UK / France 1 · France / Switzerland / UAE 1 · Netherlands / France / Switzerland / UAE 1 · France / Switzerland 1 · US / UK / Germany 1

**By degree evidence:** Unknown 3567 · Undergraduate eligible 389 · Advanced/unknown 237 · PhD 160 · Masters 48

## Newly opened (180)

| Company | Role | Category | Region | Term | Eligibility |
|--|--|--|--|--|--|
| **Amazon** | [ASIC Engineer Intern](https://amazon.jobs/en/jobs/10517535/asic-engineer-intern-annapurna-labs-2027?utm_source=github-vansh-ouckah) | Hardware / EE | US | 2027 | review required |
| **Amazon** | [Frontier AI &amp; Robotics Intern](https://www.amazon.jobs/en/jobs/10564599/2027-frontier-ai-robotics-internship-undergraduate-united-states-frontier-ai-robotics-frontier-ai-robotics?utm_source=github-vansh-ouckah) | Robotics &amp; Embodied AI | US | 2027 | review required |
| **Amazon** | [Software Development Engineer Intern, Amazon Leo 🇺🇸](https://www.amazon.jobs/en/jobs/10587999/software-development-engineer-intern-amazon-leo-summer-2027-usa?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Amazon** | [Software Development Engineer Intern, Amazon Leo, Embedded Systems 🇺🇸](https://www.amazon.jobs/en/jobs/10571374/software-development-engineer-embedded-systems-intern-amazon-leo-summer-2027-usa?utm_source=github-vansh-ouckah) | Hardware / EE | US | Summer 2027 | review required |
| **Amazon** | [Software Development Engineer Intern, Embedded Systems](https://www.amazon.jobs/en/jobs/10567914/software-development-engineer-intern-embedded-systems-summer-2027-usa?utm_source=github-vansh-ouckah) | Hardware / EE | US | Summer 2027 | review required |
| **Microsoft** | [Software Engineer Intern, Security &amp; Identity](https://apply.careers.microsoft.com/careers/job/1970393557044771?utm_source=github-vansh-ouckah) | Security | US | Summer 2027 | review required |
| **MongoDB** | [2027 - Summer Software Engineer Intern, Dublin](https://www.mongodb.com/careers/job/?gh_jid=8267099) | Software Engineering | Unknown | Summer 2027 | review required |
| **MongoDB** | [Software Engineer Intern](https://www.mongodb.com/careers/job/?gh_jid=8209134&utm_source=Simplify&ref=Simplify) | Software Engineering | US | 2027 | review required |
| **Qualcomm** | [AI and DSP Applications Engineer Intern](https://qualcomm.eightfold.ai/careers/job/446721686396?utm_source=Simplify&ref=Simplify) | Hardware / EE | Canada | Ambiguous | review required |
| **Qualcomm** | [Digital Design Engineer Intern](https://qualcomm.eightfold.ai/careers/job/446721156182?utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | Ambiguous | review required |
| **Qualcomm** | [Silicon Engineering Intern](https://qualcomm.eightfold.ai/careers/job/446721302528?utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | Ambiguous | review required |
| **Waymo** | [2027 Summer Intern, MS/PhD, Machine Learning, Driver Refinement Foundations](https://careers.withwaymo.com/jobs?gh_jid=8304574) | Robotics &amp; Embodied AI | US | Summer 2027 | review required |
| **🔥 Waymo** | [Software Engineer Intern - MS/PhD - ML Frameworks and Efficiency 🎓](https://careers.withwaymo.com/jobs?gh_jid=8287385&utm_source=Simplify&ref=Simplify) | Robotics &amp; Embodied AI | US | Summer 2027 | review required |
| **1Password** | [Developer Intern, Credential Brokering - Winter 2027](https://jobs.ashbyhq.com/1password/67bfbd8b-aba9-42b1-a8a8-833367888fba) | Security | US | Winter 2027 | review required |
| **1Password** | [Developer Intern, Developer Interfaces - Winter 2027](https://jobs.ashbyhq.com/1password/00f861d4-2b4a-4159-b6dc-8aed0cde6e39) | Security | US | Winter 2027 | review required |
| **1Password** | [Product Management Intern, End User Experience - Winter 2027](https://jobs.ashbyhq.com/1password/bef2e88e-9590-467d-8ba6-821b30529003) | Security | US | Winter 2027 | review required |
| **ABB** | [R&amp;D Software Engineer Intern](https://abb.wd3.myworkdayjobs.com/external_career_page/job/Greenville-South-Carolina-United-States-of-America/R-D-Software-Engineer_JR00050035?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **ACI Worldwide** | [Technology Intern](https://ebwg.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX/job/19943?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **ASML** | [Application Software QA Engineer Intern](https://asml.wd3.myworkdayjobs.com/en-US/asmlext1/job/San-Jose-CA-USA/Internship---Application-Software-QA-Engineer_J-00354565?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **ASML** | [Platform Software Engineer In Test Intern](https://asml.wd3.myworkdayjobs.com/asmlext1/job/San-Jose-CA-USA/Platform-Software-Engineer-In-Test---Internship-_J-00354558?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **ASML** | [Software Engineer In Test Intern, MOD](https://asml.wd3.myworkdayjobs.com/asmlext1/job/San-Jose-CA-USA/Internship---Software-Engineer-In-Test--MOD-_J-00354568?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **ASML** | [Software Quality Assurance Intern](https://asml.wd3.myworkdayjobs.com/en-US/asmlext1/job/San-Jose-CA-USA/Internship---Software-Quality-Assurance_J-00354563?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **AVARINT** | [Software Engineer Intern, DIADS](https://recruiting.paylocity.com/Recruiting/Jobs/Details/3814718?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Addepar** | [Product Manager – Early Career - AI Platform](https://job-boards.greenhouse.io/addepar1/jobs/8910404002?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Affirm** | [Software Engineer New Grad - Instruments team](https://job-boards.greenhouse.io/affirm/jobs/8011718003?utm_source=Simplify&ref=Simplify) | Software Engineering | UK | 2027 | review required |
| **Airbus** | [Operational Excellence Analyst Intern - Data Analytics - Operational Excellence](https://ag.wd3.myworkdayjobs.com/Airbus/job/Mobile-Area-AL/Summer-Internship-2027---Data-Analytics---Operational-Excellence_JR10442492?utm_source=Simplify&ref=Simplify) | Data | US | Summer 2027 | review required |
| **Altera** | [Software Intern](https://altera.wd1.myworkdayjobs.com/en-US/altera/job/Toronto-Ontario-Canada/Software-Intern_R03373?utm_source=github-vansh-ouckah) | Software Engineering | Canada | Summer 2027 | review required |
| **Ambarella** | [Physical Design Engineer Intern](https://ambarella.wd108.myworkdayjobs.com/ambarella/job/US-Headquarters/Physical-Design-Engineer-Intern_JR100393?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **American Express** | [AI Engineer Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26015552?utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | Ambiguous | review required |
| **American Family Insurance Group** | [AI Platform Engineering Intern](https://amfam.wd1.myworkdayjobs.com/en-US/Careers/job/WI-Madison/Product-Data-Engineering-Intern--Hybrid-_R39462?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **American Family Insurance Group** | [Business Intelligence Enablement Intern](https://amfam.wd1.myworkdayjobs.com/AmFamGroupInternCareers/job/WI-Madison/Summer-2027-Intern---Business-Intelligence-Enablement_R39531?utm_source=Simplify&ref=Simplify) | Data | US | Summer 2027 | review required |
| **Amperesand** | [AI/ML Engineer Intern](https://job-boards.greenhouse.io/amperesand/jobs/4465899009?utm_source=github-vansh-ouckah) | Software Engineering | US | Ambiguous | review required |
| **Anduril** | [2027 New Grad Low Observables Engineer](https://boards.greenhouse.io/andurilindustries/jobs/5269789007?gh_jid=5269789007) | Robotics &amp; Embodied AI | US | 2027 | review required |
| **Aptiv** | [HVP/Certification Engineer Intern](https://aptiv.wd5.myworkdayjobs.com/aptiv_careers/job/CAN-Kanata-2-ON---WR/HVP-Cert--Engineer-Intern_J000704379?utm_source=github-vansh-ouckah) | Software Engineering | Canada | Summer 2027 | review required |
| **Aptiv** | [Linux Engineering Intern](https://aptiv.wd5.myworkdayjobs.com/en-US/aptiv_careers/job/CAN-Kanata-2-ON---WR/Linux-Engineering-Intern_J000704371?utm_source=github-vansh-ouckah) | Software Engineering | Canada | Summer 2027 | review required |
| **Aramco Americas** | [Research and Development Intern - Boston Research Center - 2027 Summer Student Program](https://aramcoservices.applytojob.com/apply/rnpFdnTdYb/Research-And-Development-Boston-Research-Center-2027-Summer-Student-Program?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **Auto-Owners Insurance** | [Software Engineer Intern](https://aoins.wd5.myworkdayjobs.com/concord/job/Bedford-NH/Software-Engineer-Intern_R_14465?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Biogen** | [Integrated Insights &amp; Analytics Co-op, Nephrology](https://biibhr.wd3.myworkdayjobs.com/external/job/Cambridge-MA/Co-op--Integrated-Insights---Analytics--Nephrology_REQ24281?utm_source=github-vansh-ouckah) | Data | US | Summer 2027 | review required |
| **Blue Cross Blue Shield of Michigan** | [Data Analytics Intern - HEDIS](https://ejko.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_3/job/14838?utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **Brevan Howard** | [Trading Intern](https://wd3.myworkdaysite.com/recruiting/brevanhoward/BH_ExternalCareers/job/London/XMLNAME-2027-Summer-Internship-Program---Trading--London_JR101584?utm_source=Simplify&ref=Simplify) | Quant / Finance | UK | Summer 2027 | review required |
| **Brookhaven Lab** | [Data Engineering Student Assistant Intern](https://bnl.wd1.myworkdayjobs.com/externa/job/Upton-NY/Data-Engineering-Student-Assistant_JR102753?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **C.H. Robinson** | [Cyber Security Intern](https://chrobinson.wd5.myworkdayjobs.com/CHRobinson/job/Eden-Prairie-MN-United-States-of-America/Security-Internship-2027_R49322?utm_source=github-vansh-ouckah) | Security | US | 2027 | review required |
| **CAE** | [Junior Software Developer - System Integration Labs](https://cae.wd3.myworkdayjobs.com/career/job/Mirabel/Dveloppeureuse-logiciel-junior---Bancs-d-essais--Rive-Nord-_123921-1?utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | New Grad 2026 | review required |
| **CSX** | [Mechanical Engineering Intern](https://fa-eowa-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CSXCareers/job/54844?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **CVS Health** | [Innovation &amp; Technology Data Engineering Intern](https://cvshealth.wd1.myworkdayjobs.com/CVS_Health_Careers/job/NY---New-York/Innovation---Technology-Internship---Data-Engineering---Summer-2027--Undergraduate-_R1081090?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **CVS Health** | [Innovation &amp; Technology Internship - Data Science 🎓](https://cvshealth.wd1.myworkdayjobs.com/CVS_Health_Careers/job/NY---New-York/Innovation---Technology-Internship---Data-Science---Summer-2027--Undergraduate-_R1081067?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **CVS Health** | [Innovation &amp; Technology Internship - Product &amp; Agile Delivery](https://cvshealth.wd1.myworkdayjobs.com/CVS_Health_Careers/job/Hartford-Farmington-Ave-Rogers/Innovation---Technology-Internship---Product---Agile-Delivery---Summer-2027--Undergraduate-_R1080767?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **CVS Health** | [Innovation &amp; Technology Software Engineering: Data &amp; Intelligence Intern 🎓](https://cvshealth.wd1.myworkdayjobs.com/en-US/CVS_Health_Careers/job/NY---New-York/Innovation---Technology-Internship--Software-Engineering--Data---Intelligence-Summer-2027-Graduate_R1081128?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **CVS Health** | [Software Engineer Intern - Platform &amp; Applications](https://cvshealth.wd1.myworkdayjobs.com/CVS_Health_Careers/job/AZ---Scottsdale/Innovation-Technology-Internship-Software-Engineering--Platform---Applications-Summer-2027-Undergrad_R1081193?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **Carrier Global** | [Software Engineer Intern](https://carrier.wd5.myworkdayjobs.com/jobs/job/CAN01-Carrier-Syracuse-6304-Carrier-Parkway-East-Syracuse-NY-13057-USA/Software-Engineering-Intern---Summer_30220588?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Cclfg** | [Intern, Investment Analytics Engagement](https://cclfg.cclgroup.com/careers/opportunities/posting/?gh_jid=4464732009) | Data | Canada | None | review required |
| **Ciena** | [Hardware Engineer New Grad](https://ciena.wd5.myworkdayjobs.com/Careers/job/Ottawa/Hardware-Engineer---New-Grad_R031914?utm_source=Simplify&ref=Simplify) | Hardware / EE | Canada | New Grad 2026 | review required |
| **Ciena** | [Product Validation Engineer New Grad](https://ciena.wd5.myworkdayjobs.com/Careers/job/Quebec/Ingnieur-de-Validation-de-Composant--Product-Validation-Engineer---New-Grad_R031778?utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | New Grad 2026 | review required |
| **Cisco** | [Software Consulting Engineer I Intern](https://cisco.wd5.myworkdayjobs.com/cisco_careers/job/USA-RESEARCH-TRIANGLE-PARK/Software-Consulting-Engineer-I--Intern--United-States_2025180?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Cisco** | [Software Engineer Data &amp; AI II Intern](https://cisco.wd5.myworkdayjobs.com/Cisco_Careers/job/San-Jose-California-US/Software-Engineer-Data---AI-II--Intern----United-States_2026798?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Cisco** | [Software Engineer Intern, Data &amp; AI](https://cisco.wd5.myworkdayjobs.com/en-US/Cisco_Careers/job/San-Jose-California-US/Software-Engineer-Data---AI-I--Intern----United-States_2026306?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Citi** | [Software Developer New Grad - Application Development](https://citi.wd5.myworkdayjobs.com/2/job/Jacksonville-Florida-United-States/Technology--Application-Development--Full-Time-Analyst--Jacksonville---USA--2027_261004412?utm_source=Simplify&ref=Simplify) | Software Engineering | US | 2027 | review required |
| **Citi** | [Technology Analyst Intern - Application Development](https://citi.wd5.myworkdayjobs.com/2/job/Mississauga-Ontario-Canada/Technology--Application-Development--Summer-Analyst--Mississauga--Canada--2027_261003301?utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | Summer 2027 | review required |
| **Citi** | [Technology Analyst Intern - Application Development](https://citi.wd5.myworkdayjobs.com/2/job/Jacksonville-Florida-United-States/Technology--Application-Development--Summer-Analyst--Jacksonville---USA--2027_261004418?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **Citi** | [Technology Placement Analyst Intern - Application Development](https://citi.wd5.myworkdayjobs.com/2/job/Belfast--United-Kingdom/Technology---Application-Development--Placement-Analyst--Belfast-2027_261002927?utm_source=Simplify&ref=Simplify) | Software Engineering | UK | 2027 | review required |

_120 more are in [tracker.csv](tracker.csv)._

## Browse by category

Every category is listed the same way. Live geography reflects what official feeds expose today; the worldwide career-hub and academic watchlists are kept separately in [manual_checks.md](manual_checks.md).

### Software Engineering (2503 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Python Software Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018853/?gh_jid=8018853&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer \(Entry-Level\) - Python](https://www.akunacapital.com/careers/job/8013230/?gh_jid=8013230) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer Intern \(Summer 2027, Python / C++ / Full Stack / C# .NET\)](https://akunacapital.com/careers/job/8018847/) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer Intern, C# .NET Desktop](https://akunacapital.com/careers/job/8018886/?gh_jid=8018886&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer Intern, C++ 🇺🇸](https://akunacapital.com/careers/job/8018847/?gh_jid=8018847&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer Intern, Full Stack Web 🇺🇸](https://akunacapital.com/careers/job/8018893/?gh_jid=8018893&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Amazon** | [Software Development Engineer Intern, Amazon Leo 🇺🇸](https://www.amazon.jobs/en/jobs/10587999/software-development-engineer-intern-amazon-leo-summer-2027-usa?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Anthropic** | [Research Associate, Biology](https://job-boards.greenhouse.io/anthropic/jobs/5285248008) | US | research | unknown | unknown |
| **Apple** | [Software Engineer Intern, Undergrad](https://jobs.apple.com/en-us/details/200664785/software-undergrad-engineering-internships?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Apple** | [Software Engineering Intern, Masters](https://jobs.apple.com/en-us/details/200664320/software-engineering-masters-internships?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Citadel** | [Software Engineer Intern](https://www.citadel.com/careers/details/software-engineer-intern-us/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Citadel** | [Software Engineer – University Graduate](https://www.citadel.com/careers/details/software-engineer-university-graduate-us/?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Citadel Securities** | [Software Engineer – University Graduate](https://www.citadelsecurities.com/careers/details/software-engineer-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **DE Shaw** | [Software Developer Intern](https://www.deshaw.com/careers/software-developer-intern-new-york-summer-2027-5894?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **DRW** | [AI/ML Research Intern](https://www.drw.com/work-at-drw/listings/aiml-research-intern-3466679?utm_source=github-vansh-ouckah) | Unknown | research | unknown | unknown |
| **DRW** | [AI/ML Research Intern](https://job-boards.greenhouse.io/drweng/jobs/7991171) | Canada | research | unknown | unknown |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/7992936) | US |  | unknown | unknown |
| **DRW** | [Software Developer Intern](https://www.drw.com/work-at-drw/listings/software-developer-intern-3466687?utm_source=github-vansh-ouckah) | Unknown |  | unknown | unknown |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/8020364) | Netherlands |  | unknown | unknown |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/7942281) | UK |  | unknown | unknown |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/7991196) | Canada |  | unknown | unknown |
| **DRW** | [Software Developer Intern - Industrial Placement](https://job-boards.greenhouse.io/drwuniversityjobs/jobs/7364884) | UK |  | unknown | unknown |
| **Five Rings** | [Software Developer Intern 🇺🇸](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349707008?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **G-Research** | [Software Engineer Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Software-Engineering-Intern_R3746?utm_source=Simplify&ref=Simplify) | UK | research | unknown | unknown |
| **Google** | [Software Engineering Intern](https://www.google.com/about/careers/applications/jobs/results/85564713261245126-software-engineering-intern-bs-summer-2027?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **IMC** | [Software Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823924101) | US |  | unknown | unknown |
| **Jane Street** | [Fundamental Research Analyst Intern](https://www.janestreet.com/join-jane-street/position/8347286002/?utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **Jane Street** | [Linux Engineer Intern](https://www.janestreet.com/join-jane-street/position/8626260002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Network Engineer Intern](https://www.janestreet.com/join-jane-street/position/8620793002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Software Engineer Intern](https://www.janestreet.com/join-jane-street/position/8599644002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Tools and Compilers Research and Development Intern](https://www.janestreet.com/join-jane-street/position/5869205002/?utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **Jane Street** | [Windows Engineer Intern](https://www.janestreet.com/join-jane-street/position/8628843002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Man Group** | 2027 Summer Technology Internship Programme | UK |  | unknown | unknown |
| **Man Group** | [Technology Summer Internship](https://job-boards.eu.greenhouse.io/mangroup/jobs/4978895101) | Unknown |  | unknown | unknown |
| **Marshall Wace** | [Technology Intern - 2027 - Singapore](https://job-boards.greenhouse.io/mwinternshipprogram/jobs/8608327002) | Singapore |  | unknown | unknown |
| **Marshall Wace** | [Technology Intern - Hong Kong - 2027](https://job-boards.greenhouse.io/mwinternshipprogram/jobs/8608328002) | Hong Kong |  | unknown | unknown |
| **Marshall Wace** | [Technology Intern - London - 2027](https://job-boards.greenhouse.io/mwinternshipprogram/jobs/8598324002) | UK |  | unknown | unknown |
| **Marshall Wace** | [Technology Intern - New York - 2027](https://job-boards.greenhouse.io/mwinternshipprogram/jobs/8606238002) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Cloud &amp; Distributed Backend](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922923&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, CoreAI](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&utm_source=github-vansh-ouckah) | US / Global |  | unknown | unknown |

_2463 more are in [tracker.csv](tracker.csv)._

### Robotics & Embodied AI (391 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Amazon** | [Frontier AI &amp; Robotics Intern](https://www.amazon.jobs/en/jobs/10564599/2027-frontier-ai-robotics-internship-undergraduate-united-states-frontier-ai-robotics-frontier-ai-robotics?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Amazon** | [Robotics - Software Development Engineer Intern/Co-op](https://www.amazon.jobs/en/jobs/3136266/robotics-software-development-engineer-intern-co-op-2026?no_int_redir=1&utm_source=github-vansh-ouckah) | US | robot-software | unknown | unknown |
| **🔥 Amazon** | [Hardware Development Engineer Intern Co-op - Robotics](https://amazon.jobs/en/jobs/10535282/hardware-development-engineer-intern-co-op-robotics-2027?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Amazon** | [Software Development Engineer Intern - Robotics](https://amazon.jobs/en/jobs/10529525/software-development-engineer-intern-robotics-2027?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [Research Intern - Robotic Perception and Learning 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-WA-Redmond/PhD-Research-Intern--Robotic-Perception-and-Learning---2027_JR2027089?utm_source=Simplify&ref=Simplify) | US | perception,research | unknown | unknown |
| **🔥 NVIDIA** | [Research Intern - Robotics 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-WA-Seattle/Research-Intern--Robotics---Summer-2027_JR2025647?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **🔥 NVIDIA** | [Research Intern - World Models and Synthetic Data for Autonomous Driving 🎓](https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Research-Intern--World-Models-and-Synthetic-Data-for-Autonomous-Driving---Summer-2027_JR2026839-1?utm_source=github-vansh-ouckah) | US | autonomy,research | unknown | unknown |
| **🔥 NVIDIA** | [Research Scientist New Grad - Robotics Research 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-WA-Seattle/Research-Scientist--Robotics-Research----PhD-New-College-Grad-2026_JR2011473?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **🔥 NVIDIA** | [Research Scientist PhD New Grad - Autonomous Systems and Physical AI Research 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Research-Scientist--Autonomous-Systems-and-Physical-AI-Research---PhD-New-College-Grad-2026_JR2027551?utm_source=Simplify&ref=Simplify) | US | autonomy,research,phd-position | unknown | unknown |
| **Cerebras Systems** | [Supplier Quality Engineer - New Grad](https://jobs.ashbyhq.com/cerebras/04ce4198-d9b6-4aae-ad11-97708033f94a) | US | controls,robot-software,hardware,research | unknown | unknown |
| **Nuro** | [Software Engineer, AI Platform - Intern](https://nuro.ai/careersitem?gh_jid=7351061) | US | autonomous vehicles | private-scaleup | private company; verify offer |
| **Nuro** | [Software Engineer, AI Platform - New Grad](https://nuro.ai/careersitem?gh_jid=7351066) | US | autonomous vehicles | private-scaleup | private company; verify offer |
| **Palantir** | [American Tech Fellowship](https://jobs.lever.co/palantir/0ccbe620-a3ef-41d1-a5c4-68e56b3c91d0) | Unknown | controls,robot-software,hardware,funded | unknown | unknown |
| **The Allen Institute for AI** | [Research Intern - Robotics 🎓](https://job-boards.greenhouse.io/thealleninstitute/jobs/8293641?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Waymo** | [2027 Summer Intern, BS/MS, Software Engineer, RO Performance team, Release Evaluation \(Simulation\)](https://careers.withwaymo.com/jobs?gh_jid=8214729) | Poland | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, BS/MS, Software Engineering, Commercialization](https://careers.withwaymo.com/jobs?gh_jid=8268204) | Poland | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, MS, PhD, Software Engineer](https://careers.withwaymo.com/jobs?gh_jid=8250220) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, MS, Software Engineering, Behavior Test](https://careers.withwaymo.com/jobs?gh_jid=8174504) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, MS/PhD, Machine Learning, Driver Refinement Foundations](https://careers.withwaymo.com/jobs?gh_jid=8304574) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, MS/PhD, Machine Learning, Driver Refinement Foundations](https://careers.withwaymo.com/jobs?gh_jid=8243556) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, MS/PhD, Perception, Model Lifecycle](https://careers.withwaymo.com/jobs?gh_jid=8248411) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Machine Learning, Simulation Realism](https://careers.withwaymo.com/jobs?gh_jid=8265868) | UK | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Perception Systems Engineering: Pedestrian Detection Precision](https://careers.withwaymo.com/jobs?gh_jid=8234670) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Research Scientist, Visual Reasoning](https://careers.withwaymo.com/jobs?gh_jid=8292367) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Research, Behavior Post-training](https://careers.withwaymo.com/jobs?gh_jid=8289816) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Research, RSI for Autonomous Driving](https://careers.withwaymo.com/jobs?gh_jid=8306779) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Research, VLM Harnesses for AV Planning](https://careers.withwaymo.com/jobs?gh_jid=8301854) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Research, World Action Model](https://careers.withwaymo.com/jobs?gh_jid=8243732) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Research, World Modeling Evaluation](https://careers.withwaymo.com/jobs?gh_jid=8265173) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Software Engineer, Simulation](https://careers.withwaymo.com/jobs?gh_jid=8227640) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [2027 Summer Intern - AI Foundations - Recipes 🎓](https://careers.withwaymo.com/jobs?gh_jid=8306841&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [AI-driven ML Performance Engineering Intern - MS/PhD 🎓](https://careers.withwaymo.com/jobs?gh_jid=8248060&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Applied Research Scientist – New Grad - Perception Large Language Model/Vision-Language Model - PhD 🎓](https://careers.withwaymo.com/jobs?gh_jid=7488508&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Data Science Intern - PhD 🎓](https://careers.withwaymo.com/jobs?gh_jid=8221956&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Human Behavior Analytics Intern - Safety Research](https://careers.withwaymo.com/jobs?gh_jid=8197899&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [MS/PhD Intern - Sim-Realism ML Infrastructure 🎓](https://careers.withwaymo.com/jobs?gh_jid=8205680&utm_source=Simplify&ref=Simplify) | UK | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [MS/PhD, ML Systems &amp; Behavior Discovery Intern 🎓](https://careers.withwaymo.com/jobs?gh_jid=8257159&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Machine Learning Engineer Intern - MS/PhD - Simulator Realism Evaluation 🎓](https://careers.withwaymo.com/jobs?gh_jid=8214350&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Machine Learning Engineer Intern - MS/PhD 🎓](https://careers.withwaymo.com/jobs?gh_jid=8223735&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Machine Learning Engineer Intern - Road Understanding 🎓](https://careers.withwaymo.com/jobs?gh_jid=8224746&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |

_351 more are in [tracker.csv](tracker.csv)._

### Quant / Finance (302 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Quantitative Development &amp; Strategy Intern 🇺🇸](https://akunacapital.com/careers/job/8021481/?gh_jid=8021481&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Akuna Capital** | [Quantitative Research Intern 🇺🇸](https://akunacapital.com/careers/job/8036614/?gh_jid=8036614&utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **Akuna Capital University** | [Junior Quantitative Developer &amp; Strategist](https://www.akunacapital.com/careers/job/8016687/?gh_jid=8016687&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Akuna Capital University** | [Junior Quantitative Researcher](https://www.akunacapital.com/careers/job/8036541/?gh_jid=8036541&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Citadel** | [Quantitative Research Analyst University Graduate](https://www.citadel.com/careers/details/quantitative-research-analyst-university-graduate-us/?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Citadel** | [Quantitative Trader: Equity Quantitative Research – University Graduate](https://www.citadel.com/careers/details/quantitative-trader-equity-quantitative-research-university-graduate-us/?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Citadel Securities** | [Quantitative Research Analyst – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-research-analyst-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | UK / Ireland | research | unknown | unknown |
| **Citadel Securities** | [Quantitative Trader New Grad](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **Citadel Securities** | [Quantitative Trader – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-us-miami/?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Citadel Securities** | [Quantitative Trader – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-us-new-york/?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Cubist Systematic Strategies** | [Quantitative Developer Intern](https://job-boards.greenhouse.io/point72/jobs/7297613002) | US |  | unknown | unknown |
| **DRW** | [Quantitative Research Intern](https://job-boards.greenhouse.io/drweng/jobs/7818540) | US | research | unknown | unknown |
| **DRW** | [Quantitative Research Intern](https://job-boards.greenhouse.io/drweng/jobs/7957756) | UK | research | unknown | unknown |
| **DRW** | [Quantitative Research Intern](https://job-boards.greenhouse.io/drweng/jobs/8014915) | Singapore | research | unknown | unknown |
| **DRW** | [Quantitative Trading Analyst Intern](https://job-boards.greenhouse.io/drweng/jobs/7668776) | US |  | unknown | unknown |
| **DRW** | [Quantitative Trading Analyst Intern](https://job-boards.greenhouse.io/drweng/jobs/7957243) | UK |  | unknown | unknown |
| **DRW** | [Quantitative Trading Analyst Intern - IAP Winternship \(MIT Students Only\)](https://job-boards.greenhouse.io/drwuniversityjobs/jobs/8259714) | US |  | unknown | unknown |
| **Five Rings** | [Quantitative Trader Intern \(Summer 2027\)](https://job-boards.greenhouse.io/fiveringsllc/jobs/5139668008) | US |  | unknown | unknown |
| **Five Rings Capital** | [Summer Intern 2027 - Quantitative Researcher \(PhD\)](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349219008) | US | phd-position | unknown | unknown |
| **Five Rings Capital** | [Trading Operations Engineer Intern](https://job-boards.greenhouse.io/fiveringsllc/jobs/5420708008?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Hudson River Trading** | [Algorithm Developer New Grad - Quant Researcher](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8052050&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Hudson River Trading** | [Data Scientist Intern](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8257369&utm_source=Simplify&ref=Simplify) | US / UK |  | unknown | unknown |
| **Hudson River Trading** | [Software Engineer Intern](https://www.hudsonrivertrading.com/hrt-job/software-engineering-internship-c-or-python-summer-2027/?gh_src=&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **IMC** | [Quantitative Research Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4907399101) | US | research | unknown | unknown |
| **IMC Trading** | [Deep Learning Research Intern - 2027 - Sydney](https://job-boards.eu.greenhouse.io/imc/jobs/4956547101) | Australia | research | unknown | unknown |
| **IMC Trading** | [Deep Learning Research Intern - Summer 2027 - Amsterdam](https://job-boards.eu.greenhouse.io/imc/jobs/4912874101) | Netherlands | research | unknown | unknown |
| **IMC Trading** | [Graduate Quantitative Researcher \(PhD\)](https://job-boards.eu.greenhouse.io/imc/jobs/4912325101) | US | phd-position | unknown | unknown |
| **IMC Trading** | [Hardware Machine Learning PhD Research Internship](https://job-boards.eu.greenhouse.io/imc/jobs/4975945101) | US | research,phd-position | unknown | unknown |
| **IMC Trading** | [Machine Learning Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4962456101?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **IMC Trading** | [Machine Learning Research Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4907430101) | US | research | unknown | unknown |
| **IMC Trading** | [Performance Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4842595101?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **IMC Trading** | [Quantitative Research Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941208101) | Hong Kong | research | unknown | unknown |
| **IMC Trading** | [Quantitative Trader Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4936262101) | Netherlands |  | unknown | unknown |
| **IMC Trading** | [Quantitative Trader Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4823923101) | US |  | unknown | unknown |
| **IMC Trading** | [Quantitative Trader Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941205101) | Hong Kong |  | unknown | unknown |
| **IMC Trading** | [Software Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4667854101) | Netherlands |  | unknown | unknown |
| **IMC Trading** | [Software Engineer Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941206101) | Hong Kong |  | unknown | unknown |
| **IMC Trading** | [Software Engineer, Early Career](https://job-boards.eu.greenhouse.io/imc/jobs/4796143101) | US |  | unknown | unknown |
| **IMC Trading** | [Trader Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4939846101) | Netherlands |  | unknown | unknown |
| **Jane Street** | [Quantitative Researcher Intern](https://www.janestreet.com/join-jane-street/position/8498547002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |

_262 more are in [tracker.csv](tracker.csv)._

### Data (269 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Apple Bank** | [IT Data Intern - Analytics, &amp; Automation](https://applebank.wd5.myworkdayjobs.com/applebankcareers/job/New-York-NY/XMLNAME-2027-Summer-Intern--IT-Data--Analytics----Automation_2026-1414?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Jane Street** | [Data Engineer Intern](https://www.janestreet.com/join-jane-street/position/8631973002/?utm_source=github-vansh-ouckah) | US | data-eng | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Data Platform/Analytics](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922931&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Point72** | [Data Scientist Intern 🎓](https://boards.greenhouse.io/point72/jobs/8885299002?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Amazon** | [Business Intelligence Engineer Intern](https://amazon.jobs/en/jobs/10553765/business-intelligence-engineer-internship-2027-us?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Amazon** | [Data Engineer Early Career](https://amazon.jobs/en/jobs/10559101/data-engineer-early-career-2026-can?utm_source=Simplify&ref=Simplify) | Canada | data-eng | unknown | unknown |
| **🔥 Amazon** | [Data Engineer Intern](https://amazon.jobs/en/jobs/10553907/data-engineer-internship-2027-us?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **🔥 Google** | [Business Data Scientist Intern 🎓](https://www.google.com/about/careers/applications/jobs/results/134577198026629830?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Google** | [Data Scientist Research Intern - PhD 🎓](https://www.google.com/about/careers/applications/jobs/results/89965613241246406?utm_source=Simplify&ref=Simplify) | US | research,phd-position | unknown | unknown |
| **🔥 Meta** | [Data Scientist Intern - Product Analytics](https://www.metacareers.com/jobs/1633096478817942?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Airbnb** | [Strategic Finance &amp; Analytics Intern \(MBA\)](https://careers.airbnb.com/positions/8285171?gh_jid=8285171) | US |  | unknown | unknown |
| **Coinbase** | [Internal Audit Analytics Intern](https://www.coinbase.com/careers/positions/8221238?gh_jid=8221238) | US |  | unknown | unknown |
| **Figma** | [Data Engineer Intern \(2027\)](https://boards.greenhouse.io/figma/jobs/6178851004?gh_jid=6178851004) | US | data-eng | unknown | unknown |
| **Stripe** | [PhD Data Scientist, Intern](https://stripe.com/jobs/search?gh_jid=8194283) | US | phd-position | unknown | unknown |
| **Stripe** | [PhD Data Scientist, Intern](https://stripe.com/jobs/search?gh_jid=8194285) | Canada | phd-position | unknown | unknown |
| **🔥 Coinbase** | [Analytics Engineer Intern](https://boards.greenhouse.io/embed/job_app?token=8175471&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Coinbase** | [Data Engineer Intern](https://boards.greenhouse.io/embed/job_app?token=8175459&utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **🔥 Coinbase** | [Data Science Intern - Strategy, Execution, &amp; Analytics - Platform](https://boards.greenhouse.io/embed/job_app?token=8175462&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Coinbase** | [People Analytics Intern](https://boards.greenhouse.io/embed/job_app?token=8175517&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **ABB** | [Sales Excellence Data Analytics Intern](https://abb.wd3.myworkdayjobs.com/external_career_page/job/USA-NC-Cary/Sales-Excellence-Data-Analytics-Intern---Summer-2027_JR00050987?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **AECOM** | [Engineering/Data Analytics Intern](https://jobs.smartrecruiters.com/AECOM2/744000155565444?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Affinius Capital** | [Data Scientist Intern](https://careers-affiniuscapital.icims.com/jobs/2284/summer-2027-data-scientist-intern/job) | US |  | unknown | unknown |
| **Agoda** | [Associate Data Analyst \(New Graduate, Thai Speaking\) \(Marketing Analytics, Bangkok Based\)](https://job-boards.greenhouse.io/agoda/jobs/8194692) | Unknown |  | unknown | unknown |
| **Airbus** | [Operational Excellence Analyst Intern - Data Analytics - Operational Excellence](https://ag.wd3.myworkdayjobs.com/Airbus/job/Mobile-Area-AL/Summer-Internship-2027---Data-Analytics---Operational-Excellence_JR10442492?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Airgarage** | [Research Associate](https://jobs.ashbyhq.com/airgarage/279174e8-a271-4c07-b904-3d026dae76a8) | US | controls,research | unknown | unknown |
| **Allstate** | [Data Analytics Engineer Intern](https://allstate.wd5.myworkdayjobs.com/sourcing_event/job/USA---IL-Remote/Arity---Data-Analytics-Engineer-Intern_R36286?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Altar'd State** | [IT Analytics Intern](https://standoutforgood.wd12.myworkdayjobs.com/StandOutForGood/job/Knoxville-TN/Spring-2027-IT-Analytics-Intern_SOSJ12499?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **America's Tire** | [Data Engineer 1](https://discounttire.jibeapply.com/jobs/19242?icims=1&utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **American Electric Power** | [Data Scientist Intern](https://aep.wd1.myworkdayjobs.com/AEPCareerSite/job/Columbus-OH/Data-Scientist-Intern---Columbus--OH_R20499?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012784?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - US Consumer Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26011607?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Engineer 1 - Enterprise Technology Services](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26013286?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **American Express** | [Data Engineer Intern - Enterprise Technology Services](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26011831?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **American Family Insurance Group** | [Business Intelligence Enablement Intern](https://amfam.wd1.myworkdayjobs.com/AmFamGroupInternCareers/job/WI-Madison/Summer-2027-Intern---Business-Intelligence-Enablement_R39531?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Family Insurance Group** | [Data Engineer Intern](https://amfam.wd1.myworkdayjobs.com/en-US/Careers/job/WI-Madison/Summer-2027-Intern---Data-Engineer_R39675?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **Amgen** | [Data Scientist Intern](https://amgen.wd1.myworkdayjobs.com/careers/job/United-States---Remote/Undergrad-Intern---Data-Scientist---Amgen-s-Technology---Medical-Organizations--Summer-2027-_R-255704?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Amgen** | [Data Scientist Intern - Amgen’s Technology &amp; Medical Organizations](https://amgen.wd1.myworkdayjobs.com/careers/job/United-States---Remote/Grad-Intern---Data-Scientist---Amgen-s-Technology---Medical-Organizations--Summer-2027-_R-255722?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Amplify** | [Summer 2027: Data Analytics Intern](https://jobs.ashbyhq.com/amplify/7b859cc1-1354-43c5-bbd4-0571e85f7c51/application?embed=true&utm_source=Simplify&ref=Simplify) | US | data-eng,infra,research | unknown | unknown |
| **Ardian** | [Data Scientist Intern](https://ardian.wd103.myworkdayjobs.com/en-US/ArdianCareers/job/New-York/Data-Scientist-Intern---February-2027---NYC_JR1002271?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Artefact** | [Data Scientist Intern \(2024\)](https://job-boards.greenhouse.io/artefact/jobs/8564128002) | Unknown |  | unknown | unknown |

_229 more are in [tracker.csv](tracker.csv)._

### AI / ML (246 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Apple** | [SoC Machine Learning Software Engineer Intern](https://jobs.apple.com/en-us/details/200689488?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **G-Research** | [Machine Learning Engineer Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Machine-Learning-Engineer-Intern_R3773?utm_source=Simplify&ref=Simplify) | UK | research | unknown | unknown |
| **Jane Street** | [Machine Learning Engineer Intern](https://www.janestreet.com/join-jane-street/position/8611307002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Machine Learning Researcher Intern](https://www.janestreet.com/join-jane-street/position/8384490002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, AI/ML &amp; LLM](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922929&utm_source=github-vansh-ouckah) | US | llm | unknown | unknown |
| **Mistral AI** | [Applied AI, Forward Deployed Machine Learning Engineer - \(Internship\)](https://jobs.ashbyhq.com/mistral.ai/fcdb8407-20b9-4179-81b6-f2ca2c79a39b) | France | controls,nlp | unknown | unknown |
| **Point72** | [Machine Learning Researcher - Intern](https://boards.greenhouse.io/point72/jobs/7302611002?gh_jid=7302611002) | US |  | unknown | unknown |
| **Tower Research Capital** | [Machine Learning Intern](https://www.tower-research.com/open-positions/?gh_jid=7077280&utm_source=github-vansh-ouckah) | Canada | research | unknown | unknown |
| **Two Sigma** | [AI Research Scientist Intern \(MS / PhD\)](https://careers.twosigma.com/careers/JobDetail/New-York-New-York-United-States-AI-Research-Scientist-Internship-2027-Summer/14022) | US | research,phd-position | unknown | unknown |
| **🔥 Amazon** | [Applied Science Intern - Gen AI &amp; Large Language Models 🎓](https://amazon.jobs/en/jobs/10564589/2027-applied-science-internship-gen-ai-large-language-models-united-states-phd-student-science-recruiting?utm_source=Simplify&ref=Simplify) | US | llm | unknown | unknown |
| **🔥 Amazon** | [Applied Science Intern - Natural Language Processing and Speech Technologies 🎓](https://amazon.jobs/en/jobs/10564593/2027-applied-science-internship-natural-language-processing-and-speech-technologies-united-states-phd-student-science-recruiting?utm_source=Simplify&ref=Simplify) | US | nlp | unknown | unknown |
| **🔥 Amazon** | [Applied Scientist Intern - Reinforcement Learning &amp; Optimization - Machine Learning 🎓](https://amazon.jobs/en/jobs/10564597/2027-applied-science-internship-reinforcement-learning-optimization-machine-learning-united-states-phd-student-science-recruiting?utm_source=Simplify&ref=Simplify) | US | rl | unknown | unknown |
| **🔥 Amazon** | [Machine Learning Systems Software Development Engineer Intern - Annapurna Labs](https://amazon.jobs/en/jobs/10538066/ml-systems-software-development-engineer-intern-annapurna-labs-2027?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **🔥 NVIDIA** | [PhD Research Intern - Generative AI for Physical AI 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/PhD-Research-Intern--Generative-AI-for-Physical-AI---2027_JR2025025?utm_source=Simplify&ref=Simplify) | US | research,phd-position | unknown | unknown |
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
| **Perplexity** | [Internship - Machine Learning Research Engineer](https://jobs.ashbyhq.com/perplexity/b9e1ff15-d52a-46d5-abf0-26460f2a116c) | Germany | multimodal,research | unknown | unknown |
| **Perplexity** | [Internship - Search Machine Learning Engineer](https://jobs.ashbyhq.com/perplexity/9246cf02-26fd-4ae8-90c5-639c6e85e9e2) | Serbia | llm,nlp,infra,research,phd-position | unknown | unknown |
| **Perplexity** | [Internship - Search Machine Learning Engineer](https://jobs.ashbyhq.com/perplexity/71168628-1998-47d3-87a9-be7bc56a430d) | UK | llm,nlp,infra,research | unknown | unknown |
| **Qualcomm** | [Machine Learning AISW Intern](https://qualcomm.eightfold.ai/careers/job/446721636765?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Qualcomm** | [Machine Learning Compiler &amp; Performance Engineering Intern - Systems](https://qualcomm.eightfold.ai/careers/job/446721064018?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Scale AI** | [Machine Learning Research Intern](https://job-boards.greenhouse.io/scaleai/jobs/4735665005?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Sierra** | [Software Engineer Intern, Agent \(Summer 2027\)](https://jobs.ashbyhq.com/Sierra/34b31b67-268c-4270-b48f-72e59064c96e/application?embed=true&utm_source=Simplify&ref=Simplify) | US | llm,funded | unknown | posting mentions equity |
| **Sierra** | [Software Engineer, Agent \(New Grad 2027\)](https://jobs.ashbyhq.com/Sierra/149f368c-52d5-408f-ba26-ad888f318a00/application?embed=true&utm_source=Simplify&ref=Simplify) | US | autonomy,llm,research,funded | unknown | posting mentions equity |
| **Sierra** | [Software Engineer, Agent \(New Grad 2027\)](https://jobs.ashbyhq.com/sierra/79953d72-60d4-43e0-8c8c-6eccda422dce) | Singapore | autonomy,llm,research,funded | unknown | posting mentions equity |
| **Sierra** | [Software Engineer, Agent \(New Grad\)](https://jobs.ashbyhq.com/sierra/0ff928f7-cca0-4d2b-ae64-c07277ff5252/application?embed=true&utm_source=Simplify&ref=Simplify) | UK | autonomy,llm,research,funded | unknown | posting mentions equity |
| **Snowflake** | [AI Research Scientist, New Grad – Agents &amp; Reinforcement Learning](https://jobs.ashbyhq.com/snowflake/1bad12df-f443-426f-9d09-e96fc780d698/application?utm_source=Simplify&ref=Simplify) | US | autonomy,llm,rl,data-eng,infra,research,phd-position | unknown | unknown |
| **🔥 AMD** | [AI Research Infrastructure – Reinforcement Learning Post-Training Intern 🎓](https://careers.amd.com/jobs/90950?icims=1&utm_source=Simplify&ref=Simplify) | US | rl,infra,research | unknown | unknown |
| **🔥 AMD** | [AI Research Intern - Reinforcement Learning and LLM Post-Training 🎓](https://careers.amd.com/jobs/91013?icims=1&utm_source=Simplify&ref=Simplify) | US | llm,rl,research | unknown | unknown |
| **🔥 AMD** | [Generative AI and Reinforcement Learning Research Intern 🎓](https://careers.amd.com/jobs/90910?icims=1&utm_source=Simplify&ref=Simplify) | US | rl,research | unknown | unknown |

_206 more are in [tracker.csv](tracker.csv)._

### Security (223 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Jane Street** | [Cybersecurity Analyst Intern](https://www.janestreet.com/join-jane-street/position/8632723002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Microsoft** | [Security Research Intern](https://apply.careers.microsoft.com/careers/job/1970393557044769?utm_source=github-vansh-ouckah) | US | security,research | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Security &amp; Identity](https://apply.careers.microsoft.com/careers/job/1970393557044771?utm_source=github-vansh-ouckah) | US | security | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Security &amp; Identity](https://apply.careers.microsoft.com/careers/job/1970393557044765?utm_source=github-vansh-ouckah) | US | security | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Security &amp; Identity](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922930&utm_source=github-vansh-ouckah) | US | security | unknown | unknown |
| **Mistral AI** | [Applied Scientist  \(Internship\)](https://jobs.ashbyhq.com/mistral.ai/de46ba8b-00cb-4618-83df-66e15a78434e) | France | multimodal,research,phd-position | unknown | unknown |
| **Cohere** | [Machine Learning Intern/Co-op  \(Winter 2027\)](https://jobs.ashbyhq.com/cohere/36d1f52f-8270-4652-adf5-5303a0ff341b) | Canada | computer-vision,nlp,security,research,funded | unknown | unknown |
| **Cohere** | [Software Engineer Intern \(Winter 2027\)](https://jobs.ashbyhq.com/cohere/8c035d3d-081d-4c8a-914a-72f4efaad254) | Canada | autonomy,computer-vision,nlp,data-eng,infra,security,research,funded | unknown | unknown |
| **Harvey** | [Software Engineer, New Grad \(2027\)](https://jobs.ashbyhq.com/harvey/b0996df6-6b6e-42be-a4f9-0084536068f5/application?embed=true&utm_source=Simplify&ref=Simplify) | US | infra,security,research | unknown | unknown |
| **Palantir** | [Forward Deployed Infrastructure Engineer, Internship - US Government](https://jobs.lever.co/palantir/3db7e40a-28e0-4ad1-96c5-93de5bc96aa9) | US | computer-vision,infra,distributed,security | unknown | unknown |
| **Palantir** | [Forward Deployed Infrastructure Engineer, Internship - US Government](https://jobs.lever.co/palantir/8f362a1f-1eff-4327-94c1-ff46e2101c69) | US | computer-vision,infra,distributed,security | unknown | unknown |
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
| **Palantir** | [Software Engineer, New Grad](https://jobs.lever.co/palantir/94984771-0704-446c-88c6-91ce748f6d92/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,data-eng,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad](https://jobs.lever.co/palantir/c34b424e-caf2-455a-b104-ae1096ccca29/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,data-eng,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Defense](https://jobs.lever.co/palantir/18d901fc-93bb-4d18-9f04-c72031e20d79/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,data-eng,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Defense](https://jobs.lever.co/palantir/0a838e66-1ab0-4fc4-b4d3-4671c0352278/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,data-eng,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Defense](https://jobs.lever.co/palantir/f362d7aa-360d-4059-ab38-f482742693b3/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,data-eng,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Infrastructure](https://jobs.lever.co/palantir/4abf26b4-795c-420a-bf22-1ab98db268b4) | US | computer-vision,data-eng,infra,security,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Infrastructure](https://jobs.lever.co/palantir/7d75bed5-45d8-4876-840a-2d92ea79c98d) | US | computer-vision,data-eng,infra,security,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Production Infrastructure](https://jobs.lever.co/palantir/15844944-fb69-4b57-9531-e988650b20c6) | US | computer-vision,infra,security,research,funded | unknown | unknown |

_183 more are in [tracker.csv](tracker.csv)._

### Hardware / EE (197 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Hardware Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018880/?gh_jid=8018880&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Amazon** | [ASIC Engineer Intern](https://amazon.jobs/en/jobs/10517535/asic-engineer-intern-annapurna-labs-2027?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Amazon** | [Software Development Engineer Intern, Amazon Leo, Embedded Systems 🇺🇸](https://www.amazon.jobs/en/jobs/10571374/software-development-engineer-embedded-systems-intern-amazon-leo-summer-2027-usa?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **Amazon** | [Software Development Engineer Intern, Embedded Systems](https://www.amazon.jobs/en/jobs/10567914/software-development-engineer-intern-embedded-systems-summer-2027-usa?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **DRW** | [FPGA Intern](https://www.drw.com/work-at-drw/listings/fpga-intern-3484423?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **DRW** | [FPGA Intern](https://job-boards.greenhouse.io/drweng/jobs/8070392) | UK | hardware | unknown | unknown |
| **IMC** | [Hardware Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823945101) | US |  | unknown | unknown |
| **Jane Street** | [Hardware Engineer \(FPGA/ASIC\) Intern](https://www.janestreet.com/join-jane-street/position/8624440002/?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **Virtu Financial** | [2027 Internship - FPGA Engineer](https://job-boards.greenhouse.io/virtu/jobs/8638124002) | Ireland | hardware | unknown | unknown |
| **Virtu Financial** | [2027 Internship- Hardware Engineer \(FPGA\)](https://job-boards.greenhouse.io/virtu/jobs/8657286002) | US | hardware | unknown | unknown |
| **🔥 Amazon** | [ASIC Engineer Early Career](https://amazon.jobs/en/jobs/10576621/asic-engineer-early-career-2027-project-leo?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Amazon** | [ASIC Engineer Intern](https://amazon.jobs/en/jobs/10576619/asic-engineer-intern-summer-2027?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Amazon** | [ASIC Formal Verification Engineer 1](https://amazon.jobs/en/jobs/10586351/asic-formal-verification-engineer-i-annapurna-labs?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Amazon** | [Software Engineer Intern - Embedded Systems](https://amazon.jobs/en/jobs/10567914/software-development-engineer-intern-embedded-systems-summer-2027-usa?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 Amazon** | [Software Engineer Intern - Embedded Systems](https://amazon.jobs/en/jobs/10571374/software-development-engineer-embedded-systems-intern-amazon-leo-summer-2027-usa?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 Google** | [Hardware Engineer Intern - PhD 🎓](https://www.google.com/about/careers/applications/jobs/results/97352132356645574?utm_source=Simplify&ref=Simplify) | US | phd-position | unknown | unknown |
| **🔥 Meta** | [ASIC Engineer New Grad - Performance Architecture and Modeling](https://www.metacareers.com/jobs/4596319193960098?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Clocks Verification Engineer New Grad 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Clocks-Verification-Engineer---New-College-Grad-2026_JR2027579?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Physical Design Engineer New Grad - Netlisting 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Physical-Design-Engineer--Netlisting---New-College-Grad-2026_JR2017681?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Physical Design and Timing Engineer – New College Grad 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Timing-Engineer---New-College-Grad-2026_JR2013177?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Verification Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Verification-Engineer---New-College-Grad-2027_JR2027719?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Verification Engineer – New College Grad 2026](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-TX-Austin/ASIC-Verification-Engineer---New-College-Grad-2026_JR2012573?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Verification Intern](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/Canada-Toronto/ASIC-Verification-Intern---Summer-2027_JR2027982?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **🔥 NVIDIA** | [Low Power ASIC Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Low-Power-ASIC-Engineer---New-College-Grad-2027_JR2027850?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Graphcore** | [Firmware Intern](https://job-boards.greenhouse.io/graphcore/jobs/8894770002?utm_source=Simplify&ref=Simplify) | UK | hardware | unknown | unknown |
| **Qualcomm** | [AI and DSP Applications Engineer Intern](https://qualcomm.eightfold.ai/careers/job/446721686396?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Qualcomm** | [Firmware Development Intern - PAL](https://qualcomm.eightfold.ai/careers/job/446721229661?utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **Qualcomm** | [Firmware Engineer Intern - Embedded Software Engineering - Embedded Firmware and SDK Development](https://qualcomm.eightfold.ai/careers/job/446721141411?utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **Qualcomm** | [Soft IP ASIC Engineer Intern](https://qualcomm.eightfold.ai/careers/job/446721302471?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Verkada** | [Embedded Software Engineer Intern](https://job-boards.greenhouse.io/verkada/jobs/5211595007?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Verkada** | [Hardware Engineer \(Winter Co-op\)](https://job-boards.greenhouse.io/verkada/jobs/4321158007) | US |  | unknown | unknown |
| **🔥 AMD** | [ASIC Verification Engineer Intern/Co-op](https://careers.amd.com/jobs/91207?icims=1&utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op](https://careers.amd.com/jobs/91320?icims=1&utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op](https://careers.amd.com/jobs/91313?icims=1&utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op - Long Term](https://careers.amd.com/jobs/90297?icims=1&utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **🔥 Tesla** | [Embedded Software Engineer Intern - Optimus](https://www.tesla.com/careers/search/job/282340?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **AGCO** | [Embedded Software Engineer Intern](https://careers.agcocorp.com/job/Hesston-Embedded-Software-Engineering-Intern-Summer-2027-KS-67062/1440993300/?ats=successfactors&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Acron Aviation** | [Electrical Engineer Intern \(EE, RF, FPGA disciplines\) - Phoenix Site](https://jobs.lever.co/acronaviation/69dcdf12-38f2-41ab-81fb-9af7903e7329) | US | controls,hardware | unknown | unknown |
| **Acron Aviation** | [Electrical Engineer Intern - St. Pete Site](https://jobs.lever.co/acronaviation/0cd327f1-0f91-41d0-8b88-093a084fb082) | US | controls,hardware,research | unknown | unknown |
| **Acron Aviation** | [Software Engineer Intern - St. Pete Site](https://jobs.lever.co/acronaviation/19dbac7d-b4fb-4d21-9247-dc610bf55fed) | US | controls,hardware,research | unknown | unknown |

_157 more are in [tracker.csv](tracker.csv)._

### Systems & Infra (183 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Platform Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018856/?gh_jid=8018856&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **DRW** | [Platform Engineer Intern](https://www.drw.com/work-at-drw/listings/platform-engineer-intern-3468737?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **🔥 Amazon** | [Software Development Engineer 1 - AI/ML Network Infrastructure](https://amazon.jobs/en/jobs/10490741/software-development-engineer-i-ai-ml-network-infrastructure-annapurna-labs?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 NVIDIA** | [Networking Research Intern - Networking 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/PhD-Research-Intern--Networking---2027_JR2025098?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Cerebras Systems** | [DevOps Engineer - New Grad 2026](https://jobs.ashbyhq.com/cerebras/40e0d3ee-8f0a-4b19-9bf9-79410b1c7735) | Remote | infra,distributed,research | unknown | unknown |
| **Cerebras Systems** | [Software Engineer - New Grad 2026](https://jobs.ashbyhq.com/cerebras/99c289fa-8fc6-49f7-b7e8-78ac4e9d99ac/application?utm_source=Simplify&ref=Simplify) | US / Canada | hardware,infra,distributed,research | unknown | unknown |
| **Harvey** | [Software Engineering Intern \(Summer 2027\)](https://jobs.ashbyhq.com/harvey/06d64648-b84b-48ae-94a2-d9c06dfdcb5d/application?embed=true&utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **Harvey** | [Software Engineering Intern \(Summer 2027\)](https://jobs.ashbyhq.com/harvey/3a34578d-d42e-45bb-ac5c-0c3357e8cbb7/application?embed=true&utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **Intel** | [Compiler Engineering Intern](https://intel.wd1.myworkdayjobs.com/en-US/External/job/Canada-Toronto/Compiler-Engineering-Intern_JR0287934?utm_source=github-vansh-ouckah) | Canada |  | unknown | unknown |
| **Notion** | [Software Engineer, Early Career](https://jobs.ashbyhq.com/notion/297b4ece-765f-4eea-b1b8-46057cb6501f) | US | autonomy,infra,distributed,research | unknown | posting mentions equity |
| **Notion** | [Software Engineer, Early Career \(AI\)](https://jobs.ashbyhq.com/notion/85947779-6b87-466a-98bc-30a640448c28/application?utm_source=Simplify&ref=Simplify) | US | autonomy,infra,distributed | unknown | posting mentions equity |
| **Perplexity** | [Internship - Search Backend Infra Engineer](https://jobs.ashbyhq.com/perplexity/be94e89b-89d5-4f2a-a58b-7929c8d97f92) | Serbia | infra,distributed,phd-position | unknown | unknown |
| **Qualcomm** | [Display Systems Engineer Intern](https://qualcomm.eightfold.ai/careers/job/446721661677?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Ramp** | [Software Engineering Intern, Android](https://jobs.ashbyhq.com/ramp/fcf118cc-521a-4a62-9d13-945e5b6e3cb8) | US | hardware,infra,funded | unknown | unknown |
| **Ramp** | [Software Engineering Intern, Backend](https://jobs.ashbyhq.com/ramp/acf6b28d-767f-483f-8ff2-114620cd7e04) | US | hardware,infra,funded | unknown | unknown |
| **Ramp** | [Software Engineering Intern, Frontend](https://jobs.ashbyhq.com/ramp/a13ae586-f4cb-4385-8822-c42b9b54ed74) | US | hardware,infra,funded | unknown | unknown |
| **Ramp** | [Software Engineering Intern, iOS](https://jobs.ashbyhq.com/ramp/b66be397-240b-41a6-9b05-493299b270a9) | US | hardware,infra,funded | unknown | unknown |
| **Sierra Space** | [Software Engineer 1 - DevOps / DevSecOps](https://sierraspace.wd1.myworkdayjobs.com/en-US/Sierra_Space_External_Career_Site/job/Louisville-CO/Software-Engineer-I---DevOps---DevSecOps_R26394-1?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **Snowflake** | [Product Marketing, AI-Powered Data Engineering Intern \(Spring 2027\)](https://jobs.ashbyhq.com/snowflake/45f2aa43-731d-4bab-a02b-9ef979f2c86e) | US | data-eng,infra | unknown | unknown |
| **SpaceX** | [New Graduate Engineer, Infrastructure](https://boards.greenhouse.io/spacex/jobs/8893406002?gh_jid=8893406002) | US | infra | unknown | unknown |
| **🔥 AMD** | [Compiler Engineer Intern/Co-op](https://careers.amd.com/jobs/91865?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Compiler Engineer Intern/Co-op](https://careers.amd.com/jobs/91864?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Compiler Engineer Intern/Co-op - Masters 🎓](https://careers.amd.com/jobs/91867?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Acron Aviation** | [Systems Engineer Intern - St. Pete Site](https://jobs.lever.co/acronaviation/eaebe6c7-a38f-404f-ba93-210861faf184) | US | controls,hardware | unknown | unknown |
| **Aerospace Corporation** | [Cloud Solutions Engineer Intern, Site Reliability 🇺🇸](https://aero.wd5.myworkdayjobs.com/external/job/El-Segundo-CA/XMLNAME-2027-Cloud-Solutions-Engineer---Site-Reliability-Undergrad-Intern_R016936?utm_source=github-vansh-ouckah) | US | infra | unknown | unknown |
| **Agentis Capital Advisors** | [Investment Banking Summer Analyst - Infrastructure M&amp;A Advisory - Summer 2027](https://jobs.ashbyhq.com/agentis-capital-advisors/af7e9253-cea8-4287-baf9-838a900546b3) | Canada | infra,research | unknown | posting mentions equity |
| **Alan** | [Software Engineer Internship \(6 months from feb/march 2027\)](https://jobs.ashbyhq.com/alan/de4c30ae-698f-43e9-84d1-f458955fd671) | France | infra,research | unknown | posting mentions equity |
| **Amplify** | [Summer 2027: Software Engineering Intern](https://jobs.ashbyhq.com/amplify/855d22a3-f15e-49f6-854c-29e505653efa/application?embed=true&utm_source=Simplify&ref=Simplify) | US | controls,infra,distributed,research | unknown | unknown |
| **Apera AI** | [Software Developer \(Cloud Infrastructure\) – Co-Op](https://job-boards.greenhouse.io/aperaaiinc/jobs/5240274007) | Unknown | infra | unknown | unknown |
| **Arcesium** | [Infrastructure Engineer Intern](https://job-boards.greenhouse.io/arcesiumllc/jobs/5257199007?utm_source=github-vansh-ouckah) | US | infra | unknown | unknown |
| **Astreya** | [AI Infrastructure DC Design Intern](https://astreya.wd5.myworkdayjobs.com/en-US/life-at-astreya-opportunities/job/Remote-CA/AI-Infrastructure-DC-Design-Intern_R0017931?utm_source=github-vansh-ouckah) | US | infra | unknown | unknown |
| **Atlys** | [Launchpad Fellowship](https://jobs.ashbyhq.com/atlys/53dcce66-f865-4d1e-a6b0-31433d844723) | Unknown | infra,research,funded | unknown | posting mentions equity |
| **BMO Financial Group** | [Junior Cloud Engineer Co-op](https://bmo.wd3.myworkdayjobs.com/en-US/External/job/Toronto-ON-CAN/Junior-Cloud-Engineer--Summer-2027--Co-op-Internship----16-months_R260029417-1?utm_source=github-vansh-ouckah) | Canada |  | unknown | unknown |
| **Base Power** | [Supply Chain Tooling Engineer Intern](https://jobs.ashbyhq.com/base-power/7fce3b16-c132-453b-a836-a3bcbd21abd2) | US | data-eng,research | unknown | unknown |
| **Blissway** | [Embedded Systems Engineer New Grad](https://jobs.ashbyhq.com/blissway/51d6d839-9801-4436-bfc2-918bae428ed8/application?embed=true&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/San-Diego-CA/University---2027-Summer-Games-Systems-Engineer-Intern---San-Diego--CA_R0248365?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/McLean-VA/University---2027-Summer-Games-Systems-Engineer-Intern---McLean--VA_R0248361?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Huntsville-AL/University---2027-Summer-Games-Systems-Engineer-Intern---Huntsville--AL_R0249188?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Fort-Walton-Beach-FL/University---2027-Summer-Games-Systems-Engineer-Intern---Ft-Walton-Beach--FL_R0248388?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Honolulu-HI/University---2027-Summer-Games-Systems-Engineer-Intern---Honolulu--HI_R0248370?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |

_143 more are in [tracker.csv](tracker.csv)._

### Computational Science (85 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **🔥 NVIDIA** | [PhD Research Intern - AI for Climate and Weather Simulation 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/PhD-Research-Intern--AI-for-Climate-and-Weather-Simulation---2027_JR2026949?utm_source=Simplify&ref=Simplify) | US / Canada | research,climate,phd-position | unknown | unknown |
| **🔥 NVIDIA** | [Quantum and Chemistry Research Intern - Quantum and AI for Chemistry 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/Canada-Toronto/PhD-Research-Intern--Quantum-and-AI-for-Chemistry---2027_JR2024997?utm_source=Simplify&ref=Simplify) | Canada | research | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship](https://jobs.lever.co/palantir/1b6f1d82-d459-4dea-8bc2-8d2ffe6f881a) | France | autonomy,computer-vision,infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - France](https://jobs.lever.co/palantir/ac0dc094-2480-43c2-8495-26ade227ff4f) | US | infra,funded | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - US Government](https://jobs.lever.co/palantir/315f695d-04d1-4a9a-848e-cb2bec7a997e) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - US Government](https://jobs.lever.co/palantir/e0010393-c300-446f-bf67-fa2ef067f16f) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - US Government](https://jobs.lever.co/palantir/e6ff8bf2-135e-474d-ad37-24f490ae1dd2) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - Warp Speed](https://jobs.lever.co/palantir/b3d81928-6c26-432f-8a0a-36602c2eefcb/apply?utm_source=github-vansh-ouckah) | US | autonomy,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - Warp Speed](https://jobs.lever.co/palantir/66b495eb-aaf9-4bf9-a759-41854534add7/apply?utm_source=Simplify&ref=Simplify) | US | autonomy,infra,funded | unknown | unknown |
| **Palantir** | [Software Engineer, Internship](https://jobs.lever.co/palantir/3531977a-9b2f-40a0-a486-4eeb38e75fc1) | Singapore | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship](https://jobs.lever.co/palantir/76a60923-bb49-40f5-b061-7c7eb1299602) | UK | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Infrastructure](https://jobs.lever.co/palantir/fd3603a9-7016-45c6-9c8d-04c9279ab85e) | UK | computer-vision,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Query Engines](https://jobs.lever.co/palantir/da774f81-c98c-4dcf-9b9c-949fd7d90a13?utm_source=github-vansh-ouckah) | US | data-eng,infra,distributed,phd-position | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Query Engines](https://jobs.lever.co/palantir/3e59369e-1392-42f2-8d03-86648e87e963) | UK | data-eng,infra,distributed,phd-position | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad](https://jobs.lever.co/palantir/d372c805-d0cd-4a10-9522-fbecc78d6f3e/apply?utm_source=Simplify&ref=Simplify) | UK | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad](https://jobs.lever.co/palantir/2458ba08-de79-4e8f-b553-060f9568727e) | Singapore | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Infrastructure](https://jobs.lever.co/palantir/9265acce-12cd-4179-8c50-55d15963532b) | UK | computer-vision,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Query Engines](https://jobs.lever.co/palantir/0f7d1e01-1f74-4786-944d-910208d390fa/apply?utm_source=Simplify&ref=Simplify) | UK | data-eng,infra,distributed,phd-position | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Query Engines](https://jobs.lever.co/palantir/90329118-d9b7-4b96-acdf-13377e3196ac/apply?utm_source=Simplify&ref=Simplify) | US | data-eng,infra,distributed,phd-position,funded | unknown | unknown |
| **Snowflake** | [Software Engineer Intern - Berlin \(2026\)](https://jobs.ashbyhq.com/snowflake/41e65c6c-a01e-4f40-af14-ae75d3b95e27) | Germany | hardware,data-eng,infra,distributed,research,phd-position | unknown | unknown |
| **Snowflake** | [Software Engineer Intern - Zurich \(2026\)](https://jobs.ashbyhq.com/snowflake/26a0ae52-97a6-4a46-9216-3c382570d89b) | Switzerland | controls,hardware,data-eng,infra,distributed,research,phd-position | unknown | unknown |
| **🔥 Tesla** | [Physics Engine Development Engineer Intern - Optimus](https://www.tesla.com/careers/search/job/282147?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Ambrook** | [Software Engineering Intern](https://jobs.ashbyhq.com/ambrook/e458b046-aa7f-4022-bca5-63cdfd495456) | US | computer-vision,infra,climate | unknown | unknown |
| **Americanpublichealthassociation** | [Climate, Health and Equity Internship: 2027 spring term](https://job-boards.greenhouse.io/americanpublichealthassociation/jobs/4434254009) | US | climate | unknown | unknown |
| **Antares Nuclear** | [Mechanical Engineering Design Intern - Summer 2027](https://jobs.ashbyhq.com/antares/9accca59-103b-4f54-978a-d5bb46bd9c62) | US | hardware,research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Multiphysics Software Intern - Summer 2027](https://jobs.ashbyhq.com/antares/922a527d-9826-446d-9aba-ffc611995830) | US | infra,research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Nuclear Engineering Intern - Summer 2027](https://jobs.ashbyhq.com/antares/e92ae489-1b1a-4616-a9c8-7c2390698af8) | US | research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Nuclear Operations &amp; Licensing Engineering Intern - Summer 2027](https://jobs.ashbyhq.com/antares/ec96a761-509f-44e9-90aa-e1fee5388aa1) | Unknown | research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Quality Engineering Intern - Summer 2027](https://jobs.ashbyhq.com/antares/9335fe9a-a994-4209-bd97-9a6070f4e94f) | US | hardware,research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Reactor Software Engineering Intern - Summer 2027](https://jobs.ashbyhq.com/Antares/419ef2df-f0aa-4b68-994a-077e08a959e3/application?embed=true&utm_source=Simplify&ref=Simplify) | US | controls,hardware,research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Space Mechanical Design Engineering Intern - Summer 2027](https://jobs.ashbyhq.com/antares/7feb2782-3bdc-4efe-b459-9751db944f81) | US | hardware,research,climate,funded | unknown | unknown |
| **Base Power** | [Electrical Engineering Intern](https://jobs.ashbyhq.com/base-power/7284737d-7e04-43e0-af1f-858103f64e97) | US | hardware | unknown | unknown |
| **Base Power** | [Hardware Engineering Intern](https://jobs.ashbyhq.com/base-power/f22cee0e-55d9-42cd-806e-1c1fc7217770) | US | hardware | unknown | unknown |
| **Base Power** | [Mechanical Engineering Intern](https://jobs.ashbyhq.com/base-power/717274d7-09dc-4176-b307-07301074b87f) | US | hardware | unknown | unknown |
| **Blue Cross Blue Shield of Michigan** | [Epidemiology / Biostatistics Intern](https://ejko.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_3/job/14949?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Exa** | [Software Engineer, Intern](https://jobs.ashbyhq.com/exa/a9e01521-66f1-481b-89da-ec01d4620f16?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Fab2** | [Embedded Software Engineering Intern - Summer](https://jobs.ashbyhq.com/fab2/15020e6e-be1c-4455-95a3-aa798474cec4) | US | controls,hardware,funded | unknown | unknown |
| **Fab2** | [Embedded Software Engineering Intern - Winter](https://jobs.ashbyhq.com/fab2/3c7fd0f1-b25f-413c-8e62-6ef00a9d47da) | US | controls,hardware,funded | unknown | unknown |
| **Fab2** | [Fab Software Engineering Intern - Summer](https://jobs.ashbyhq.com/fab2/36ab33ab-82e7-4cc4-8137-f451fd6036a0) | US | controls,infra,distributed,funded | unknown | unknown |
| **Fab2** | [Fab Software Engineering Intern - Winter](https://jobs.ashbyhq.com/fab2/0c4dc4f4-01c9-4138-a666-e7234cda7e95) | US | controls,infra,distributed,funded | unknown | unknown |

_45 more are in [tracker.csv](tracker.csv)._

### HCI / XR (2 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **OpenArt AI** | [Early Adopter &amp; Product Builder Intern, Creative AI](https://jobs.ashbyhq.com/openart/8dd52ba6-a5b6-40b1-95fe-50de352fa254/application?embed=true&utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **Simular** | [Design Engineer Intern](https://jobs.ashbyhq.com/simular/3c53a046-4fc0-4b67-9295-1912abf16262) | Singapore | autonomy,controls | unknown | unknown |

### Early-company / equity reality check

The company signal is a discovery aid, not a prediction. Private-company options can become valuable, but can also expire, dilute, remain illiquid, or end up worth zero. `private company; verify offer` means the posting does not prove that equity is included. Ask for the option count **and fully diluted percentage**, strike price, vesting/cliff, exercise window, latest common valuation, and liquidation preferences.

## Closing within 10 days

| Days | Deadline | Company | Role | Region |
|--:|--|--|--|--|
| 6 | 2026-10-30 | **Man Group** | 2027 Summer Technology Internship Programme | UK |
| 6 | 2026-10-30 | **Blackstone** | 2027 Software Engineer Summer Analyst | UK |
| 6 | 2026-10-30 | **London Stock Exchange Group** | Engineering Summer Internship Programme | UK |
| 8 | 2026-11-01 | **J.P. Morgan** | 2027 Summer Internship | UK |
| 10 | 2026-11-03 | **Baillie Gifford** | Summer Internship 2027 | UK |

## Elite and high-tier live postings (655)

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
| **Akuna Capital University** | [Junior Quantitative Developer &amp; Strategist](https://www.akunacapital.com/careers/job/8016687/?gh_jid=8016687&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Akuna Capital University** | [Junior Quantitative Researcher](https://www.akunacapital.com/careers/job/8036541/?gh_jid=8036541&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Amazon** | [ASIC Engineer Intern](https://amazon.jobs/en/jobs/10517535/asic-engineer-intern-annapurna-labs-2027?utm_source=github-vansh-ouckah) | Hardware / EE | US | 2027 | review required |
| **Amazon** | [Frontier AI &amp; Robotics Intern](https://www.amazon.jobs/en/jobs/10564599/2027-frontier-ai-robotics-internship-undergraduate-united-states-frontier-ai-robotics-frontier-ai-robotics?utm_source=github-vansh-ouckah) | Robotics &amp; Embodied AI | US | 2027 | review required |
| **Amazon** | [Robotics - Software Development Engineer Intern/Co-op](https://www.amazon.jobs/en/jobs/3136266/robotics-software-development-engineer-intern-co-op-2026?no_int_redir=1&utm_source=github-vansh-ouckah) | Robotics &amp; Embodied AI | US | 2026 | review required |
| **Amazon** | [Software Development Engineer Intern, Amazon Leo 🇺🇸](https://www.amazon.jobs/en/jobs/10587999/software-development-engineer-intern-amazon-leo-summer-2027-usa?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Amazon** | [Software Development Engineer Intern, Amazon Leo, Embedded Systems 🇺🇸](https://www.amazon.jobs/en/jobs/10571374/software-development-engineer-embedded-systems-intern-amazon-leo-summer-2027-usa?utm_source=github-vansh-ouckah) | Hardware / EE | US | Summer 2027 | review required |
| **Amazon** | [Software Development Engineer Intern, Embedded Systems](https://www.amazon.jobs/en/jobs/10567914/software-development-engineer-intern-embedded-systems-summer-2027-usa?utm_source=github-vansh-ouckah) | Hardware / EE | US | Summer 2027 | review required |
| **Anthropic** | [Research Associate, Biology](https://job-boards.greenhouse.io/anthropic/jobs/5285248008) | Software Engineering | US | Unknown | review required |
| **Apple** | [SoC Machine Learning Software Engineer Intern](https://jobs.apple.com/en-us/details/200689488?utm_source=github-vansh-ouckah) | AI / ML | US | Summer 2027 | review required |
| **Apple** | [Software Engineer Intern, Undergrad](https://jobs.apple.com/en-us/details/200664785/software-undergrad-engineering-internships?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Apple** | [Software Engineering Intern, Masters](https://jobs.apple.com/en-us/details/200664320/software-engineering-masters-internships?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Apple Bank** | [IT Data Intern - Analytics, &amp; Automation](https://applebank.wd5.myworkdayjobs.com/applebankcareers/job/New-York-NY/XMLNAME-2027-Summer-Intern--IT-Data--Analytics----Automation_2026-1414?utm_source=Simplify&ref=Simplify) | Data | US | Summer 2027 | review required |
| **Citadel** | [Quantitative Research Analyst University Graduate](https://www.citadel.com/careers/details/quantitative-research-analyst-university-graduate-us/?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Citadel** | [Quantitative Trader: Equity Quantitative Research – University Graduate](https://www.citadel.com/careers/details/quantitative-trader-equity-quantitative-research-university-graduate-us/?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Citadel** | [Software Engineer Intern](https://www.citadel.com/careers/details/software-engineer-intern-us/?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Citadel** | [Software Engineer – University Graduate](https://www.citadel.com/careers/details/software-engineer-university-graduate-us/?utm_source=Simplify&ref=Simplify) | Software Engineering | US | New Grad 2026 | review required |
| **Citadel Securities** | [Quantitative Research Analyst – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-research-analyst-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | Quant / Finance | UK / Ireland | New Grad 2026 | review required |
| **Citadel Securities** | [Quantitative Trader New Grad](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | Quant / Finance | UK | New Grad 2026 | review required |
| **Citadel Securities** | [Quantitative Trader – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-us-miami/?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Citadel Securities** | [Quantitative Trader – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-us-new-york/?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Citadel Securities** | [Software Engineer – University Graduate](https://www.citadelsecurities.com/careers/details/software-engineer-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | Software Engineering | UK | New Grad 2026 | review required |
| **Cubist Systematic Strategies** | [Quantitative Developer Intern](https://job-boards.greenhouse.io/point72/jobs/7297613002) | Quant / Finance | US | Summer 2027 | review required |
| **DE Shaw** | [Software Developer Intern](https://www.deshaw.com/careers/software-developer-intern-new-york-summer-2027-5894?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **DRW** | [AI/ML Research Intern](https://www.drw.com/work-at-drw/listings/aiml-research-intern-3466679?utm_source=github-vansh-ouckah) | Software Engineering | Unknown | Summer 2027 | review required |
| **DRW** | [AI/ML Research Intern](https://job-boards.greenhouse.io/drweng/jobs/7991171) | Software Engineering | Canada | None | review required |
| **DRW** | [FPGA Intern](https://www.drw.com/work-at-drw/listings/fpga-intern-3484423?utm_source=github-vansh-ouckah) | Hardware / EE | US | Summer 2027 | review required |
| **DRW** | [FPGA Intern](https://job-boards.greenhouse.io/drweng/jobs/8070392) | Hardware / EE | UK | None | review required |
| **DRW** | [Platform Engineer Intern](https://www.drw.com/work-at-drw/listings/platform-engineer-intern-3468737?utm_source=github-vansh-ouckah) | Systems &amp; Infra | US | Summer 2027 | review required |
| **DRW** | [Quantitative Research Intern](https://job-boards.greenhouse.io/drweng/jobs/7818540) | Quant / Finance | US | Ambiguous | review required |
| **DRW** | [Quantitative Research Intern](https://job-boards.greenhouse.io/drweng/jobs/7957756) | Quant / Finance | UK | None | review required |
| **DRW** | [Quantitative Research Intern](https://job-boards.greenhouse.io/drweng/jobs/8014915) | Quant / Finance | Singapore | None | review required |
| **DRW** | [Quantitative Trading Analyst Intern](https://job-boards.greenhouse.io/drweng/jobs/7668776) | Quant / Finance | US | Ambiguous | review required |
| **DRW** | [Quantitative Trading Analyst Intern](https://job-boards.greenhouse.io/drweng/jobs/7957243) | Quant / Finance | UK | None | review required |
| **DRW** | [Quantitative Trading Analyst Intern - IAP Winternship \(MIT Students Only\)](https://job-boards.greenhouse.io/drwuniversityjobs/jobs/8259714) | Quant / Finance | US | None | review required |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/7992936) | Software Engineering | US | Ambiguous | review required |
| **DRW** | [Software Developer Intern](https://www.drw.com/work-at-drw/listings/software-developer-intern-3466687?utm_source=github-vansh-ouckah) | Software Engineering | Unknown | Summer 2027 | review required |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/8020364) | Software Engineering | Netherlands | None | review required |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/7942281) | Software Engineering | UK | None | review required |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/7991196) | Software Engineering | Canada | None | review required |
| **DRW** | [Software Developer Intern - Industrial Placement](https://job-boards.greenhouse.io/drwuniversityjobs/jobs/7364884) | Software Engineering | UK | None | review required |
| **Five Rings** | [Quantitative Trader Intern \(Summer 2027\)](https://job-boards.greenhouse.io/fiveringsllc/jobs/5139668008) | Quant / Finance | US | Summer 2027 | review required |
| **Five Rings** | [Software Developer Intern 🇺🇸](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349707008?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Five Rings Capital** | [Summer Intern 2027 - Quantitative Researcher \(PhD\)](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349219008) | Quant / Finance | US | Summer 2027 | review required |
| **Five Rings Capital** | [Trading Operations Engineer Intern](https://job-boards.greenhouse.io/fiveringsllc/jobs/5420708008?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer 2027 | review required |
| **G-Research** | [Machine Learning Engineer Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Machine-Learning-Engineer-Intern_R3773?utm_source=Simplify&ref=Simplify) | AI / ML | UK | Ambiguous | review required |
| **G-Research** | [Software Engineer Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Software-Engineering-Intern_R3746?utm_source=Simplify&ref=Simplify) | Software Engineering | UK | Ambiguous | review required |
| **Google** | [Software Engineering Intern](https://www.google.com/about/careers/applications/jobs/results/85564713261245126-software-engineering-intern-bs-summer-2027?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Hudson River Trading** | [Algorithm Developer New Grad - Quant Researcher](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8052050&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Hudson River Trading** | [Data Scientist Intern](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8257369&utm_source=Simplify&ref=Simplify) | Quant / Finance | US / UK | Ambiguous | review required |
| **Hudson River Trading** | [Software Engineer Intern](https://www.hudsonrivertrading.com/hrt-job/software-engineering-internship-c-or-python-summer-2027/?gh_src=&utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
| **IMC** | [Hardware Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823945101) | Hardware / EE | US | Summer 2027 | review required |
| **IMC** | [Quantitative Research Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4907399101) | Quant / Finance | US | Summer 2027 | review required |
| **IMC** | [Software Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823924101) | Software Engineering | US | Summer 2027 | review required |
| **IMC Trading** | [Deep Learning Research Intern - 2027 - Sydney](https://job-boards.eu.greenhouse.io/imc/jobs/4956547101) | Quant / Finance | Australia | 2027 | review required |
| **IMC Trading** | [Deep Learning Research Intern - Summer 2027 - Amsterdam](https://job-boards.eu.greenhouse.io/imc/jobs/4912874101) | Quant / Finance | Netherlands | Summer 2027 | review required |
| **IMC Trading** | [Graduate Quantitative Researcher \(PhD\)](https://job-boards.eu.greenhouse.io/imc/jobs/4912325101) | Quant / Finance | US | Unknown | review required |
| **IMC Trading** | [Hardware Machine Learning PhD Research Internship](https://job-boards.eu.greenhouse.io/imc/jobs/4975945101) | Quant / Finance | US | Unknown | review required |
| **IMC Trading** | [Machine Learning Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4962456101?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Machine Learning Research Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4907430101) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Performance Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4842595101?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Quantitative Research Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941208101) | Quant / Finance | Hong Kong | 2027 | review required |
| **IMC Trading** | [Quantitative Trader Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4936262101) | Quant / Finance | Netherlands | Unknown | review required |
| **IMC Trading** | [Quantitative Trader Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4823923101) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Quantitative Trader Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941205101) | Quant / Finance | Hong Kong | 2027 | review required |
| **IMC Trading** | [Software Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4667854101) | Quant / Finance | Netherlands | Unknown | review required |
| **IMC Trading** | [Software Engineer Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941206101) | Quant / Finance | Hong Kong | 2027 | review required |
| **IMC Trading** | [Software Engineer, Early Career](https://job-boards.eu.greenhouse.io/imc/jobs/4796143101) | Quant / Finance | US | Unknown | review required |
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
| **Jane Street** | [Sales and Trading Intern](https://www.janestreet.com/join-jane-street/position/8347385002/?utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
| **Jane Street** | [Software Engineer Intern](https://www.janestreet.com/join-jane-street/position/8599644002/?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Jane Street** | [Tools and Compilers Research and Development Intern](https://www.janestreet.com/join-jane-street/position/5869205002/?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Jane Street** | [Trading Desk Operations Engineer Intern](https://www.janestreet.com/join-jane-street/position/8621450002/?utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
| **Jane Street** | [Windows Engineer Intern](https://www.janestreet.com/join-jane-street/position/8628843002/?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Jump Trading** | [Campus AI Research Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8052281) | Quant / Finance | US | Unknown | review required |
| **Jump Trading** | [Campus AI Research Engineer - Deep Learning \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8052338) | Quant / Finance | US | Unknown | review required |
| **Jump Trading** | [Campus AI Research Engineer – Research Automation \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8052351) | Quant / Finance | US | Unknown | review required |
| **Jump Trading** | [Campus AI Researcher, PhD/Postdoc \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7976964) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus AI/ML Researcher \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027938) | Quant / Finance | Singapore / China / Hong Kong | Unknown | review required |
| **Jump Trading** | [Campus ASIC Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7974837) | Quant / Finance | Unknown | Unknown | review required |

_555 more are in [tracker.csv](tracker.csv)._

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
