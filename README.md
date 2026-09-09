# 🎯 Universal Academic & Career Tracker — Internships · Research · PhD · New Grad

<p align="center">
  <a href="https://abyyworld.github.io/internship-tracker/"><img alt="Open the tracker — 1858 open postings" src="https://img.shields.io/badge/Open%20the%20tracker-1858%20open%20postings-1f6feb?style=for-the-badge&labelColor=0d1117"></a>
  <a href="https://abyyworld.github.io/internship-tracker/studio.html"><img alt="Tailor my CV — in the browser" src="https://img.shields.io/badge/Tailor%20my%20CV-in%20the%20browser-2ea043?style=for-the-badge&labelColor=0d1117"></a>
</p>

<p align="center"><b><a href="https://abyyworld.github.io/internship-tracker/">https://abyyworld.github.io/internship-tracker/</a></b><br>
Search and filter every posting, then tailor your CV for one — in the browser, on a phone, with nothing to install.</p>

> Last verified run: **2026-09-09** · **1858 verified-open postings** · **39 research / PhD / postdoc positions**

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

## At a glance

| Metric | Count |
|--|--:|
| Verified-open postings | 1858 |
| Roles discovered today | 102 |
| New verified postings | 102 |
| Research / PhD / postdoc positions | 39 |
| Elite tier | 226 |
| High tier | 234 |
| Eligibility still needs review | 1858 |
| Deadlines within 10 days | 0 |

**By category:** Software Engineering 963 · Quant / Finance 215 · Data 170 · AI / ML 151 · Robotics & Embodied AI 128 · Hardware / EE 100 · Security 53 · Systems & Infra 52 · Computational Science 26

**By region:** US 1597 · UK 84 · Canada 61 · Unknown 27 · Singapore 14 · Netherlands 9 · US / Canada 5 · US / UK 5 · Ireland 4 · US / Australia 4 · UK / Australia 4 · Hong Kong 3 · France 3 · Switzerland 3 · US / Italy 3 · US / Austria 3 · Poland 2 · UK / Ireland 2 · Australia 2 · China 2 · China / Hong Kong 2 · US / Global 2 · Singapore / China / Hong Kong / Australia 2 · South Korea 2 · Germany 2 · Serbia 2 · US / UAE 2 · Singapore / China / Hong Kong 1 · US / France / Singapore / Hong Kong 1 · Remote 1 · India 1 · Spain 1 · US / Canada / UK 1 · US / Europe 1

**By degree evidence:** Unknown 1562 · Advanced/unknown 182 · PhD 52 · Undergraduate eligible 50 · Masters 12

## Newly opened (102)

