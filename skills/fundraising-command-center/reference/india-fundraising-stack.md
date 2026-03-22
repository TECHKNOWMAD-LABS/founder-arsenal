---
name: "india-fundraising-stack"
description: "Comprehensive India-specific fundraising reference covering DPIIT recognition, central/state government schemes, grants, tax benefits, SEBI/RBI/FEMA regulations, Indian VC ecosystem, angel networks, accelerators, capital instruments compliant with Indian law, and auto-matching engine for scheme eligibility. Use when user mentions Indian startup, India fundraising, DPIIT, angel tax, SEBI, RBI, FEMA, state startup policy, SISFS, MUDRA, SIDBI, AIM, BIRAC, MeitY, iDEX, or any India-specific capital raising."
type: reference
---

# India Fundraising Stack

Complete reference for raising capital in India. Covers 200+ government schemes across 34 ministries, 50+ foundations/special bodies, sector-specific grants across 15+ verticals, all 28 state + 8 UT policies, regulatory frameworks, and the full domestic investor ecosystem.

## Reference File Architecture

This is the index file. Detailed data lives in companion references — load on demand by sector:

| Reference File | Lines | Coverage |
|---------------|-------|----------|
| [`india-govt-schemes-master.md`](india-govt-schemes-master.md) | 1,282 | 135+ schemes across 34 ministries/departments |
| [`india-foundations-directory.md`](india-foundations-directory.md) | 829 | 50+ special bodies, foundations (Indian + international) |
| [`india-sector-grants.md`](india-sector-grants.md) | 900 | 68+ sector-specific grants, challenges, innovation programs |

**Loading protocol:** Load this index file first. When user's sector/need is identified, load the relevant companion file for detailed scheme data.

---

## EXPANDED AUTO-MATCH ENGINE (200+ Schemes)

When a user describes their startup in conversation, extract these signals and match against the FULL scheme database:

### Signal Extraction Template

```
COMPANY PROFILE:
- Sector: [extract from conversation]
- Stage: [idea/prototype/revenue/scaling]
- Age: [years since incorporation]
- Turnover: [last FY]
- Location: [state/city]
- Entity type: [Pvt Ltd/LLP/Partnership/OPC]
- DPIIT recognized: [yes/no/unknown]
- Founder demographics: [women/SC/ST/PH/minority/general]
- Revenue model: [B2B SaaS/B2C/marketplace/hardware/deep tech/biotech/agritech/defence/space]
- Employees: [count, % in India]
- Foreign investors: [yes/no/planned]
- IP status: [patents filed/granted/none]

MATCHING CRITERIA:
1. Central schemes → match by sector + stage + turnover + age
2. State schemes → match by registered office location
3. Sector-specific → match by industry vertical
4. Demographic bonuses → women/SC/ST/PH get enhanced benefits
5. Regulatory requirements → FEMA/SEBI based on investor nationality
```

### Auto-Match Decision Tree

