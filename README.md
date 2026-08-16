# 🎯 Universal Academic & Career Tracker — Internships · Research · PhD · New Grad

> Last verified run: **2026-08-16** · **1075 verified-open postings** · **29 research / PhD / postdoc positions**

This tracker watches community internship boards and official Greenhouse, Ashby, and Lever feeds. Career hubs and forecast programmes are kept separate from real postings. Unknown work-authorisation or sponsorship data means **review required**, never assumed eligible.

## Filter jobs, generate a CV, then use Simplify

[Open the filterable Role Radar dashboard](https://abyyworld.github.io/internship-tracker/) for search, category, position type, region, term, degree, company-type, and CV-support filters.

The CV editor runs from a clone of this repository. See [SETUP.md](SETUP.md) for first-time configuration, then:

```bash
./start-autoapply.command   # macOS
python3 -m autoapply bridge  # any platform
```

Any job posting on any site can be tailored for: the `tailor-anywhere.user.js` userscript puts a **✦ Tailor my CV** button on pages that read like a job advert, reads the posting, and opens it in the same local editor — the tracker's own feeds are a starting point, not the limit.

Every dashboard card has a native **✦ Edit CV for this job** button; Tampermonkey is not required for the dashboard. It opens a private localhost editor containing the complete master CV and tailors it to the selected posting: sections and entries reordered to lead with the evidence that posting cares about, every line rewritten against its stated requirements, and a summary written for the role. Each proposal can be accepted, rejected, or edited before exporting a job-specific PDF; untouched content is preserved, and the employer application remains a separate button where Simplify can autofill.

Every proposal is checked before it is shown. A rewrite may not introduce a number, a named technology, an employer, a date, or a qualification the CV does not already evidence, and a metric earned on one project may not reappear as the result of another. Keyword coverage is counted against the CV rather than taken from the model, and requirements the CV genuinely cannot evidence are reported as gaps instead of being written around.

Any OpenAI-compatible endpoint drives it — OpenAI, Groq, OpenRouter, Cerebras, Together, GitHub Models, Google AI Studio, or a model running locally under Ollama for nothing. The provider and model are chosen in the editor. Each provider keeps its own key file **and its own chosen model**, so switching provider asks for that provider's key instead of sending the previous one to an account that never issued it, and never posts one provider's model id to another. **Test this provider** sends one cheap request and reports the endpoint, the status, the provider's own words, the parameters that endpoint refused and the models it offers — because a rejected key and a working one look identical until something asks.

The GitHub repository never receives the private profile, fact bank, API keys, drafts, or generated PDFs. The editor runs on `127.0.0.1`, stores the API key locally as a mode-0600 private file, requires review of every proposed change, and never submits an application.

Pressing **Generate suggestions** sends the selected job description and master CV text to the configured endpoint through the user's own account. Merely opening the editor, editing by hand, or exporting a PDF makes no network call. Pointing the editor at a local model means the CV never leaves the machine at all.

> ⚠️ **5 previously seen roles are stale because at least one source failed or was not checked. They were not marked closed.**

## At a glance

| Metric | Count |
|--|--:|
| Verified-open postings | 1075 |
| Roles discovered today | 1 |
| New verified postings | 1 |
| Research / PhD / postdoc positions | 29 |
| Elite tier | 185 |
| High tier | 131 |
| Eligibility still needs review | 1075 |
| Deadlines within 10 days | 0 |

**By category:** Software Engineering 510 · Quant / Finance 168 · AI / ML 118 · Robotics & Embodied AI 87 · Security 53 · Data 46 · Hardware / EE 38 · Systems & Infra 38 · Computational Science 17

**By region:** US 903 · UK 63 · Unknown 25 · Canada 23 · Singapore 12 · Netherlands 9 · Hong Kong 4 · Ireland 4 · US / Canada 4 · Switzerland 4 · France 2 · US / Global 2 · South Korea 2 · Serbia 2 · US / Austria 2 · US / UAE 2 · US / Australia 2 · UK / Ireland 1 · US / France / Singapore / Hong Kong 1 · Australia 1 · Germany 1 · Poland 1 · India 1 · US / Netherlands 1 · US / Canada / UK 1 · US / Europe 1 · UK / Australia 1

**By degree evidence:** Unknown 910 · Advanced/unknown 89 · PhD 40 · Undergraduate eligible 30 · Masters 6

## Newly opened (1)

| Company | Role | Category | Region | Term | Eligibility |
|--|--|--|--|--|--|
| **RTX** | [Software Engineer Intern](https://globalhr.wd5.myworkdayjobs.com/fr-CA/Private_Posting_No_TMP/job/US-CA-SAN-JOSE-826--200-Holger-Way--BLDG-826/Software-Engineering-Intern--Summer-2027-_01867392?utm_source=Simplify&ref=Simplify) | Software Engineering | US | Summer 2027 | review required |

## Browse by category

Every category is listed the same way. Live geography reflects what official feeds expose today; the worldwide career-hub and academic watchlists are kept separately in [manual_checks.md](manual_checks.md).

### Software Engineering (510 live)

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
| **Optiver** | [Software Engineer Intern](https://www.optiver.com/join-us/jobs/technology/austin/software-engineer-intern-summer-2027-austin/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Optiver** | [Software Engineer Intern](https://www.optiver.com/join-us/jobs/technology/chicago/software-engineer-intern-summer-2027-chicago/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Squarepoint Capital** | [Intern Software Developer - London - 2027](https://www.squarepoint-capital.com/open-opportunities?id=7231006&gh_jid=7231006) | UK |  | unknown | unknown |
| **Squarepoint Capital** | [Intern Software Developer - Singapore - 2027](https://www.squarepoint-capital.com/open-opportunities?id=6201998&gh_jid=6201998) | Singapore |  | unknown | unknown |
| **Tower Research Capital** | [Risk Intern - 6 Month Internship Opportunity](https://www.tower-research.com/open-positions/?gh_jid=7789933) | Singapore | research | unknown | unknown |
| **Virtu Financial** | [2027 Internship - Software Engineer](https://job-boards.greenhouse.io/virtu/jobs/8551566002) | Ireland |  | unknown | unknown |
| **Virtu Financial** | [2027 Internship – Core Operations Engineer](https://job-boards.greenhouse.io/virtu/jobs/6329460002) | Singapore |  | unknown | unknown |
| **Virtu Financial** | [2027 Internship – Software Engineer](https://job-boards.greenhouse.io/virtu/jobs/5513756002) | Singapore |  | unknown | unknown |
| **Virtu Financial** | [Frontend Developer Internship](https://job-boards.greenhouse.io/virtu/jobs/8657500002?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Virtu Financial** | [Software Engineer Intern - Software Engineer](https://job-boards.greenhouse.io/virtu/jobs/8624410002?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |

_470 more are in [tracker.csv](tracker.csv)._

### Quant / Finance (168 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Quantitative Development &amp; Strategy Intern 🇺🇸](https://akunacapital.com/careers/job/8021481/?gh_jid=8021481&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Akuna Capital** | [Quantitative Research Intern 🇺🇸](https://akunacapital.com/careers/job/8036614/?gh_jid=8036614&utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **Citadel** | [Quantitative Research Analyst University Graduate](https://www.citadel.com/careers/details/quantitative-research-analyst-university-graduate-us/?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Citadel** | [Quantitative Trader: Equity Quantitative Research – University Graduate](https://www.citadel.com/careers/details/quantitative-trader-equity-quantitative-research-university-graduate-us/?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Citadel Securities** | [Quantitative Research Analyst – University Graduate](https://www.citadelsecurities.com/careers/details/quantitative-research-analyst-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | UK / Ireland | research | unknown | unknown |
| **Citadel Securities** | [Quantitative Trader New Grad](https://www.citadelsecurities.com/careers/details/quantitative-trader-university-graduate-europe/?utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **Cubist Systematic Strategies** | [Quantitative Developer Intern](https://job-boards.greenhouse.io/embed/job_app?for=point72&jr_id=6a07069024dcb03739f1ec72&token=7297613002&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **DRW** | [Quantitative Research Intern](https://www.drw.com/work-at-drw/listings/quantitative-research-intern-3413670?utm_source=github-vansh-ouckah) | US | research | unknown | unknown |
| **DRW** | [Quantitative Trading Analyst Intern](https://job-boards.greenhouse.io/drweng/jobs/7957243?utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **DRW** | [Quantitative Trading Analyst Intern](https://www.drw.com/work-at-drw/listings/quantitative-trading-analyst-intern-3375090?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Five Rings** | [Quantitative Trader Intern \(Summer 2027\)](https://job-boards.greenhouse.io/fiveringsllc/jobs/5139668008) | US |  | unknown | unknown |
| **G-Research** | [Quantitative Research Internship 🎓](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Quant-Research-Internship_R3691?utm_source=Simplify&ref=Simplify) | UK | research | unknown | unknown |
| **Hudson River Trading** | [Algorithm Developer New Grad - Quant Researcher](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8052050&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Hudson River Trading** | [Algorithm Development Intern - Quant Research 🎓](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8059837&utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Hudson River Trading** | [Software Engineer Intern](https://www.hudsonrivertrading.com/hrt-job/software-engineering-internship-c-or-python-summer-2027/?gh_src=&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Hudson River Trading** | [Software Engineer Intern - C++ or Python](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8052083&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **IMC Trading** | [Graduate Quantitative Researcher \(PhD\)](https://job-boards.eu.greenhouse.io/imc/jobs/4912325101) | US | phd-position | unknown | unknown |
| **IMC Trading** | [Hardware Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823945101?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **IMC Trading** | [Hardware Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4927149101) | Netherlands |  | unknown | unknown |
| **IMC Trading** | [Hardware Machine Learning PhD Research Internship](https://job-boards.eu.greenhouse.io/imc/jobs/4829785101) | US | research,phd-position | unknown | unknown |
| **IMC Trading** | [Machine Learning Research Intern 🎓](https://job-boards.eu.greenhouse.io/imc/jobs/4912874101?utm_source=Simplify&ref=Simplify) | Netherlands | research | unknown | unknown |
| **IMC Trading** | [Machine Learning Research Intern 🎓](https://job-boards.eu.greenhouse.io/imc/jobs/4907430101?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **IMC Trading** | [Quant Research Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941208101) | Hong Kong | research | unknown | unknown |
| **IMC Trading** | [Quantitative Research Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4907399101?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **IMC Trading** | [Quantitative Trader Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823923101?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **IMC Trading** | [Quantitative Trader Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4936262101) | Netherlands |  | unknown | unknown |
| **IMC Trading** | [Software Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4667854101) | Netherlands |  | unknown | unknown |
| **IMC Trading** | [Software Engineer Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941206101) | Hong Kong |  | unknown | unknown |
| **IMC Trading** | [Software Engineer, Early Career](https://job-boards.eu.greenhouse.io/imc/jobs/4577504101) | US |  | unknown | unknown |
| **IMC Trading** | [Trader Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4939846101) | Netherlands |  | unknown | unknown |
| **IMC Trading** | [Trader Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941205101) | Hong Kong |  | unknown | unknown |
| **Jane Street** | [Quantitative Researcher Intern](https://www.janestreet.com/join-jane-street/position/8498547002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Quantitative Trader Intern](https://www.janestreet.com/join-jane-street/position/8617344002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Sales and Trading Intern](https://www.janestreet.com/join-jane-street/apply/8537797002?gh_jid=8537797002&utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **Jane Street** | [Sales and Trading Intern](https://www.janestreet.com/join-jane-street/position/8347385002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Trading Desk Operations Engineer Intern](https://www.janestreet.com/join-jane-street/position/8621450002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jump Trading** | [Campus AI Research Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8052281) | US | research | unknown | unknown |
| **Jump Trading** | [Campus AI Research Engineer - Deep Learning \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8052338) | US | research | unknown | unknown |
| **Jump Trading** | [Campus AI Research Engineer – Research Automation \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8052351) | US | research | unknown | unknown |
| **Jump Trading** | [Campus AI Researcher, PhD/Postdoc \(Full-Time\)](https://www.jumptrading.com/hr/job?gh_jid=7976923) | UK | phd-position | unknown | unknown |

_128 more are in [tracker.csv](tracker.csv)._

### AI / ML (118 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **G-Research** | [Machine Learning Research Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Machine-Learning-Research-Internship_R3682?utm_source=Simplify&ref=Simplify) | UK | research | unknown | unknown |
| **G-Research** | [Natural Language Processing Intern](https://gresearch.wd103.myworkdayjobs.com/G-Research/job/London-UK/Natural-Language-Processing-Internship_R3686?utm_source=Simplify&ref=Simplify) | UK | nlp,research | unknown | unknown |
| **Jane Street** | [Machine Learning Engineer Intern](https://www.janestreet.com/join-jane-street/position/8611307002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Jane Street** | [Machine Learning Researcher Intern](https://www.janestreet.com/join-jane-street/position/8384490002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, AI/ML &amp; LLM](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922929&utm_source=github-vansh-ouckah) | US | llm | unknown | unknown |
| **Two Sigma** | [AI Research Scientist Intern \(MS / PhD\)](https://careers.twosigma.com/careers/JobDetail/New-York-New-York-United-States-AI-Research-Scientist-Internship-2027-Summer/14022) | US | research,phd-position | unknown | unknown |
| **Two Sigma** | [AI Research Scientist Intern - 2027 Summer](https://twosigma.avature.net/careers/JobDetail/14096?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **🔥 NVIDIA** | [Applied Machine Learning Engineer – New College Grad 2026 - Circuit Design 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Applied-Machine-Learning-Engineer--Circuit-Design---New-College-Grad-2026_JR2011517?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [Deep Learning Software Engineer – New College Grad - TensorRT Performance](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Deep-Learning-Software-Engineer--TensorRT-Performance---New-College-Grad-2026_JR2015071?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [Research Scientist New Grad - Efficient Deep Learning 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Research-Scientist--Efficient-Deep-Learning---New-College-Grad-2026_JR2019729-1?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **🔥 NVIDIA** | [Research Scientist – PhD New College Grad - Generative AI for Physical AI 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Research-Scientist--Generative-AI-for-Physical-AI---PhD-New-College-Grad-2026_JR2016032?utm_source=Simplify&ref=Simplify) | US | research,phd-position | unknown | unknown |
| **🔥 NVIDIA** | [Software Engineer New Grad - Deep Learning Libraries](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Software-Engineer--Deep-Learning-Libraries---New-College-Graduate-2026_JR2023252?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Cerebras Systems** | [Kernel Engineer - New Grad](https://jobs.ashbyhq.com/cerebras/9c7da4b8-446b-4bf2-8d07-23241590bf2e) | US / Canada | hardware,research,neuroscience,phd-position | unknown | unknown |
| **Databricks** | [PhD GenAI Research Scientist Intern](https://databricks.com/company/careers/open-positions/job?gh_jid=7011263002) | US | research,phd-position | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - Commercial](https://jobs.lever.co/palantir/d5486403-c050-4920-b2e0-91b69b61ebb2/apply?utm_source=Simplify&ref=Simplify) | US | autonomy,hardware,llm,computer-vision,infra | unknown | unknown |
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
| **Snowflake** | [AI Research Scientist, New Grad – Agents &amp; Reinforcement Learning](https://jobs.ashbyhq.com/snowflake/1bad12df-f443-426f-9d09-e96fc780d698/application?utm_source=Simplify&ref=Simplify) | US | autonomy,llm,rl,data-eng,infra,research,phd-position | unknown | unknown |
| **Allen Control Systems** | [Junior Computer Vision &amp; Machine Learning Engineer](https://jobs.ashbyhq.com/allen-control-systems/cfb348d0-ab31-4fa5-9bd5-def1de764ca9/application?embed=true&utm_source=Simplify&ref=Simplify) | US | perception,controls,computer-vision | unknown | unknown |
| **Atoms** | [Machine Learning PhD Software Engineer Intern 🎓](https://job-boards.greenhouse.io/cssmerge/jobs/8693034002?utm_source=Simplify&ref=Simplify) | US | phd-position | unknown | unknown |
| **ByteDance** | [Applied Machine Learning Production Engineer Intern](https://joinbytedance.com/search/7670009669494704437?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **ByteDance** | [Student Researcher, Multimodal Interaction &amp; World Model \(Seed\)](https://joinbytedance.com/search/7623548747208739077) | US | multimodal | unknown | unknown |
| **ByteDance** | [Student Researcher, Vision Foundation Model \(Seed\)](https://joinbytedance.com/search/7623544831999346997) | US | embodied-ai | unknown | unknown |
| **Castleton Commodities International** | [Data Science Machine Learning Intern](https://osv-cci.wd1.myworkdayjobs.com/en-US/CCICareers/job/Stamford-CT/Data-Science-Machine-Learning-Internship--Summer-2027-_R1344?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Castleton Commodities International** | [Data Science Machine Learning Intern](https://osv-cci.wd1.myworkdayjobs.com/en-US/CCICareers/job/London-UK/Data-Science-Machine-Learning-Internship--Summer-2027-_R1345?utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **Epic Games** | [Machine Learning Intern - Special Projects - Epic Research Group 🎓](https://epicgames.com/careers/jobs/5708589004?gh_jid=5708589004&utm_source=Simplify&ref=Simplify) | UK | research | unknown | unknown |
| **Epic Games** | [Machine Learning Intern - Special Projects - Epic Research Group 🎓](https://epicgames.com/careers/jobs/6138140004?gh_jid=6138140004&utm_source=Simplify&ref=Simplify) | Canada | research | unknown | unknown |
| **Epic Games** | [Machine Learning Intern 🎓](https://epicgames.com/careers/jobs/6138134004?gh_jid=6138134004&utm_source=Simplify&ref=Simplify) | US / Canada / UK |  | unknown | unknown |
| **Etched AI** | [Infrastructure Intern](https://jobs.ashbyhq.com/etched/1b073af4-6764-45ca-a22d-40a4823f0877) | Unknown | hardware,llm,infra,research,phd-position | unknown | unknown |
| **Gladstone Institutes** | [Research Engineer 1 - AI / Machine Learning - Jain Lab](https://gladstone.wd503.myworkdayjobs.com/careers/job/San-Francisco/Research-Engineer--ai--I-II-or-III---Jain-Lab_REQ-3845?utm_source=Simplify&ref=Simplify) | US | research | unknown | unknown |
| **Intercontinental Exchange, Inc.** | [Artificial Intelligence, Data &amp; Machine Learning Intern](https://careers.ice.com/jobs/12830?lang=en-us&iis=LinkedIn&iisn=Linkedin&mode=apply&jr_id=69e67bb27820c036924d0af9&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Machine Learning PhD New Grad - Artificial Intelligence 🎓](https://careers.jhuapl.edu/jobs/59010?icims=1&utm_source=Simplify&ref=Simplify) | US | phd-position | unknown | unknown |

_78 more are in [tracker.csv](tracker.csv)._

### Robotics & Embodied AI (87 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Amazon** | [Robotics - Software Development Engineer Intern/Co-op](https://www.amazon.jobs/en/jobs/3136266/robotics-software-development-engineer-intern-co-op-2026?no_int_redir=1&utm_source=github-vansh-ouckah) | US | robot-software | unknown | unknown |
| **Nuro** | [Software Engineer, AI Platform - Intern](https://nuro.ai/careersitem?gh_jid=7351061) | US | autonomous vehicles | private-scaleup | private company; verify offer |
| **Nuro** | [Software Engineer, AI Platform - New Grad](https://nuro.ai/careersitem?gh_jid=7351066) | US | autonomous vehicles | private-scaleup | private company; verify offer |
| **Palantir** | [American Tech Fellowship](https://jobs.lever.co/palantir/0ccbe620-a3ef-41d1-a5c4-68e56b3c91d0) | Unknown | controls,robot-software,hardware,funded | unknown | unknown |
| **🔥 Waymo** | [Applied Research Scientist – New Grad - Perception Large Language Model/Vision-Language Model - PhD 🎓](https://careers.withwaymo.com/jobs?gh_jid=7488508&utm_source=Simplify&ref=Simplify) | US | autonomous vehicles | established | company-dependent |
| **Deft Robotics** | [Electrical Engineer Intern \(Spring-Summer 2026\)](https://jobs.ashbyhq.com/deft-ai/0d16afe8-30a9-43df-90d5-ccba1cb97b69) | US | humanoid robotics | emerging-startup | private company; verify offer |
| **Deft Robotics** | [Mechanical Engineer Intern \(Spring-Summer 2026\)](https://jobs.ashbyhq.com/deft-ai/1bef1405-cd24-4da7-b1e7-0ca02e8f5eb2) | US | humanoid robotics | emerging-startup | private company; verify offer |
| **Dyna Robotics** | [Research Internship](https://jobs.ashbyhq.com/dyna-robotics/5a431519-ee6b-4cb7-8a3a-422727053a09) | US | robot learning | emerging-startup | private company; verify offer |
| **Generalist AI** | [Research Assistant](https://jobs.ashbyhq.com/generalist/fc7c7b49-248a-4849-a473-a0bd246e5486) | US | general-purpose robotics | emerging-startup | private company; verify offer |
| **Lightwheel** | [Developer Advocate / Research Community Intern](https://jobs.ashbyhq.com/lightwheel/e22363b9-9c4f-4991-8de3-339b8e9399df) | US | robot learning | emerging-startup | private company; verify offer |
| **Physical Intelligence** | [Research Internships](https://jobs.ashbyhq.com/physicalintelligence/f020ff1a-4b4c-4415-8434-2da5010a7076) | US | embodied AI | emerging-startup | private company; verify offer |
| **Sunday Robotics** | [Manufacturing Engineering Intern \(Fall 2026\)](https://jobs.ashbyhq.com/sunday/08feb65a-08b0-462d-aebf-4f0239a16ed8) | US | home robotics | emerging-startup | private company; verify offer |
| **1X** | [AI Residency](https://jobs.ashbyhq.com/1x/5b2b4c73-13b5-46ca-8467-8024741a4b57) | US | humanoid robotics | private-scaleup | private company; verify offer |
| **1X** | [Internship - Manufacturing Engineering \(Fall\)](https://jobs.ashbyhq.com/1x/7d93444c-01f5-485c-89ef-24164f30441d) | US | humanoid robotics | private-scaleup | private company; verify offer |
| **ANYbotics** | [Internship - Reinforcement Learning for Navigation](https://jobs.lever.co/anybotics/9d34ce1f-0dae-4cf3-85b0-d231dfb4851b) | Switzerland | legged robots | private-scaleup | private company; verify offer |
| **ANYbotics** | [Product Data Management Internship](https://jobs.lever.co/anybotics/74b68707-86aa-4efc-9efb-94ca5ad82698) | Switzerland | legged robots | private-scaleup | private company; verify offer |
| **ANYbotics** | [Robotics Lab Technician Intern](https://jobs.lever.co/anybotics/9755ae0f-f740-40bc-bc13-be52c505748b) | Switzerland | legged robots | private-scaleup | private company; verify offer |
| **ANYbotics** | [Software Engineering Internship - AI Platform](https://jobs.lever.co/anybotics/7e305a48-4628-4a6a-b054-0367b6f6e586) | Switzerland | legged robots | private-scaleup | private company; verify offer |
| **Anduril** | [2026 Early Career Electrical Engineer](https://boards.greenhouse.io/andurilindustries/jobs/4802172007?gh_jid=4802172007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [2026 Early Career Engineering Finance Associate](https://boards.greenhouse.io/andurilindustries/jobs/5159092007?gh_jid=5159092007) | US | autonomous systems | private-scaleup | private company; verify offer |
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
| **Anduril** | [Early Career Firmware Engineer](https://boards.greenhouse.io/andurilindustries/jobs/5167865007?utm_source=Simplify&ref=Simplify) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [Early Career Software Engineer](https://boards.greenhouse.io/andurilindustries/jobs/4802146007?utm_source=Simplify&ref=Simplify) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [Mission Engineer, Air Dominance &amp; Strike, Early Career](https://boards.greenhouse.io/andurilindustries/jobs/5174562007?gh_jid=5174562007) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Anduril** | [Software Engineer Intern](https://job-boards.greenhouse.io/andurilindustries/jobs/5148079007?gh_jid=5148079007&utm_source=github-vansh-ouckah) | US | autonomous systems | private-scaleup | private company; verify offer |
| **Applied Intuition** | [Embedded Software Engineer - New Grad \(2027\)](https://jobs.ashbyhq.com/applied/6971d533-1536-448b-96b8-544ad5383f44/application?embed=true&utm_source=Simplify&ref=Simplify) | US | autonomy tooling | private-scaleup | private company; verify offer |
| **Applied Intuition** | [Research Engineer - New Grad \(2027\)](https://jobs.ashbyhq.com/applied/45fc41cd-8280-4010-ba1f-def6114b3e39/application?embed=true&utm_source=Simplify&ref=Simplify) | US | autonomy tooling | private-scaleup | private company; verify offer |
| **Applied Intuition** | [Research Intern - 3D Vision and Generation, Self-Driving](https://jobs.ashbyhq.com/applied/91e0686e-272a-4780-b33d-d7860b94a7b4) | US | autonomy tooling | private-scaleup | private company; verify offer |
| **Applied Intuition** | [Research Intern - Reinforcement Learning, Robotics](https://jobs.ashbyhq.com/applied/bb953f29-0059-4a40-aa9e-3a8c88733902) | US | autonomy tooling | private-scaleup | private company; verify offer |
| **Applied Intuition** | [Research Intern - Reinforcement Learning, Self-Driving](https://jobs.ashbyhq.com/applied/ce58d9fd-f22b-4336-80b5-ba1e8d764526) | US | autonomy tooling | private-scaleup | private company; verify offer |
| **Applied Intuition** | [Research Intern - Robotic Hardware, Simulation and Data](https://jobs.ashbyhq.com/applied/5bb0567a-8d07-4cc4-be7c-c06b31361883) | US | autonomy tooling | private-scaleup | private company; verify offer |

_47 more are in [tracker.csv](tracker.csv)._

### Security (53 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Jane Street** | [Cybersecurity Analyst Intern](https://www.janestreet.com/join-jane-street/position/8632723002/?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Security &amp; Identity](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922930&utm_source=github-vansh-ouckah) | US | security | unknown | unknown |
| **Cohere** | [Machine Learning Intern/Co-op  \(Winter 2027\)](https://jobs.ashbyhq.com/cohere/36d1f52f-8270-4652-adf5-5303a0ff341b) | Canada | computer-vision,nlp,security,research,funded | unknown | unknown |
| **Cohere** | [Software Engineer Intern \(Fall / Winter 2026\)](https://jobs.ashbyhq.com/cohere/8c035d3d-081d-4c8a-914a-72f4efaad254) | Canada | autonomy,computer-vision,nlp,data-eng,infra,security,research,funded | unknown | unknown |
| **Notion** | [Governance, Risk, and Compliance Intern \(Fall 2026\)](https://jobs.ashbyhq.com/notion/6ccbc30c-2de0-4395-af14-3641cd15961b) | US | security | unknown | posting mentions equity |
| **Palantir** | [Forward Deployed Infrastructure Engineer, New Grad - US Government](https://jobs.lever.co/palantir/33243fb5-6907-40c7-930c-968b25d825d0) | US | autonomy,llm,infra,distributed,security,funded | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - AUS Government](https://jobs.lever.co/palantir/395a4483-fc3d-4b77-a500-501923fd0976) | Australia | infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - Defense Tech](https://jobs.lever.co/palantir/cccfe1bd-f15b-4fe5-b044-c793e7961c1b) | US | computer-vision,infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - UK Government](https://jobs.lever.co/palantir/26e23f5d-083b-45aa-b223-1a6e43d960bf) | UK | autonomy,llm,computer-vision,infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - UK Government](https://jobs.lever.co/palantir/b4aa51a2-bc43-4d67-bf55-12db7feefb3a/apply?utm_source=Simplify&ref=Simplify) | UK | autonomy,hardware,llm,computer-vision,infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - US Government](https://jobs.lever.co/palantir/cbe90327-3e6e-451c-a54c-1d3cbcef5aeb/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,infra,security,funded | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, New Grad - US Government](https://jobs.lever.co/palantir/d1ac83d0-e923-42a5-8e6d-58dd0cab25ca/apply?utm_source=Simplify&ref=Simplify) | US | computer-vision,infra,security,funded | unknown | unknown |
| **Palantir** | [Privacy &amp; Civil Liberties Engineer - New Grad](https://jobs.lever.co/palantir/95e0d2b0-437a-4096-a5c6-0f247f426c90) | US | security,funded | unknown | unknown |
| **Palantir** | [Privacy and Civil Liberties Software Engineer, Internship](https://jobs.lever.co/palantir/09846827-b931-4a9f-bd64-c3bb8860187b/apply?utm_source=Simplify&ref=Simplify) | US | infra,security | unknown | unknown |
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
| **Ramp** | [Software Engineer Internship, Android](https://jobs.ashbyhq.com/ramp/67fadb77-43d8-4449-954b-d4cf2c6d3b8b) | US | hardware,infra,security,funded | unknown | unknown |

_13 more are in [tracker.csv](tracker.csv)._

### Data (46 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Citadel** | [Sector Data Scientist Intern](https://www.citadel.com/careers/details/sector-data-scientist-2027-intern-us/?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Jane Street** | [Data Engineer Intern](https://www.janestreet.com/join-jane-street/position/8631973002/?utm_source=github-vansh-ouckah) | US | data-eng | unknown | unknown |
| **Microsoft** | [Software Engineer Intern, Data Platform/Analytics](https://apply.careers.microsoft.com/careers?query=intern&start=0&location=untied+states&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0&pid=1970393556922931&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Tower Research Capital** | [Business Analytics Intern - 6 Month Internship Opportunity](https://www.tower-research.com/open-positions/?gh_jid=8041512) | Netherlands | research | unknown | unknown |
| **🔥 Figma** | [Data Scientist, Core Data 🎓](https://job-boards.greenhouse.io/figma/jobs/5976930004?gh_jid=5976930004&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **AMERICAN SYSTEMS** | [Data Engineer - Junior](https://careers-americansystems.icims.com/jobs/4391/job?mobile=true&needsRedirect=false&utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **Affinius Capital** | [Data Scientist Intern](https://careers-affiniuscapital.icims.com/jobs/2284/summer-2027-data-scientist-intern/job) | US |  | unknown | unknown |
| **AlixPartners** | [Data Scientist Intern 🎓](https://www.alixpartners.com/careers/7725335003?gh_jid=7725335003&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Campus Undergraduate Summer Internship - Strategy &amp; Analytics - Credit &amp; Fraud Risk](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26011984?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **American Express** | [Data Engineer 1 - Global Servicing Technology](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26011091?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **American Express** | [Undergraduate Intern - Strategy &amp; Analytics](https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/26011990?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Aon** | [Data &amp; Analytics Associate - Early Careers](https://jobs.aon.com/jobs/105952?icims=1&utm_source=Simplify&ref=Simplify) | Canada |  | unknown | unknown |
| **Applied Materials** | [Data Scientist New Grad - Masters Degree 🎓](https://amat.wd1.myworkdayjobs.com/External/job/Santa-ClaraCA/Data-Scientist-New-College-Grad---Masters-Degree--Santa-Clara--CA-_R2625997?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Bluehawk** | [Exploitation Specialist - Data Scientist - Junior](https://careers-bluehawk.icims.com/jobs/2822/job?mobile=true&needsRedirect=false&utm_source=Simplify&ref=Simplify) | US | security | unknown | unknown |
| **Capgemini** | [Junior Data Engineer/Junior Data Scientist](https://careers.capgemini.com/job/New-York,-NY-Junior-Data-EngineerJunior-Data-Scientist-NY-10001/1418866433/?ats=successfactors&utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **Capgemini** | [Junior Data Engineer/Junior Data Scientist](https://careers.capgemini.com/job/Atlanta,-GA-Junior-Data-EngineerJunior-Data-Scientist-GA-30301/1418864933/?ats=successfactors&utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **CarbonChain** | [Junior Data Engineer](https://job-boards.greenhouse.io/carbonchain/jobs/6121104004?utm_source=Simplify&ref=Simplify) | UK | data-eng,climate | unknown | unknown |
| **Cigna Group** | [Technology Development Program New Grad - Data &amp; Analytics Engineering Track](https://cigna.wd5.myworkdayjobs.com/cignacareers/job/Bloomfield-CT/Technology-Development-Program--TECDP----Data---Analytics-Engineering-Track_26009518-1?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Cortica** | [Junior AI Data Engineer](https://job-boards.greenhouse.io/allcareers/jobs/8692383002?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **Delta Air Lines** | [Reservations Co-op \(Spring 2027, data analytics / process improvement\)](https://delta.avature.net/en_US/careers/JobDetail?jobId=32928) | US |  | unknown | unknown |
| **GlobalFoundries** | [Global Tapeout and Mask Operations New College Graduate - Biz App and Data Engineer](https://globalfoundries.wd1.myworkdayjobs.com/External/job/USA---Texas---Austin/Global-Tapeout-and-Mask-Operations--Biz-App-and-Data-Engineer--2026-New-College-Graduate-_JR-2502471-1?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **GuideWell Mutual** | [Enterprise Analytics Intern](http://fa-etum-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/41879?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Guidehouse** | [Data Engineer 1](https://guidehouse.wd1.myworkdayjobs.com/external/job/US---TX-San-Antonio/Data-Engineer_42995?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **Guidehouse** | [Data Engineer 1 - Data Science &amp; Analysis](https://guidehouse.wd1.myworkdayjobs.com/external/job/US---TX-San-Antonio/Data-Engineer_43115?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **Hitachi** | [Junior Condition Monitoring and Analytics Engineer](https://hitachi.wd1.myworkdayjobs.com/hitachi/job/HRERSU-London-Ludgate/Maintenance-Analytics-Engineer_R0108106?utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **Knowledge Services** | [Junior Data Engineer](https://careers-knowledgeservices.icims.com/jobs/31209/job?mobile=true&needsRedirect=false&utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **LPL Financial Holdings** | [Data Engineer Intern - Data](https://lplfinancial.wd1.myworkdayjobs.com/university/job/Fort-MillCharlotte/Summer-Intern-2027---Data_R-052914?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **LiveScore Group** | [Junior Data Scientist - Marketing Analytics](https://job-boards.greenhouse.io/livescore9/jobs/8683687002?utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **Loblaw Companies** | [Data Engineer 1](https://myview.wd3.myworkdayjobs.com/paradox_careers/job/1-Presidents-Choice-Circle-Brampton-ON/Data-Engineer-I_R2000691512?utm_source=Simplify&ref=Simplify) | Canada | data-eng | unknown | unknown |
| **Montenson** | [Data Analytics Intern - Insights](https://fa-esgu-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/23342?utm_source=Simplify&ref=Simplify) | Unknown |  | unknown | unknown |
| **Nestle** | [Associate Product Ownership - Junior Data Engineer](https://jobdetails.nestle.com/job/North-York-Associate-Product-Ownership-Jr_-Data-Engineer-(12-months-contract)-ON/1418872933/?ats=successfactors&utm_source=Simplify&ref=Simplify) | Canada | data-eng | unknown | unknown |
| **Publicis Groupe** | [Junior Data Scientist](https://careers.publicisgroupe.com/jobs/155621?icims=1&utm_source=Simplify&ref=Simplify) | UK |  | unknown | unknown |
| **RBI** | [Data Engineer 1](https://rbi.wd3.myworkdayjobs.com/RBI_External_Career_Site/job/Corp---Miami-Corporate-Office/Data-Engineer-I--Burger-King_R3622?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **Sallie Mae** | [Early Career Development Program Associate - Analytics](https://sallie-mae.wd5.myworkdayjobs.com/Careers/job/Newark-DE/Associate--Analytics---Early-Career-Development-Program_R26_000512?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **The Boeing Company** | [Data Analytics Intern](https://boeing.wd1.myworkdayjobs.com/en-US/EXTERNAL_CAREERS/details/Boeing-Summer-2027-Internship-Program--Paid----Data-Analytics-Intern_JR2026520976-1?q=JR2026520976&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **Uline** | [Business Intelligence Developer Intern](https://uline.wd1.myworkdayjobs.com/en-US/Uline_Careers/job/Pleasant-Prairie-WI/Business-Intelligence-Developer-Internship---Summer-2027_R265685?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **University of Maryland - College Park** | [Junior Data Engineer - Faculty Specialist](https://umd.wd1.myworkdayjobs.com/UMCP/job/University-of-Maryland-College-Park/Junior-Data-Engineer--Faculty-Specialist-_JR104102?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **Varsity Brands** | [Data Engineer 1](https://careers.varsitybrands.com/global/en/job/JR114562?utm_source=Simplify&ref=Simplify) | US | data-eng | unknown | unknown |
| **Vertiv** | [Planning Analytics Intern - Summer 2027](https://egup.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX/job/20279236?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Vertiv** | [Sales Data Analytics Intern - Summer 2027](https://egup.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX/job/20279293?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |

_6 more are in [tracker.csv](tracker.csv)._

### Hardware / EE (38 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Hardware Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018880/?gh_jid=8018880&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **DRW** | [FPGA Intern](https://www.drw.com/work-at-drw/listings/fpga-intern-3484423?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **Jane Street** | [Hardware Engineer \(FPGA/ASIC\) Intern](https://www.janestreet.com/join-jane-street/position/8624440002/?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **Optiver** | [FPGA Engineer Intern](https://www.optiver.com/join-us/jobs/8402114002/?gh_jid=8402114002&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Optiver** | [FPGA Engineer Intern](https://www.optiver.com/join-us/jobs/8641352002/?gh_jid=8641352002&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Virtu Financial** | [2027 Internship - FPGA Engineer](https://job-boards.greenhouse.io/virtu/jobs/8638124002) | Ireland | hardware | unknown | unknown |
| **Virtu Financial** | [Hardware Engineer Intern - FPGA 🎓](https://job-boards.greenhouse.io/virtu/jobs/8657286002?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Design Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Design-Engineer---New-College-Grad-2026_JR2021534?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Physical Design Engineer New Grad - Netlisting 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Physical-Design-Engineer--Netlisting---New-College-Grad-2026_JR2017681?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Physical Design and Timing Engineer – New College Grad 🎓](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Timing-Engineer---New-College-Grad-2026_JR2013177?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [ASIC Verification Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/ASIC-Verification-Engineer---New-College-Grad-2026_JR2020640?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [Low Power ASIC Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Low-Power-ASIC-Engineer---New-College-Grad-2026_JR2017005?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **AeroVironment** | [Software Engineer 1 - Embedded](https://avav.wd1.myworkdayjobs.com/en-US/avav/job/Sunrise-FL/Software-Engineer-I-1_8366?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Apex Technology, Inc.** | [Software Engineering Intern, Embedded Systems](https://jobs.ashbyhq.com/apex-technology-inc/5ec2dfa9-724d-4ce4-ab97-5067ec747f11?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **Blue Origin** | [Avionics / Embedded Software Engineer 1 - Early Career](https://blueorigin.wd5.myworkdayjobs.com/blueorigin/job/Greater-Seattle-Area/Avionics---Embedded-Software-Engineer-I---Early-Career--2026-Starts-_R70055?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Ciena** | [Embedded Software Developer New Grad](https://ciena.wd5.myworkdayjobs.com/Careers/job/Ottawa/Embedded-Software-Developer---New-Grad_R031490?utm_source=Simplify&ref=Simplify) | Canada | hardware | unknown | unknown |
| **DMC Engineering** | [Entry Level Embedded Engineer](https://www.dmcinfo.com/careers/open-positions?gh_jid=5136284008&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Etched** | [Firmware Intern](https://jobs.ashbyhq.com/Etched/8134a9bf-9624-48dd-98be-0bf1c3cb1f55?utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **Garmin** | [Embedded Software Engineer 1](https://careers.garmin.com/jobs/19134?icims=1&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Garmin** | [Software Engineer 1 - Embedded Aviation](https://careers.garmin.com/jobs/18513?icims=1&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Gentex Corporation** | [Embedded Software Engineer 1](https://gentex.wd5.myworkdayjobs.com/Gentex/job/Zeeland-MI/Embedded-Software-Engineer-I_REQ026014?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **HPR \(Hyannis Port Research\)** | [FPGA Engineer Intern](https://job-boards.greenhouse.io/hyannisportresearch/jobs/7822801003?utm_source=Simplify&ref=Simplify) | US | hardware,research | unknown | unknown |
| **Honeywell** | [Embedded Engineer 1 New Grad](https://ibqbjb.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/Honeywell/job/140055?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Honeywell** | [Hardware Engineer 1](https://ibqbjb.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/Honeywell/job/137946?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Midmark** | [Firmware Engineering Co-op \(Spring 2027\)](https://hcor.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/4333) | US | hardware | unknown | unknown |
| **Observable Space** | [Junior Embedded Software Engineer](https://jobs.ashbyhq.com/observable-space/97e8073f-a23e-4360-ba9c-a3869ad58ab1/application?embed=true&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Panasonic Holdings** | [Software Engineer 1 - Embedded Systems](https://careers.na.panasonic.com/jobs/50269?icims=1&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **RTX** | [Digital Hardware Engineer 1](https://globalhr.wd5.myworkdayjobs.com/rec_rtx_ext_gateway/job/US-AL-HUNTSVILLE-315--315-Bob-Heath-Dr--BOB-HEATH/Digital-Hardware-Engineer-I_01841999-1?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **RTX** | [Embedded Software Engineer 1](https://globalhr.wd5.myworkdayjobs.com/rec_rtx_ext_gateway/job/US-IA-CEDAR-RAPIDS-137--855-35Th-St-NE--BLDG-137/Embedded-Software-Engineer-I--Onsite-_01866161-1?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **RTX** | [Embedded Software Engineer 1](https://globalhr.wd5.myworkdayjobs.com/fr-CA/Private_Posting_No_TMP/job/US-CT-EAST-HARTFORD-ETC--400-Main-St--BLDG-ETC/Embedded-Software-Engineer---P1_01864540?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **RTX** | [FPGA Engineer 1](https://globalhr.wd5.myworkdayjobs.com/rec_rtx_ext_gateway/job/US-AL-HUNTSVILLE-315--315-Bob-Heath-Dr--BOB-HEATH/FPGA-Engineer-I_01863350-1?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **RTX** | [FPGA Engineer 1](https://globalhr.wd5.myworkdayjobs.com/rec_rtx_ext_gateway/job/US-TX-MCKINNEY-513WD--2501-W-University-Dr--WING-D-BLDG/FPGA-Engineer-I_01857935?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **RTX** | [FPGA Engineer 1 - Airborne RF Electronics Design](https://globalhr.wd5.myworkdayjobs.com/rec_rtx_ext_gateway/job/US-TX-MCKINNEY-513WC--2501-W-University-Dr--WING-C-BLDG/FPGA-Engineer-I_01866334-1?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Revel** | [Embedded Software Engineer - Entry-Junior](https://jobs.ashbyhq.com/revel/444b5704-3840-4b0a-ba34-f82eab8c430f/application?embed=true&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Seagate Technology** | [Firmware Engineer - Early Career 🎓](https://seagatecareers.com/job/Longmont-Firmware-Engineer-Early-Career-CO-80501/1417701800/?ats=successfactors&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **TETRAMEM** | [Software Engineer Intern, Embedded](https://tetramem.hrmdirect.com/employment/job-opening.php?req=3491042#job&utm_source=github-vansh-ouckah) | US | hardware | unknown | unknown |
| **TP-Link Systems** | [Early Career Embedded Software Engineer](https://apply.workable.com/tp-link-usa-corp/j/F943A617EC/apply?utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **🔥 ByteDance** | [ASIC Design Engineer Intern - Video Silicon IP](https://jobs.bytedance.com/en/position/7673638856678279429/detail?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |

### Systems & Infra (38 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Akuna Capital** | [Platform Engineer Intern 🇺🇸](https://akunacapital.com/careers/job/8018856/?gh_jid=8018856&utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **DRW** | [Platform Engineer Intern](https://www.drw.com/work-at-drw/listings/platform-engineer-intern-3468737?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **🔥 NVIDIA** | [Backend Compiler Engineer New Grad](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Backend-Compiler-Engineer---New-College-Grad-2026_JR2021242?utm_source=Simplify&ref=Simplify) | US / Canada |  | unknown | unknown |
| **Cerebras Systems** | [DevOps Engineer - New Grad 2026](https://jobs.ashbyhq.com/cerebras/40e0d3ee-8f0a-4b19-9bf9-79410b1c7735) | Canada | infra,distributed,research | unknown | unknown |
| **Cerebras Systems** | [Software Engineer - New Grad 2026](https://jobs.ashbyhq.com/cerebras/99c289fa-8fc6-49f7-b7e8-78ac4e9d99ac/application?utm_source=Simplify&ref=Simplify) | US / Canada | hardware,infra,distributed,research | unknown | unknown |
| **Cloudflare** | [Systems Engineer - Global Resource Management \(Data Residency\)](https://boards.greenhouse.io/cloudflare/jobs/8015230?gh_jid=8015230) | Unknown |  | unknown | unknown |
| **Notion** | [Software Engineer, Early Career](https://jobs.ashbyhq.com/notion/297b4ece-765f-4eea-b1b8-46057cb6501f/application?utm_source=Simplify&ref=Simplify) | US | autonomy,infra,distributed,research | unknown | posting mentions equity |
| **Notion** | [Software Engineer, Early Career \(AI\)](https://jobs.ashbyhq.com/notion/85947779-6b87-466a-98bc-30a640448c28/application?utm_source=Simplify&ref=Simplify) | US | autonomy,infra,distributed | unknown | posting mentions equity |
| **Perplexity** | [AI Inference Internship](https://jobs.ashbyhq.com/perplexity/79a07e2d-6150-4929-80fe-bbe13a641763) | UK | infra,distributed,phd-position | unknown | unknown |
| **Perplexity** | [Internship - Search Backend Infra Engineer](https://jobs.ashbyhq.com/perplexity/be94e89b-89d5-4f2a-a58b-7929c8d97f92) | Serbia | infra,distributed | unknown | unknown |
| **Applied Materials** | [Software Engineer New Grad - DevOps](https://amat.wd1.myworkdayjobs.com/External/job/GloucesterMA/XMLNAME-2027-Software-Engineer--DevOps---New-College-Grad---Bachelor-s--Gloucester--MA-_R2625762?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **Blissway** | [Embedded Systems Engineer New Grad](https://jobs.ashbyhq.com/blissway/51d6d839-9801-4436-bfc2-918bae428ed8/application?embed=true&utm_source=Simplify&ref=Simplify) | US | hardware | unknown | unknown |
| **Crusoe** | [Software Engineer 1 - Storage](https://jobs.ashbyhq.com/Crusoe/4f5d34ed-0c05-4eec-b8f8-14663e114b02/application?embed=true&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Dedalus Labs** | [Systems Engineer / Product Manager Intern \(Summer 2027\)](https://www.ycombinator.com/companies/dedalus-labs/jobs/YtbvXM8-systems-engineer-summer-2027-intern) | US |  | unknown | unknown |
| **Etched** | [Infrastructure Intern](https://jobs.ashbyhq.com/Etched/80926a71-0a62-4bf8-a877-b6d96df279b7?utm_source=github-vansh-ouckah) | US | infra | unknown | unknown |
| **Etched AI** | [Chip Simulation Software Intern](https://jobs.ashbyhq.com/etched/27e5bd6b-9357-45f0-9e79-cfa2bf4eeba8) | Unknown | hardware,infra,research,phd-position | unknown | unknown |
| **Etched AI** | [Electrical Platform Intern](https://jobs.ashbyhq.com/etched/904ddf46-55fc-4a8f-8b49-f32cfe88116a) | Unknown | hardware,infra,research | unknown | unknown |
| **Etched AI** | [Firmware Intern](https://jobs.ashbyhq.com/etched/699f3ab2-07e4-466c-9d76-3d4a3abb4ebc) | Unknown | hardware,infra,research,phd-position | unknown | unknown |
| **Etched AI** | [Performance Tools Intern](https://jobs.ashbyhq.com/etched/f02e8035-7dc9-4b0c-aab7-75bbb4e975b8) | Unknown | hardware,infra,research | unknown | unknown |
| **Everfox** | [Embedded Systems Engineer 1](https://evergreenix.wd1.myworkdayjobs.com/external-careers2/job/UK---London/Embedded-Systems-Engineer-I_JR500701?utm_source=Simplify&ref=Simplify) | UK | hardware | unknown | unknown |
| **FactSet** | [Software Engineer 1 - Infrastructure](https://factset.wd108.myworkdayjobs.com/FactSetCareers/job/London-GBR/Software-Engineer-I--Infrastructure_R32300?utm_source=Simplify&ref=Simplify) | UK | infra | unknown | unknown |
| **General Dynamics Information Technology** | [Systems Engineer Intern](https://www.gd.com/careers/systems-engineer-intern-albany-ny-us-rq225289-gdit-opportunity?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **General Dynamics Mission Systems** | [Entry Level Infrastructure Software Engineer](https://careers-gdms.icims.com/jobs/72580/job?mobile=true&needsRedirect=false&utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **Lightfield** | [Early Career Infrastructure Software Engineer](https://jobs.ashbyhq.com/Lightfield/9a7ef2f9-577a-4242-b884-719e3cdf4420/application?embed=true&utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **Poshmark** | [Cloud Platform Engineer Intern, Growth 🛂](https://jobs.ashbyhq.com/poshmark/062b84e6-1633-43ae-870b-83cb62893caa?utm_source=github-vansh-ouckah) | US |  | unknown | unknown |
| **StepStone Group** | [Private Equity Infrastructure &amp; Real Assets Summer Analyst 🛂](https://www.stepstonegroup.com/current-opportunities/?gh_jid=7872890) | US | infra | unknown | unknown |
| **🔥 ByteDance** | [AI Network Automation Engineer Intern - Global Physical Network Infrastructure](https://jobs.bytedance.com/en/position/7670690923748870405/detail?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 ByteDance** | [Backend and Infrastructure Software Engineer New Grad - Dev Infra](https://jobs.bytedance.com/en/position/7667894766036322565/detail?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 ByteDance** | [Software Engineer Intern - AI Infrastructure Compute 🎓](https://jobs.bytedance.com/en/position/7667377525182662965/detail?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 ByteDance** | [Software Engineer Intern - Traffic Infrastructure](https://jobs.bytedance.com/en/position/7672626707586746629/detail?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 ByteDance** | [Software Engineer New Grad - AI Infrastructure-Compute Efficiency &amp; Scheduling](https://jobs.bytedance.com/en/position/7668799020705679669/detail?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 ByteDance** | [Software Engineer New Grad - Traffic Infrastructure](https://jobs.bytedance.com/en/position/7665849950984194309/detail?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 Oracle** | [Systems Software Engineer 1 - Cloud Infrastructure](https://eeho.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_45001/job/342326?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 TikTok** | [AI Agent Product Manager Intern - Product Infrastructure-Customer Service Platform](https://lifeattiktok.com/search/7670010726514493749?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 TikTok** | [Backend Software Engineer Intern - Product Infrastructure](https://lifeattiktok.com/search/7667935633764370741?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 TikTok** | [Product Manager Intern - Product Infrastructure - Account](https://lifeattiktok.com/search/7670009830602721589?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |
| **🔥 TikTok** | [Research Engineer Intern - Agentic Systems &amp; AI Infrastructure - Generalized Architecture](https://lifeattiktok.com/search/7667934792727906565?utm_source=Simplify&ref=Simplify) | US | infra,research | unknown | unknown |
| **🔥 TikTok** | [Software Engineer New Grad - Ads Infrastructure](https://lifeattiktok.com/search/7668879883938203957?utm_source=Simplify&ref=Simplify) | US | infra | unknown | unknown |

### Computational Science (17 live)

| Company | Role | Region | Focus | Company signal | Equity signal |
|--|--|--|--|--|--|
| **Palantir** | [Forward Deployed Software Engineer, Internship](https://jobs.lever.co/palantir/1b6f1d82-d459-4dea-8bc2-8d2ffe6f881a) | France | autonomy,computer-vision,infra,security | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - France](https://jobs.lever.co/palantir/ac0dc094-2480-43c2-8495-26ade227ff4f) | US | infra,funded | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - Intel](https://jobs.lever.co/palantir/9e40d77f-b07c-437b-98e7-def9b0184d89) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - Poland](https://jobs.lever.co/palantir/d582cd84-14fd-4aa3-b413-15982d286bd9) | US | infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - US Government](https://jobs.lever.co/palantir/315f695d-04d1-4a9a-848e-cb2bec7a997e) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - US Government](https://jobs.lever.co/palantir/e0010393-c300-446f-bf67-fa2ef067f16f) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Forward Deployed Software Engineer, Internship - US Government](https://jobs.lever.co/palantir/e6ff8bf2-135e-474d-ad37-24f490ae1dd2) | US | computer-vision,infra | unknown | unknown |
| **Palantir** | [Software Engineer, Internship](https://jobs.lever.co/palantir/76a60923-bb49-40f5-b061-7c7eb1299602) | UK | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, Internship - Infrastructure](https://jobs.lever.co/palantir/fd3603a9-7016-45c6-9c8d-04c9279ab85e) | UK | computer-vision,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad](https://jobs.lever.co/palantir/d372c805-d0cd-4a10-9522-fbecc78d6f3e/apply?utm_source=Simplify&ref=Simplify) | UK | computer-vision,data-eng,infra,research | unknown | unknown |
| **Palantir** | [Software Engineer, New Grad - Infrastructure](https://jobs.lever.co/palantir/9265acce-12cd-4179-8c50-55d15963532b/apply?utm_source=Simplify&ref=Simplify) | UK | computer-vision,infra,research | unknown | unknown |
| **Snowflake** | [Software Engineer Intern - Berlin \(2026\)](https://jobs.ashbyhq.com/snowflake/41e65c6c-a01e-4f40-af14-ae75d3b95e27) | Germany | hardware,data-eng,infra,distributed,research,phd-position | unknown | unknown |
| **BP** | [Geoscience Intern - Geoscientist 🎓](https://bpinternational.wd3.myworkdayjobs.com/bpEarlyCareers/job/United-States-of-America---Texas---Houston/Summer-Intern---Geoscientist---Houston-TX_RQ114816?utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [AI/ML Data Scientist/Engineer New Grad - Analytic Capabilities 🎓](https://careers.jhuapl.edu/jobs/57801?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Data Scientist New Grad - Data Science - System Performance Evaluation](https://careers.jhuapl.edu/jobs/57653?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **Johns Hopkins Applied Physics Laboratory** | [Systems Engineer/Analyst New Grad - Multi-Mission Planning Development 🎓](https://careers.jhuapl.edu/jobs/58164?icims=1&utm_source=Simplify&ref=Simplify) | US |  | unknown | unknown |
| **University Corporation for Atmospheric Research** | [CESM Software Engineer 1 - Computer Engineering](https://ucar.wd5.myworkdayjobs.com/UCAR_Careers/job/Boulder-CO/CESM-Software-Engineer-I_REQ-2026-117-1?utm_source=Simplify&ref=Simplify) | US | research,climate | unknown | unknown |

### Early-company / equity reality check

The company signal is a discovery aid, not a prediction. Private-company options can become valuable, but can also expire, dilute, remain illiquid, or end up worth zero. `private company; verify offer` means the posting does not prove that equity is included. Ask for the option count **and fully diluted percentage**, strike price, vesting/cliff, exercise window, latest common valuation, and liquidation preferences.

## Elite and high-tier live postings (316)

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
| **Cubist Systematic Strategies** | [Quantitative Developer Intern](https://job-boards.greenhouse.io/embed/job_app?for=point72&jr_id=6a07069024dcb03739f1ec72&token=7297613002&utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
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
| **Hudson River Trading** | [Software Engineer Intern](https://www.hudsonrivertrading.com/hrt-job/software-engineering-internship-c-or-python-summer-2027/?gh_src=&utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
| **Hudson River Trading** | [Software Engineer Intern - C++ or Python](https://www.hudsonrivertrading.com/careers/job/?gh_jid=8052083&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Ambiguous | review required |
| **IMC** | [Software Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823924101) | Software Engineering | US | Summer 2027 | review required |
| **IMC Trading** | [Graduate Quantitative Researcher \(PhD\)](https://job-boards.eu.greenhouse.io/imc/jobs/4912325101) | Quant / Finance | US | Unknown | review required |
| **IMC Trading** | [Hardware Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823945101?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Hardware Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4927149101) | Quant / Finance | Netherlands | Unknown | review required |
| **IMC Trading** | [Hardware Machine Learning PhD Research Internship](https://job-boards.eu.greenhouse.io/imc/jobs/4829785101) | Quant / Finance | US | Unknown | review required |
| **IMC Trading** | [Machine Learning Research Intern 🎓](https://job-boards.eu.greenhouse.io/imc/jobs/4912874101?utm_source=Simplify&ref=Simplify) | Quant / Finance | Netherlands | Summer 2027 | review required |
| **IMC Trading** | [Machine Learning Research Intern 🎓](https://job-boards.eu.greenhouse.io/imc/jobs/4907430101?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Quant Research Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941208101) | Quant / Finance | Hong Kong | 2027 | review required |
| **IMC Trading** | [Quantitative Research Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4907399101?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Quantitative Trader Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4823923101?utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Summer 2027 | review required |
| **IMC Trading** | [Quantitative Trader Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4936262101) | Quant / Finance | Netherlands | Unknown | review required |
| **IMC Trading** | [Software Engineer Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4667854101) | Quant / Finance | Netherlands | Unknown | review required |
| **IMC Trading** | [Software Engineer Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941206101) | Quant / Finance | Hong Kong | 2027 | review required |
| **IMC Trading** | [Software Engineer, Early Career](https://job-boards.eu.greenhouse.io/imc/jobs/4577504101) | Quant / Finance | US | Unknown | review required |
| **IMC Trading** | [Trader Intern](https://job-boards.eu.greenhouse.io/imc/jobs/4939846101) | Quant / Finance | Netherlands | Unknown | review required |
| **IMC Trading** | [Trader Intern 2027](https://job-boards.eu.greenhouse.io/imc/jobs/4941205101) | Quant / Finance | Hong Kong | 2027 | review required |
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
| **Jump Trading** | [Campus ASIC Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7974837) | Quant / Finance | Unknown | Unknown | review required |
| **Jump Trading** | [Campus C++ Software Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027946) | Quant / Finance | Singapore | Unknown | review required |
| **Jump Trading** | [Campus Crypto Researcher \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7362318) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus Data Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7975008) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus Data Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8002998) | Quant / Finance | US | Unknown | review required |
| **Jump Trading** | [Campus FPGA Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7974391) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus FPGA Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8003013) | Quant / Finance | US | Unknown | review required |
| **Jump Trading** | [Campus ML Research Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7977145) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus Python Software Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027955) | Quant / Finance | Singapore | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Researcher \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8010307) | Quant / Finance | Netherlands | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Researcher \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027939) | Quant / Finance | Singapore | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Researcher \(M1/M2 Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8059384) | Quant / Finance | France | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Researcher Intern - PhD 🎓](https://boards.greenhouse.io/embed/job_app?token=8049938&utm_source=Simplify&ref=Simplify) | Quant / Finance | US | Ambiguous | review required |
| **Jump Trading** | [Campus Quantitative Researcher, UG/MS \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7982648) | Quant / Finance | US | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Trader \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027941) | Quant / Finance | Singapore | Unknown | review required |
| **Jump Trading** | [Campus Quantitative Trader \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8050772) | Quant / Finance | Netherlands | Unknown | review required |
| **Jump Trading** | [Campus Software Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7975026) | Quant / Finance | UK | Unknown | review required |
| **Jump Trading** | [Campus Systems Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8027952) | Quant / Finance | Singapore | Unknown | review required |
| **Jump Trading** | [Campus Systems Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=8000323) | Quant / Finance | Netherlands | Unknown | review required |
| **Jump Trading** | [Campus Systems Engineer Intern](https://www.jumptrading.com/hr/job?gh_jid=8007788&utm_source=github-vansh-ouckah) | Quant / Finance | US | Summer 2027 | review required |
| **Jump Trading** | [Campus Trading Team Software Engineer  \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7565728) | Quant / Finance | Hong Kong | Unknown | review required |
| **Jump Trading** | [Campus UI Software Engineer \(Intern\)](https://www.jumptrading.com/hr/job?gh_jid=7974943) | Quant / Finance | UK | Unknown | review required |

_216 more are in [tracker.csv](tracker.csv)._

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