| Company | Role | Category | Region | Term | Eligibility |
|--|--|--|--|--|--|
| **Two Sigma** | [Software Engineering Intern - Summer 2027](https://twosigma.avature.net/careers/JobDetail/14016?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **Coinbase** | [Credit Risk Intern](https://www.coinbase.com/careers/positions/8175369?gh_jid=8175369) | Software Engineering | US | Unknown | review required |
| **Coinbase** | [Payment Risk Intern](https://www.coinbase.com/careers/positions/8175447?gh_jid=8175447) | Software Engineering | US | Unknown | review required |
| **Coinbase** | [User Research Intern](https://www.coinbase.com/careers/positions/8175360?gh_jid=8175360) | Software Engineering | US | Unknown | review required |
| **Graphcore** | [Intern, Mechanical Engineering](https://job-boards.greenhouse.io/graphcore/jobs/8780063002) | Software Engineering | US | Unknown | review required |
| **Snowflake** | [Applied AI Intern - Warsaw](https://jobs.ashbyhq.com/snowflake/90190b16-fd27-4366-8c10-9c4896157681) | AI / ML | Poland | None | review required |
| **Verkada** | [Technical Support Engineering Intern - Spring 2027](https://job-boards.greenhouse.io/verkada/jobs/5056164007) | Software Engineering | US | Spring 2027 | review required |
| **Verkada** | [Technical Support Engineering Intern - Summer 2027](https://job-boards.greenhouse.io/verkada/jobs/5233011007) | Software Engineering | US | Summer 2027 | review required |
| **🔥 Coinbase** | [Analytics Engineer Intern](https://boards.greenhouse.io/embed/job_app?token=8175471&utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **🔥 Coinbase** | [Data Engineer Intern](https://boards.greenhouse.io/embed/job_app?token=8175459&utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **🔥 Coinbase** | [Data Science Intern - Strategy, Execution, &amp; Analytics - Platform](https://boards.greenhouse.io/embed/job_app?token=8175462&utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **🔥 Coinbase** | [Machine Learning Engineer Intern 🎓](https://boards.greenhouse.io/embed/job_app?token=8175441&utm_source=Simplify&ref=Simplify) | AI / ML | US | Ambiguous | review required |
| **🔥 Coinbase** | [People Analytics Intern](https://boards.greenhouse.io/embed/job_app?token=8175517&utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **🔥 Coinbase** | [Product Manager Intern - HR Technology](https://boards.greenhouse.io/embed/job_app?token=8175504&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **🔥 Coinbase** | [Software Engineer Intern](https://boards.greenhouse.io/embed/job_app?token=8168315&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **🔥 Datadog** | [Software Engineer Intern - Summer](https://careers.datadoghq.com/detail/8052118/?gh_jid=8052118&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer | review required |
| **🔥 SpaceX** | [Software Engineer New Grad - Software - Starship](https://boards.greenhouse.io/spacex/jobs/8743362002?utm_source=Simplify&ref=Simplify) | Software Engineering | US | New Grad 2026 | review required |
| **Bedrock Robotics** | [Internship 2027 Sensor Hardware Test Engineer](https://jobs.ashbyhq.com/bedrock-robotics/1f413f83-b897-4938-a19e-ab91bd326c51/application?embed=true&utm_source=Simplify&ref=Simplify) | Robotics &amp; Embodied AI | US | 2027 | review required |
| **AArete** | [Data Architecture &amp; Engineering Intern](https://jobs.jobvite.com/aarete/job/otGLAfwe?nl=1&nl=1&fr=false&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **ABB** | [Application Engineering Intern - Summer 2027](https://abb.wd3.myworkdayjobs.com/external_career_page/job/Alpharetta-Georgia-United-States-of-America/Application-Engineering-Intern---Summer-2027_JR00045706?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **AeroVironment** | [Software Engineer 1](https://avav.wd1.myworkdayjobs.com/en-US/avav/job/Sunrise-FL/Software-Engineer-I_8682?utm_source=Simplify&ref=Simplify) | Software Engineering | US | New Grad 2026 | review required |
| **Allen Control Systems** | [Computer Vision Intern - Machine Learning](https://jobs.ashbyhq.com/allen-control-systems/a7831fef-7125-4c03-b828-5f0472989037/application?embed=true&utm_source=Simplify&ref=Simplify) | AI / ML | US | Ambiguous | review required |
| **Allen Control Systems** | [Systems Engineering Intern](https://jobs.ashbyhq.com/allen-control-systems/9945f76d-6d03-45f0-b431-fc69d31f5476/application?embed=true&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Applied Intuition** | [Electrical System Integration Engineer - New Grad](https://jobs.ashbyhq.com/applied/6b9a508b-359f-43c1-aa83-cabf55c3e03e) | Robotics &amp; Embodied AI | US | Unknown | review required |
| **Applied Intuition** | [Mechanical Engineer - New Grad](https://jobs.ashbyhq.com/applied/6e57a97e-62bb-46fb-92ec-dd12831fd6f9) | Robotics &amp; Embodied AI | US | Unknown | review required |
| **Applied Materials** | [Software Engineering Intern - Masters 🎓](https://amat.wd1.myworkdayjobs.com/External/job/Santa-ClaraCA/XMLNAME-2027-Software-Engineering-Intern--Masters---Santa-Clara--CA-_R2628265?utm_source=Simplify&ref=Simplify) | Software Engineering | US | 2027 | review required |
| **BlueCross BlueShield of Nebraska** | [Healthcare Reimbursement Analytics Intern - Summer 2027](https://nebraskablue.wd1.myworkdayjobs.com/BCBSNE/job/Omaha-NE/Healthcare-Reimbursement-Analytics-Intern---Summer-2027_JR101410?utm_source=Simplify&ref=Simplify) | Data | US | Summer 2027 | review required |
| **Boeing** | [Applied Mathematician Intern - Engineering &amp; Technology Innovation 🎓](https://boeing.wd1.myworkdayjobs.com/EXTERNAL_CAREERS/job/USA---North-Charleston-SC/Boeing-Engineering---Technology-Innovation-Graduate-Researcher-Program--Applied-Mathematician-Intern_JR2026523704?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Boeing** | [Artificial Intelligence Software Engineer Intern - Graduate Researcher Program 🎓](https://boeing.wd1.myworkdayjobs.com/EXTERNAL_CAREERS/job/USA---Tukwila-WA/Boeing-Engineering---Technology-Innovation-Graduate-Researcher-Program--Software-Engineering-Artificial-Intelligence-Intern_JR2026523687?utm_source=Simplify&ref=Simplify) | AI / ML | US | Ambiguous | review required |
| **Boeing** | [Microelectronics R&amp;D Intern - Engineering &amp; Technology Innovation 🎓](https://boeing.wd1.myworkdayjobs.com/EXTERNAL_CAREERS/job/USA---Huntington-Beach-CA/Boeing-Engineering---Technology-Innovation-Graduate-Researcher-Program--Microelectronics-R-D-Intern_JR2026523675?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **C.H. Robinson** | [Software Engineer Intern](https://chrobinson.wd5.myworkdayjobs.com/CHRobinson/job/Eden-Prairie-MN-United-States-of-America/Software-Engineering-Internship-2027_R49323?utm_source=Simplify&ref=Simplify) | Software Engineering | US | 2027 | review required |
| **CHAOS Industries** | [Electrical Engineer Intern - Summer 2027](https://job-boards.greenhouse.io/chaosindustries/jobs/5226632007?utm_source=Simplify&ref=Simplify) | Hardware / EE | US | Summer 2027 | review required |
| **CHAOS Industries** | [Software Engineer Intern](https://job-boards.greenhouse.io/chaosindustries/jobs/5226636007?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **COUNTRY Financial** | [Automation Developer Intern](https://countryfinancial.wd5.myworkdayjobs.com/COUNTRYCorporateInternships/job/Bloomington-IL/Automation-Developer-Intern_R26_0000001000?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **COUNTRY Financial** | [Information Technology Services Intern](https://countryfinancial.wd5.myworkdayjobs.com/COUNTRYCorporateInternships/job/Bloomington-IL/Information-Technology-Services-Intern_R26_0000000977?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **COUNTRY Financial** | [Market Analytics Intern](https://countryfinancial.wd5.myworkdayjobs.com/COUNTRYCorporateInternships/job/Bloomington-IL/Market-Analytics-Intern_R26_0000000948?utm_source=Simplify&ref=Simplify) | Data | US | Ambiguous | review required |
| **CTG** | [Software Engineer 1](https://careers.ctg.com/jobs/17557?icims=1&utm_source=Simplify&ref=Simplify) | Software Engineering | US | New Grad 2026 | review required |
| **Capital One** | [AI Engineering Intern 🎓](https://capitalone.wd12.myworkdayjobs.com/Capital_One/job/New-York-NY/Current-Master-s--AI-Engineering-Internship-Program---Summer-2027_R249109-1?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **Capital One** | [Applied Research Intern 🎓](https://capitalone.wd12.myworkdayjobs.com/Capital_One/job/New-York-NY/Current-PhD--Applied-Research-Internship-Program---Summer-2027_R244323-1?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **Capital One** | [Data Analyst New Grad - Data Analyst](https://capitalone.wd12.myworkdayjobs.com/Capital_One/job/Toronto-ON/Associate--Data-Analyst---New-Grad--2027-Start_R999613-1?utm_source=Simplify&ref=Simplify) | Software Engineering | Canada | 2027 | review required |
| **Dick's Sporting Goods** | [Data Analytics &amp; Engineering Intern](https://dickssportinggoods.wd1.myworkdayjobs.com/en-US/DSG/job/Customer-Support-Center/Data-Analytics---Engineering---Summer-2027-Internship_202608778-1?utm_source=Simplify&ref=Simplify) | Data | US | Summer 2027 | review required |
| **Dimensional Fund Advisors** | [Software Engineer Intern](https://dimensional.wd5.myworkdayjobs.com/dfa_careers/job/Austin/Internship-in-Technology---Software-Engineer_2026-9022?utm_source=Simplify&ref=Simplify) | Software Engineering | US | 2026 | review required |
| **Ercot** | [IT Intern - Enterprise Data &amp; AI Administration](https://ercot.wd1.myworkdayjobs.com/ercot_careers/job/Taylor-TX/Intern---IT--Enterprise-Data---AI-Administration_R2478?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Gallup** | [Artificial Intelligence/Machine Learning Research Intern](https://job-boards.greenhouse.io/gallup/jobs/4395921009?utm_source=Simplify&ref=Simplify) | AI / ML | US | Ambiguous | review required |
| **Gallup** | [Data Engineering Intern](https://job-boards.greenhouse.io/gallup/jobs/4395454009?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Gallup** | [Data Science Intern - Summer 2027](https://job-boards.greenhouse.io/gallup/jobs/4395491009?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **Gallup** | [Software Engineer Intern - Summer 2027](https://job-boards.greenhouse.io/gallup/jobs/4395897009?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **General Dynamics Mission Systems** | [Software Engineer Intern](https://careers-gdms.icims.com/jobs/74687/job?mobile=true&needsRedirect=false&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **General Motors** | [Global Customer Research Intern 🎓](https://generalmotors.wd5.myworkdayjobs.com/Careers_GM/job/Warren-Michigan-United-States-of-America/XMLNAME-2027-Summer-Intern--Global-Customer-Research-Intern--Master-MBA-Degree-_JR-202619679?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **Goldman Sachs** | [Summer Analyst Intern - Americas - Engineering](https://higher.gs.com/roles/171565?type=students&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer | review required |
| **Goldman Sachs** | [Summer Analyst Intern - Americas - Engineering](https://higher.gs.com/roles/171564?type=students&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer | review required |
| **Huntington Ingalls Industries** | [Software Engineer 1](https://careers.huntingtoningalls.com/job/Newport-News-SOFTWARE-ENGINEER-1-Virg/1408046100/?ats=successfactors&utm_source=Simplify&ref=Simplify) | Software Engineering | US | New Grad 2026 | review required |
| **ID.me** | [Data Scientist New Grad 🎓](https://job-boards.greenhouse.io/idmeuniversityrecruiting/jobs/7986505003?utm_source=Simplify&ref=Simplify) | Data | US | New Grad 2026 | review required |
| **K2 Space** | [Simulation Software Engineering Intern](https://job-boards.greenhouse.io/k2spacecorporation/jobs/5418727008?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Kustomer** | [Software Engineer – Early Career - Full Stack](https://jobs.ashbyhq.com/kustomer/4037272a-7fd3-4040-906b-47fde875a817/application?utm_source=Simplify&ref=Simplify) | Software Engineering | US | New Grad 2026 | review required |
| **Meijer** | [Data Science Intern](https://meijer.wd5.myworkdayjobs.com/en-US/Meijer/job/Grand-Rapids-MI/Data-Science-Intern---Summer-2027_R000699579?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **Meijer** | [Store Analytics Intern](https://meijer.wd5.myworkdayjobs.com/en-US/Meijer/job/Grand-Rapids-MI/Store-Analytics-Intern--Summer-2027_R000698651?utm_source=Simplify&ref=Simplify) | Data | US | Summer 2027 | review required |
| **Moog** | [Hardware Design Engineering Intern](https://moog.wd5.myworkdayjobs.com/moog_external_career_site/job/Mineral-Wells-TX/Intern--Hardware-Design-Engineering_R-26-19887?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Moog** | [Software Engineer Intern - Military Aircraft](https://moog.wd5.myworkdayjobs.com/moog_external_career_site/job/Mineral-Wells-TX/Intern--Software-Engineering_R-26-19888-1?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **Motorola** | [Software Engineer Intern](https://motorolasolutions.wd5.myworkdayjobs.com/Careers/job/Chicago-IL/Software-Engineering-Intern---Summer-2027_R68388?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |

_42 more are in [tracker.csv](tracker.csv)._

## Browse by category

Every category is listed the same way. Live geography reflects what official feeds expose today; the worldwide career-hub and academic watchlists are kept separately in [manual_checks.md](manual_checks.md).

### Software Engineering (963 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Software Engineer \(Entry-Level\) - Python](https://www.akunacapital.com/careers/job/8013230/?gh_jid=8013230) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer Intern \(Summer 2027, Python / C++ / Full Stack / C# .NET\)](https://akunacapital.com/careers/job/8018847/) | US |  | unknown | unknown |
| **Akuna Capital University** | [Entry Level Software Engineer - C++](https://www.akunacapital.com/careers/job/8013085/?gh_jid=8013085&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Akuna Capital University** | [Software Engineer Intern - C# .NET Desktop](https://www.akunacapital.com/careers/job/8018886/?gh_jid=8018886&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Akuna Capital University** | [Software Engineer Intern - C++](https://www.akunacapital.com/careers/job/8018847/?gh_jid=8018847&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Akuna Capital University** | [Software Engineer Intern - Full Stack Web](https://www.akunacapital.com/careers/job/8018893/?gh_jid=8018893&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Akuna Capital University** | [Software Engineer Intern - Python](https://www.akunacapital.com/careers/job/8018853/?gh_jid=8018853&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Apple** | [Software Engineer Intern, Undergrad](https://jobs.apple.com/en-us/details/200664785/software-undergrad-engineering-internships?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Apple** | [Software Engineering Intern, Masters](https://jobs.apple.com/en-us/details/200664320/software-engineering-masters-internships?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Citadel** | [Software Engineer Intern](https://www.citadel.com/careers/details/software-engineer-intern-us/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Citadel** | [Software Engineer – University Graduate](https://www.citadel.com/careers/details/software-engineer-university-graduate-us/?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Citadel Securities** | [Software Engineer – University Graduate](https://www.citadelsecurities.com/careers/details/software-engineer-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **DE Shaw** | [Software Developer Intern](https://www.deshaw.com/careers/software-developer-intern-new-york-summer-2027-5894?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **DRW** | [AI/ML Research Intern](https://www.drw.com/work-at-drw/listings/aiml-research-intern-3466679?utm_source=github-vansh-ouckah) | Unknown | research | unknown | unknown |
| **DRW** | [Software Developer Intern](https://www.drw.com/work-at-drw/listings/software-developer-intern-3467328?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **DRW** | [Software Developer Intern](https://www.drw.com/work-at-drw/listings/software-developer-intern-3466687?utm_source=github-vansh-ouckah) | Unknown |  | unknown | unknown |
| **Five Rings Capital** | [Software Developer Intern - Software Developer](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349707008?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **G-Research** | [Data Science Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Data-Science-Internship_R3679?utm_source=Simplify&ref=Simplify) | UK | research | unknown | unknown |
| **Google** | [Software Engineering Intern](https://www.google.com/about/careers/applications/jobs/results/85564713261245126-software-engineering-intern-bs-summer-2027?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **IMC** | [Software Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823924101) | US |  | unknown | unknown |
| **Jane Street** | [Fundamental Research Analyst Intern](https://www.janestreet.com/join-jane-street/position/8347286002/?utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **Jane Street** | [Linux Engineer Intern](https://www.janestreet.com/join-jane-street/position/8626260002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Network Engineer Intern](https://www.janestreet.com/join-jane-street/position/8620793002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Software Engineer Intern](https://www.janestreet.com/join-jane-street/position/8599644002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Tools and Compilers Research and Development Intern](https://www.janestreet.com/join-jane-street/position/5869205002/?utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **Jane Street** | [Windows Engineer Intern](https://www.janestreet.com/join-jane-street/position/8628843002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
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
| **Two Sigma** | [Software Engineering Intern - Summer 2027](https://twosigma.avature.net/careers/JobDetail/14016?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Virtu Financial** | [2027 Internship - Software Engineer](https://job-boards.greenhouse.io/virtu/jobs/8551566002) | Ireland |  | unknown | unknown |
| **Virtu Financial** | [2027 Internship – Core Operations Engineer](https://job-boards.greenhouse.io/virtu/jobs/6329460002) | Singapore |  | unknown | unknown |
| **Virtu Financial** | [2027 Internship – Software Engineer](https://job-boards.greenhouse.io/virtu/jobs/5513756002) | Singapore |  | unknown | unknown |

_923 more are in [tracker.csv](tracker.csv)._

### Quant / Finance (215 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital University** | [Junior Quantitative Developer &amp; Strategist](https://www.akunacapital.com/careers/job/8016687/?gh_jid=8016687&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Akuna Capital University** | [Junior Quantitative Researcher](https://www.akunacapital.com/careers/job/8036541/?gh_jid=8036541&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Akuna Capital University** | [Junior Quantitative Researcher - Prediction Markets](https://www.akunacapital.com/careers/job/7863348/?gh_jid=7863348&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Akuna Capital University** | [Quantitative Development &amp; Strategy Intern](https://www.akunacapital.com/careers/job/8021481/?gh_jid=8021481&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Akuna Capital University** | [Quantitative Research Intern](https://www.akunacapital.com/careers/job/8036614/?gh_jid=8036614&utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Citadel** | [Quantitative Research Analyst University Graduate](https://www.citadel.com/careers/details/quantitative-research-analyst-university-graduate-us/?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Citadel** | [Quantitative Trader: Equity Quantitative Research – University Graduate](https://www.citadel.com/careers/details/quantitative-trader-equity-quantitative-research-university-graduate-us/?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Citadel Securities** | [Quantitative Research Analyst – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-research-analyst-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | UK / Ireland | research | unknown | unknown |
| **Citadel Securities** | [Quantitative Trader New Grad](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **Citadel Securities** | [Quantitative Trader – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-us-miami/?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Citadel Securities** | [Quantitative Trader – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-us-new-york/?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Cubist Systematic Strategies** | [Quantitative Developer Intern](https://job-boards.greenhouse.io/point72/jobs/7297613002) | US |  | unknown | unknown |
| **DRW** | [Quantitative Research Intern](https://www.drw.com/work-at-drw/listings/quantitative-research-intern-3413670?utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **DRW** | [Quantitative Trading Analyst Intern](https://job-boards.greenhouse.io/drweng/jobs/7957243?utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **DRW** | [Quantitative Trading Analyst Intern](https://www.drw.com/work-at-drw/listings/quantitative-trading-analyst-intern-3375090?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Five Rings Capital** | [Quantitative Researcher Intern 🎓](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349219008?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Five Rings Capital** | [Quantitative Trader Intern - Quantitative Trader](https://job-boards.greenhouse.io/fiveringsllc/jobs/5139668008?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
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
| **IMC Trading** | [Machine Learning Research Intern - Summer 2027 - Amsterdam](https://job-boards.eu.greenhouse.io/imc/jobs/4912874101) | Netherlands | research | unknown | unknown |
| **IMC Trading** | [Machine Learning Research Intern - Summer 2027 - Sydney](https://job-boards.eu.greenhouse.io/imc/jobs/4956547101) | Australia | research | unknown | unknown |
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

_175 more are in [tracker.csv](tracker.csv)._

### Data (170 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Citadel** | [Sector Data Scientist Intern](https://www.citadel.com/careers/details/sector-data-scientist-2027-intern-us/?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Jane Street** | [Data Engineer Intern](https://www.janestreet.com/join-jane-street/position/8631973002/?utm_source=github-vansh-ouckah) | US | data-eng | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Data Platform/Analytics](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922931&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Tower Research Capital** | [Business Analytics Intern - 6 Month Internship Opportunity](https://www.tower-research.com/open-positions/?gh_jid=8041512) | Netherlands | research | unknown | unknown |
| **Figma** | [Data Scientist, Core Data -  PhD \(2026\)](https://boards.greenhouse.io/figma/jobs/5976930004?gh_jid=5976930004) | US | phd-position | unknown | unknown |
| **🔥 Coinbase** | [Analytics Engineer Intern](https://boards.greenhouse.io/embed/job_app?token=8175471&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Coinbase** | [Data Engineer Intern](https://boards.greenhouse.io/embed/job_app?token=8175459&utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **🔥 Coinbase** | [Data Science Intern - Strategy, Execution, &amp; Analytics - Platform](https://boards.greenhouse.io/embed/job_app?token=8175462&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Coinbase** | [People Analytics Intern](https://boards.greenhouse.io/embed/job_app?token=8175517&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **AArete** | [Business Analytics Intern - Summer 2027](https://jobs.jobvite.com/aarete/job/oBXLAfwD?nl=1&nl=1&fr=false&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **AMERICAN SYSTEMS** | [Data Engineer - Junior](https://careers-americansystems.icims.com/jobs/4391/job?mobile=true&needsRedirect=false&utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **Affinius Capital** | [Data Scientist Intern](https://careers-affiniuscapital.icims.com/jobs/2284/summer-2027-data-scientist-intern/job) | US |  | unknown | unknown |
| **Allegheny County** | [Business Analytics Intern](https://alleghenycounty.bamboohr.com/careers/663/?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Allied Solutions** | [Sales Analytics Intern](https://alliedsolutions.wd501.myworkdayjobs.com/Allied_External/job/Carmel-IN/Sales-Analytics-Intern_R-011098?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012703?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012782?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012784?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012783?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - Global Servicing - Financial Crimes Risk &amp; Controls](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012627?utm_source=Simplify&ref=Simplify) | US | controls | unknown | unknown |
| **American Express** | [Data Analytics Intern - US Consumer Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26011607?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Engineer Intern - Enterprise Technology Services](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012333?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **American Express** | [Data Engineer Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012781?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **American Express** | [Data Engineer Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012764?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **Aramark** | [Junior Data Engineer](https://aramarkcareers.com/UnitedStates/job/Rockville-Jr_-Data-Engineer-MD-20850/1426145000/?ats=successfactors&utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **Arch Capital Group** | [Data and Analytics Intern](https://archgroup.wd1.myworkdayjobs.com/careers/job/Farmington-CT-United-States-of-America/Data-and-Analytics-Intern_R26_845?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Arthur J. Gallagher &amp; Co.** | [Data Analytics Intern](https://jobs.ajg.com/jobs/57701?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Auto-Owners Insurance** | [Business Intelligence Developer Intern - Summer 2027](https://aoins.wd5.myworkdayjobs.com/AutoOwners/job/Lansing-MI/Business-Intelligence-Developer-Internship---Summer-2027_R_14417?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Baird** | [Capital Markets Compliance Data &amp; Analytics Intern](https://baird.wd1.myworkdayjobs.com/careers/job/WI-Milwaukee/Internship---Capital-Markets-Compliance-Data---Analytics--Year-Round-_R2026962-2?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Blackstone** | [Data Engineer Summer Analyst - Blackstone Technology &amp; Innovations](https://blackstone.wd1.myworkdayjobs.com/zh-CN/Blackstone_Campus_Careers/job/Miami/XMLNAME-2027-Blackstone-Technology-and-Innovations--Data-Engineer-Summer-Analyst_45022?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **BlueCross BlueShield of Nebraska** | [Data Intern - Data Science - Data Analytics](https://nebraskablue.wd1.myworkdayjobs.com/BCBSNE/job/Omaha-NE/Data-Intern--Summer-2027_JR101406?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **BlueCross BlueShield of Nebraska** | [Healthcare Reimbursement Analytics Intern - Summer 2027](https://nebraskablue.wd1.myworkdayjobs.com/BCBSNE/job/Omaha-NE/Healthcare-Reimbursement-Analytics-Intern---Summer-2027_JR101410?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Huntsville-AL/University---2027-Summer-Games-Data-Scientist-Intern---Huntsville--AL_R0248407?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern - 2027 Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Honolulu-HI/University---2027-Summer-Games--Data-Scientist-Intern---Honolulu--HI_R0248406?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Rome-NY/University--2027-Summer-Games-Data-Scientist-Intern_R0248143?utm_source=Simplify&ref=Simplify) | US / Italy |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Colorado-Springs-CO/University--2027-Summer-Games-Data-Scientist-Intern_R0248132?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern - University](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Annapolis-Junction-MD/University---2027-Summer-Games-Data-Scientist-Intern---Annapolis-Junction--MD_R0248408?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern - University](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Charleston-SC/University---2027-Summer-Games-Data-Scientist-Intern_R0248137?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern - University](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Atlanta-GA/University--2027-Summer-Games-Data-Scientist-Intern_R0248140?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern - University](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/McLean-VA/University---2027-Summer-Games-Data-Scientist-Intern---McLean--VA_R0248037?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Data Scientist Intern - University](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/San-Diego-CA/University---2027-Summer-Games-Data-Scientist-Intern---San-Diego--CA_R0248045?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |

_130 more are in [tracker.csv](tracker.csv)._

### AI / ML (151 live)

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
| **🔥 NVIDIA** | [Generative AI Ph.D. Research Intern 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/NVIDIA-2027-Internships--PhD-Research-Generative-AI_JR2023475?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **🔥 NVIDIA** | [Large Language Models Intern - Research 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/NVIDIA-2027-Internships--PhD-Research-Large-Language-Models_JR2023837?utm_source=Simplify&ref=Simplify) | US | llm,research | unknown | unknown |
| **🔥 NVIDIA** | [Research Scientist New Grad - Circuits 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Research-Scientist--Circuits---New-College-Grad-2026_JR2010010?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
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
| **Perplexity** | [Internship - Machine Learning Research Engineer](https://jobs.ashbyhq.com/perplexity/b9e1ff15-d52a-46d5-abf0-26460f2a116c) | Germany | multimodal,research | unknown | unknown |
| **Perplexity** | [Internship - Search Machine Learning Engineer](https://jobs.ashbyhq.com/perplexity/9246cf02-26fd-4ae8-90c5-639c6e85e9e2) | Serbia | llm,nlp,infra,research,phd-position | unknown | unknown |
| **Perplexity** | [Internship - Search Machine Learning Engineer](https://jobs.ashbyhq.com/perplexity/71168628-1998-47d3-87a9-be7bc56a430d) | UK | llm,nlp,infra,research | unknown | unknown |
| **Sierra** | [Software Engineer, Agent \(New Grad 2027\)](https://jobs.ashbyhq.com/Sierra/149f368c-52d5-408f-ba26-ad888f318a00/application?embed=true&utm_source=Simplify&ref=Simplify) | US | autonomy,llm,research,funded | unknown | posting mentions equity |
| **Sierra** | [Software Engineer, Agent \(New Grad 2027\)](https://jobs.ashbyhq.com/sierra/79953d72-60d4-43e0-8c8c-6eccda422dce) | Singapore | autonomy,llm,research,funded | unknown | posting mentions equity |
| **Snowflake** | [AI Research Scientist, New Grad – Agents &amp; Reinforcement Learning](https://jobs.ashbyhq.com/snowflake/1bad12df-f443-426f-9d09-e96fc780d698/application?utm_source=Simplify&ref=Simplify) | US | autonomy,llm,rl,data-eng,infra,research,phd-position | unknown | unknown |
| **Snowflake** | [Applied AI Intern - Warsaw](https://jobs.ashbyhq.com/snowflake/90190b16-fd27-4366-8c10-9c4896157681) | Poland | controls,llm,data-eng,infra,distributed,research,phd-position | unknown | unknown |
| **🔥 AMD** | [Machine Learning Intern/Co-op - Artificial Intelligence 🎓](https://careers.amd.com/jobs/91181?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Machine Learning Intern/Co-op - Machine Learning - Artificial Intelligence](https://careers.amd.com/jobs/90892?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Machine Learning Intern/Co-op - Multiple Teams](https://careers.amd.com/jobs/91170?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Machine Learning/Artificial Intelligence Intern/Co-op](https://careers.amd.com/jobs/91363?icims=1&utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **🔥 Coinbase** | [Machine Learning Engineer Intern 🎓](https://boards.greenhouse.io/embed/job_app?token=8175441&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **AeroVironment** | [Machine Learning Intern](https://avav.wd1.myworkdayjobs.com/en-US/avav/job/Minneapolis-MN/Summer-2027-Machine-Learning-Intern_8389?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Allen Control Systems** | [Computer Vision Intern - Machine Learning](https://jobs.ashbyhq.com/allen-control-systems/a7831fef-7125-4c03-b828-5f0472989037/application?embed=true&utm_source=Simplify&ref=Simplify) | US | perception,controls,computer-vision | unknown | unknown |

_111 more are in [tracker.csv](tracker.csv)._

### Robotics & Embodied AI (128 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Amazon** | [Robotics - Software Development Engineer Intern/Co-op](https://www.amazon.jobs/en/jobs/3136266/robotics-software-development-engineer-intern-co-op-2026?no_int_redir=1&utm_source=github-vansh-ouckah) | US | robot-software | unknown | unknown |
| **🔥 Amazon** | [Software Development Engineer Intern - Robotics](https://amazon.jobs/en/jobs/10529525/software-development-engineer-intern-robotics-2027?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [Research Scientist New Grad - Robotics Research 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-WA-Seattle/Research-Scientist--Robotics-Research----PhD-New-College-Grad-2026_JR2011473?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **🔥 NVIDIA** | [Robotics Intern - Ph.D. Research 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/NVIDIA-2027-Internships--PhD-Research-Robotics_JR2023847?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Nuro** | [Software Engineer, AI Platform - Intern](https://nuro.ai/careersitem?gh_jid=7351061) | US | autonomous vehicles | private-scaleup | private company; verify offer |
| **Nuro** | [Software Engineer, AI Platform - New Grad](https://nuro.ai/careersitem?gh_jid=7351066) | US | autonomous vehicles | private-scaleup | private company; verify offer |
| **Waymo** | [2027 Summer Intern, BS, SysEng Software Engineer](https://careers.withwaymo.com/jobs?gh_jid=8174099) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, BS/MS, Pipeline and Test Health Engineer](https://careers.withwaymo.com/jobs?gh_jid=8177651) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Applied Research Scientist – New Grad - Perception Large Language Model/Vision-Language Model - PhD 🎓](https://careers.withwaymo.com/jobs?gh_jid=7488508&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Data Science Intern - Commercialization Testing 🎓](https://careers.withwaymo.com/jobs?gh_jid=8167323&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Software Engineering Intern - Behavior Test - MS 🎓](https://careers.withwaymo.com/jobs?gh_jid=8174504&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **Bedrock Robotics** | [Internship 2027 Sensor Hardware Test Engineer](https://jobs.ashbyhq.com/bedrock-robotics/1f413f83-b897-4938-a19e-ab91bd326c51/application?embed=true&utm_source=Simplify&ref=Simplify) | US | construction autonomy | emerging-startup | private company; verify offer |
| **Deft Robotics** | [Electrical Engineer Intern \(Spring-Summer 2026\)](https://jobs.ashbyhq.com/deft-ai/0d16afe8-30a9-43df-90d5-ccba1cb97b69) | US | humanoid robotics | emerging-startup | private company; verify offer |
| **Deft Robotics** | [Mechanical Engineer Intern \(Spring-Summer 2026\)](https://jobs.ashbyhq.com/deft-ai/1bef1405-cd24-4da7-b1e7-0ca02e8f5eb2) | US | humanoid robotics | emerging-startup | private company; verify offer |
| **Dyna Robotics** | [Research Internship](https://jobs.ashbyhq.com/dyna-robotics/5a431519-ee6b-4cb7-8a3a-422727053a09) | US | robot learning | emerging-startup | private company; verify offer |
| **Generalist AI** | [Research Assistant](https://jobs.ashbyhq.com/generalist/fc7c7b49-248a-4849-a473-a0bd246e5486) | US | general-purpose robotics | emerging-startup | private company; verify offer |
| **Lightwheel** | [Developer Advocate / Research Community Intern](https://jobs.ashbyhq.com/lightwheel/e22363b9-9c4f-4991-8de3-339b8e9399df) | US | robot learning | emerging-startup | private company; verify offer |
| **Physical Intelligence** | [Research Internships](https://jobs.ashbyhq.com/physicalintelligence/f020ff1a-4b4c-4415-8434-2da5010a7076) | US | embodied AI | emerging-startup | private company; verify offer |
| **RoboForce** | [Robotics Electrical Engineering Intern](https://job-boards.greenhouse.io/roboforce/jobs/5181214008) | US | industrial robotics | emerging-startup | private company; verify offer |
| **1X** | [AI Residency](https://jobs.ashbyhq.com/1x/5b2b4c73-13b5-46ca-8467-8024741a4b57) | US | humanoid robotics | private-scaleup | private company; verify offer |
| **1X** | [Internship - Manufacturing Engineering \(Fall\)](https://jobs.ashbyhq.com/1x/7d93444c-01f5-485c-89ef-24164f30441d) | US | humanoid robotics | private-scaleup | private company; verify offer |
| **ANYbotics** | [Software Engineering Internship - AI Platform](https://jobs.lever.co/anybotics/7e305a48-4628-4a6a-b054-0367b6f6e586) | Switzerland | legged robots | private-scaleup | private company; verify offer |
| **Anduril** | [2026 Early Career Electrical Engineer](https://boards.greenhouse.io/andurilindustries/jobs/4802172007?gh_jid=4802172007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2026 Early Career Flight Test Engineer, Mission Autonomy](https://boards.greenhouse.io/andurilindustries/jobs/5185089007?gh_jid=5185089007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2026 Early Career Manufacturing Engineer](https://boards.greenhouse.io/andurilindustries/jobs/5176254007?gh_jid=5176254007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2026 Early Career Mechanical Engineer](https://boards.greenhouse.io/andurilindustries/jobs/4802167007?gh_jid=4802167007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2026 Early Career Test &amp; Evaluation Systems Integrator](https://boards.greenhouse.io/andurilindustries/jobs/5185888007?gh_jid=5185888007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2026 Mechanical Engineering Intern](https://boards.greenhouse.io/andurilindustries/jobs/5211102007?gh_jid=5211102007) | UK / Australia | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2026 Robotics Engineer Intern](https://boards.greenhouse.io/andurilindustries/jobs/5211095007?gh_jid=5211095007) | UK / Australia | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2026 Software Engineering Intern](https://boards.greenhouse.io/andurilindustries/jobs/5211077007?gh_jid=5211077007) | UK / Australia | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2027 Early Career Electrical Engineer](https://boards.greenhouse.io/andurilindustries/jobs/5136925007?gh_jid=5136925007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2027 Early Career Manufacturing Engineer](https://boards.greenhouse.io/andurilindustries/jobs/5136970007?gh_jid=5136970007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2027 Early Career Mechanical Engineer](https://boards.greenhouse.io/andurilindustries/jobs/5136984007?gh_jid=5136984007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2027 Electrical Engineer Intern](https://boards.greenhouse.io/andurilindustries/jobs/5148101007?gh_jid=5148101007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2027 Manufacturing Engineer Intern](https://boards.greenhouse.io/andurilindustries/jobs/5153218007?gh_jid=5153218007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2027 Mechanical Engineer Intern](https://boards.greenhouse.io/andurilindustries/jobs/5153187007?gh_jid=5153187007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [Early Career Flight Software Engineer](https://boards.greenhouse.io/andurilindustries/jobs/5228868007?utm_source=Simplify&ref=Simplify) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [Early Career Software Engineer](https://boards.greenhouse.io/andurilindustries/jobs/4802146007?utm_source=Simplify&ref=Simplify) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [Mission Engineer, Air Dominance &amp; Strike, Early Career](https://boards.greenhouse.io/andurilindustries/jobs/5174562007?gh_jid=5174562007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [Software Engineer Intern](https://job-boards.greenhouse.io/andurilindustries/jobs/5148079007?gh_jid=5148079007&utm_source=github-vansh-ouckah) | US | autonomous systems | private-scaleup | private company; verify offer |

_88 more are in [tracker.csv](tracker.csv)._

### Hardware / EE (100 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital University** | [Hardware Engineer Intern](https://www.akunacapital.com/careers/job/8018880/?gh_jid=8018880&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **DRW** | [FPGA Intern](https://www.drw.com/work-at-drw/listings/fpga-intern-3484423?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **IMC** | [Hardware Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823945101) | US |  | unknown | unknown |
| **Jane Street** | [Hardware Engineer \(FPGA/ASIC\) Intern](https://www.janestreet.com/join-jane-street/position/8624440002/?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **Optiver** | [FPGA Engineer Intern](https://www.optiver.com/join-us/jobs/8402114002/?gh_jid=8402114002&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Optiver** | [FPGA Engineer Intern](https://www.optiver.com/join-us/jobs/8641352002/?gh_jid=8641352002&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Susquehanna International Group** | [FPGA Engineer Intern](https://careers-sig.icims.com/jobs/11446/job?mobile=true&needsRedirect=false&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
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
| **Verkada** | [Hardware Engineer \(Winter Co-op\)](https://job-boards.greenhouse.io/verkada/jobs/4321158007) | US |  | unknown | unknown |
| **🔥 AMD** | [ASIC Package Engineer Intern Co-op 🎓](https://careers.amd.com/jobs/91469?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [ASIC Package Engineering Intern Co-op 🎓](https://careers.amd.com/jobs/91471?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [ASIC Verification Engineer Intern/Co-op](https://careers.amd.com/jobs/91207?icims=1&utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Co-op/Intern 🎓](https://careers.amd.com/jobs/90809?icims=1&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op](https://careers.amd.com/jobs/91320?icims=1&utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op](https://careers.amd.com/jobs/91313?icims=1&utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op - Long Term](https://careers.amd.com/jobs/90297?icims=1&utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op 🎓](https://careers.amd.com/jobs/90805?icims=1&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineering Intern Co-op - Undergrad](https://careers.amd.com/jobs/90807?icims=1&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 AMD** | [Hardware Engineer Intern/Co-op](https://careers.amd.com/jobs/90894?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Hardware Engineer Intern/Co-op - Hardware Engineering 🎓](https://careers.amd.com/jobs/91182?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Tesla** | [Embedded Software Engineer Intern - Optimus](https://www.tesla.com/careers/search/job/282340?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **AeroVironment** | [Embedded Software Engineer Intern](https://avav.wd1.myworkdayjobs.com/en-US/avav/job/Simi-Valley-CA/Summer-2027-Embedded-Software-Engineering-Intern_8388?utm_source=Simplify&ref=Simplify) | US / Australia | hardware | unknown | unknown |
| **Alarm.com** | [Embedded Software Engineer 1](https://job-boards.greenhouse.io/alarmcom/jobs/8622530002?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Apex** | [Software Engineer Intern - Embedded Systems](https://jobs.ashbyhq.com/apex-technology-inc/4203604c-2330-4c89-8432-37af718a6bda/application?embed=true&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Apex Technology, Inc.** | [Software Engineering Intern, Embedded Systems](https://jobs.ashbyhq.com/apex-technology-inc/5ec2dfa9-724d-4ce4-ab97-5067ec747f11?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **Axon** | [Embedded Engineer Intern](https://job-boards.greenhouse.io/axontalentcommunity/jobs/7800627003?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Blue Origin** | [ASIC Engineer - Early Career](https://blueorigin.wd5.myworkdayjobs.com/blueorigin/job/Greater-Seattle-Area/ASIC-Engineer---Early-Career_R70802?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Blue Origin** | [Avionics / Embedded Software Engineer 1 - 2027 Starts](https://blueorigin.wd5.myworkdayjobs.com/blueorigin/job/Greater-Seattle-Area/Avionics---Embedded-Software-Engineer-I---Early-Career--2027-Starts-_R71324?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Blue Origin** | [Avionics / Embedded Software Engineer 1 - Early Career](https://blueorigin.wd5.myworkdayjobs.com/blueorigin/job/Greater-Seattle-Area/Avionics---Embedded-Software-Engineer-I---Early-Career--2026-Starts-_R70055?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Boeing** | [Entry Level ASIC/FPGA Verification Engineer - Space Electronics](https://boeing.wd1.myworkdayjobs.com/external_subsidiary/job/USA---Mountain-View-CA/Entry-Level-ASIC-FPGA-Verification-Engineer---Space-Electronics---MTV_JR2026520435-2?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |

_60 more are in [tracker.csv](tracker.csv)._

### Security (53 live)

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
| **Palantir** | [Software Engineer, New Grad - Production Infrastructure](https://jobs.lever.co/palantir/15844944-fb69-4b57-9531-e988650b20c6) | US | computer-vision,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Production Infrastructure](https://jobs.lever.co/palantir/4d5a144e-87ea-45e2-a68c-3fad590629af) | US | computer-vision,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Production Infrastructure](https://jobs.lever.co/palantir/e1a6c138-98bf-45e2-97f7-2c70371cc38a) | US | computer-vision,infra,security,research,funded | unknown | unknown |
| **Palantir** | [Year at Palantir - Forward Deployed Software Engineer, Internship - Commercial](https://jobs.lever.co/palantir/75cc1c09-8ebd-44c8-b3bc-d122cd1fecb3) | US | autonomy,infra,security,research | unknown | unknown |
| **Palantir** | [Year at Palantir - Forward Deployed Software Engineer, Internship - USG](https://jobs.lever.co/palantir/5c4c65c5-77da-4d36-856c-4ade87631019) | US | autonomy,infra,security,research | unknown | unknown |
| **Palantir** | [Year at Palantir - Forward Deployed Software Engineer, Internship - USG](https://jobs.lever.co/palantir/5c7bb70c-83ea-43e7-8055-0c8f319f4333) | US | autonomy,infra,security,research | unknown | unknown |
| **Palantir** | [Year at Palantir - Software Engineer, Internship](https://jobs.lever.co/palantir/655f9937-a4ce-4e7d-80e2-a6659af07329) | US | autonomy,infra,security,research | unknown | unknown |

_13 more are in [tracker.csv](tracker.csv)._

### Systems & Infra (52 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Platform Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018856/?gh_jid=8018856&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **DRW** | [Platform Engineer Intern](https://www.drw.com/work-at-drw/listings/platform-engineer-intern-3468737?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **🔥 Google** | [Software Engineering or Site Reliability Engineering PhD Intern 🎓](https://www.google.com/about/careers/applications/jobs/results/80037545080955590?utm_source=Simplify&ref=Simplify) | UK | infra,phd-position | unknown | unknown |
| **🔥 NVIDIA** | [Backend Compiler Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Backend-Compiler-Engineer---New-College-Grad-2026_JR2021242?utm_source=Simplify&ref=Simplify) | US / Canada |  | unknown | unknown |
| **Cerebras Systems** | [DevOps Engineer - New Grad 2026](https://jobs.ashbyhq.com/cerebras/40e0d3ee-8f0a-4b19-9bf9-79410b1c7735) | Remote | infra,distributed,research | unknown | unknown |
| **Cerebras Systems** | [Software Engineer - New Grad 2026](https://jobs.ashbyhq.com/cerebras/99c289fa-8fc6-49f7-b7e8-78ac4e9d99ac/application?utm_source=Simplify&ref=Simplify) | US / Canada | hardware,infra,distributed,research | unknown | unknown |
| **Cloudflare** | [Systems Engineer - Global Resource Management \(Data Residency\)](https://boards.greenhouse.io/cloudflare/jobs/8015230?gh_jid=8015230) | Unknown |  | unknown | unknown |
| **Notion** | [Software Engineer, Early Career](https://jobs.ashbyhq.com/notion/297b4ece-765f-4eea-b1b8-46057cb6501f/application?utm_source=Simplify&ref=Simplify) | US | autonomy,infra,distributed,research | unknown | posting mentions equity |
| **Notion** | [Software Engineer, Early Career \(AI\)](https://jobs.ashbyhq.com/notion/85947779-6b87-466a-98bc-30a640448c28/application?utm_source=Simplify&ref=Simplify) | US | autonomy,infra,distributed | unknown | posting mentions equity |
| **Perplexity** | [Internship - Search Backend Infra Engineer](https://jobs.ashbyhq.com/perplexity/be94e89b-89d5-4f2a-a58b-7929c8d97f92) | Serbia | infra,distributed,phd-position | unknown | unknown |
| **🔥 AMD** | [Compiler Engineer Intern/Co-op](https://careers.amd.com/jobs/91865?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Compiler Engineer Intern/Co-op](https://careers.amd.com/jobs/91864?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Compiler Engineer Intern/Co-op - Masters 🎓](https://careers.amd.com/jobs/91867?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Blissway** | [Embedded Systems Engineer New Grad](https://jobs.ashbyhq.com/blissway/51d6d839-9801-4436-bfc2-918bae428ed8/application?embed=true&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/San-Diego-CA/University---2027-Summer-Games-Systems-Engineer-Intern---San-Diego--CA_R0248365?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/McLean-VA/University---2027-Summer-Games-Systems-Engineer-Intern---McLean--VA_R0248361?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Fort-Walton-Beach-FL/University---2027-Summer-Games-Systems-Engineer-Intern---Ft-Walton-Beach--FL_R0248388?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Honolulu-HI/University---2027-Summer-Games-Systems-Engineer-Intern---Honolulu--HI_R0248370?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/San-Diego-CA/University---2027-Summer-Games-Systems-Engineer-Intern---El-Segundo--CA_R0248366?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Atlanta-GA/University---2027-Summer-Games--Systems-Engineer-Intern---Atlanta--GA_R0248381?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - University](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Colorado-Springs-CO/University---2027-Summer-Games-Systems-Engineer-Intern---Colorado-Springs--CO_R0248368?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - University](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Rome-NY/University---2027-Summer-Games-Systems-Engineer-Intern---Rome--NY_R0248386?utm_source=Simplify&ref=Simplify) | US / Italy |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - University - 2027 Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Annapolis-Junction-MD/University---2027-Summer-Games-Systems-Engineer-Intern---Annapolis-Junction--MD_R0248384?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Brunswick** | [Systems Engineer Co-op - Software Engineering](https://brunswick.wd1.myworkdayjobs.com/en-US/search/job/Fond-du-Lac-WI/Mercury-Marine---Systems-Software-Engineering-Co-op_JR-051212?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Crusoe** | [Software Engineer 1 - Storage](https://jobs.ashbyhq.com/Crusoe/4f5d34ed-0c05-4eec-b8f8-14663e114b02/application?embed=true&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Dedalus Labs** | [Systems Engineer / Product Manager Intern \(Summer 2027\)](https://www.ycombinator.com/companies/dedalus-labs/jobs/YtbvXM8-systems-engineer-summer-2027-intern) | US |  | unknown | unknown |
| **Etched** | [Infrastructure Intern](https://jobs.ashbyhq.com/Etched/80926a71-0a62-4bf8-a877-b6d96df279b7?utm_source=github-vansh-ouckah) | US | infra | unknown | unknown |
| **Etched AI** | [Chip Simulation Software Intern](https://jobs.ashbyhq.com/etched/27e5bd6b-9357-45f0-9e79-cfa2bf4eeba8) | Unknown | hardware,infra,research,phd-position | unknown | unknown |
| **Etched AI** | [Electrical Platform Intern](https://jobs.ashbyhq.com/etched/904ddf46-55fc-4a8f-8b49-f32cfe88116a) | Unknown | hardware,infra,research | unknown | unknown |
| **Etched AI** | [Firmware Intern](https://jobs.ashbyhq.com/etched/699f3ab2-07e4-466c-9d76-3d4a3abb4ebc) | Unknown | hardware,infra,research,phd-position | unknown | unknown |
| **Etched AI** | [Performance Tools Intern](https://jobs.ashbyhq.com/etched/f02e8035-7dc9-4b0c-aab7-75bbb4e975b8) | Unknown | hardware,infra,research | unknown | unknown |
| **GE Vernova** | [CIC Systems Engineer Co-op](https://gevernova.wd5.myworkdayjobs.com/only_confidential_executive_recruiting/job/Rochester/GE-Vernova-CIC-Systems-Engineer-Co-op---Spring---Summer-2027_R5051807-1?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **GE Vernova** | [Hardware Engineer Intern - Critical Infrastructure Communications](https://gevernova.wd5.myworkdayjobs.com/only_confidential_executive_recruiting/job/Rochester/GE-Vernova-Grid-Solutions---Hardware-Engineering-Intern--Critical-Infrastructure-Communications----Spring-Summer-2027_R5051647-1?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **GE Vernova** | [Software Engineer Co-op - Critical Infrastructure Communication](https://gevernova.wd5.myworkdayjobs.com/only_confidential_executive_recruiting/job/Rochester/GE-Vernova-Software-Engineering---Co-op---Spring-Summer-2027_R5051780-1?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **GE Vernova** | [Software Engineering Co-op - Critical Infrastructure Communication Engineering](https://gevernova.wd5.myworkdayjobs.com/only_confidential_executive_recruiting/job/Rochester/GE-Vernova-Software-Engineering---Co-op--Summer---Fall_R5051794-1?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **General Dynamics Information Technology** | [Systems Engineer Intern](https://www.gd.com/careers/systems-engineer-intern-albany-ny-us-rq225289-gdit-opportunity?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Lightfield** | [Early Career Infrastructure Software Engineer](https://jobs.ashbyhq.com/Lightfield/9a7ef2f9-577a-4242-b884-719e3cdf4420/application?embed=true&utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **Poshmark** | [Cloud Platform Engineer Intern, Growth 🛂](https://jobs.ashbyhq.com/poshmark/062b84e6-1633-43ae-870b-83cb62893caa?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **StepStone Group** | [Private Equity Infrastructure &amp; Real Assets Summer Analyst 🛂](https://www.stepstonegroup.com/current-opportunities/?gh_jid=7872890) | US | infra | unknown | unknown |
| **🔥 ByteDance** | [AI Network Automation Engineer Intern - Global Physical Network Infrastructure](https://jobs.bytedance.com/en/position/7670690923748870405/detail?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |

_12 more are in [tracker.csv](tracker.csv)._

### Computational Science (26 live)

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
| **Palantir** | [Software Engineer, New Grad - Infrastructure](https://jobs.lever.co/palantir/9265acce-12cd-4179-8c50-55d15963532b) | UK | computer-vision,infra,research | unknown | unknown |
| **Snowflake** | [Software Engineer Intern - Berlin \(2026\)](https://jobs.ashbyhq.com/snowflake/41e65c6c-a01e-4f40-af14-ae75d3b95e27) | Germany | hardware,data-eng,infra,distributed,research,phd-position | unknown | unknown |
| **🔥 Tesla** | [Physics Engine Development Engineer Intern - Optimus](https://www.tesla.com/careers/search/job/282147?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Data Analyst New Grad - Engagement Optimization](https://careers.jhuapl.edu/jobs/59507?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Data Scientist New Grad - Computer Scientist - Decision Systems 🎓](https://careers.jhuapl.edu/jobs/59918?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Data Scientist/Engineer New Grad - Analytic Capabilities 🎓](https://careers.jhuapl.edu/jobs/59818?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Engineer/Analyst/Scientist Intern - C2 Resilience Sciences](https://careers.jhuapl.edu/jobs/59832?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Engineer/SW Developer/Analyst Intern - Maritime Force Engagement Control](https://careers.jhuapl.edu/jobs/59598?icims=1&utm_source=Simplify&ref=Simplify) | US | controls | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Mission Systems Engineering Intern](https://careers.jhuapl.edu/jobs/59883?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Sensor Systems Intern - Data Analytics](https://careers.jhuapl.edu/jobs/59958?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Sensor Systems/Data Analytics New Grad](https://careers.jhuapl.edu/jobs/59770?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Software Developer Intern - Tactical System Prototyping and Deployment](https://careers.jhuapl.edu/jobs/59564?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Software Developer New Grad - Engagement Optimization](https://careers.jhuapl.edu/jobs/59510?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Software Development Intern](https://careers.jhuapl.edu/jobs/59745?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Software Engineering/ML/Data Scientist New Grad - Intelligence Systems 🎓](https://careers.jhuapl.edu/jobs/59654?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Systems &amp; Software Engineer New Grad - Multi-Domain Mission Planning Development](https://careers.jhuapl.edu/jobs/59974?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Merck** | [Computational Toxicology Intern - AI/ML Computational Toxicology](https://msd.wd5.myworkdayjobs.com/searchjobs/job/USA---Pennsylvania---West-Point/XMLNAME-2027-Future-Talent-Program---AI-ML-Computational-Toxicology---Intern_R412871?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |

### Early-company / equity reality check

The company signal is a discovery aid, not a prediction. Private-company options can become valuable, but can also expire, dilute, remain illiquid, or end up worth zero. `private company; verify offer` means the posting does not prove that equity is included. Ask for the option count **and fully diluted percentage**, strike price, vesting/cliff, exercise window, latest common valuation, and liquidation preferences.

## Elite and high-tier live postings (460)

| Company | Role | Category | Region | Term | Eligibility |
|--|--|--|--|--|--|
| **Akuna Capital** | [Platform Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018856/?gh_jid=8018856&utm_source=github-vansh-ouckah) | Systems &amp; Infra | US | Summer 2027 | review required |
| **Akuna Capital** | [Software Engineer \(Entry-Level\) - Python](https://www.akunacapital.com/careers/job/8013230/?gh_jid=8013230) | Software Engineering | US | Unknown | review required |
| **Akuna Capital** | [Software Engineer Intern \(Summer 2027, Python / C++ / Full Stack / C# .NET\)](https://akunacapital.com/careers/job/8018847/) | Software Engineering | US | Summer 2027 | review required |
| **Akuna Capital University** | [Entry Level Software Engineer - C++](https://www.akunacapital.com/careers/job/8013085/?gh_jid=8013085&utm_source=Simplify&ref=Simplify) | Software Engineering | US | New Grad 2026 | review required |
| **Akuna Capital University** | [Hardware Engineer Intern](https://www.akunacapital.com/careers/job/8018880/?gh_jid=8018880&utm_source=Simplify&ref=Simplify) | Hardware / EE | US | Summer 2027 | review required |
| **Akuna Capital University** | [Junior Quantitative Developer &amp; Strategist](https://www.akunacapital.com/careers/job/8016687/?gh_jid=8016687&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Akuna Capital University** | [Junior Quantitative Researcher](https://www.akunacapital.com/careers/job/8036541/?gh_jid=8036541&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Akuna Capital University** | [Junior Quantitative Researcher - Prediction Markets](https://www.akunacapital.com/careers/job/7863348/?gh_jid=7863348&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Akuna Capital University** | [Quantitative Development &amp; Strategy Intern](https://www.akunacapital.com/careers/job/8021481/?gh_jid=8021481&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer 2027 | review required |
| **Akuna Capital University** | [Quantitative Research Intern](https://www.akunacapital.com/careers/job/8036614/?gh_jid=8036614&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer 2027 | review required |
| **Akuna Capital University** | [Software Engineer Intern - C# .NET Desktop](https://www.akunacapital.com/careers/job/8018886/?gh_jid=8018886&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **Akuna Capital University** | [Software Engineer Intern - C++](https://www.akunacapital.com/careers/job/8018847/?gh_jid=8018847&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **Akuna Capital University** | [Software Engineer Intern - Full Stack Web](https://www.akunacapital.com/careers/job/8018893/?gh_jid=8018893&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **Akuna Capital University** | [Software Engineer Intern - Python](https://www.akunacapital.com/careers/job/8018853/?gh_jid=8018853&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
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
| **Citadel Securities** | [Quantitative Trader – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-us-miami/?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Citadel Securities** | [Quantitative Trader – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-us-new-york/?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
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
| **Five Rings Capital** | [Quantitative Researcher Intern 🎓](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349219008?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Ambiguous | review required |
| **Five Rings Capital** | [Quantitative Trader Intern - Quantitative Trader](https://job-boards.greenhouse.io/fiveringsllc/jobs/5139668008?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer 2027 | review required |
| **Five Rings Capital** | [Software Developer Intern - Software Developer](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349707008?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
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
| **IMC Trading** | [Machine Learning Research Intern - Summer 2027 - Amsterdam](https://job-boards.eu.greenhouse.io/imc/jobs/4912874101) | Quant / Finance | Netherlands | Summer 2027 | review required |
| **IMC Trading** | [Machine Learning Research Intern - Summer 2027 - Sydney](https://job-boards.eu.greenhouse.io/imc/jobs/4956547101) | Quant / Finance | Australia | Summer 2027 | review required |
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
| **Jump Trading** | [Campus C++ Software Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027860) | Quant / Finance | China | Unknown | review required |
| **Jump Trading** | [Campus Crypto Researcher \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7362318) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus Data Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8002998) | Quant / Finance | US | Unknown | review required |
| **Jump Trading** | [Campus Data Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7975008) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus FPGA Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7974391) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus ML Research Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7977145) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus Python Software Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027923) | Quant / Finance | China | Unknown | review required |
| **Jump Trading** | [Campus Python Software Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027955) | Quant / Finance | Singapore | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Researcher \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8010307) | Quant / Finance | Netherlands | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Researcher \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027939) | Quant / Finance | Singapore | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Researcher \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027900) | Quant / Finance | China / Hong Kong | Winter/Spring 2027 | review required |

_360 more are in [tracker.csv](tracker.csv)._

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