```
START
├── Is the startup DPIIT recognized?
│   ├── No → PRIORITY: Get DPIIT recognition first (unlocks 90% of schemes)
│   │   (Eligibility: Pvt Ltd/LLP/Partnership; <10yr old, 20yr for deep tech;
│   │    turnover <INR 200Cr, INR 300Cr for deep tech)
│   └── Yes → Continue
│
├── What stage?
│   ├── Idea/Prototype →
│   │   ├── Central: SISFS (up to 20L), AIM-ANIC, DST-NIDHI PRAYAS (10L)
│   │   ├── State: Match by location (see state table)
│   │   ├── Sector: See SECTOR MATCH below
│   │   └── Foundations: Social Alpha Quest (50L), Tata Social Enterprise Challenge (1Cr),
│   │       HDFC Parivartan SmartUp (50L), Wadhwani Liftoff (zero-equity)
│   │
│   ├── Early Revenue →
│   │   ├── Central: SISFS (up to 50L), MUDRA Kishore/Tarun (5-20L), CGTMSE (up to 5Cr)
│   │   ├── State: Match by location
│   │   ├── Sector: See SECTOR MATCH below
│   │   └── VC/Angels: IAN, LetsVenture, IPV, Venture Catalysts, Titan Capital, Better Capital
│   │
│   └── Scaling →
│       ├── Central: SIDBI FoF (via AIFs), CGSS (up to 10Cr guarantee)
│       ├── VC/PE: Peak XV, Accel, Elevation, Blume, Kalaari, etc.
│       ├── International: Gates Foundation, USAID DIV, IFC, ADB
│       └── Cross-border: FEMA compliance for foreign capital
│
├── SECTOR MATCH (load india-sector-grants.md for details):
│   ├── Defence/Aerospace → iDEX DISC/ADITI (up to 25Cr), DRDO TDF (up to 50Cr),
│   │   Navy SPRINT, Army/IAF challenges, BEL, HAL
│   ├── Space → IN-SPACe TAF (up to 25Cr), VC Fund (10,000Cr), NSIL tech transfer
│   ├── Biotech/Pharma → BIRAC (BIG 50L, SBIRI, BIPP, PACE, SEED, LEAP, SPARSH, E-YUVA),
│   │   ICMR (up to 15Cr CAR), DBT, National Biopharma Mission ($250M), Wellcome Trust
│   ├── Healthcare → ICMR FIWC (8Cr), Ayushman Bharat, Grand Challenges India,
│   │   National Health Mission innovation
│   ├── Agriculture/Food → RKVY-RAFTAAR (up to 25L seed), NABARD AgriSURE (750Cr),
│   │   NABARD NGIF/NCF (1,300Cr), ICAR, MANAGE-CIA, MoFPI PMKSY/PMFME/PLI,
│   │   ITC Agri Udaan, Omnivore, Ankur Capital
│   ├── Energy/CleanTech → MNRE solar/wind, National Green Hydrogen Mission (19,744Cr,
│   │   up to 5Cr per startup), BEE ADEETIE (1,000Cr), NTPC/NHPC challenges,
│   │   CII ASCEND, Social Alpha Techtonic
│   ├── Fintech → RBI Innovation Hub (RBIH), IFSCA sandbox (GIFT City grants 15-75L),
│   │   SEBI Innovation Sandbox, IRDAI sandbox, NPCI programs, SIDBI fintech
│   ├── IT/Software/AI → MeitY GENESIS (490Cr), SAMRIDH (40L), TIDE 2.0,
│   │   NASSCOM DeepTech Club, Google for Startups, Microsoft for Startups,
│   │   AWS Activate (up to $100K credits)
│   ├── Education → Smart India Hackathon, IIC programs, AICTE/UGC,
│   │   NISP (1% institutional budget for innovation), Toycathon, Manthan
│   ├── Water/Sanitation → Atal Bhujal Yojana, Namami Gange tech, WASH challenges
│   ├── Urban/Smart Cities → Smart Cities CIX, AMRUT, India Urban Data Exchange
│   ├── Textiles/Fashion → SAMARTH, National Technical Textiles Mission,
│   │   Silk Samagra, PowerTex India
│   ├── Electronics/Semiconductor → India Semiconductor Mission 2.0 (76,000Cr),
│   │   DLI scheme, SPECS, Modified ESDM
│   ├── Logistics/Mobility/EV → PM E-DRIVE (10,900Cr), PLI Auto (25,938Cr),
│   │   PM Gati Shakti, Sagarmala S2I2
│   ├── Rural/Social Impact → SVEP, DAY-NRLM, VCF-SC (500Cr), ASIIM (30L per SC startup),
│   │   National SC/ST Hub (25% capital subsidy up to 1Cr), Acumen Fund,
│   │   Village Capital, Aavishkaar
│   ├── Creative/AVGC → AVGC-XR task force, NFDC, India Design Council,
│   │   TN AVGC grants (250Cr + 1Cr per startup)
│   ├── Tourism → Swadesh Darshan 2.0, PRASHAD scheme
│   ├── Fisheries → PMMSY (20,050Cr), Blue Revolution
│   ├── Animal Husbandry/Dairy → AHIDF (15,000Cr), NLM
│   ├── Mining/Steel/Coal → Steel Research Mission, Coal Startup Innovation Challenge
│   ├── Chemicals/Pharma → Bulk Drug Parks, Medical Device Parks, PLI Pharma (15,000Cr)
│   ├── Earth Sciences/Ocean → MoES programs, Deep Ocean Mission
│   ├── Nuclear/Atomic Energy → Nuclear Energy Mission (20,000Cr for SMRs)
│   ├── Railways → Rail Tech Innovation Portal, Rail Innovation Challenge
│   ├── Civil Aviation/Drones → PLI Drones (120Cr), UDAN scheme
│   └── MSME (any sector) → CLCSS (15% subsidy), ZED, SFURTI, ASPIRE,
│       MSME Champions, IP Facilitation, TReDS, SAMBANDH procurement,
│       Digital MSME, MSE-CDP cluster development
│
├── FOUNDATION/SPECIAL BODY MATCH (load india-foundations-directory.md):
│   ├── Social Impact → Tata Trusts/Social Alpha, Azim Premji Foundation,
│   │   Skoll Foundation ($1-1.5M), Acumen ($42.5M India), Villgro
│   ├── Women-led → NITI Aayog WEP, NASSCOM Tech.WE, TiE Women ($100K+),
│   │   Stand-Up India, PMEGP enhanced (10% extra)
│   ├── SC/ST-led → VCF-SC/ASIIM (30L), Stand-Up India, National SC/ST Hub,
│   │   Karnataka ELEVATE Unnati, PMEGP enhanced
│   ├── Tribal → TRIFED Van Dhan, UNNATI for NE states
│   ├── Student → SSIP Gujarat, Smart India Hackathon, IIC, TiE University,
│   │   Wadhwani Ignite, AICTE programs
│   ├── International funding → Gates Foundation, USAID DIV (up to $15M tiered),
│   │   UNDP Youth Co:Lab (3.5L), UNICEF Venture Fund ($100K),
│   │   World Bank, ADB ($846M skills), IFC ($16.72B India),
│   │   JICA, GIZ, Ford Foundation, Rockefeller, MacArthur
│   ├── Tech giants → Google for Startups ($350K credits + $2M AI),
│   │   Microsoft ($150K credits), Amazon ASVF ($350M fund),
│   │   AWS Activate ($100K credits)
│   └── Industry bodies → NASSCOM (8,600+ startups), FICCI, CII, TiE,
│       Wadhwani Foundation (INR 300Cr invested)
│
├── Is the founder women/SC/ST/PH/minority/tribal?
│   ├── Yes → Flag enhanced benefits across ALL matching schemes
│   │   (typically +5-35% additional subsidy or reserved allocation)
│   └── No → Standard benefits
│
├── Is the startup in Northeast India?
│   ├── Yes → UNNATI (INR 10,037Cr for all 8 NE states), NEVF,
│   │   state-specific NE policies, enhanced PMEGP rates
│   └── No → Continue
│
├── Does the startup have foreign investors or plans for foreign capital?
│   ├── Yes → Trigger FEMA/FDI compliance checklist
│   │   (FC-GPR within 30 days, Rule 11UA pricing, Press Note 3 for China)
│   └── No → Domestic instruments only
│
└── OUTPUT: Ranked list of ALL eligible schemes with:
    - Scheme name and administering body
    - Funding amount/range
    - Eligibility match confidence (high/medium/low)
    - Application method and URL
    - Enhanced benefits for demographics if applicable
    - Recommended stacking order
```

