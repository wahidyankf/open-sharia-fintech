export type CVEntry = {
  type: "about" | "work" | "education" | "honor" | "certification" | "language";
  title: string;
  organization: string;
  period: string;
  details: string[];
  links?: { [key: string]: string };
  employmentType?: string;
  location?: string;
  locationType?: string;
  skills?: string[];
  programmingLanguages?: string[];
  frameworks?: string[];
  aiSkills?: string[];
};

export const cvData: CVEntry[] = [
  {
    title: "About Me",
    organization: "",
    period: "",
    details: [
      "Technology and engineering leader with nearly nine years of experience, including more than three years in Indonesia's regulated fintech sector: digital banking, Islamic (Sharia-compliant) financial services, and P2P lending. Leads multidisciplinary teams across product engineering, platform, mobile, data, information security, and IT governance for systems that run customer accounts, payments, and financing.",
      "Delivered a core-banking migration that reduced operating costs by 95%, equivalent to 30% of Hijra Group's monthly revenue; an AI-augmented software-delivery model that increased engineering throughput by 90%+ while keeping operating-expense (OPEX) growth within 5%; and test automation that reduced regression cycles from more than five days to under five hours. Also secured ISO 27001:2022, maintained 100% regulatory IT audit success and zero IT security incidents, led Hijra Bank's data warehouse migration ensuring 100% regulatory compliance, and strengthened eKYC, Anti-Money Laundering (AML), and fraud detection controls.",
      "Work bridges technical architecture and business strategy: from cyber-security hardening and automated threat intelligence to payment integrations with Indomaret, Indonesia's nationwide convenience-store network. Builds high-trust, high-performance teams for reliable financial technology and contributes to Open Sharia Enterprise (OSE), an open-source initiative for ethical, Sharia-compliant enterprise software. Also shares software-engineering and Islamic-fintech insights through a blog and YouTube channel, AyoKoding (ayokoding.com).",
    ],
    links: {
      github: "https://github.com/wahidyankf",
      githubOrg: "https://github.com/organiclever",
      linkedin: "https://www.linkedin.com/in/wahidyan-kresna-fridayoka/",
      website: "https://wahidyankf.com",
      email: "wahidyankf@gmail.com",
    },
    type: "about",
  },
  {
    title: "Head of Engineering - Hijra Bank",
    organization: "Hijra",
    period: "March 2025 - July 2026",
    employmentType: "Full-time",
    location: "Jakarta, Indonesia",
    locationType: "Hybrid",
    details: [
      "Led technical strategy for core banking, payments, and financing across Product, Platform, Mobile, SEIT, Data Engineering, InfoSec, and IT GRC; owned IT/Engineering compliance, board reporting, and audit outcomes.",
      "Pushed the Direct Switching initiative from inception through UAT; its production release is pending. Open Banking/API capabilities and additional cash-in and cash-out channels remained in planning and initial development.",
      "Migrated Hijra Bank's data warehouse from the Hijra Group-level environment, ensuring 100% regulatory compliance; secured ISO 27001:2022, maintained 100% success across regulatory IT audits, and strengthened eKYC, Anti-Money Laundering (AML), and fraud-detection controls.",
      "Maintained zero IT security incidents; strengthened WAF protections, automated reconnaissance, and threat-intelligence capabilities with zero downtime.",
      "Achieved the Product Engineering Pipeline OKR through an AI-augmented SDLC: raised GitHub throughput, PR velocity, and resolution rates by 90%+ while keeping engineering OPEX within its 5% ceiling. Built a T-shaped organization; two product managers shipped UI fixes and code through engineer pairing, PR review, and test coverage.",
      "Delivered merchant-withdrawal integration across 20,000+ Indomaret stores in 400+ cities and adopted BI SNAP. Led special-nisbah time-deposit and savings products; from March 2025 to July 2026, online time-deposit balances grew 39.60% and combined online savings and time-deposit balances grew 16.24%. DPK reached an all-time high.",
      "Reduced monthly interbank OPEX by more than 25% through user tiering without affecting month-over-month user growth. Advanced React Native, monorepo, and Data Engineering platforms while sustaining 99%+ uptime.",
      "Used XP during restructuring to stabilize delivery. Modernized profit-sharing approvals, regulatory tracking, and business workflows with automation; maintained team morale, velocity, and 0% voluntary turnover.",
    ],
    skills: [
      "Engineering Management",
      "Systems Design",
      "Software Engineering",
      "Core Banking",
      "Frontend Engineering",
      "Data Engineering",
      "Backend Engineering",
      "Information Security",
      "Software Testing",
    ],
    programmingLanguages: ["JavaScript", "SQL", "Java", "TypeScript", "Python"],
    frameworks: ["React.js", "React Native", "Next.js", "Spring Boot"],
    aiSkills: ["AI-augmented SDLC"],
    type: "work",
  },
  {
    title: "Engineering Manager - Hijra Bank",
    organization: "Hijra",
    period: "July 2024 - February 2025",
    employmentType: "Full-time",
    location: "Indonesia",
    locationType: "Hybrid",
    details: [
      "Led up to 24 engineers across backend, frontend, mobile/React Native, SEIT, and SQA in the Bank domain, encompassing core banking, transactions, consumer lifecycle, financing, data engineering, and release management. Maintained 0% voluntary turnover. Served as IT Executive Officer for Hijra Bank, responsible for regulatory reporting, ISO 27001:2022 certification audits, and internal IT governance compliance.",
      "Led Hijra Bank's high-priority core-banking migration from Mambu to IBA, achieving a 95% reduction in core-banking operational costs—equivalent to 30% of Hijra Group's monthly revenue—in under six months. The implementation covered product requirements, document finalization, development, testing, and Hijra Bank's first serious automation-testing process.",
      "Stabilized Hijra Bank's release train and expanded automation testing to all critical business flows. The work resulted in zero production hotfixes and reduced regression testing from more than five days to under five hours.",
      "Spearheaded the Financing Originating System (FOS) initiative from concept toward implementation to streamline the financing process and reduce Non-Performing Loans (NPLs).",
    ],
    skills: [
      "Engineering Management",
      "Systems Design",
      "Software Engineering",
      "Core Banking",
      "Frontend Engineering",
      "Data Engineering",
      "Backend Engineering",
      "Financing Engineering",
      "Software Testing",
    ],
    programmingLanguages: ["JavaScript", "Python", "SQL", "Java", "TypeScript"],
    frameworks: ["React.js", "React Native", "Next.js", "Spring Boot"],
    type: "work",
  },
  {
    title: "Engineering Manager - Alami P2P Lending and Hijra Bank Financing",
    organization: "Hijra",
    period: "December 2022 - July 2024",
    employmentType: "Full-time",
    location: "Indonesia",
    locationType: "Remote",
    details: [
      "Led Hijra Group's Financing domain (Bank and Alami P2P Lending), Risk Management & Reporting, and Data Engineering teams of up to 25 engineers across backend, frontend, mobile/React Native, SEIT, SQA, and data engineering. Maintained an 8% voluntary-turnover rate (2 of 25 team members) and stabilized the team through strategic reprioritization after organizational restructuring.",
      "Spearheaded the Bank's financing products—home and commercial financing—product-engineering back office, and user onboarding on web and mobile applications, including sales and risk-management dashboards. This foundational work established a key revenue stream for Hijra Group.",
      "Drove Supply Chain Financing (SCF) adoption, contributing to 50% of total financing-application disbursements in Alami P2P Lending.",
      "Optimized Alami's back-office system, reducing the financing application submission-to-disbursement SLA by 25%, from 14 to 10 days.",
      "Led extraction of the credit engine for cross-group use within Hijra (Bank and Alami), saving hundreds of development hours and eliminating application inconsistencies.",
      "Collaborated with Legal and Compliance to ensure 100% compliance with OJK regulations for Hijra Group's P2P Lending and Bank engineering teams, including AML implementation, automated regulatory reporting, and back-office governance.",
      "Implemented developer-productivity initiatives: Trunk-Based Development adoption, Kubernetes-migration support, CI/CD integration, unit, integration, and E2E testing, and quality and infrastructure improvements. These changes made development faster, easier, and more secure while reducing operating costs.",
      "Transformed the five-person QA team from manual processes to automated testing, improving team delivery and workforce stability; promoted a developer-owned testing approach to reinforce the transformation.",
    ],
    skills: [
      "Engineering Management",
      "Systems Design",
      "Software Engineering",
      "Frontend Engineering",
      "Backend Engineering",
      "Software Testing",
      "Financing Engineering",
      "Data Engineering",
    ],
    programmingLanguages: ["JavaScript", "Java", "Python", "TypeScript", "SQL"],
    frameworks: ["React.js", "Next.js", "React Native", "Spring Boot"],
    type: "work",
  },
  {
    type: "work",
    title: "Engineering Manager",
    organization: "GudangAda",
    period: "July 2022 - December 2022",
    employmentType: "Full-time",
    location: "Indonesia",
    locationType: "Hybrid",
    details: [
      "Led GudangAda's (Gada) 11-member, multinational, distributed engineering team responsible for the Warehouse Management System (WMS).",
      "Launched bin-related WMS features (organizing inventory within warehouse locations) for internally operated warehouses, improving inventory organization and enabling more effective inbound/outbound operations (e.g., First Expired First Out (FEFO) recommendations).",
      "Delivered paperless WMS projects, significantly increasing accuracy and productivity. For example, invoice automation reduced creation and delivery time to partners by several days.",
      "Drove the adoption of a unified web automation framework (Cypress and TypeScript) across Gada's tech team, increasing product iteration velocity by automating previously manual web application E2E testing. The TypeScript introduction also fostered collaboration and code sharing between the QE and FE teams.",
      "Championed FE mono repo adoption within the WMS team, projected to increase FE team productivity by over 20% while improving maintainability and correctness through dependency graph analysis. This initiative also created a foundation for company-wide FE productivity and maintainability improvements.",
      "Spearheaded WMS engineering excellence initiatives, resulting in significantly accelerated testing and boosted developer productivity. Key improvements included mandating QE coverage for critical path positive cases, increasing unit testing adoption, implementing static type checking, modernizing development environments, and Dockerizing database development.",
    ],
    skills: [
      "Engineering Management",
      "Frontend Engineering",
      "Backend Engineering",
      "Software Testing",
      "Systems Design",
      "Software Engineering",
    ],
    programmingLanguages: ["JavaScript", "Python", "TypeScript", "SQL"],
    frameworks: ["React.js", "Next.js", "Django"],
  },
  {
    type: "work",
    title: "Engineering Manager",
    organization: "Ruangguru",
    period: "November 2021 - July 2022",
    employmentType: "Full-time",
    location: "Indonesia",
    locationType: "Remote",
    details: [
      "Led Skill Academy's (SA) 14-member, distributed engineering team responsible for the Payment, Promotion, and Discovery stream (SA-PPD). Successfully mentored and promoted two engineers to senior roles.",
      "Spearheaded developing and launching a highly successful user reward and OTP system, contributing to over 50% of SA's total transactions with a 99% disbursement success rate (the remaining 1% attributed to user input errors).",
      "Improved partnership utility software, streamlining SA's learning partnerships and contributing hundreds of billion Rupiah in secured partnership contracts.",
      "Led SA-PPD's backend re-architecture project, increasing system load capacity by over 200% and resolving domain coupling issues.",
      "Drove SA's frontend platform team initiative, resulting in a 35% improvement in Android app loading time, more than doubling the Lighthouse performance score for SA's web (from 10 to 50), and establishing CI/CD tooling for the React Native app deployment, saving approximately 2 hours of APK build time per day.",
      "Led SA-PPD's SEO project, increasing organic traffic by over 6 times (Jan-Jun 2022) and saving hundreds of millions of Rupiah per month in ad spending (e.g., over 500 million Rupiah in June 2022). Notably, organic traffic users demonstrated six times greater engagement than paid users.",
      "Spearheaded the development of dynamic landing pages and a public API, enabling SA's marketing UI engineers to save over a hundred engineering efforts monthly.",
      "Served as an advisory member of the SA-FE committee, guiding efforts to address technical debt and improve the developer experience, including ReasonML to TypeScript migration and web and mobile platform enhancements. Also actively participated in Ruangguru's FE hiring committee.",
    ],
    skills: [
      "Engineering Management",
      "Systems Design",
      "Frontend Engineering",
      "Software Engineering",
      "Software Testing",
    ],
    programmingLanguages: ["JavaScript", "Golang", "ReasonML", "TypeScript", "SQL"],
    frameworks: ["React.js", "Next.js", "ReasonReact"],
  },
  {
    type: "work",
    title: "Technical Lead",
    organization: "Ruangguru",
    period: "August 2021 - October 2021",
    employmentType: "Full-time",
    location: "Jakarta, Indonesia",
    locationType: "Remote",
    details: [
      "Led Skill Academy's payment, promotion, and discovery stream's (SA-PPD) distributed engineering team of 6. In addition, being responsible for the SA-PPD engineering alignment with its stakeholders and its BE & FE engineers' Career Development Plan (CDP).",
      "Led Skill Academy's FE (SA-FE) general technical endeavor by creating its roadmap, alignments with SA streams (e.g., SA-PPD, SA-Learning), and alignments with Ruangguru's FE (RG-FE) platform team. The alignment with SA streams ensured that the SA business grew, and SA-FE could pragmatically chase the RG's engineering excellence principle (e.g., web SEO and performance improvement for SA-PPD, learning journey stabilization for SA-Learning). At the same time, the alignments with the RG-FE team enable the SA-FE squad to benefit from adopting the technological advancement in RG-FE and vice versa (e.g., X-State for the central model adoption). Also responsible for the CDP of every engineer in SA-FE (i.e., seven engineers in total).",
      'Saving hundreds of engineering hours per month by prioritizing eliminating hassle-recurrent jobs in the SA-PPD engineering team (e.g., dynamic ranking, dynamic content adoption). Ensure that the engineering team can focus on what "matters" the most (create delightful products and strive for engineering excellence).',
    ],
    skills: [
      "Engineering Management",
      "Systems Design",
      "Backend Engineering",
      "Frontend Engineering",
      "Software Engineering",
    ],
    programmingLanguages: ["JavaScript", "Golang", "ReasonML", "TypeScript", "SQL"],
    frameworks: ["React.js", "React Native", "ReasonReact"],
  },
  {
    type: "work",
    title: "Senior Frontend Engineer",
    organization: "Ruangguru",
    period: "September 2019 - October 2021",
    employmentType: "Full-time",
    location: "Jakarta, Indonesia",
    locationType: "Remote",
    details: [
      "Developed most of Skill Academy's (SA) learning journey (using ReasonML) and CMS (using plain React.js) modules during the short inception period. Made sure that this critical project could be launched on time (8 weeks) while making it run-time error-free.",
      'Became frontend engineering lead for SA team (i.e., led 7 FE engineers) and was responsible for all of its client-side platforms (i.e., Web, Mobile, and CMS using ReasonML, TypeScript, Flow, JS, Cordova, React, React Native, Next.js). Made sure the team members could grow and stay happy while ensuring the SA team met the business needs and its technical debt "payment." Also heavily involved in driving SA\'s FE architecture (e.g., FSM-pattern adoption, heavy feature-toggle usage, offline-first architecture, tracking, testing adoption, dynamic rendering).',
      "Worked with various teams and stakeholders during the ideation, screening, execution, and retrospection phase, ensuring that only the most impactful features were shipped into production while keeping the deadline in check. Made SA the top product in the Indonesian market and became one of the most profitable business units in Ruangguru's history. Thus, it became one of Ruangguru's backbones during the COVID-19 pandemic.",
      "I was involved in Ruangguru's FE engineering committee and influenced its road map. One of the results was that Ruangguru's FE team quickly (i.e., about four weeks from the initial discussion) converged the convention and technological stacks for the then-new TypeScript adoption in Ruangguru's FE future projects.",
      "Heavily involved in Ruangguru's new FE engineer hiring. This involvement results in a faster FE engineering hiring process while ensuring only technical and culturally fit candidates pass. I also streamlined the FE team's onboarding process by creating documents and guides, resulting in a faster, more precise, and smoother onboarding for the new engineers while making it more scalable and reproducible.",
    ],
    skills: ["Frontend Engineering", "Systems Design", "Software Engineering"],
    programmingLanguages: ["JavaScript", "TypeScript", "ReasonML", "SQL", "HTML", "CSS"],
    frameworks: ["React.js", "React Native", "ReasonReact"],
  },
  {
    title: "Frontend Engineer",
    organization: "Ruangguru",
    period: "January 2018 - August 2019",
    employmentType: "Full-time",
    location: "Greater Jakarta Area, Indonesia",
    locationType: "Hybrid",
    details: [
      "Became one of the pioneering engineers in Ruang Belajar's Desktop app development using ReasonML, ReasonReact, and Electron. Heavily involved in its core and primitive UI components development (created more than 50% of it) and routing design, while also helping other engineers (mobile engineers) to pick up React and web technology in general. This project is the first joint project between Ruangguru's frontend and Mobile engineers. Opening up a new possibility of higher app development's velocity in Ruangguru.",
      "Involved in Ruangguru's new frontend engineer hiring process by assessing their computational thinking and React.js problem-solving skills through coding challenges. This involvement results in a faster frontend engineering division's hiring process while ensuring that only the high-quality one passed.",
      "Developed Ruang Kerja CMS question and question-set modules using React and Draft.js. Resulting in well-functioning rich-text editor implementation for question and question-set generation tasks in Ruang Kerja apps.",
      "Developed and set up various internal frontend tooling, including command-line applications to bootstrap new web projects, miscellaneous UI kits, rich text editor, and JavaScript utility functions. Resulting in a higher code sharing and development speed for Ruangguru's engineering team.",
      "Led a team of frontend developers to create Ruang Kerja's company dashboard using React JS stacks, flow-typed, and data visualization tools. Also did end-to-end testing for it using cypress. Resulting in a finely crafted and runtime-error-free dashboard web app.",
      "Became one of the pioneering engineers in Ruang Kerja's React Native app development. Resulting in more efficient engineering resource usage for Ruangguru by expanding the uses of its frontend engineers while theoretically cutting the cost of apps development down almost to 50% without losing any of native apps' development speed.",
    ],
    skills: ["Frontend Engineering", "Software Engineering"],
    programmingLanguages: ["JavaScript", "TypeScript", "ReasonML", "HTML", "CSS"],
    frameworks: ["React.js", "React Native", "ReasonReact"],
    type: "work",
  },
  {
    title: "Junior Frontend Engineer",
    organization: "Ruangguru",
    period: "October 2017 - December 2017",
    employmentType: "Full-time",
    location: "Greater Jakarta Area, Indonesia",
    locationType: "Hybrid",
    details: [
      "Led a team of frontend developers to develop and optimize Ruang Uji's react stacks and deployment. The result was more than 53.86% smaller initial download size (all assets included), 9.52% lower request number, 46.72% faster finish time, 137.10% faster DOMContentLoad time, and 62.49% faster load time than the original angular.js' stacks (2G connection, 256kbps 800ms RTT). I also made subsequent pages load substantially faster by implementing on-point code optimization, aggressive code-splitting, and various images' lazy loading.",
      "Refactored https://ruangguru.com/ assets and code base using IMGIX, AWS S3 bucket, and fastly CDN. The result was a load time speed improvement of more than 300% (from more than 12 seconds average to under 3 seconds) and the advancement of its https://www.webpagetest.org/ average score of B to all A's without sacrificing its assets' apparent quality.",
      "Rewrote and migrated Ruang Uji (https://uji.ruangguru.com) from Angular 1's (AngularJS) stacks to React.js' stacks from scratch. Thus solved the old \"exam event\" problem (e.g., no automatic submission in the background, submission error handler, continuing to the last exam on reload) at Ruang Uji. This project also results in the tech stack's modernization, making it less error-prone.",
      "Automated web apps' bug tracking using sentry (Raven.js) and deployment from Gitlab to AWS S3 and production using Codeship. The result was more precise bug tracking and faster web app integration, deployment, and delivery.",
    ],
    skills: ["Frontend Engineering", "Software Engineering"],
    programmingLanguages: ["JavaScript", "Flow Type", "HTML", "CSS"],
    frameworks: ["React.js"],
    type: "work",
  },
  {
    title: "Hijra Keep On Moving Awards 2025: Outstanding Cost-Slasher",
    organization: "Hijra",
    period: "October 2025",
    details: [
      "Associated with: Head of Engineering at Hijra Bank",
      "Description: Award for executing the most impactful cost-cutting initiative — the core banking migration achieving 95% reduction in operational costs.",
    ],
    type: "honor",
  },
  {
    title: "Certificate of Appreciation: Hijra Group's Exceptional Performer",
    organization: "Hijra Group",
    period: "May 2024",
    details: [
      "Associated with: Engineering Manager - Alami P2P Lending and Hijra Bank Financing at Hijra",
      'Description: Appreciation for "Exceptional Performance" in the performance appraisal cycle 2023, based on Hijra Group\'s CFR 2023.',
    ],
    type: "honor",
  },
  {
    title: "Ruangguru's Chief of The Month: September 2019",
    organization: "Ruangguru",
    period: "September 2019",
    details: [
      "Associated with: Senior Frontend Engineer at Ruangguru",
      "Description: Ruang Guru's Most Performant Employee Award for September 2019",
    ],
    type: "honor",
  },
  {
    title: "Ruangguru's Chief of The Month: August 2018",
    organization: "Ruangguru",
    period: "August 2018",
    details: [
      "Associated with: Frontend Engineer at Ruangguru",
      "Description: Ruang Guru's Most Performant Employee Award for August 2018.",
    ],
    type: "honor",
  },
  {
    title: "Certificate of Completion - System Design Assessment",
    organization: "AlgoExpert",
    period: "December 2021",
    details: ["Credential ID: 524646adaa", "Skills: System Design"],
    links: {
      credential: "https://certificate.algoexpert.io/SE-524646adaa",
    },
    type: "certification",
  },
  {
    title: "An Introduction to Programming in Go",
    organization: "Educative, Inc.",
    period: "July 2021",
    details: ["Credential ID: 665EM3iZrX0Llgn9Vsj5MP6Nkm3lu7"],
    type: "certification",
  },
  {
    title: "Learn Node.js: The Complete Course for Beginners",
    organization: "Educative, Inc.",
    period: "July 2021",
    details: ["Credential ID: xGD3yRS9YWMvWjXkyc7wykvXPYm0UE"],
    type: "certification",
  },
  {
    title: "Mastering Concurrency in Go",
    organization: "Educative, Inc.",
    period: "July 2021",
    details: ["Credential ID: VmBEWXTXZ3oBWRnP0hMJ0pz5myoNcr"],
    type: "certification",
  },
  {
    title: "Web Application and Software Architecture 101",
    organization: "Educative, Inc.",
    period: "July 2021",
    details: ["Credential ID: lvrojo6L9GzT6gnWN532pOuNqEn94myQDuM"],
    type: "certification",
  },
  {
    title: "Database Design Fundamentals for Software Engineers",
    organization: "Educative, Inc.",
    period: "June 2021",
    details: ["Credential ID: KOnpGJIBLJ90p2rlvcQAw1vNO38rtB"],
    type: "certification",
  },
  {
    title: "Languages",
    organization: "",
    period: "",
    details: [
      "Bahasa Indonesia|Native or bilingual proficiency",
      "English|Full professional proficiency",
      "German|Limited working proficiency",
      "Arabic|Elementary proficiency",
    ],
    type: "language",
  },
  {
    title: "Master's Program, Electrical Systems Engineering (not completed)",
    organization: "Paderborn University, Germany",
    period: "October 2013 - October 2016",
    details: [
      "English-taught program; 42 of 120 ECTS credited, weighted grade 1.95 (German scale)",
      "Selected completed modules: Introduction to Algorithm (1.7), Projects I - Energy Structure (1.0), Management of Technical Projects (1.7)",
    ],
    type: "education",
  },
  {
    title: "German Language Study",
    organization: "VHS Aachen, Germany",
    period: "October 2012 - October 2013",
    details: ["One year of German-language study ahead of postgraduate studies in Germany"],
    type: "education",
  },
  {
    title: "Bachelor of Engineering (B.Eng.)",
    organization: "Institut Teknologi Bandung",
    period: "July 2005 - July 2011",
    details: ["Field of study: Electrical and Electronics Engineering", "Grade: 3.0"],
    type: "education",
  },
];

