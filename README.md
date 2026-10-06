# 🎯 Universal Academic & Career Tracker — Internships · Research · PhD · New Grad

<p align="center">
  <a href="https://abyyworld.github.io/internship-tracker/"><img alt="Open the tracker — 3965 open postings" src="https://img.shields.io/badge/Open%20the%20tracker-3965%20open%20postings-1f6feb?style=for-the-badge&labelColor=0d1117"></a>
  <a href="https://abyyworld.github.io/internship-tracker/studio.html"><img alt="Tailor my CV — in the browser" src="https://img.shields.io/badge/Tailor%20my%20CV-in%20the%20browser-2ea043?style=for-the-badge&labelColor=0d1117"></a>
</p>

<p align="center"><b><a href="https://abyyworld.github.io/internship-tracker/">https://abyyworld.github.io/internship-tracker/</a></b><br>
Search and filter every posting, then tailor your CV for one — in the browser, on a phone, with nothing to install.</p>

> Last verified run: **2026-10-06** · **3965 verified-open postings** · **172 research / PhD / postdoc positions**

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
| Verified-open postings | 3965 |
| Roles discovered today | 175 |
| New verified postings | 175 |
| Research / PhD / postdoc positions | 172 |
| Elite tier | 243 |
| High tier | 329 |
| Eligibility still needs review | 3957 |
| Deadlines within 10 days | 1 |

**By category:** Software Engineering 2272 · Quant / Finance 306 · Robotics & Embodied AI 293 · Data 281 · AI / ML 228 · Security 178 · Hardware / EE 175 · Systems & Infra 147 · Computational Science 84 · HCI / XR 1

**By region:** US 3100 · Unknown 170 · UK 153 · Canada 147 · Singapore 51 · Remote 43 · France 37 · Germany 33 · US / Austria 23 · South Korea 19 · Hong Kong 17 · Netherlands 15 · Brazil 12 · China 10 · New Zealand 10 · India 9 · US / Australia 9 · Spain 8 · Switzerland 8 · Mexico 8 · US / UK 7 · US / Canada 5 · Taiwan 5 · Global 5 · Ireland 4 · Serbia 4 · US / Netherlands 4 · Italy 4 · Singapore / China / Hong Kong 3 · US / France 3 · Poland 3 · US / Italy 3 · Singapore / Hong Kong 3 · UK / Ireland 2 · Australia 2 · China / Hong Kong 2 · US / Global 2 · Singapore / China / Hong Kong / Australia 2 · US / UAE 2 · UAE 2 · Austria 2 · France / Japan / Hong Kong 1 · US / France / Singapore / Hong Kong 1 · Denmark 1 · UK / Australia 1 · Sweden 1 · US / Canada / UK 1 · Portugal 1 · US / Europe 1 · UK / France 1 · France / Switzerland / UAE 1 · Netherlands / France / Switzerland / UAE 1 · France / Switzerland 1 · US / UK / Germany 1 · US / Poland 1

**By degree evidence:** Unknown 3240 · Undergraduate eligible 337 · Advanced/unknown 213 · PhD 130 · Masters 45

## Newly opened (175)