### Ministry-Level Coverage Map (34 Ministries)

| Ministry/Department | Schemes | Key Programs | Reference File |
|-------------------|---------|--------------|----------------|
| Commerce & Industry (DPIIT) | 7 | SISFS, FFS, CGSS, SIPP, 80-IAC | india-govt-schemes-master.md |
| MSME | 13 | CLCSS, ZED, SFURTI, ASPIRE, Champions, TReDS | india-govt-schemes-master.md |
| Agriculture | 5+ | RKVY-RAFTAAR, MIDH, e-NAM, ACABC | india-govt-schemes-master.md |
| Food Processing | 4 | PMKSY, PMFME, PLI Food, Mega Food Parks | india-govt-schemes-master.md |
| Textiles | 4 | SAMARTH, PowerTex, Silk Samagra, NTTM | india-govt-schemes-master.md |
| Fisheries/Animal Husbandry | 4 | PMMSY, Blue Revolution, AHIDF, NLM | india-govt-schemes-master.md |
| Renewable Energy | 4 | PM-KUSUM, Green Hydrogen, solar schemes | india-govt-schemes-master.md |
| Environment | 2 | CAMPA, National Clean Energy Fund | india-govt-schemes-master.md |
| Health | 3 | Ayushman Bharat infra, NHM, PMBJP | india-govt-schemes-master.md |
| Education | 5 | SPARC, IMPRINT, IIC, SIH, NISP | india-govt-schemes-master.md |
| Rural Development | 3 | DAY-NRLM, DDU-GKY, SVEP | india-govt-schemes-master.md |
| Housing & Urban | 3 | Smart Cities, AMRUT, CIX | india-govt-schemes-master.md |
| Social Justice | 4 | VCF-SC, ASIIM, Stand-Up India, SC/ST Hub | india-govt-schemes-master.md |
| Tribal Affairs | 2 | Van Dhan, TRIFED programs | india-govt-schemes-master.md |
| Minority Affairs | 2 | USTTAD, Seekho Aur Kamao | india-govt-schemes-master.md |
| Women & Child Dev | 2 | WEP, Mahila E-Haat | india-govt-schemes-master.md |
| Skill Development | 3 | PMKVY, SANKALP, JSS | india-govt-schemes-master.md |
| Culture | 1 | Heritage/creative economy | india-govt-schemes-master.md |
| Tourism | 2 | Swadesh Darshan 2.0, PRASHAD | india-govt-schemes-master.md |
| Ports/Shipping | 2 | Sagarmala, S2I2 | india-govt-schemes-master.md |
| Civil Aviation | 2 | UDAN, Drone PLI | india-govt-schemes-master.md |
| Railways | 2 | Innovation portal, Rail Tech Policy 2026 | india-govt-schemes-master.md |
| Coal | 1 | Coal Startup Innovation Challenge | india-govt-schemes-master.md |
| Steel | 1 | Steel Research & Tech Mission | india-govt-schemes-master.md |
| Chemicals/Pharma | 3 | Bulk Drug Parks, Medical Device Parks, PLI | india-govt-schemes-master.md |
| Earth Sciences | 2 | Deep Ocean Mission, MoES programs | india-govt-schemes-master.md |
| Jal Shakti | 2 | Atal Bhujal Yojana, Namami Gange | india-govt-schemes-master.md |
| Power/Heavy Industries | 3 | PM E-DRIVE, Smart Grid, UJALA | india-govt-schemes-master.md |
| Atomic Energy | 2 | Nuclear Energy Mission, tech transfer | india-govt-schemes-master.md |
| Defence/DRDO | 8 | iDEX, TDF, DARE to DREAM, SPRINT | india-sector-grants.md |
| CSIR | 2 | Innovation Complexes, URDIP IPR | india-govt-schemes-master.md |
| ICMR | 5 | FIWC, CAR, GIA, extramural grants | india-sector-grants.md |
| ICAR | 2 | Agri innovation, KVK programs | india-govt-schemes-master.md |
| NITI Aayog/AIM | 6 | AIM 2.0, AICs, ANIC, WEP | india-foundations-directory.md |