export const parseDate = (dateString: string): Date => {
  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  const [month, year] = dateString.split(" ");
  const monthIndex = months.indexOf(month);
  if (monthIndex === -1) {
    throw new Error(`Invalid month: ${month}`);
  }
  return new Date(parseInt(year), monthIndex);
};

export const calculateDuration = (period: string): number => {
  const [start, end] = period.split(" - ");
  const startDate = parseDate(start);
  const endDate = end === "Present" ? new Date() : parseDate(end);

  // Calculate full months
  const months = (endDate.getFullYear() - startDate.getFullYear()) * 12 + (endDate.getMonth() - startDate.getMonth());

  // Add 1 to include both start and end months
  return months + 1;
};

// The calendar month a date falls in, as a single comparable integer.
const toMonthIndex = (date: Date): number => date.getFullYear() * 12 + date.getMonth();

export const calculateTotalDuration = (periods: { start: Date; end: Date }[]): number => {
  if (periods.length === 0) return 0;

  // Each period is an inclusive [startMonth, endMonth] range. Merge the ranges
  // before counting: adding each period's own inclusive length would count a
  // shared month twice whenever one role starts in the month another ended.
  const ranges = periods
    .map((period) => ({
      start: toMonthIndex(period.start),
      end: toMonthIndex(period.end),
    }))
    .filter((range) => range.end >= range.start)
    .sort((a, b) => a.start - b.start);

  if (ranges.length === 0) return 0;

  let totalMonths = 0;
  let spanStart = ranges[0].start;
  let spanEnd = ranges[0].end;

  for (const range of ranges.slice(1)) {
    if (range.start <= spanEnd + 1) {
      // Overlapping or back-to-back: extend the span rather than recounting it.
      spanEnd = Math.max(spanEnd, range.end);
    } else {
      totalMonths += spanEnd - spanStart + 1;
      spanStart = range.start;
      spanEnd = range.end;
    }
  }

  return totalMonths + (spanEnd - spanStart + 1);
};