| Company | Role | Category | Region | Term | Eligibility |
|--|--|--|--|--|--|
| **Cloudflare** | [People Analytics Data Engineering Intern \(Winter/Spring 2027\)](https://boards.greenhouse.io/cloudflare/jobs/8241790?gh_jid=8241790) | Data | Unknown | Winter/Spring 2027 | review required |
| **Nuro** | [Software Engineer New Grad - Routing](https://nuro.ai/careersitem?gh_jid=8248317&utm_source=Simplify&ref=Simplify) | Robotics &amp; Embodied AI | US | Ambiguous | review required |
| **🔥 AMD** | [AI Training Systems and Performance Engineer Intern/Co-op 🎓](https://careers.amd.com/jobs/93332?icims=1&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **🔥 AMD** | [PhD Agentic/ML System Co-op 🎓](https://careers.amd.com/jobs/91767?icims=1&utm_source=Simplify&ref=Simplify) | Software Engineering | US | Ambiguous | review required |
| **🔥 AMD** | [PhD Large Language Model Engineer Co-op 🎓](https://careers.amd.com/jobs/91764?icims=1&utm_source=Simplify&ref=Simplify) | AI / ML | US | Ambiguous | review required |
| **🔥 Cloudflare** | [Software Engineer Intern](https://boards.greenhouse.io/cloudflare/jobs/8245211?utm_source=Simplify&ref=Simplify) | Software Engineering | UK | 2027 | review required |
| **🔥 Figma** | [AI Applied Scientist Intern 🎓](https://boards.greenhouse.io/figma/jobs/6207801004?utm_source=Simplify&ref=Simplify) | Software Engineering | US | 2027 | review required |
| **🔥 Waymo** | [MS/PhD, ML Systems &amp; Behavior Discovery Intern 🎓](https://careers.withwaymo.com/jobs?gh_jid=8257159&utm_source=Simplify&ref=Simplify) | Robotics &amp; Embodied AI | US | Summer 2027 | review required |
| **🔥 Waymo** | [Software Engineer Intern - MS/PhD - Eval Data Infra 🎓](https://careers.withwaymo.com/jobs?gh_jid=8257205&utm_source=Simplify&ref=Simplify) | Robotics &amp; Embodied AI | US | Summer 2027 | review required |
| **Bedrock Robotics** | [2027 Internship Test Operations Engineer](https://jobs.ashbyhq.com/bedrock-robotics/66deac22-a655-413e-8f46-3d956860619a) | Robotics &amp; Embodied AI | US | 2027 | review required |
| **American Family Insurance Group** | [Data Analyst Intern](https://amfam.wd1.myworkdayjobs.com/AmFamGroupInternCareers/job/WI-Madison/Summer-2027-Intern---Data-Analyst_R39615?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |
| **Americanpublichealthassociation** | [Climate, Health and Equity Internship: 2027 spring term](https://job-boards.greenhouse.io/americanpublichealthassociation/jobs/4434254009) | Computational Science | US | Spring 2027 | review required |
| **Anduril** | [2027 Quality &amp; Test Engineer Intern](https://boards.greenhouse.io/andurilindustries/jobs/5257674007?gh_jid=5257674007) | Robotics &amp; Embodied AI | US | 2027 | review required |
| **Anduril** | [2027 Reliability Engineer Intern](https://boards.greenhouse.io/andurilindustries/jobs/5257682007?gh_jid=5257682007) | Robotics &amp; Embodied AI | US | 2027 | review required |
| **Anduril** | [2027 Systems Engineer Intern](https://boards.greenhouse.io/andurilindustries/jobs/5257690007?gh_jid=5257690007) | Robotics &amp; Embodied AI | US | 2027 | review required |
| **Anduril** | [Winter 2027 Quality &amp; Test Engineer Co-op](https://boards.greenhouse.io/andurilindustries/jobs/5257571007?gh_jid=5257571007) | Robotics &amp; Embodied AI | US | Winter 2027 | review required |
| **Anduril** | [Winter 2027 Reliability Engineer Co-op](https://boards.greenhouse.io/andurilindustries/jobs/5257693007?gh_jid=5257693007) | Robotics &amp; Embodied AI | US | Winter 2027 | review required |
| **Arc** | [Electrical Integration Engineering Intern](https://job-boards.greenhouse.io/arcboatcompany/jobs/5442838008) | Software Engineering | US | None | review required |
| **Arc** | [Mechanical Engineering Intern - Powertrain](https://job-boards.greenhouse.io/arcboatcompany/jobs/5442958008) | Software Engineering | US | None | review required |
| **Arc** | [Powertrain Electrical Engineer Intern](https://job-boards.greenhouse.io/arcboatcompany/jobs/5443971008) | Hardware / EE | US | None | review required |
| **Arc** | [Vehicle Controls Engineering Intern](https://job-boards.greenhouse.io/arcboatcompany/jobs/5442902008) | Software Engineering | US | None | review required |
| **Arondite** | [Software Engineer Intern](https://apply.workable.com/arondite/j/D3211449EF/apply?utm_source=Simplify&ref=Simplify) | Software Engineering | UK | Ambiguous | review required |
| **Artefact** | [R&amp;D Intern - Fairness in Deep Learning - Paris](https://job-boards.greenhouse.io/artefact/jobs/8870446002) | AI / ML | France | None | review required |
| **Artefactlinkedin** | [R&amp;D Intern - Fairness in Deep Learning - Paris](https://job-boards.greenhouse.io/artefactlinkedin/jobs/8870459002) | AI / ML | France | None | review required |
| **Astera Labs** | [ATE Engineer Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731409005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Advanced DV Engineer Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731412005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Applied AI Engineer Intern \(Silicon Engineering\)](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4727602005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Applied AI Intern \(Non-Silicon\)](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4728357005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Applied AI New Grad - Non Silicon](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731594005?utm_source=Simplify&ref=Simplify) | Software Engineering | US | 2027 | review required |
| **Astera Labs** | [DFT Engineering Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4728387005) | Software Engineering | US / Canada | None | review required |
| **Astera Labs** | [Data Analyst Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731996005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Data Analyst New Grad](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731994005?utm_source=Simplify&ref=Simplify) | Software Engineering | US | 2027 | review required |
| **Astera Labs** | [Data Analytics Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731995005) | Data | US | None | review required |
| **Astera Labs** | [Design Architecture Engineer Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731413005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Design Engineering Intern \(CCE2\)](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4727655005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Design Verification Engineer Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4722012005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Digital Design Engineer Intern \(Toronto\)](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731399005) | Software Engineering | Canada | None | review required |
| **Astera Labs** | [Digital Design Engineering Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731407005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Electrical Validation Engineer Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4724534005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Emulation Engineering Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731394005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Engineering Ops Technology Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731411005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Field Applications Engineer Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4729786005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Firmware Engineer Intern \(Ottawa\)](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731406005) | Hardware / EE | Canada | None | review required |
| **Astera Labs** | [Firmware Engineering Intern \(Optical\)](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4738565005) | Hardware / EE | US | None | review required |
| **Astera Labs** | [Hardware Design Engineer Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4728560005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Hardware Electrical Validation Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4740145005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Hardware Lab Engineer Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4729020005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Hardware Test/Mechanical Engineer Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4724114005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Lab Strategy Engineer Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731583005) | Software Engineering | US | None | review required |
| **Astera Labs** | [NPI Engineer Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4728552005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Packaging Automation &amp; Data Engineering Intern \(Spring 2027 - January Start\)](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4738127005) | Software Engineering | US | Spring 2027 | review required |
| **Astera Labs** | [Packaging Engineer Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4728619005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Performance Engineering Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4726727005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Physical Design Engineer Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4727569005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Physical Design Engineer Intern \(Toronto\)](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731401005) | Software Engineering | Canada | None | review required |
| **Astera Labs** | [Platform Software Diagnostics Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4724492005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Platform Solutions Engineer Intern \(CE\)](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731587005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Platform Solutions Product Management Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731590005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Product Applications Engineer Intern \(Leo\)](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4732216005) | Software Engineering | US | None | review required |
| **Astera Labs** | [Product Applications Engineer Intern \(Scorpio\)](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4732364005) | Software Engineering | Unknown | None | review required |

_115 more are in [tracker.csv](tracker.csv)._

## Browse by category

Every category is listed the same way. Live geography reflects what official feeds expose today; the worldwide career-hub and academic watchlists are kept separately in [manual_checks.md](manual_checks.md).

### Software Engineering (2272 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Python Software Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018853/?gh_jid=8018853&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer \(Entry-Level\) - Python](https://www.akunacapital.com/careers/job/8013230/?gh_jid=8013230) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer Intern \(Summer 2027, Python / C++ / Full Stack / C# .NET\)](https://akunacapital.com/careers/job/8018847/) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer Intern, C# .NET Desktop](https://akunacapital.com/careers/job/8018886/?gh_jid=8018886&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer Intern, C++ 🇺🇸](https://akunacapital.com/careers/job/8018847/?gh_jid=8018847&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Akuna Capital** | [Software Engineer Intern, Full Stack Web 🇺🇸](https://akunacapital.com/careers/job/8018893/?gh_jid=8018893&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Akuna Capital University** | [Entry Level Software Engineer - C++](https://www.akunacapital.com/careers/job/8013085/?gh_jid=8013085&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
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
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/7991196) | Canada |  | unknown | unknown |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/8020364) | Netherlands |  | unknown | unknown |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/7942281) | UK |  | unknown | unknown |
| **DRW** | [Software Developer Intern \(C++\)](https://job-boards.greenhouse.io/drweng/jobs/8014910) | Singapore |  | unknown | unknown |
| **DRW** | [Software Developer Intern - Industrial Placement](https://job-boards.greenhouse.io/drwuniversityjobs/jobs/7364884) | UK |  | unknown | unknown |
| **Five Rings** | [Software Developer Intern 🇺🇸](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349707008?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **G-Research** | [Software Engineer Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Software-Engineering-Intern_R3746?utm_source=Simplify&ref=Simplify) | UK | research | unknown | unknown |
| **Google** | [Software Engineering Intern](https://www.google.com/about/careers/applications/jobs/results/85564713261245126-software-engineering-intern-bs-summer-2027?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Google** | Software Engineering Intern, 2027 | UK |  | unknown | unknown |
| **IMC** | [Software Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823924101) | US |  | unknown | unknown |
| **Jane Street** | [Fundamental Research Analyst Intern](https://www.janestreet.com/join-jane-street/position/8347286002/?utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **Jane Street** | [Linux Engineer Intern](https://www.janestreet.com/join-jane-street/position/8626260002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Network Engineer Intern](https://www.janestreet.com/join-jane-street/position/8620793002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Software Engineer Intern](https://www.janestreet.com/join-jane-street/position/8599644002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Tools and Compilers Research and Development Intern](https://www.janestreet.com/join-jane-street/position/5869205002/?utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **Jane Street** | [Windows Engineer Intern](https://www.janestreet.com/join-jane-street/position/8628843002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Man Group** | [Investment Risk 2027 Summer Internship](https://job-boards.eu.greenhouse.io/mangroup/jobs/4988792101) | UK |  | unknown | unknown |
| **Man Group** | [2027 Summer Technology Internship Programme](https://job-boards.eu.greenhouse.io/mangroup/jobs/4978934101) | UK |  | unknown | unknown |
| **Man Group** | 2027 Summer Technology Internship Programme | UK |  | unknown | unknown |
| **Man Group** | [Technology Summer Internship](https://job-boards.eu.greenhouse.io/mangroup/jobs/4978895101) | Unknown |  | unknown | unknown |
| **Marshall Wace** | [Technology Intern - 2027 - Singapore](https://job-boards.greenhouse.io/mwinternshipprogram/jobs/8608327002) | Singapore |  | unknown | unknown |
| **Marshall Wace** | [Technology Intern - Hong Kong - 2027](https://job-boards.greenhouse.io/mwinternshipprogram/jobs/8608328002) | Hong Kong |  | unknown | unknown |
| **Marshall Wace** | [Technology Intern - London - 2027](https://job-boards.greenhouse.io/mwinternshipprogram/jobs/8598324002) | UK |  | unknown | unknown |

_2232 more are in [tracker.csv](tracker.csv)._

### Quant / Finance (306 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Quantitative Development &amp; Strategy Intern 🇺🇸](https://akunacapital.com/careers/job/8021481/?gh_jid=8021481&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Akuna Capital** | [Quantitative Research Intern 🇺🇸](https://akunacapital.com/careers/job/8036614/?gh_jid=8036614&utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **Akuna Capital University** | [Junior Quantitative Developer &amp; Strategist](https://www.akunacapital.com/careers/job/8016687/?gh_jid=8016687&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Akuna Capital University** | [Junior Quantitative Researcher](https://www.akunacapital.com/careers/job/8036541/?gh_jid=8036541&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Akuna Capital University** | [Junior Quantitative Researcher - Prediction Markets](https://www.akunacapital.com/careers/job/7863348/?gh_jid=7863348&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
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
| **Five Rings** | [Quantitative Trader Intern \(Summer 2027\)](https://job-boards.greenhouse.io/fiveringsllc/jobs/5139668008) | US |  | unknown | unknown |
| **Five Rings Capital** | [Summer Intern 2027 - Quantitative Researcher \(PhD\)](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349219008) | US | phd-position | unknown | unknown |
| **Five Rings Capital** | [Trading Operations Engineer Intern](https://job-boards.greenhouse.io/fiveringsllc/jobs/5420708008?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Hudson River Trading** | [Algorithm Developer New Grad - Quant Researcher](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8052050&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Hudson River Trading** | [Data Scientist Intern](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8257369&utm_source=Simplify&ref=Simplify) | US / UK |  | unknown | unknown |
| **Hudson River Trading** | [Software Engineer Intern](https://www.hudsonrivertrading.com/hrt-job/software-engineering-internship-c-or-python-summer-2027/?gh_src=&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **IMC** | [Quantitative Research Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4907399101) | US | research | unknown | unknown |
| **IMC Trading** | [Deep Learning Research Intern - Summer 2027 - Amsterdam](https://job-boards.eu.greenhouse.io/imc/jobs/4912874101) | Netherlands | research | unknown | unknown |
| **IMC Trading** | [Graduate Quantitative Researcher \(PhD\)](https://job-boards.eu.greenhouse.io/imc/jobs/4912325101) | US | phd-position | unknown | unknown |
| **IMC Trading** | [Hardware Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4927149101) | Netherlands |  | unknown | unknown |
| **IMC Trading** | [Hardware Machine Learning PhD Research Internship](https://job-boards.eu.greenhouse.io/imc/jobs/4975945101) | US | research,phd-position | unknown | unknown |
| **IMC Trading** | [Machine Learning Research Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4907430101) | US | research | unknown | unknown |
| **IMC Trading** | [Machine Learning Research Intern - Summer 2027 - Sydney](https://job-boards.eu.greenhouse.io/imc/jobs/4956547101) | Australia | research | unknown | unknown |
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
| **Jane Street** | [Quantitative Trader Intern](https://www.janestreet.com/join-jane-street/position/8617344002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Sales and Trading Intern](https://www.janestreet.com/join-jane-street/position/8347385002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |

_266 more are in [tracker.csv](tracker.csv)._

### Robotics & Embodied AI (293 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Amazon** | [Robotics - Software Development Engineer Intern/Co-op](https://www.amazon.jobs/en/jobs/3136266/robotics-software-development-engineer-intern-co-op-2026?no_int_redir=1&utm_source=github-vansh-ouckah) | US | robot-software | unknown | unknown |
| **🔥 Amazon** | [Software Development Engineer Intern - Robotics](https://amazon.jobs/en/jobs/10529525/software-development-engineer-intern-robotics-2027?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [Research Scientist New Grad - Robotics Research 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-WA-Seattle/Research-Scientist--Robotics-Research----PhD-New-College-Grad-2026_JR2011473?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Nuro** | [Software Engineer New Grad - Routing](https://nuro.ai/careersitem?gh_jid=8248317&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | private-scaleup | private company; verify offer |
| **Nuro** | [Software Engineer, AI Platform - Intern](https://nuro.ai/careersitem?gh_jid=7351061) | US | autonomous vehicles | private-scaleup | private company; verify offer |
| **Nuro** | [Software Engineer, AI Platform - New Grad](https://nuro.ai/careersitem?gh_jid=7351066) | US | autonomous vehicles | private-scaleup | private company; verify offer |
| **Waymo** | [2027 Summer Intern, BS/MS, Software Engineer, RO Performance team, Release Evaluation \(Simulation\)](https://careers.withwaymo.com/jobs?gh_jid=8214729) | Poland | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, MS, Software Engineering, Behavior Test](https://careers.withwaymo.com/jobs?gh_jid=8174504) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, MS/PhD, Machine Learning, Driver Refinement Foundations](https://careers.withwaymo.com/jobs?gh_jid=8243556) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Machine Learning, Computer Vision](https://careers.withwaymo.com/jobs?gh_jid=8193295) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Perception Systems Engineering: Pedestrian Detection Precision](https://careers.withwaymo.com/jobs?gh_jid=8234670) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Research, World Action Model](https://careers.withwaymo.com/jobs?gh_jid=8243732) | US | autonomous vehicles | established | company-dependent |
| **Waymo** | [2027 Summer Intern, PhD, Software Engineer, Simulation](https://careers.withwaymo.com/jobs?gh_jid=8227640) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [AI-driven ML Performance Engineering Intern - MS/PhD 🎓](https://careers.withwaymo.com/jobs?gh_jid=8248060&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Applied Research Scientist – New Grad - Perception Large Language Model/Vision-Language Model - PhD 🎓](https://careers.withwaymo.com/jobs?gh_jid=7488508&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Data Science Intern - PhD 🎓](https://careers.withwaymo.com/jobs?gh_jid=8221956&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Embedded Intern - Software Engineer](https://careers.withwaymo.com/jobs?gh_jid=8221198&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Human Behavior Analytics Intern - Safety Research](https://careers.withwaymo.com/jobs?gh_jid=8197899&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [MS/PhD Intern - Sim-Realism ML Infrastructure 🎓](https://careers.withwaymo.com/jobs?gh_jid=8205680&utm_source=Simplify&ref=Simplify) | UK | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [MS/PhD, ML Systems &amp; Behavior Discovery Intern 🎓](https://careers.withwaymo.com/jobs?gh_jid=8257159&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Machine Learning Engineer Intern - MS/PhD - Simulator Realism Evaluation 🎓](https://careers.withwaymo.com/jobs?gh_jid=8214350&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Machine Learning Engineer Intern - MS/PhD 🎓](https://careers.withwaymo.com/jobs?gh_jid=8223735&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Machine Learning Engineer Intern - Road Understanding 🎓](https://careers.withwaymo.com/jobs?gh_jid=8224746&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Machine Learning Intern - Computer Vision 🎓](https://careers.withwaymo.com/jobs?gh_jid=8202025&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Machine Learning Research Intern - Planning/Prediction 🎓](https://careers.withwaymo.com/jobs?gh_jid=8237997&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Perception Intern - Evaluation 🎓](https://careers.withwaymo.com/jobs?gh_jid=8248327&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Perception Intern - Multiple Teams 🎓](https://careers.withwaymo.com/jobs?gh_jid=8227411&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Planner Machine Learning Intern 🎓](https://careers.withwaymo.com/jobs?gh_jid=8234876&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Product Data Science Intern 🎓](https://careers.withwaymo.com/jobs?gh_jid=8199365&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Software Engineer Intern - Driver Refinement Foundations](https://careers.withwaymo.com/jobs?gh_jid=8224900&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Software Engineer Intern - MS/PhD - Eval Data Infra 🎓](https://careers.withwaymo.com/jobs?gh_jid=8257205&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Software Engineer Intern - MS/PhD - Onboard Developer Platform 🎓](https://careers.withwaymo.com/jobs?gh_jid=8240198&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Software Engineer Intern - MS/PhD - Simulation 🎓](https://careers.withwaymo.com/jobs?gh_jid=8221851&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Software Engineer Intern - MS/PhD - Systems Intelligence &amp; Machine Learning 🎓](https://careers.withwaymo.com/jobs?gh_jid=8233746&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Software Engineer Intern - MS/PhD 🎓](https://careers.withwaymo.com/jobs?gh_jid=8224729&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Software Engineer Intern - Simulation Evaluation ML Model 🎓](https://careers.withwaymo.com/jobs?gh_jid=8221795&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Software Engineering Intern - Commercialization](https://careers.withwaymo.com/jobs?gh_jid=8198218&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Software Engineering Intern - Labeling](https://careers.withwaymo.com/jobs?gh_jid=8238525&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Software Engineering Intern - MS/PhD - Sys Intel &amp; ML 🎓](https://careers.withwaymo.com/jobs?gh_jid=8234161&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **🔥 Waymo** | [Software Engineering Intern - Multiple Teams 🎓](https://careers.withwaymo.com/jobs?gh_jid=8208465&utm_source=Simplify&ref=Simplify) | UK | autonomous vehicles | established | company-dependent |

_253 more are in [tracker.csv](tracker.csv)._

### Data (281 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Jane Street** | [Data Engineer Intern](https://www.janestreet.com/join-jane-street/position/8631973002/?utm_source=github-vansh-ouckah) | US | data-eng | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Data Platform/Analytics](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922931&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **🔥 Google** | [Business Data Scientist Intern 🎓](https://www.google.com/about/careers/applications/jobs/results/134577198026629830?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Google** | [Data Scientist Intern - Product 🎓](https://www.google.com/about/careers/applications/jobs/results/119184035237765830?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Google** | [Data Scientist Research Intern - PhD 🎓](https://www.google.com/about/careers/applications/jobs/results/89965613241246406?utm_source=Simplify&ref=Simplify) | US | research,phd-position | unknown | unknown |
| **Cloudflare** | [People Analytics Data Engineering Intern \(Winter/Spring 2027\)](https://boards.greenhouse.io/cloudflare/jobs/8241790?gh_jid=8241790) | Unknown | data-eng | unknown | unknown |
| **Coinbase** | [Internal Audit Analytics Intern](https://www.coinbase.com/careers/positions/8221238?gh_jid=8221238) | US |  | unknown | unknown |
| **Figma** | [Data Engineer Intern \(2027\)](https://boards.greenhouse.io/figma/jobs/6178851004?gh_jid=6178851004) | US | data-eng | unknown | unknown |
| **Figma** | [Data Scientist, Core Data -  PhD \(2026\)](https://boards.greenhouse.io/figma/jobs/5976930004?gh_jid=5976930004) | US | phd-position | unknown | unknown |
| **Stripe** | [PhD Data Scientist, Intern](https://stripe.com/jobs/search?gh_jid=8194283) | US | phd-position | unknown | unknown |
| **Stripe** | [PhD Data Scientist, Intern](https://stripe.com/jobs/search?gh_jid=8194285) | Canada | phd-position | unknown | unknown |
| **🔥 Coinbase** | [Analytics Engineer Intern](https://boards.greenhouse.io/embed/job_app?token=8175471&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Coinbase** | [Data Engineer Intern](https://boards.greenhouse.io/embed/job_app?token=8175459&utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **🔥 Coinbase** | [Data Science Intern - Strategy, Execution, &amp; Analytics - Platform](https://boards.greenhouse.io/embed/job_app?token=8175462&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Coinbase** | [People Analytics Intern](https://boards.greenhouse.io/embed/job_app?token=8175517&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Affinius Capital** | [Data Scientist Intern](https://careers-affiniuscapital.icims.com/jobs/2284/summer-2027-data-scientist-intern/job) | US |  | unknown | unknown |
| **Agoda** | [Associate Data Analyst \(New Graduate, Thai Speaking\) \(Marketing Analytics, Bangkok Based\)](https://job-boards.greenhouse.io/agoda/jobs/8194692) | Unknown |  | unknown | unknown |
| **Airgarage** | [Research Associate](https://jobs.ashbyhq.com/airgarage/279174e8-a271-4c07-b904-3d026dae76a8) | US | controls,research | unknown | unknown |
| **Altar'd State** | [IT Analytics Intern](https://standoutforgood.wd12.myworkdayjobs.com/StandOutForGood/job/Knoxville-TN/Spring-2027-IT-Analytics-Intern_SOSJ12499?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012782?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012784?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012783?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Analytics Intern - US Consumer Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26011607?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Engineer 1 - Enterprise Technology Services](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26013286?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **American Express** | [Data Engineer Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012781?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **American Express** | [Data Engineer Intern - Enterprise Technology Services 🎓](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26012764?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **American Family Insurance Group** | [Internal Data and Analytics Intern - Summer 2027](https://amfam.wd1.myworkdayjobs.com/AmFamGroupInternCareers/job/WI-Madison/Internal-Data-and-Analytics-Intern---Summer-2027_R39401?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Amgen** | [Data Scientist Intern](https://amgen.wd1.myworkdayjobs.com/careers/job/United-States---Remote/Undergrad-Intern---Data-Scientist---Amgen-s-Technology---Medical-Organizations--Summer-2027-_R-255704?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Amgen** | [Data Scientist Intern - Amgen’s Technology &amp; Medical Organizations](https://amgen.wd1.myworkdayjobs.com/careers/job/United-States---Remote/Grad-Intern---Data-Scientist---Amgen-s-Technology---Medical-Organizations--Summer-2027-_R-255722?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Aon** | [Data &amp; Analytics Associate - Early Careers](https://jobs.aon.com/jobs/105952?icims=1&utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Applied Materials** | [Data Scientist New Grad - Bachelor's/Master's 🎓](https://amat.wd1.myworkdayjobs.com/External/job/AustinTX/Data-Scientist-New-College-Grad--Bachelor-s-Master-s--Austin--TX-_R2627684?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Artefact** | [Data Scientist Intern \(2024\)](https://job-boards.greenhouse.io/artefact/jobs/8564128002) | Unknown |  | unknown | unknown |
| **Artefact** | [Data Scientist Intern - Paris](https://job-boards.greenhouse.io/artefact/jobs/8785269002) | France |  | unknown | unknown |
| **Artefact** | [Intern Data Engineer](https://job-boards.greenhouse.io/artefact/jobs/4593319002) | China | data-eng | unknown | unknown |
| **Artefactlinkedin** | [Data Scientist Intern - Paris](https://job-boards.greenhouse.io/artefactlinkedin/jobs/8785636002) | France |  | unknown | unknown |
| **Artefactlinkedin** | [Intern Data Engineer Brazil](https://job-boards.greenhouse.io/artefactlinkedin/jobs/7306842002) | Brazil | data-eng | unknown | unknown |
| **Artefactlinkedin** | [Intern Data Scientist Brazil](https://job-boards.greenhouse.io/artefactlinkedin/jobs/7322632002) | Brazil |  | unknown | unknown |
| **Arthur J. Gallagher &amp; Co.** | [Data Analytics Intern](https://jobs.ajg.com/jobs/57701?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Astera Labs** | [Data Analytics Intern](https://job-boards.greenhouse.io/asteraearlycareer2027/jobs/4731995005) | US |  | unknown | unknown |
| **Audaxgroup** | [Data Analytics Co-Op](https://job-boards.greenhouse.io/audaxgroup/jobs/4722880005) | US |  | unknown | unknown |

_241 more are in [tracker.csv](tracker.csv)._

### AI / ML (228 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Jane Street** | [Machine Learning Engineer Intern](https://www.janestreet.com/join-jane-street/position/8611307002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Machine Learning Researcher Intern](https://www.janestreet.com/join-jane-street/position/8384490002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, AI/ML &amp; LLM](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922929&utm_source=github-vansh-ouckah) | US | llm | unknown | unknown |
| **Mistral AI** | [Applied AI, Forward Deployed Machine Learning Engineer - \(Internship\)](https://jobs.ashbyhq.com/mistral.ai/fcdb8407-20b9-4179-81b6-f2ca2c79a39b) | France | controls,nlp | unknown | unknown |
| **Point72** | [Machine Learning Researcher - Intern](https://boards.greenhouse.io/point72/jobs/7302611002?gh_jid=7302611002) | US |  | unknown | unknown |
| **Two Sigma** | [AI Research Scientist Intern \(MS / PhD\)](https://careers.twosigma.com/careers/JobDetail/New-York-New-York-United-States-AI-Research-Scientist-Internship-2027-Summer/14022) | US | research,phd-position | unknown | unknown |
| **🔥 Amazon** | [Machine Learning Systems Software Development Engineer Intern - Annapurna Labs](https://amazon.jobs/en/jobs/10538066/ml-systems-software-development-engineer-intern-annapurna-labs-2027?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **🔥 NVIDIA** | [Research Scientist New Grad - Circuits 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Research-Scientist--Circuits---New-College-Grad-2026_JR2010010?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **🔥 NVIDIA** | [Research Scientist New Grad - Electronic Design Automation 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Research-Scientist--Electronic-Design-Automation---New-College-Grad-2026_JR2012979?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
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
| **Qualcomm** | [Machine Learning Compiler &amp; Performance Engineering Intern - Systems](https://qualcomm.eightfold.ai/careers/job/446721064018?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Qualcomm** | [Machine Learning Engineer New Grad - AI Processors - Machine Learning Engineering](https://qualcomm.eightfold.ai/careers/job/446721063770?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Sierra** | [Software Engineer Intern, Agent \(Summer 2027\)](https://jobs.ashbyhq.com/Sierra/34b31b67-268c-4270-b48f-72e59064c96e/application?embed=true&utm_source=Simplify&ref=Simplify) | US | llm,funded | unknown | posting mentions equity |
| **Sierra** | [Software Engineer, Agent \(New Grad 2027\)](https://jobs.ashbyhq.com/Sierra/149f368c-52d5-408f-ba26-ad888f318a00/application?embed=true&utm_source=Simplify&ref=Simplify) | US | autonomy,llm,research,funded | unknown | posting mentions equity |
| **Sierra** | [Software Engineer, Agent \(New Grad 2027\)](https://jobs.ashbyhq.com/sierra/79953d72-60d4-43e0-8c8c-6eccda422dce) | Singapore | autonomy,llm,research,funded | unknown | posting mentions equity |
| **Snowflake** | [AI Research Scientist, New Grad – Agents &amp; Reinforcement Learning](https://jobs.ashbyhq.com/snowflake/1bad12df-f443-426f-9d09-e96fc780d698/application?utm_source=Simplify&ref=Simplify) | US | autonomy,llm,rl,data-eng,infra,research,phd-position | unknown | unknown |
| **🔥 AMD** | [AI Research Infrastructure – Reinforcement Learning Post-Training Intern 🎓](https://careers.amd.com/jobs/90950?icims=1&utm_source=Simplify&ref=Simplify) | US | rl,infra,research | unknown | unknown |
| **🔥 AMD** | [AI Research Intern - Reinforcement Learning and LLM Post-Training 🎓](https://careers.amd.com/jobs/91013?icims=1&utm_source=Simplify&ref=Simplify) | US | llm,rl,research | unknown | unknown |
| **🔥 AMD** | [Generative AI and Reinforcement Learning Research Intern 🎓](https://careers.amd.com/jobs/90910?icims=1&utm_source=Simplify&ref=Simplify) | US | rl,research | unknown | unknown |
| **🔥 AMD** | [Machine Learning Intern/Co-op - Artificial Intelligence 🎓](https://careers.amd.com/jobs/91181?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Machine Learning Intern/Co-op - Machine Learning - Artificial Intelligence](https://careers.amd.com/jobs/90892?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Machine Learning Intern/Co-op - Multiple Teams](https://careers.amd.com/jobs/91170?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Machine Learning System Engineering Intern/Co-op 🎓](https://careers.amd.com/jobs/92342?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Machine Learning/Artificial Intelligence Intern/Co-op](https://careers.amd.com/jobs/91363?icims=1&utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **🔥 AMD** | [PhD Large Language Model Engineer Co-op 🎓](https://careers.amd.com/jobs/91764?icims=1&utm_source=Simplify&ref=Simplify) | US | llm,phd-position | unknown | unknown |
| **🔥 Coinbase** | [Machine Learning Engineer Intern 🎓](https://boards.greenhouse.io/embed/job_app?token=8175441&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |

_188 more are in [tracker.csv](tracker.csv)._

### Security (178 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Jane Street** | [Cybersecurity Analyst Intern](https://www.janestreet.com/join-jane-street/position/8632723002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Security &amp; Identity](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922930&utm_source=github-vansh-ouckah) | US | security | unknown | unknown |
| **Mistral AI** | [Applied Scientist  \(Internship\)](https://jobs.ashbyhq.com/mistral.ai/de46ba8b-00cb-4618-83df-66e15a78434e) | France | multimodal,research,phd-position | unknown | unknown |
| **Mistral AI** | [Applied Scientist \(Internship in Paris or London\)](https://jobs.ashbyhq.com/mistral.ai/60ab6a5e-9b02-4ae7-a0fb-4c7d9ec0fdf8) | South Korea | multimodal,research,phd-position | unknown | unknown |
| **Cohere** | [Machine Learning Intern/Co-op  \(Winter 2027\)](https://jobs.ashbyhq.com/cohere/36d1f52f-8270-4652-adf5-5303a0ff341b) | Canada | computer-vision,nlp,security,research,funded | unknown | unknown |
| **Cohere** | [Software Engineer Intern \(Winter 2027\)](https://jobs.ashbyhq.com/cohere/8c035d3d-081d-4c8a-914a-72f4efaad254) | Canada | autonomy,computer-vision,nlp,data-eng,infra,security,research,funded | unknown | unknown |
| **Harvey** | [Software Engineer, New Grad \(2027\)](https://jobs.ashbyhq.com/harvey/b0996df6-6b6e-42be-a4f9-0084536068f5/application?embed=true&utm_source=Simplify&ref=Simplify) | US | infra,security,research | unknown | unknown |
| **Palantir** | [Forward Deployed Infrastructure Engineer, Internship - US Government](https://jobs.lever.co/palantir/3db7e40a-28e0-4ad1-96c5-93de5bc96aa9) | US | computer-vision,infra,distributed,security | unknown | unknown |
| **Palantir** | [Forward Deployed Infrastructure Engineer, Internship - US Government](https://jobs.lever.co/palantir/8f362a1f-1eff-4327-94c1-ff46e2101c69) | US | computer-vision,infra,distributed,security | unknown | unknown |
| **Palantir** | [Forward Deployed Infrastructure Engineer, Internship - US Government](https://jobs.lever.co/palantir/cf5f44ff-1b0b-4752-bcd4-2dc88798f25b) | US | computer-vision,infra,distributed,security | unknown | unknown |
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

_138 more are in [tracker.csv](tracker.csv)._

### Hardware / EE (175 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Hardware Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018880/?gh_jid=8018880&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **DRW** | [FPGA Intern](https://www.drw.com/work-at-drw/listings/fpga-intern-3484423?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **DRW** | [FPGA Intern](https://job-boards.greenhouse.io/drweng/jobs/8070392) | UK | hardware | unknown | unknown |
| **IMC** | [Hardware Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823945101) | US |  | unknown | unknown |
| **Jane Street** | [Hardware Engineer \(FPGA/ASIC\) Intern](https://www.janestreet.com/join-jane-street/position/8624440002/?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **Susquehanna International Group** | [FPGA Engineer Intern](https://careers-sig.icims.com/jobs/11446/job?mobile=true&needsRedirect=false&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Virtu Financial** | [2027 Internship - FPGA Engineer](https://job-boards.greenhouse.io/virtu/jobs/8638124002) | Ireland | hardware | unknown | unknown |
| **Virtu Financial** | [2027 Internship- Hardware Engineer \(FPGA\)](https://job-boards.greenhouse.io/virtu/jobs/8657286002) | US | hardware | unknown | unknown |
| **🔥 Google** | [Hardware Engineer Intern](https://www.google.com/about/careers/applications/jobs/results/122803627516404422?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Google** | [Hardware Engineer Intern - PhD 🎓](https://www.google.com/about/careers/applications/jobs/results/97352132356645574?utm_source=Simplify&ref=Simplify) | US | phd-position | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Design Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Design-Engineer---New-College-Grad-2026_JR2021534?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Floorplan Design Engineer New Grad 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Floorplan-Design-Engineer---New-College-Grad-2026_JR2024651?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Physical Design Engineer New Grad - Netlisting 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Physical-Design-Engineer--Netlisting---New-College-Grad-2026_JR2017681?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Physical Design and Timing Engineer – New College Grad 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Timing-Engineer---New-College-Grad-2026_JR2013177?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Verification Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Verification-Engineer---New-College-Grad-2026_JR2020640?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Verification Engineer – New College Grad 2026](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-TX-Austin/ASIC-Verification-Engineer---New-College-Grad-2026_JR2012573?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [Hardware Physical Design / VLSI Intern](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/NVIDIA-2027-Internships--Hardware-Physical-Design---VLSI_JR2023501?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 NVIDIA** | [Low Power ASIC Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Low-Power-ASIC-Engineer---New-College-Grad-2026_JR2017005?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Graphcore** | [Firmware Engineering Intern](https://job-boards.greenhouse.io/graphcore/jobs/8841894002) | US | hardware | unknown | unknown |
| **Qualcomm** | [Firmware Development Intern - PAL](https://qualcomm.eightfold.ai/careers/job/446721229661?utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **Qualcomm** | [Firmware Engineer Intern - Embedded Software Engineering - Embedded Firmware and SDK Development](https://qualcomm.eightfold.ai/careers/job/446721141411?utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **Qualcomm** | [Soft IP ASIC Engineer Intern](https://qualcomm.eightfold.ai/careers/job/446721302471?utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Verkada** | [Embedded Software Engineer Intern](https://job-boards.greenhouse.io/verkada/jobs/5211595007?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Verkada** | [Hardware Engineer \(Winter Co-op\)](https://job-boards.greenhouse.io/verkada/jobs/4321158007) | US |  | unknown | unknown |
| **🔥 AMD** | [ASIC Package Engineering Intern Co-op](https://careers.amd.com/jobs/91466?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [ASIC Verification Engineer Intern/Co-op](https://careers.amd.com/jobs/91207?icims=1&utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Co-op/Intern 🎓](https://careers.amd.com/jobs/90809?icims=1&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op](https://careers.amd.com/jobs/91320?icims=1&utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op](https://careers.amd.com/jobs/90301?icims=1&utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineer Intern/Co-op 🎓](https://careers.amd.com/jobs/90805?icims=1&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 AMD** | [Firmware Engineering Intern Co-op - Undergrad](https://careers.amd.com/jobs/90807?icims=1&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 AMD** | [Hardware Engineer Intern/Co-op](https://careers.amd.com/jobs/90894?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 Tesla** | [Embedded Software Engineer Intern - Optimus](https://www.tesla.com/careers/search/job/282340?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **AeroVironment** | [Embedded Software Engineer Intern](https://avav.wd1.myworkdayjobs.com/en-US/avav/job/Simi-Valley-CA/Summer-2027-Embedded-Software-Engineering-Intern_8549?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **AeroVironment** | [Embedded Software Engineer Intern](https://avav.wd1.myworkdayjobs.com/en-US/avav/job/Simi-Valley-CA/Summer-2027-Embedded-Software-Engineering-Intern_8388?utm_source=Simplify&ref=Simplify) | US / Australia | hardware | unknown | unknown |
| **Aescape** | [Junior Electrical &amp; Firmware Engineer](https://jobs.ashbyhq.com/aescape/5ab3f804-c547-40e3-b496-53f1d3b5048e/application?embed=true&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Alarm.com** | [Embedded Software Engineer 1](https://job-boards.greenhouse.io/alarmcom/jobs/8622530002?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Ambiqmicroinc** | [Embedded Software Intern](https://job-boards.greenhouse.io/ambiqmicroinc/jobs/4404901009) | Singapore | hardware | unknown | unknown |
| **Apex** | [Avionics Test Engineering Internship \(Spring 2027\)](https://jobs.ashbyhq.com/apex-technology-inc/aea24b77-7673-4478-83af-4f16f5337673) | US | controls,hardware | unknown | posting mentions equity |
| **Apex** | [Simulation Software Engineering Internship \(Spring or Summer 2027\)](https://jobs.ashbyhq.com/apex-technology-inc/d3e21f84-3637-4521-833d-fd07b3ca5f2e/application?embed=true&utm_source=Simplify&ref=Simplify) | US | controls,hardware | unknown | posting mentions equity |

_135 more are in [tracker.csv](tracker.csv)._

### Systems & Infra (147 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Platform Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018856/?gh_jid=8018856&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **DRW** | [Platform Engineer Intern](https://job-boards.greenhouse.io/drweng/jobs/7997729) | US |  | unknown | unknown |
| **🔥 Google** | [Software Engineering or Site Reliability Engineering PhD Intern 🎓](https://www.google.com/about/careers/applications/jobs/results/80037545080955590?utm_source=Simplify&ref=Simplify) | UK | infra,phd-position | unknown | unknown |
| **🔥 NVIDIA** | [Software Engineer New Grad - DGX Cloud AI Infrastructure](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Software-Engineer--DGX-Cloud-AI-Infrastructure---New-College-Grad-2026_JR2026477?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **Cerebras Systems** | [DevOps Engineer - New Grad 2026](https://jobs.ashbyhq.com/cerebras/40e0d3ee-8f0a-4b19-9bf9-79410b1c7735) | Remote | infra,distributed,research | unknown | unknown |
| **Cerebras Systems** | [Software Engineer - New Grad 2026](https://jobs.ashbyhq.com/cerebras/99c289fa-8fc6-49f7-b7e8-78ac4e9d99ac/application?utm_source=Simplify&ref=Simplify) | US / Canada | hardware,infra,distributed,research | unknown | unknown |
| **Harvey** | [Software Engineering Intern \(Summer 2027\)](https://jobs.ashbyhq.com/harvey/06d64648-b84b-48ae-94a2-d9c06dfdcb5d/application?embed=true&utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **Harvey** | [Software Engineering Intern \(Summer 2027\)](https://jobs.ashbyhq.com/harvey/3a34578d-d42e-45bb-ac5c-0c3357e8cbb7/application?embed=true&utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **Harvey** | [Software Engineering Intern \(Winter 2027\)](https://jobs.ashbyhq.com/harvey/d40e15aa-2351-4be8-ac8f-1faf60bfcdbf) | Canada | infra | unknown | unknown |
| **Notion** | [Software Engineer, Early Career](https://jobs.ashbyhq.com/notion/297b4ece-765f-4eea-b1b8-46057cb6501f/application?utm_source=Simplify&ref=Simplify) | US | autonomy,infra,distributed,research | unknown | posting mentions equity |
| **Notion** | [Software Engineer, Early Career \(AI\)](https://jobs.ashbyhq.com/notion/85947779-6b87-466a-98bc-30a640448c28) | US | autonomy,infra,distributed | unknown | posting mentions equity |
| **Perplexity** | [Internship - Search Backend Infra Engineer](https://jobs.ashbyhq.com/perplexity/be94e89b-89d5-4f2a-a58b-7929c8d97f92) | Serbia | infra,distributed,phd-position | unknown | unknown |
| **Ramp** | [Software Engineer Internship, Frontend](https://jobs.ashbyhq.com/ramp/a13ae586-f4cb-4385-8822-c42b9b54ed74) | US | hardware,infra,funded | unknown | unknown |
| **Ramp** | [Software Engineering Intern, Android](https://jobs.ashbyhq.com/ramp/fcf118cc-521a-4a62-9d13-945e5b6e3cb8) | US | hardware,infra,funded | unknown | unknown |
| **Ramp** | [Software Engineering Intern, Backend](https://jobs.ashbyhq.com/ramp/acf6b28d-767f-483f-8ff2-114620cd7e04) | US | hardware,infra,funded | unknown | unknown |
| **Ramp** | [Software Engineering Intern, iOS](https://jobs.ashbyhq.com/ramp/b66be397-240b-41a6-9b05-493299b270a9) | US | hardware,infra,funded | unknown | unknown |
| **🔥 AMD** | [Compiler Engineer Intern/Co-op](https://careers.amd.com/jobs/91865?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Compiler Engineer Intern/Co-op](https://careers.amd.com/jobs/91864?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 AMD** | [Compiler Engineer Intern/Co-op - Masters 🎓](https://careers.amd.com/jobs/91867?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Agentis Capital Advisors** | [Investment Banking Summer Analyst - Infrastructure M&amp;A Advisory - Summer 2027](https://jobs.ashbyhq.com/agentis-capital-advisors/af7e9253-cea8-4287-baf9-838a900546b3) | Canada | infra,research | unknown | posting mentions equity |
| **Alan** | [Software Engineer Internship \(6 months from feb/march 2027\)](https://jobs.ashbyhq.com/alan/de4c30ae-698f-43e9-84d1-f458955fd671) | France | infra,research | unknown | posting mentions equity |
| **Alpic** | [Internship - Software Engineer - Final Year](https://jobs.ashbyhq.com/alpic/c8b6be69-51ff-4f8d-ad2d-f2f6db94139a) | France | infra | unknown | unknown |
| **Apera AI** | [Software Developer \(Cloud Infrastructure\) – Co-Op](https://job-boards.greenhouse.io/aperaaiinc/jobs/5240274007) | Unknown | infra | unknown | unknown |
| **Atlys** | [Launchpad Fellowship](https://jobs.ashbyhq.com/atlys/53dcce66-f865-4d1e-a6b0-31433d844723) | Unknown | infra,research,funded | unknown | posting mentions equity |
| **Base Power** | [Supply Chain Tooling Engineer Intern](https://jobs.ashbyhq.com/base-power/7fce3b16-c132-453b-a836-a3bcbd21abd2) | US | data-eng,research | unknown | unknown |
| **Blissway** | [Embedded Systems Engineer New Grad](https://jobs.ashbyhq.com/blissway/51d6d839-9801-4436-bfc2-918bae428ed8/application?embed=true&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/San-Diego-CA/University---2027-Summer-Games-Systems-Engineer-Intern---San-Diego--CA_R0248365?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/McLean-VA/University---2027-Summer-Games-Systems-Engineer-Intern---McLean--VA_R0248361?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Huntsville-AL/University---2027-Summer-Games-Systems-Engineer-Intern---Huntsville--AL_R0249188?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Fort-Walton-Beach-FL/University---2027-Summer-Games-Systems-Engineer-Intern---Ft-Walton-Beach--FL_R0248388?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Honolulu-HI/University---2027-Summer-Games-Systems-Engineer-Intern---Honolulu--HI_R0248370?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/San-Diego-CA/University---2027-Summer-Games-Systems-Engineer-Intern---El-Segundo--CA_R0248366?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Atlanta-GA/University---2027-Summer-Games--Systems-Engineer-Intern---Atlanta--GA_R0248381?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - University](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Colorado-Springs-CO/University---2027-Summer-Games-Systems-Engineer-Intern---Colorado-Springs--CO_R0248368?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - University](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Rome-NY/University---2027-Summer-Games-Systems-Engineer-Intern---Rome--NY_R0248386?utm_source=Simplify&ref=Simplify) | US / Italy |  | unknown | unknown |
| **Booz Allen** | [Systems Engineer Intern - University - 2027 Summer Games](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Annapolis-Junction-MD/University---2027-Summer-Games-Systems-Engineer-Intern---Annapolis-Junction--MD_R0248384?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Brunswick** | [Systems Engineer Co-op - Software Engineering](https://brunswick.wd1.myworkdayjobs.com/en-US/search/job/Fond-du-Lac-WI/Mercury-Marine---Systems-Software-Engineering-Co-op_JR-051212?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Claylabs** | [Early Career Software Engineer](https://jobs.ashbyhq.com/claylabs/16778e12-31cb-4ca1-a321-7f629a7cf273/application?embed=true&utm_source=Simplify&ref=Simplify) | US | infra,research | unknown | unknown |
| **Claylabs** | [Software Engineering Intern](https://jobs.ashbyhq.com/claylabs/5b7eced2-36bd-4265-a2a8-da0f786e47aa) | US | infra,research | unknown | unknown |
| **Compeer Financial** | [Intern Infrastructure Engineering](https://job-boards.greenhouse.io/compeerfinancial/jobs/5422577008) | Unknown | infra | unknown | unknown |

_107 more are in [tracker.csv](tracker.csv)._

### Computational Science (84 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Palantir** | [Forward Deployed Software Engineer, Internship](https://jobs.lever.co/palantir/1b6f1d82-d459-4dea-8bc2-8d2ffe6f881a) | France | autonomy,computer-vision,infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - France](https://jobs.lever.co/palantir/ac0dc094-2480-43c2-8495-26ade227ff4f) | US | infra,funded | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - Intel](https://jobs.lever.co/palantir/9e40d77f-b07c-437b-98e7-def9b0184d89) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - US Government](https://jobs.lever.co/palantir/315f695d-04d1-4a9a-848e-cb2bec7a997e) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - US Government](https://jobs.lever.co/palantir/e0010393-c300-446f-bf67-fa2ef067f16f) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - US Government](https://jobs.lever.co/palantir/e6ff8bf2-135e-474d-ad37-24f490ae1dd2) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Software Engineer, Internship](https://jobs.lever.co/palantir/3531977a-9b2f-40a0-a486-4eeb38e75fc1) | Singapore | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship](https://jobs.lever.co/palantir/76a60923-bb49-40f5-b061-7c7eb1299602) | UK | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Infrastructure](https://jobs.lever.co/palantir/fd3603a9-7016-45c6-9c8d-04c9279ab85e) | UK | computer-vision,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad](https://jobs.lever.co/palantir/d372c805-d0cd-4a10-9522-fbecc78d6f3e/apply?utm_source=Simplify&ref=Simplify) | UK | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad](https://jobs.lever.co/palantir/2458ba08-de79-4e8f-b553-060f9568727e) | Singapore | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Infrastructure](https://jobs.lever.co/palantir/9265acce-12cd-4179-8c50-55d15963532b) | UK | computer-vision,infra,research | unknown | unknown |
| **Snowflake** | [Software Engineer Intern - Berlin \(2026\)](https://jobs.ashbyhq.com/snowflake/41e65c6c-a01e-4f40-af14-ae75d3b95e27) | Germany | hardware,data-eng,infra,distributed,research,phd-position | unknown | unknown |
| **🔥 Tesla** | [Physics Engine Development Engineer Intern - Optimus](https://www.tesla.com/careers/search/job/282147?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Adaptyv** | [Internship Bioengineering / Molecular Biology](https://jobs.ashbyhq.com/adaptyv/b2c0c8b3-55fd-49e2-9c2d-4bc5e58ac414) | Switzerland | infra,research | unknown | unknown |
| **Altoslabs** | [Neuroscience Research Associate / Research Specialist](https://job-boards.greenhouse.io/altoslabs/jobs/6179150004) | US | research,neuroscience | unknown | unknown |
| **Americanpublichealthassociation** | [Climate, Health and Equity Internship: 2027 spring term](https://job-boards.greenhouse.io/americanpublichealthassociation/jobs/4434254009) | US | climate | unknown | unknown |
| **Antares Nuclear** | [Mechanical Engineering Design Intern - Summer 2027](https://jobs.ashbyhq.com/antares/9accca59-103b-4f54-978a-d5bb46bd9c62) | US | hardware,research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Multiphysics Software Intern - Summer 2027](https://jobs.ashbyhq.com/antares/922a527d-9826-446d-9aba-ffc611995830) | US | infra,research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Nuclear Engineering Intern - Summer 2027](https://jobs.ashbyhq.com/antares/e92ae489-1b1a-4616-a9c8-7c2390698af8) | US | research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Nuclear Operations &amp; Licensing Engineering Intern - Summer 2027](https://jobs.ashbyhq.com/antares/ec96a761-509f-44e9-90aa-e1fee5388aa1) | Unknown | research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Quality Engineering Intern - Summer 2027](https://jobs.ashbyhq.com/antares/9335fe9a-a994-4209-bd97-9a6070f4e94f) | US | hardware,research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Reactor Software Engineering Intern - Summer 2027](https://jobs.ashbyhq.com/Antares/419ef2df-f0aa-4b68-994a-077e08a959e3/application?embed=true&utm_source=Simplify&ref=Simplify) | US | controls,hardware,research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Space Mechanical Design Engineering Intern - Summer 2027](https://jobs.ashbyhq.com/antares/7feb2782-3bdc-4efe-b459-9751db944f81) | US | hardware,research,climate,funded | unknown | unknown |
| **Antares Nuclear** | [Supply Chain Engineering Intern - Summer 2027](https://jobs.ashbyhq.com/antares/f98379e4-ca61-4d0e-9cf8-c9d23e0f0e6a) | US | research,climate,funded | unknown | unknown |
| **Base Power** | [Electrical Engineering Intern](https://jobs.ashbyhq.com/base-power/7284737d-7e04-43e0-af1f-858103f64e97) | US | hardware | unknown | unknown |
| **Base Power** | [Hardware Engineering Intern](https://jobs.ashbyhq.com/base-power/f22cee0e-55d9-42cd-806e-1c1fc7217770) | US | hardware | unknown | unknown |
| **Base Power** | [Mechanical Engineering Intern](https://jobs.ashbyhq.com/base-power/717274d7-09dc-4176-b307-07301074b87f) | US | hardware | unknown | unknown |
| **Booz Allen** | [Quantum Computing Research Intern](https://bah.wd1.myworkdayjobs.com/bah_jobs/job/Washington-DC/University---Summer-2027-Quantum-Computing-Research-Intern_R0249046?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Eightsleep** | [Research Associate](https://jobs.ashbyhq.com/eightsleep/67f41097-75aa-4bb7-b937-0b709804984a) | US | controls,hardware,research,neuroscience | unknown | posting mentions equity |
| **Exa** | [Software Engineer, Intern](https://jobs.ashbyhq.com/exa/a9e01521-66f1-481b-89da-ec01d4620f16?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Fab2** | [Embedded Software Engineering Intern - Summer](https://jobs.ashbyhq.com/fab2/15020e6e-be1c-4455-95a3-aa798474cec4) | US | controls,hardware,funded | unknown | unknown |
| **Fab2** | [Embedded Software Engineering Intern - Winter](https://jobs.ashbyhq.com/fab2/3c7fd0f1-b25f-413c-8e62-6ef00a9d47da) | US | controls,hardware,funded | unknown | unknown |
| **Fab2** | [Fab Software Engineering Intern - Summer](https://jobs.ashbyhq.com/fab2/36ab33ab-82e7-4cc4-8137-f451fd6036a0) | US | controls,infra,distributed,funded | unknown | unknown |
| **Fab2** | [Fab Software Engineering Intern - Winter](https://jobs.ashbyhq.com/fab2/0c4dc4f4-01c9-4138-a666-e7234cda7e95) | US | controls,infra,distributed,funded | unknown | unknown |
| **Fab2** | [Rust Software Engineering Intern, Chip Design Tools - Summer](https://jobs.ashbyhq.com/fab2/2b0ab443-c7d8-4547-9766-111747f0b361) | US | controls,data-eng,funded | unknown | unknown |
| **Fab2** | [Rust Software Engineering Intern, Chip Design Tools - Winter](https://jobs.ashbyhq.com/fab2/4e3958f5-4e0d-4acc-9072-e40822ddf904) | US | controls,data-eng,funded | unknown | unknown |
| **Fourier** | [Fall 2026 / Winter 2027 R&amp;D Engineering Intern – Hydrogen Systems](https://jobs.ashbyhq.com/fourier/5b8d0c16-3b74-40ff-b5e6-9fdde6db0e86) | Unknown | controls,hardware | unknown | unknown |
| **H3X Technologies** | [Electromagnetics Engineering Intern \(Spring\)](https://jobs.ashbyhq.com/h3x-technologies/930b8250-4c6d-4df0-a326-892fd594759a) | Unknown | hardware,phd-position | unknown | unknown |
| **Helion** | [Computational Plasma Research Summer 2027 Intern](https://jobs.ashbyhq.com/helion/d2a1f8af-a310-44af-a5bc-c68816ebb7f6/application?embed=true&utm_source=Simplify&ref=Simplify) | US | research,phd-position | unknown | unknown |

_44 more are in [tracker.csv](tracker.csv)._

### HCI / XR (1 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Simular** | [Design Engineer Intern](https://jobs.ashbyhq.com/simular/3c53a046-4fc0-4b67-9295-1912abf16262) | Singapore | autonomy,controls | unknown | unknown |

### Early-company / equity reality check

The company signal is a discovery aid, not a prediction. Private-company options can become valuable, but can also expire, dilute, remain illiquid, or end up worth zero. `private company; verify offer` means the posting does not prove that equity is included. Ask for the option count **and fully diluted percentage**, strike price, vesting/cliff, exercise window, latest common valuation, and liquidation preferences.

## Closing within 10 days

| Days | Deadline | Company | Role | Region |
|--:|--|--|--|--|
| 5 | 2026-10-11 | **Bank of America** | Summer 2027 Analyst | UK |

## Elite and high-tier live postings (572)

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
| **Akuna Capital University** | [Entry Level Software Engineer - C++](https://www.akunacapital.com/careers/job/8013085/?gh_jid=8013085&utm_source=Simplify&ref=Simplify) | Software Engineering | US | New Grad 2026 | review required |
| **Akuna Capital University** | [Junior Quantitative Developer &amp; Strategist](https://www.akunacapital.com/careers/job/8016687/?gh_jid=8016687&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Akuna Capital University** | [Junior Quantitative Researcher](https://www.akunacapital.com/careers/job/8036541/?gh_jid=8036541&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Akuna Capital University** | [Junior Quantitative Researcher - Prediction Markets](https://www.akunacapital.com/careers/job/7863348/?gh_jid=7863348&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Amazon** | [Robotics - Software Development Engineer Intern/Co-op](https://www.amazon.jobs/en/jobs/3136266/robotics-software-development-engineer-intern-co-op-2026?no_int_redir=1&utm_source=github-vansh-ouckah) | Robotics &amp; Embodied AI | US | 2026 | review required |
| **Apple** | [Software Engineer Intern, Undergrad](https://jobs.apple.com/en-us/details/200664785/software-undergrad-engineering-internships?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Apple** | [Software Engineering Intern, Masters](https://jobs.apple.com/en-us/details/200664320/software-engineering-masters-internships?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
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
| **DRW** | [Platform Engineer Intern](https://job-boards.greenhouse.io/drweng/jobs/7997729) | Systems &amp; Infra | US | Ambiguous | review required |
| **DRW** | [Quantitative Research Intern](https://job-boards.greenhouse.io/drweng/jobs/7818540) | Quant / Finance | US | Ambiguous | review required |
| **DRW** | [Quantitative Research Intern](https://job-boards.greenhouse.io/drweng/jobs/7957756) | Quant / Finance | UK | None | review required |
| **DRW** | [Quantitative Research Intern](https://job-boards.greenhouse.io/drweng/jobs/8014915) | Quant / Finance | Singapore | None | review required |
| **DRW** | [Quantitative Trading Analyst Intern](https://job-boards.greenhouse.io/drweng/jobs/7668776) | Quant / Finance | US | Ambiguous | review required |
| **DRW** | [Quantitative Trading Analyst Intern](https://job-boards.greenhouse.io/drweng/jobs/7957243) | Quant / Finance | UK | None | review required |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/7992936) | Software Engineering | US | Ambiguous | review required |
| **DRW** | [Software Developer Intern](https://www.drw.com/work-at-drw/listings/software-developer-intern-3466687?utm_source=github-vansh-ouckah) | Software Engineering | Unknown | Summer 2027 | review required |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/7991196) | Software Engineering | Canada | None | review required |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/8020364) | Software Engineering | Netherlands | None | review required |
| **DRW** | [Software Developer Intern](https://job-boards.greenhouse.io/drweng/jobs/7942281) | Software Engineering | UK | None | review required |
| **DRW** | [Software Developer Intern \(C++\)](https://job-boards.greenhouse.io/drweng/jobs/8014910) | Software Engineering | Singapore | None | review required |
| **DRW** | [Software Developer Intern - Industrial Placement](https://job-boards.greenhouse.io/drwuniversityjobs/jobs/7364884) | Software Engineering | UK | None | review required |
| **Five Rings** | [Quantitative Trader Intern \(Summer 2027\)](https://job-boards.greenhouse.io/fiveringsllc/jobs/5139668008) | Quant / Finance | US | Summer 2027 | review required |
| **Five Rings** | [Software Developer Intern 🇺🇸](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349707008?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Five Rings Capital** | [Summer Intern 2027 - Quantitative Researcher \(PhD\)](https://job-boards.greenhouse.io/fiveringsllc/jobs/5349219008) | Quant / Finance | US | Summer 2027 | review required |
| **Five Rings Capital** | [Trading Operations Engineer Intern](https://job-boards.greenhouse.io/fiveringsllc/jobs/5420708008?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer 2027 | review required |
| **G-Research** | [Software Engineer Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Software-Engineering-Intern_R3746?utm_source=Simplify&ref=Simplify) | Software Engineering | UK | Ambiguous | review required |
| **Google** | [Software Engineering Intern](https://www.google.com/about/careers/applications/jobs/results/85564713261245126-software-engineering-intern-bs-summer-2027?utm_source=github-vansh-ouckah) | Software Engineering | US | Summer 2027 | review required |
| **Google** | Software Engineering Intern, 2027 | Software Engineering | UK | Summer 2027 | eligible |
| **Hudson River Trading** | [Algorithm Developer New Grad - Quant Researcher](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8052050&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | New Grad 2026 | review required |
| **Hudson River Trading** | [Data Scientist Intern](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8257369&utm_source=Simplify&ref=Simplify) | Quant / Finance | US / UK | Ambiguous | review required |
| **Hudson River Trading** | [Software Engineer Intern](https://www.hudsonrivertrading.com/hrt-job/software-engineering-internship-c-or-python-summer-2027/?gh_src=&utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
| **IMC** | [Hardware Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823945101) | Hardware / EE | US | Summer 2027 | review required |
| **IMC** | [Quantitative Research Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4907399101) | Quant / Finance | US | Summer 2027 | review required |
| **IMC** | [Software Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823924101) | Software Engineering | US | Summer 2027 | review required |
| **IMC Trading** | [Deep Learning Research Intern - Summer 2027 - Amsterdam](https://job-boards.eu.greenhouse.io/imc/jobs/4912874101) | Quant / Finance | Netherlands | Summer 2027 | review required |
| **IMC Trading** | [Graduate Quantitative Researcher \(PhD\)](https://job-boards.eu.greenhouse.io/imc/jobs/4912325101) | Quant / Finance | US | Unknown | review required |
| **IMC Trading** | [Hardware Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4927149101) | Quant / Finance | Netherlands | Unknown | review required |
| **IMC Trading** | [Hardware Machine Learning PhD Research Internship](https://job-boards.eu.greenhouse.io/imc/jobs/4975945101) | Quant / Finance | US | Unknown | review required |
| **IMC Trading** | [Machine Learning Research Intern \(Summer 2027\)](https://job-boards.eu.greenhouse.io/imc/jobs/4907430101) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Machine Learning Research Intern - Summer 2027 - Sydney](https://job-boards.eu.greenhouse.io/imc/jobs/4956547101) | Quant / Finance | Australia | Summer 2027 | review required |
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
| **Jump Trading** | [Campus C++ Software Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027860) | Quant / Finance | China | Unknown | review required |
| **Jump Trading** | [Campus C++ Software Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027946) | Quant / Finance | Singapore | Unknown | review required |
| **Jump Trading** | [Campus Crypto Researcher \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7362318) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus Data Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8002998) | Quant / Finance | US | Unknown | review required |
| **Jump Trading** | [Campus Data Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7975008) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus FPGA Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7974391) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus ML Research Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7977145) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus Python Software Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027955) | Quant / Finance | Singapore | Unknown | review required |

_472 more are in [tracker.csv](tracker.csv)._

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