---

## 1. DPIIT RECOGNITION (Gateway to Everything)

### What It Unlocks
- Section 80-IAC: 3-year income tax holiday
- Angel Tax exemption (abolished from FY 2024-25, but recognition still needed for other benefits)
- Self-certification under 6 labour laws and 3 environmental laws
- Fast-track patent examination (80% fee rebate)
- Priority in government procurement (relaxed turnover/experience criteria)
- Access to SISFS, CGSS, and most state schemes
- Fund of Funds access via SIDBI

### Eligibility
- Entity type: Private Limited, LLP, or Registered Partnership
- Age: Not more than 10 years from incorporation (5 years for LLP prior to amendment)
- Turnover: Not exceeded INR 100 crore in any FY
- Working toward innovation, development, or improvement of products/processes/services
- Not formed by splitting or restructuring existing business

### Process
1. Register on Startup India portal (startupindia.gov.in)
2. Submit incorporation certificate, description of innovation
3. Auto-recognition for entities meeting criteria
4. For tax benefits (80-IAC): Apply separately to Inter-Ministerial Board (IMB)

---

## 2. CENTRAL GOVERNMENT SCHEMES

### A. Startup India Seed Fund Scheme (SISFS)

| Parameter | Details |
|-----------|---------|
| **Total Corpus** | INR 945 crore |
| **Per Startup** | Up to INR 20 lakh (grant for validation) + up to INR 50 lakh (debt/convertible debentures for commercialization) |
| **Eligibility** | DPIIT recognized, incorporated <2 years, not received >INR 10L govt funding |
| **Apply Through** | Empanelled incubators (200+ across India) |
| **Website** | seedfund.startupindia.gov.in |

### B. SIDBI Fund of Funds for Startups (FFS 2.0)

| Parameter | Details |
|-----------|---------|
| **Total Corpus** | INR 20,000 crore (announced Union Budget 2025) |
| **Mechanism** | Invests in SEBI-registered AIFs (Category I) who then invest in startups |
| **Per AIF** | Varies by fund size and mandate |
| **Impact** | Has catalyzed INR 1.15 lakh crore invested in 1,000+ startups |
| **Website** | sidbi.in/ffs |

### C. Credit Guarantee Scheme for Startups (CGSS)

| Parameter | Details |
|-----------|---------|
| **Guarantee** | Up to INR 10 crore per startup (raised from earlier limits) |
| **Fee** | 1-2% annual guarantee fee |
| **For** | Loans/debt from scheduled banks, NBFCs, AIFs |
| **Eligibility** | DPIIT recognized, CIBIL score requirements |
| **Website** | ncgtc.in |

### D. MUDRA Loans (Micro Units Development & Refinance Agency)

| Category | Amount | Purpose |
|----------|--------|---------|
| **Shishu** | Up to INR 50,000 | Starting/ideation |
| **Kishore** | INR 50,001 to INR 5 lakh | Early growth |
| **Tarun** | INR 5 lakh to INR 10 lakh | Scaling |
| **Tarun Plus** | INR 10 lakh to INR 20 lakh | Expansion (added 2024) |

- No collateral required
- Available at all banks, NBFCs, MFIs
- Website: mudra.org.in

### E. CGTMSE (Credit Guarantee Fund Trust for MSEs)

| Parameter | Details |
|-----------|---------|
| **Guarantee** | Up to INR 5 crore (collateral-free) |
| **For** | MSMEs including startups registered as MSME/Udyam |
| **Guarantee Fee** | 0.37-2% annually based on loan amount |
| **Via** | All scheduled commercial banks |

### F. PMEGP (Prime Minister's Employment Generation Programme)

| Parameter | Details |
|-----------|---------|
| **Subsidy** | 15-35% of project cost (varies by area/category) |
| **Max Project Cost** | INR 50 lakh (manufacturing), INR 20 lakh (service) |
| **General Category** | 15% (urban), 25% (rural) |
| **Special Category** | 25% (urban), 35% (rural) — women, SC/ST, OBC, minorities, PH, ex-servicemen |
| **Website** | kviconline.gov.in/pmegp |

### G. Stand-Up India 2.0

| Parameter | Details |
|-----------|---------|
| **For** | SC/ST and women entrepreneurs |
| **Loan** | INR 10 lakh to INR 1 crore |
| **Purpose** | Greenfield enterprise in manufacturing, service, agri-allied |
| **Collateral** | Composite loan; CGTMSE cover available |

---

## 3. INNOVATION & RESEARCH GRANTS

### A. Atal Innovation Mission (AIM) Programs

| Program | Amount | Purpose |
|---------|--------|---------|
| **Atal Incubation Centre (AIC)** | Up to INR 10 crore over 5 years | Establish new incubator |
| **ANIC (Atal New India Challenge)** | Up to INR 1 crore per challenge | Product innovation grants |
| **ARISE (Atal Research & Innovation for Small Enterprises)** | Up to INR 50 lakh | SME innovation funding |
| **Atal Tinkering Labs (ATL)** | INR 20 lakh per lab | School-level innovation |

### B. DST (Department of Science & Technology) - NIDHI Suite