export const formatDuration = (months: number): string => {
  const years = Math.floor(months / 12);
  const remainingMonths = months % 12;

  if (years > 0 && remainingMonths > 0) {
    return `${years} year${years > 1 ? "s" : ""} ${remainingMonths} month${remainingMonths > 1 ? "s" : ""}`;
  } else if (years > 0) {
    return `${years} year${years > 1 ? "s" : ""}`;
  } else {
    return `${remainingMonths} month${remainingMonths > 1 ? "s" : ""}`;
  }
};

type SkillTotal = { name: string; duration: number };

// A dated engagement — a CV work entry or a personal project — that can carry
// skills, programming languages, and/or frameworks into the shared rollup.
// Structural typing lets callers pass CVEntry[] or Project[] (or a mix)
// without this module importing either feature's concrete type.
export type SkillSource = {
  period: string;
  skills?: string[];
  programmingLanguages?: string[];
  frameworks?: string[];
  aiSkills?: string[];
};

/**
 * Aggregates one facet (skills, languages, or frameworks) across every dated
 * source passed in — CV work entries and personal projects alike.
 *
 * The five-year window decides *which* items are listed: an item appears only
 * if it was used in an engagement active within the window. The duration
 * reported alongside each item is a lifetime total across all sources, so it
 * is not truncated by that window. Overlapping date ranges for the same item
 * (e.g. a skill used in a job and a concurrent side project) are merged, not
 * double-counted — see calculateTotalDuration.
 */