| Program | Amount | Purpose |
|---------|--------|---------|
| **PRAYAS** | Up to INR 10 lakh | Proof of concept |
| **SSP (Startup Support Programme)** | Up to INR 1 crore | Early-stage support |
| **EIR (Entrepreneur-in-Residence)** | INR 30,000/month stipend (12 mo) | Innovator support |
| **NIDHI-TBI** | Up to INR 6.4 crore | Technology Business Incubator setup |
| **Accelerator** | Up to INR 4 crore | Accelerator setup |
| **CoE (Centres of Excellence)** | Up to INR 5 crore | Sector-specific centers |
| **Seed Support** | Up to INR 1 crore | Seed funding |

### C. BIRAC (Biotechnology Industry Research Assistance Council)

| Program | Amount | Purpose |
|---------|--------|---------|
| **BIG (Biotechnology Ignition Grant)** | Up to INR 50 lakh | Early-stage biotech |
| **SBIRI** | Up to INR 50L (Phase I), INR 1Cr (Phase II) | Biotech product dev |
| **BIPP** | Up to 50% of project cost | Late-stage biotech |
| **CRS** | Variable | Contract research |
| **LEAP** | Up to INR 1 crore | Biotech acceleration |

### D. MeitY (Ministry of Electronics & IT)

| Program | Amount | Purpose |
|---------|--------|---------|
| **GENESIS** | INR 490 crore total allocation | GenAI startup support |
| **SAMRIDH** | Up to INR 40 lakh per startup | Scaling assistance |
| **TIDE 2.0** | Up to INR 7.5 crore per incubator | Tech incubation |
| **AI Programme** | Up to INR 10 crore | AI startup development |

### E. iDEX (Innovations for Defence Excellence)

| Program | Amount | Purpose |
|---------|--------|---------|
| **SPARK** | Up to INR 1.5 crore | Defence innovation |
| **Prime** | Up to INR 10 crore | Scaled defence solutions |
| **Open Challenges** | Variable | Specific defence needs |
| **Website** | idex.gov.in |

### F. IN-SPACe (Indian National Space Promotion & Authorization Centre)

| Program | Details |
|---------|---------|
| **VC Fund** | INR 1,000 crore for space startups |
| **Tech Adoption Fund** | INR 500 crore |
| **ISRO Tech Transfer** | Access to ISRO technologies |
| **Testing Infrastructure** | Shared ISRO facilities |

### G. NABARD (Agriculture)

| Program | Amount | Purpose |
|---------|--------|---------|
| **AgriSURE Fund** | INR 750 crore | Agritech investments |
| **Green Impact Fund** | INR 1,000 crore | Sustainable agriculture |
| **NABVENTURES** | Via fund of funds | Agri startup investment |

---

## 4. TAX BENEFITS FOR INDIAN STARTUPS

### Angel Tax — ABOLISHED (FY 2024-25 onwards)
- Section 56(2)(viib) no longer applies
- Previously taxed premium over FMV at 30.9%
- Eliminated for ALL investor categories (domestic + foreign)
- Massive ecosystem reform

### Section 80-IAC — Income Tax Holiday
- 3-year tax holiday (consecutive) within first 10 years
- Must be DPIIT recognized + IMB approved
- Turnover under INR 100 crore
- Paid-up capital + share premium not exceeding INR 25 crore

### Section 54GB — Capital Gains Exemption
- Exemption from capital gains when investing residential property sale proceeds into eligible startups
- Channels household wealth into startup ecosystem

### ESOP Taxation (Two-Stage)
- **At Exercise**: FMV minus exercise price taxed as salary (perquisite)
- **At Sale**: Capital gains tax (STCG 20% listed / slab unlisted; LTCG 12.5%)
- **Startup Deferral**: Perquisite tax deferred up to 5 years for IMB-certified startups

### GST Exemptions
- No GST on equity/share issuance
- GST applies to services (consulting, legal) used during fundraising
- Input tax credit available on fundraising-related services

---

## 5. REGULATORY FRAMEWORK FOR FOREIGN CAPITAL

### FDI Policy (Automatic Route — 100% in most sectors)

| Sector | FDI Cap | Route |
|--------|---------|-------|
| IT/Software | 100% | Automatic |
| E-commerce (Marketplace) | 100% | Automatic |
| Insurance | 100% | Automatic (Budget 2025, if premium invested in India) |
| Defence | 74% | Automatic |
| Space | 100% | Automatic (2024, varies by activity) |
| Telecom | 100% | Automatic |
| Multi-brand retail | 51% | Government approval |
| Print media | 26% | Government approval |

### Press Note 3 (2020) — China/Land Border Restriction
- ALL FDI from countries sharing land border with India requires government approval
- Applies to: China, Pakistan, Bangladesh, Afghanistan, Myanmar, Bhutan, Nepal
- Includes beneficial ownership — even indirect Chinese investment requires approval
- Significantly impacts Chinese VC investment into Indian startups

### FEMA Compliance for Foreign Investment

| Instrument | Requirement |
|-----------|-------------|
| Equity shares | Pricing per Rule 11UA (FMV by registered valuer) |
| CCPS/CCD | Must be mandatorily convertible; pricing per FMV |
| Convertible notes | Min INR 25 lakh per investor per tranche; max 10-year conversion |
| SAFE notes | NOT legally recognized in India; use iSAFE (as CCPS) |
| ECB (External Commercial Borrowing) | Simplified 2026 framework; sector-specific caps |