const topItemsLastFiveYears = (
  data: SkillSource[],
  selectItems: (entry: SkillSource) => string[] | undefined,
): SkillTotal[] => {
  const fiveYearsAgo = new Date();
  fiveYearsAgo.setFullYear(fiveYearsAgo.getFullYear() - 5);

  const itemInfo: {
    [key: string]: { usedInWindow: boolean; periods: { start: Date; end: Date }[] };
  } = {};

  data
    .filter((entry) => !!entry.period)
    .forEach((entry) => {
      const [startStr, endStr] = entry.period.split(" - ");
      if (!startStr || !endStr) return;
      const start = parseDate(startStr);
      const end = endStr === "Present" ? new Date() : parseDate(endStr);

      selectItems(entry)?.forEach((name) => {
        const info = (itemInfo[name] ??= { usedInWindow: false, periods: [] });
        if (end >= fiveYearsAgo) {
          info.usedInWindow = true;
        }
        info.periods.push({ start, end });
      });
    });

  return Object.entries(itemInfo)
    .filter(([, info]) => info.usedInWindow)
    .map(([name, info]) => ({
      name,
      duration: calculateTotalDuration(info.periods),
    }))
    .sort((a, b) => b.duration - a.duration) // Longest-held first
    .slice(0, 10);
};

export const getTopSkillsLastFiveYears = (data: SkillSource[]): SkillTotal[] =>
  topItemsLastFiveYears(data, (entry) => entry.skills);

export const getTopLanguagesLastFiveYears = (data: SkillSource[]): SkillTotal[] =>
  topItemsLastFiveYears(data, (entry) => entry.programmingLanguages);

export const getTopFrameworksLastFiveYears = (data: SkillSource[]): SkillTotal[] =>
  topItemsLastFiveYears(data, (entry) => entry.frameworks);

export const getTopAISkillsLastFiveYears = (data: SkillSource[]): SkillTotal[] =>
  topItemsLastFiveYears(data, (entry) => entry.aiSkills);