### Post-Investment Reporting

| Form | When | Purpose |
|------|------|---------|
| FC-GPR | Within 30 days of allotment | Report equity issuance to foreign investors |
| FC-TRS | Within 60 days of transfer | Report share transfer |
| Form CN | Within 30 days | Convertible note issuance to foreigners |
| Annual Return on Foreign Liabilities and Assets (FLA) | Annually by July 15 | All entities with foreign investment |

### SEBI AIF (Alternative Investment Fund) Regulations

| Category | Type | Key Rules |
|----------|------|-----------|
| **Cat I** | VC Funds, Angel Funds, SME Funds, Social Venture, Infra | Min corpus INR 20Cr; max 25% in one company |
| **Cat II** | PE Funds, Debt Funds, Fund of Funds | No specific incentives; borrowing limited |
| **Cat III** | Hedge Funds, PIPE Funds | Leverage up to 2x NAV; max 10% in one company |
| **Angel Fund** | Sub-category of Cat I | Min corpus INR 5Cr; min investment INR 25L; range INR 10L-25Cr per company |

### Capital Instruments Legal in India (vs Global)

| Global Instrument | India Equivalent | Legal Status |
|-------------------|-----------------|--------------|
| SAFE Note | iSAFE (as CCPS) | Legal via workaround |
| Convertible Note | Convertible Note (regulated) | Legal; min INR 25L for foreign |
| Priced Equity | Equity Shares | Legal; pricing per Rule 11UA |
| CCD | Compulsorily Convertible Debentures | Legal; must convert within 10 years |
| CCPS | Compulsorily Convertible Preference Shares | Legal; common for VC deals |
| Venture Debt | NCDs + Warrants | Legal; growing market |
| RBF | Revenue-share agreement | Legal; not specifically regulated |

---

## 6. INDIAN VC ECOSYSTEM (2024-2025)

### Market Overview
- Total VC invested (2024): $13.7B (up 43% from $9.6B in 2023)
- Total VC invested (2025 projected): ~$15B
- Deal count (2024): 1,270 deals (up 45%)
- AI startup funding: $643M across 100 deals (2025)
- Fund launches (2025): $12.1B raised by startup VCs (up 39%)

### Tier 1 VC Firms (Multi-Stage, $500M+ AUM)

| Firm | Latest Fund | Focus |
|------|-------------|-------|
| **Peak XV (ex-Sequoia India)** | $2.5B across funds (2024) | Seed to growth |
| **Accel India** | $650M (Jan 2025) | Early to growth |
| **Elevation Capital** | $670M | Fintech, consumer, SaaS |
| **Lightspeed India** | ~$500M | Consumer, SaaS, health |
| **Nexus (Z47)** | $700M | Software, fintech, deep tech |

### Tier 2 (Early/Growth, $100-500M)

| Firm | Latest Fund | Focus |
|------|-------------|-------|
| **Blume Ventures** | Fund V $175M close (2025) | Pre-seed to A, deep tech |
| **Chiratae Ventures** | Fund V $150M (2025) | Enterprise, health, SaaS |
| **Stellaris VP** | ~$160M | B2B SaaS, fintech, health |
| **Prime VP** | Fund V $100M | SaaS, fintech, health |
| **Kalaari Capital** | ~$200M | E-com, D2C, consumer |
| **3one4 Capital** | $100M+ AUM | Deep tech, SaaS |

### Tier 3 (Specialized/Sector)

| Firm | Focus | Typical Check |
|------|-------|---------------|
| **Omnivore** | Agritech, food, climate | $500K-$5M |
| **Ankur Capital** | Deep science/impact | $500K-$2M |
| **WaterBridge** | B2C, logistics, supply chain | $500K-$3M |
| **Fireside Ventures** | Consumer brands, D2C | $1-5M |
| **India Quotient** | Bharat-focused, vernacular | $200K-$2M |

### Pre-Seed/Seed Specialists

| Firm | AUM/Fund | Typical Check |
|------|----------|---------------|
| **Titan Capital** | INR 200Cr Winners Fund | $100K-$500K |
| **Better Capital** | $100M+ AUM | $50K-$250K |
| **iSeed** | Fund II $15M | ~$250K |

### Angel Networks

| Network | Members | Investments |
|---------|---------|-------------|
| **Indian Angel Network (IAN)** | 470+ across 11 countries | 198 investments |
| **Mumbai Angels** | 750+ across 10 countries | 200+ investments, 100+ exits |
| **LetsVenture** | 19,530 investors | 950+ investments |
| **Venture Catalysts/9Unicorns** | 4,500+ across 36 cities | 176 investments |
| **Inflection Point Ventures** | 24,000+ members | 200+ investments |
| **Chennai Angels** | Regional (South) | Active co-investment |
| **Hyderabad Angels** | Regional (South) | Active co-investment |

### Accelerators/Incubators (520+ in India)

| Program | Location | Key Offering |
|---------|----------|-------------|
| **T-Hub 2.0** | Hyderabad | World's largest incubator (572K sq ft) |
| **NASSCOM 10000 Startups** | Pan-India | Tech startup platform |
| **Axilor Ventures** | Bangalore | 12-week accelerator, Infosys-backed |
| **Villgro** | Chennai | Social enterprise incubator |
| **CIIE.CO** | IIM Ahmedabad | Deep tech, climate |
| **JioGenNext** | Mumbai | Reliance ecosystem access |
| **Zone Startups (BSE)** | Mumbai | Fintech accelerator |
| **Google for Startups** | Pan-India | AI/ML, equity-free |
| **Microsoft for Startups** | Pan-India | Azure credits, enterprise connects |

### Indian Fundraising Benchmarks

| Stage | India Median Round | India Median Valuation | vs US Discount |
|-------|-------------------|----------------------|----------------|
| Pre-Seed | INR 50L-1.5Cr ($60-180K) | INR 3-10Cr ($360K-1.2M) | 70-80% |
| Seed | $2.7M | $5-16M | 30-50% |
| Series A | $8-12M | $25-50M | 30-40% |
| Series B | $25-40M | $80-200M | 20-30% |

---

## 7. STATE SCHEMES — COMPLETE REFERENCE

### Auto-Match by State

When user mentions their location, match to these schemes:

| State | Max Seed Fund | Key Program | Special Benefits |
|-------|--------------|-------------|------------------|
| **Karnataka** | INR 50L | ELEVATE | 43% women-led; Beyond Bengaluru fund |
| **Maharashtra** | INR 5-10L | Maha-Fund (INR 500Cr) | Innovation City near Mumbai |
| **Tamil Nadu** | INR 10-15L | TANSEED | Green/Rural/Women enhanced |
| **Telangana** | INR 25L-1Cr | T-Fund, T-Spark | T-Hub 2.0 incubation |
| **Kerala** | INR 15L | KSUM Seed | 6% soft loan; KFC up to 10Cr |
| **Gujarat** | INR 30L | iCreate | SSIP 2.0 for students |
| **Rajasthan** | INR 15-25L | Bhamashah Techno Fund | QRate-ranked; INR 500Cr total |
| **Uttar Pradesh** | INR 10L | StartinUP | Monthly sustenance allowance |
| **Madhya Pradesh** | INR 30L | MP Startup Fund (INR 100Cr) | 18% enhanced for women/SC/ST |
| **Haryana** | INR 10L | Startup Haryana | Patent 100% reimbursement |
| **Punjab** | INR 3L | IMP Punjab | Interest subsidy 8% for 5yr |
| **Andhra Pradesh** | Policy-defined | AP Innovation 4.0 | 10 CoEs; Ratan Tata Hub |
| **West Bengal** | Via VC Fund | Bengal Silicon Valley | 20% earmarked for startups |
| **Delhi** | Via INR 200Cr VC | Draft Policy 2025 | 18 focus sectors |
| **Odisha** | Via INR 100Cr FoF | Startup Odisha | INR 20-22K monthly allowance |
| **Assam** | INR 50L | Assam Policy 2025-30 (INR 397Cr) | 25% women, 20% rural reserved |
| **Goa** | INR 10L | Startup Goa | Salary reimbursement 50% |
| **Bihar** | INR 10L | Bihar Startup Fund | Interest-free 10-year loan |
| **Jharkhand** | INR 10L | ABVIL Portal | INR 10-25K monthly allowance |
| **Chhattisgarh** | INR 10L | CG Policy 2025-30 (INR 100Cr) | Employment subsidy INR 5-6K/mo |
| **Chandigarh** | INR 7-9L | CH Policy 2025 | +INR 12-14L commercialization |
| **Uttarakhand** | INR 15L | UK Venture Fund (INR 200Cr) | INR 20K monthly allowance |
| **Himachal Pradesh** | Variable | CM Startup Scheme | Job-creator conversion focus |
| **J&K** | Policy-defined | J&K Policy 2024-27 | Target 2,000 startups by 2027 |
| **Arunachal Pradesh** | INR 5L (state) + 20L (SISFS) | Via incubators | NE focus |
| **Tripura** | Policy-defined | Tripura Policy 2024 | IT + non-IT coverage |
| **NE States (All 8)** | Variable | UNNATI Scheme (INR 10,037Cr) | Central NE industrial scheme |

### Enhanced Benefits Flags

**Women-led startups** get enhanced benefits in: Karnataka (43% reservation in ELEVATE), Tamil Nadu (TANSEED GreenTech), Madhya Pradesh (+3% on all subsidies), Assam (25% funding reservation), Chhattisgarh (10% reserved incubator seats + 10% subsidy enhancement), Chandigarh (+INR 2L bonus), Odisha (INR 2K extra monthly), Stand-Up India, PMEGP (10% extra subsidy).

**SC/ST-led startups** get enhanced benefits in: Karnataka (ELEVATE Unnati INR 9.52Cr), Madhya Pradesh (+3% on subsidies), Stand-Up India (dedicated scheme), PMEGP (10% extra), Odisha (INR 2K extra monthly).

---

## 8. GIFT CITY (International Financial Services Centre)

### Tax Benefits
- 100% income tax holiday for 10 consecutive years out of 15 (extended to 20 out of 25)
- Post-holiday: 15% corporate tax
- No capital gains tax on specified securities
- No STT, no stamp duty, no GST on IFSC transactions
- Budget 2025 extended deadline to March 2030

### For Startups
- Access to global investor network
- Fintech Framework by IFSCA
- Zone Startups collaboration for accelerator programs
- Gujarat state incentives (OPEX/CAPEX support)

### For Fund Managers
- Set up AIFs in GIFT City with international tax efficiency
- Pass-through benefits for non-resident investors
- Easier relocation of funds to GIFT City

---

## 9. CROSS-BORDER: US VCs INTO INDIA / INDIA VCs INTO US

### US VC Investing in India
- Automatic route for most sectors (100% FDI)
- Pricing: Must follow Rule 11UA (FMV by registered valuer)
- Reporting: FC-GPR within 30 days
- Withholding: DTAA (India-US) reduces withholding to 15-25% on dividends
- Press Note 3: Does NOT apply to US investors

### Indian Startup Raising from US VCs
- Preferred structure: India Pvt Ltd (operating) + US Delaware C-Corp (holding/flip)
- "Flip" structure: Create US holding company that owns India subsidiary
- Common for companies targeting US listing / YC / US institutional investors
- Tax implications: Transfer pricing on inter-company transactions

### Indian Startup Expanding to US
- Incorporate Delaware C-Corp as subsidiary or holding
- Maintain India entity for Indian operations + government scheme eligibility
- Cross-border structuring must comply with FEMA, Transfer Pricing, DTAA

---

## 10. PLI (Production Linked Incentive) SCHEMES

14 sectors with INR 1.97 lakh crore total allocation:

| Sector | PLI Allocation | Relevance to Startups |
|--------|---------------|----------------------|
| Electronics/IT Hardware | INR 7,325Cr | Hardware startups |
| Pharmaceuticals | INR 15,000Cr | Pharma/biotech |
| Telecom/Networking | INR 12,195Cr | Telecom startups |
| Food Processing | INR 10,900Cr | FoodTech/AgriTech |
| White Goods (ACs, LEDs) | INR 6,238Cr | Manufacturing startups |
| Solar PV | INR 24,000Cr | CleanTech/renewable |
| Auto/Auto Components | INR 25,938Cr | EV/mobility startups |
| Textiles | INR 10,683Cr | FashionTech startups |
| Specialty Steel | INR 6,322Cr | Materials startups |
| Semiconductors/Display | INR 76,000Cr | Chip design startups |
| Drones | INR 120Cr | Drone startups |
| Advanced Chemistry Cell | INR 18,100Cr | Battery/energy storage |

---

## 11. CORPORATE INNOVATION PROGRAMS

| Corporate | Program | Offering |
|-----------|---------|----------|
| **Reliance (JioGenNext)** | MAP (Market Access Program) | No equity, Reliance ecosystem access |
| **Tata Group** | Tata Innoverse | Innovation challenges |
| **Infosys Innovation Fund** | Wipro Ventures model | Enterprise tech, AI investments |
| **Coal India** | Open innovation | Mining/energy tech challenges |
| **ONGC** | Energy Startup Challenges | Oil & gas innovation |
| **NTPC** | Innovation Challenges | Power/energy startups |
| **Indian Railways** | Innovation challenges | Rail tech solutions |
| **ISRO/IN-SPACe** | Tech Transfer + VC Fund | Space tech startups |

---

## 12. SCHEME STACKING STRATEGY FOR INDIAN STARTUPS

### Optimal Stack by Stage

**Idea Stage (Year 0-1)**
1. Get DPIIT recognition (Day 1)
2. Register as MSME/Udyam
3. Apply: MUDRA Shishu (INR 50K) + State seed fund (INR 3-50L)
4. Apply: DST-NIDHI PRAYAS (INR 10L) if tech/science
5. Join state incubator for free workspace

**Prototype Stage (Year 1-2)**
1. Apply: SISFS (up to INR 20L validation grant)
2. Apply: Sector grant (BIRAC BIG for biotech, iDEX SPARK for defence, MeitY for IT)
3. Apply: State startup scheme for additional seed
4. File patents (80% fee rebate via DPIIT)
5. Stack: CGTMSE for collateral-free bank loan (up to INR 5Cr)

**Early Revenue Stage (Year 2-3)**
1. Apply: SISFS commercialization (up to INR 50L)
2. Apply: Section 80-IAC for 3-year tax holiday
3. Raise angel round (IAN, LetsVenture, Venture Catalysts)
4. Stack: MUDRA Tarun Plus (INR 20L) for working capital
5. Apply: PLI scheme if manufacturing

**Growth Stage (Year 3-5)**
1. Raise VC (Peak XV, Accel, Elevation, etc.)
2. Access SIDBI FoF-backed AIFs
3. Apply: CGSS for credit guarantee on debt (up to INR 20Cr)
4. Consider venture debt (InnoVen, Trifecta, Alteria)
5. If foreign investors: FEMA compliance + FC-GPR reporting

**Scale Stage (Year 5+)**
1. Growth equity + late-stage VCs
2. Consider GIFT City for international structuring
3. Pre-IPO: SEBI SME platform or main board
4. Secondary market transactions for employee liquidity
5. International expansion via flip structure if needed
