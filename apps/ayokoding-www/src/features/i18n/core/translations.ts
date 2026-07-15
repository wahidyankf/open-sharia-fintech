import type { Locale } from "./config";

const translations: Record<Locale, Record<string, string>> = {
  en: {
    readMore: "Read More",
    lastUpdated: "Last updated",
    publishedOn: "Published on",
    author: "Author",
    tags: "Tags",
    categories: "Categories",
    share: "Share",
    relatedContent: "Related Content",
    openSourceProject: "Open-Source Project",
    search: "Search...",
    onThisPage: "On this page",
    previous: "Previous",
    next: "Next",
    noResults: "No results found",
    toggleTheme: "Toggle theme",
    skipToContent: "Skip to content",
    toolsPageTitle: "Tools",
    toolsPageCalcLink: "Cost of Living Calculator",
    toolsPageCalcDesc: "Compare monthly living costs, savings, and the minimum role needed across cities.",
    breadcrumbHome: "Home",
    breadcrumbCalculator: "Calculator",

    // Calculator — page
    calcTitle: "Cost of Living Calculator",
    calcSubtitle: "Compare cost of living and salary savings across cities",
    ariaTabsNav: "Calculator tabs",
    tabCostOfLiving: "Cost of living",
    tabCostDesc: "Compare monthly living costs across cities",
    tabSavings: "Savings",
    tabSavingsDesc: "See how much you'd save",
    tabMinRole: "Minimum role",
    tabMinRoleDesc: "Find the min role you need",
    dataLastUpdated: "Data last updated",
    estimatesOnly: "Estimates only",

    // Calculator — disclaimers
    disclaimerPension: "Savings are before voluntary pension / retirement contributions.",
    disclaimerClothing: "Clothing and personal care are folded into lifestyle expenses.",
    disclaimerFx:
      "A positive USD savings figure does not mean equal purchasing power — USD uses a nominal FX snapshot, not PPP.",
    disclaimerSnapshot: "Data is a snapshot — verify current figures before making relocation decisions.",
    disclaimerTax:
      "Tax is a simplified effective rate (federal + sub-national for US/CA/CH only) — not a full bracket calculation; excludes filing status, deductions, benefits-in-kind, and contribution caps.",
    disclaimerHealthcare: "Healthcare models out-of-pocket costs only; the funding scheme is shown per country.",
    disclaimerRelocation:
      "Relocation sunk costs are a one-time estimate kept out of monthly savings math; the cash cushion is a reserve you keep, not a sunk cost.",
    disclaimerRoleSalary:
      "Role salary is modeled at the national (country) level — cities inherit their country's p25/median/p75 distribution.",
    disclaimerNonSalary:
      "Non-salary comp (RSU/equity + bonus) is informational total-comp context only, not part of the savings math.",

    // Calculator — geo filters
    labelRegion: "Region",
    labelCountry: "Country",
    labelCity: "City",
    optAllRegions: "All regions",
    optAllCountries: "All countries",
    optAllCities: "All cities",
    clearRegion: "Clear",
    regionAutoAdvisory: "Region updated automatically to match the selected country.",

    // Calculator — region display names (UWT-004). The serialized region KEY stays English
    // (URL stability); only these display labels are localized. MENA/Nordics are expanded.
    regionAsean: "ASEAN",
    regionJapan: "Japan",
    regionEurope: "Europe",
    regionNordics: "Nordics (Northern Europe)",
    regionAmericas: "Americas",
    regionMena: "MENA (Middle East & North Africa)",
    regionAsia: "Asia",
    regionOceania: "Oceania",
    regionAfrica: "Africa",

    // Calculator — controls
    labelAdults: "Adults",
    labelPreschoolKids: "Preschool children",
    labelSchoolKids: "School-age children",
    labelSchoolType: "School type",
    optPublic: "Public",
    optPrivate: "Private",
    schoolTypeHint: "add school-age children to choose",
    // UWT-015: native hover tooltip (title) on the disabled Public/Private buttons so a
    // first-timer learns the prerequisite without relying on the screen-reader-only hint.
    schoolTypeDisabledTitle: "Add a school-age child to enable this option",
    foreignerPublicSchoolNote:
      "Public school isn't open to foreign residents in every country; where it isn't (e.g. UAE, Singapore), the private-school cost is used instead.",
    publicSchoolForeignerFlag: "public n/a → private",
    publicSchoolForeignerFlagBadge: "Private — public not open to foreigners",
    labelArea: "Area",
    optCenter: "City center",
    optRural: "Rural",

    // Calculator — cost-of-living table
    colCountry: "Country",
    colCity: "City",
    colHealthcareScheme: "Healthcare scheme",
    tooltipHealthcareScheme:
      "How healthcare costs are funded in this country: tax-funded, mandatory payroll insurance, or out-of-pocket.",
    colHousing: "Housing",
    colFood: "Food",
    colTransport: "Transport",
    colUtilities: "Utilities",
    colHealthcareOOP: "Healthcare (OOP)",
    colHealthcareOOPPrefix: "Healthcare",
    colChildcare: "Childcare",
    colSchool: "School",
    colEssentials: "Essentials",
    colTotal: "Total",
    previewMonthlyEstimate: "estimated monthly essentials",
    // UWT-006: labels the pre-populated min-role preview panel as illustrative.
    previewExampleLabel: "Example",
    colRelocationSunk: "Relocation (sunk)",
    colLiquidityReserve: "Liquidity reserve",
    tooltipRelocationSunk:
      "One-time sunk costs: rental deposit, key money, moving, and visa fees. Not a monthly expense.",
    tooltipLiquidityReserve:
      "Cash cushion you keep on hand — not a sunk cost. Covers first months before salary starts.",
    oopLegend: "OOP = out-of-pocket — healthcare you pay yourself, on top of any tax-funded or insurance coverage.",

    // Calculator — healthcare scheme badges
    healthcareTaxFunded: "tax-funded",
    healthcareMandatoryPayroll: "mandatory payroll insurance",
    healthcareOutOfPocket: "out-of-pocket",

    // Calculator — city detail
    sectionMonthlyExpenses: "Monthly expenses",
    sectionRelocationCosts: "Relocation costs",
    labelHousing: "Housing",
    labelFood: "Food",
    labelTransport: "Transport",
    labelUtilities: "Utilities",
    labelHealthcareOOP: "Healthcare (OOP)",
    labelChildcare: "Childcare",
    labelSchool: "School",
    labelEssentialsSubtotal: "Essentials subtotal",
    labelMonthlyTotal: "Monthly total",
    labelRelocationSunkCost: "One-time relocation sunk cost",
    labelLiquidityReserve: "Liquidity reserve (cash cushion — kept, not spent)",
    backToAllCities: "← Back to all cities",

    // Calculator — savings table
    savingsEmptyStateMessage: "Enter your gross monthly salary to see how much you could save in each city.",
    grossMonthlySalaryLabel: "Gross monthly salary (before tax)",
    salaryCurrencyIndicator: "Currency: USD",
    salaryCurrencyExplanation: "Salaries are compared in USD across all cities.",
    annualGrossLabel: "Annual gross",
    nonSalaryCompNote: "Non-salary comp (RSU/equity + bonus) is informational only — not in savings math.",
    colNet: "Net (monthly)",
    colSavingsEssential: "Savings after essentials ↕",
    colSavingsLifestyle: "Savings after lifestyle",
    colNonSalaryComp: "Typical non-salary comp (info, annual)",
    colTotalComp: "Total comp (info, annual)",
    sortBySavings: "Sort by savings",
    subNationalIndicator: "(fed+state)",

    // Calculator — min-role table
    labelBaselineSource: "How to set your target",
    optSavingsTarget: "Monthly savings target",
    optReferenceRole: "Match a role",
    optMySalary: "My salary",
    hintSavingsTarget: "Enter a monthly savings goal — the table marks the lowest role whose best city reaches it.",
    hintReferenceRole:
      "Pick a role and city as the yardstick — the table marks the lowest role that saves at least as much, no dollar figure needed.",
    hintMySalary:
      "Enter your current gross salary — the table marks the lowest role that saves at least what you do today.",
    labelMonthlySavingsTarget: "Monthly savings target",
    labelTargetCurrency: "Target currency",
    labelRefCity: "Reference city",
    labelRefRole: "Reference role",
    labelMyGrossMonthly: "My gross monthly",
    labelMySalaryCity: "My salary city",
    labelSalaryInputCurrency: "Salary currency",
    labelDisplayCurrency: "Display currency",
    rankBasisNote:
      "Ranking key: essential savings (housing + food + transport + utilities + healthcare + school). Lifestyle excluded — personal preference variable.",
    nonSalaryRankNote: "Non-salary comp (RSU / equity / bonus) is informational only — not used in ranking.",
    noQualifierMessage: "No role reaches this savings bar in any city.",
    minRoleEmptyStateMessage: "Enter a monthly savings target to see which roles reach it in each city.",
    seRolesCaption: "Roles: software-engineering (IC + management)",
    qualifyingDivider: "— roles below do not reach the savings bar —",
    moreBelowBar: "more (city, role) pairs below your bar (not shown)",
    colRole: "Role",
    colTrack: "Track",
    colBestCity: "Best city",
    colP25: "P25 (monthly)",
    colMedian: "Median",
    colP75: "P75",
    colEssentialSavings: "Essential savings",
    colNonSalaryCompInfo: "Non-salary comp",
    minimumMarker: "← min",
    // UWT-010: percentile gloss tooltips for the salary-distribution headers.
    tooltipP25: "25th-percentile monthly salary — a quarter of people in this role earn less.",
    tooltipMedian: "Median (50th-percentile) monthly salary for this role.",
    tooltipP75: "75th-percentile monthly salary — a quarter of people in this role earn more.",
    // UWT-013: expanded Track labels (the table renders these instead of bare "ic"/"mgmt").
    trackIc: "Individual contributor",
    trackMgmt: "Management",
    // UWT-003: gloss for the shortened "Non-salary comp" header.
    tooltipNonSalaryComp: "RSU/equity + bonus — annual total, informational only, not used in savings math.",

    // IA navigation revamp — landing homepage + global nav
    heroHeading: "Learn to build software, the clear way.",
    heroIntro:
      "AyoKoding is an open, bilingual learning hub for software engineering — practical guides, worked examples, and free tools that grow with you.",
    heroCtaLearn: "Start learning",
    heroCtaTools: "Explore tools",
    navLearn: "Learn",
    navTools: "Tools",
    browseTitle: "Browse",
    browseIntro: "Browse every AyoKoding section in one place.",
    sectionBlurbFallback: "Explore this section.",
    toolsTeaserKicker: "Tools",
    toolsTeaserTitle: "Cost of Living Calculator",
    toolsTeaserDesc: "Compare monthly living costs, savings, and the minimum role you need across cities.",
    toolsTeaserCta: "Open the calculator",
    footerLearn: "Learn",
    footerTools: "Tools",
    footerAbout: "About",
    footerBrowseAll: "Browse all",
    footerCalculator: "Cost of Living Calculator",
    footerAboutAyokoding: "About AyoKoding",
    footerTerms: "Terms & Conditions",
    footerProject: "Project",
    sectionExploreHeading: "Explore",

    // Mobile nav drawer — preset width control
    mobileNavWidthLabel: "Drawer width",
    mobileNavWidthDefault: "Default",
    mobileNavWidthWide: "Wide",

    // Resizable docs sidebar — drag/keyboard handle accessible name
    resizableSidebarHandleLabel: "Resize panel",
  },
  id: {
    readMore: "Baca Selengkapnya",
    lastUpdated: "Terakhir diperbarui",
    publishedOn: "Dipublikasikan pada",
    author: "Penulis",
    tags: "Tag",
    categories: "Kategori",
    share: "Bagikan",
    relatedContent: "Konten Terkait",
    openSourceProject: "Proyek Open-Source",
    search: "Cari...",
    onThisPage: "Di halaman ini",
    previous: "Sebelumnya",
    next: "Selanjutnya",
    noResults: "Tidak ada hasil",
    toggleTheme: "Ubah tema",
    skipToContent: "Langsung ke konten",
    toolsPageTitle: "Alat",
    toolsPageCalcLink: "Kalkulator Biaya Hidup",
    toolsPageCalcDesc:
      "Bandingkan biaya hidup bulanan, tabungan, dan jabatan minimum yang dibutuhkan di berbagai kota.",
    breadcrumbHome: "Beranda",
    breadcrumbCalculator: "Kalkulator",

    // Calculator — page
    calcTitle: "Kalkulator Biaya Hidup",
    calcSubtitle: "Bandingkan biaya hidup dan tabungan gaji di berbagai kota",
    ariaTabsNav: "Tab kalkulator",
    tabCostOfLiving: "Biaya hidup",
    tabCostDesc: "Bandingkan biaya hidup bulanan di berbagai kota",
    tabSavings: "Tabungan",
    tabSavingsDesc: "Lihat seberapa banyak yang bisa Anda hemat",
    tabMinRole: "Jabatan minimum",
    tabMinRoleDesc: "Temukan jabatan minimum yang Anda butuhkan",
    dataLastUpdated: "Data terakhir diperbarui",
    estimatesOnly: "Hanya perkiraan",

    // Calculator — disclaimers
    disclaimerPension: "Tabungan sebelum kontribusi pensiun / dana hari tua sukarela.",
    disclaimerClothing: "Pakaian dan perawatan pribadi termasuk dalam pengeluaran gaya hidup.",
    disclaimerFx:
      "Angka tabungan USD positif tidak berarti daya beli yang sama — USD menggunakan snapshot FX nominal, bukan PPP.",
    disclaimerSnapshot: "Data adalah snapshot — verifikasi angka terkini sebelum membuat keputusan relokasi.",
    disclaimerTax:
      "Pajak menggunakan tarif efektif yang disederhanakan (federal + sub-nasional untuk AS/CA/CH saja) — bukan perhitungan bracket penuh; tidak termasuk status pengisian, potongan, tunjangan natura, dan batas kontribusi.",
    disclaimerHealthcare: "Kesehatan memodelkan biaya out-of-pocket saja; skema pendanaan ditampilkan per negara.",
    disclaimerRelocation:
      "Biaya sunk relokasi adalah perkiraan sekali dan tidak termasuk dalam perhitungan tabungan bulanan; cadangan tunai adalah dana yang Anda simpan, bukan biaya.",
    disclaimerRoleSalary:
      "Gaji jabatan dimodelkan di tingkat nasional (negara) — kota mewarisi distribusi p25/median/p75 negaranya.",
    disclaimerNonSalary:
      "Kompensasi non-gaji (RSU/ekuitas + bonus) hanya sebagai konteks informasi total kompensasi, bukan bagian dari perhitungan tabungan.",

    // Calculator — geo filters
    labelRegion: "Wilayah",
    labelCountry: "Negara",
    labelCity: "Kota",
    optAllRegions: "Semua wilayah",
    optAllCountries: "Semua negara",
    optAllCities: "Semua kota",
    clearRegion: "Hapus",
    regionAutoAdvisory: "Wilayah diperbarui otomatis agar sesuai dengan negara yang dipilih.",

    // Calculator — region display names (UWT-004). The serialized region KEY stays English
    // (URL stability); only these display labels are localized. MENA/Nordics are expanded.
    regionAsean: "ASEAN",
    regionJapan: "Jepang",
    regionEurope: "Eropa",
    regionNordics: "Nordik (Eropa Utara)",
    regionAmericas: "Amerika",
    regionMena: "Timur Tengah & Afrika Utara",
    regionAsia: "Asia",
    regionOceania: "Oseania",
    regionAfrica: "Afrika",

    // Calculator — controls
    labelAdults: "Dewasa",
    labelPreschoolKids: "Anak prasekolah",
    labelSchoolKids: "Anak usia sekolah",
    labelSchoolType: "Jenis sekolah",
    optPublic: "Negeri",
    optPrivate: "Swasta",
    schoolTypeHint: "tambahkan anak usia sekolah untuk memilih",
    // UWT-015: native hover tooltip (title) on the disabled Public/Private buttons.
    schoolTypeDisabledTitle: "Tambahkan anak usia sekolah untuk mengaktifkan opsi ini",
    foreignerPublicSchoolNote:
      "Sekolah negeri nggak terbuka buat warga asing di semua negara; di tempat yang nggak (mis. UEA, Singapura), biaya sekolah swasta yang dipakai.",
    publicSchoolForeignerFlag: "negeri n/a → swasta",
    publicSchoolForeignerFlagBadge: "Swasta — negeri tak terbuka untuk WNA",
    labelArea: "Wilayah",
    optCenter: "Pusat kota",
    optRural: "Pedesaan",

    // Calculator — cost-of-living table
    colCountry: "Negara",
    colCity: "Kota",
    colHealthcareScheme: "Skema kesehatan",
    tooltipHealthcareScheme:
      "Bagaimana biaya kesehatan didanai di negara ini: didanai pajak, asuransi penggajian wajib, atau bayar sendiri.",
    colHousing: "Perumahan",
    colFood: "Makanan",
    colTransport: "Transportasi",
    colUtilities: "Utilitas",
    colHealthcareOOP: "Kesehatan (OOP)",
    colHealthcareOOPPrefix: "Kesehatan",
    colChildcare: "Penitipan anak",
    colSchool: "Sekolah",
    colEssentials: "Kebutuhan pokok",
    colTotal: "Total",
    previewMonthlyEstimate: "perkiraan kebutuhan pokok bulanan",
    // UWT-006: labels the pre-populated min-role preview panel as illustrative.
    previewExampleLabel: "Contoh",
    colRelocationSunk: "Relokasi (biaya hangus)",
    colLiquidityReserve: "Cadangan likuiditas",
    tooltipRelocationSunk:
      "Biaya hangus sekali: deposit sewa, uang kunci, pindahan, dan biaya visa. Bukan pengeluaran bulanan.",
    tooltipLiquidityReserve:
      "Dana cadangan yang Anda simpan — bukan biaya hangus. Menutup bulan-bulan awal sebelum gaji mulai.",
    oopLegend:
      "OOP = out-of-pocket — biaya kesehatan yang Anda bayar sendiri, di luar jaminan dari pajak atau asuransi.",

    // Calculator — healthcare scheme badges
    healthcareTaxFunded: "didanai pajak",
    healthcareMandatoryPayroll: "asuransi penggajian wajib",
    healthcareOutOfPocket: "bayar sendiri",

    // Calculator — city detail
    sectionMonthlyExpenses: "Pengeluaran bulanan",
    sectionRelocationCosts: "Biaya relokasi",
    labelHousing: "Perumahan",
    labelFood: "Makanan",
    labelTransport: "Transportasi",
    labelUtilities: "Utilitas",
    labelHealthcareOOP: "Kesehatan (OOP)",
    labelChildcare: "Penitipan anak",
    labelSchool: "Sekolah",
    labelEssentialsSubtotal: "Subtotal kebutuhan pokok",
    labelMonthlyTotal: "Total bulanan",
    labelRelocationSunkCost: "Biaya sunk relokasi sekali",
    labelLiquidityReserve: "Cadangan likuiditas (dana cadangan — disimpan, tidak dibelanjakan)",
    backToAllCities: "← Kembali ke semua kota",

    // Calculator — savings table
    savingsEmptyStateMessage:
      "Masukkan gaji kotor bulanan Anda untuk melihat berapa banyak yang bisa Anda hemat di setiap kota.",
    grossMonthlySalaryLabel: "Gaji kotor bulanan (sebelum pajak)",
    salaryCurrencyIndicator: "Mata uang: USD",
    salaryCurrencyExplanation: "Gaji dibandingkan dalam USD di semua kota.",
    annualGrossLabel: "Total gaji tahunan",
    nonSalaryCompNote:
      "Kompensasi non-gaji (RSU/ekuitas + bonus) hanya informasi — tidak termasuk dalam perhitungan tabungan.",
    colNet: "Bersih (bulanan)",
    colSavingsEssential: "Tabungan setelah kebutuhan pokok ↕",
    colSavingsLifestyle: "Tabungan setelah gaya hidup",
    colNonSalaryComp: "Kompensasi non-gaji tipikal (info, tahunan)",
    colTotalComp: "Total kompensasi (info, tahunan)",
    sortBySavings: "Urutkan berdasarkan tabungan",
    subNationalIndicator: "(federal+negara bagian)",

    // Calculator — min-role table
    labelBaselineSource: "Cara menetapkan target",
    optSavingsTarget: "Target tabungan bulanan",
    optReferenceRole: "Samakan jabatan",
    optMySalary: "Gaji saya",
    hintSavingsTarget:
      "Masukkan target tabungan bulanan — tabel menandai jabatan terendah yang kota terbaiknya mencapainya.",
    hintReferenceRole:
      "Pilih jabatan dan kota sebagai patokan — tabel menandai jabatan terendah yang menabung setidaknya sebanyak itu, tanpa perlu angka.",
    hintMySalary:
      "Masukkan gaji kotor Anda saat ini — tabel menandai jabatan terendah yang menabung setidaknya sebanyak Anda sekarang.",
    labelMonthlySavingsTarget: "Target tabungan bulanan",
    labelTargetCurrency: "Mata uang target",
    labelRefCity: "Kota referensi",
    labelRefRole: "Jabatan referensi",
    labelMyGrossMonthly: "Gaji kotor bulanan saya",
    labelMySalaryCity: "Kota gaji saya",
    labelSalaryInputCurrency: "Mata uang gaji",
    labelDisplayCurrency: "Mata uang tampilan",
    rankBasisNote:
      "Kunci peringkat: tabungan kebutuhan pokok (perumahan + makanan + transportasi + utilitas + kesehatan + sekolah). Gaya hidup dikecualikan — variabel preferensi pribadi.",
    nonSalaryRankNote: "Kompensasi non-gaji (RSU / ekuitas / bonus) hanya informasi — tidak digunakan dalam peringkat.",
    noQualifierMessage: "Tidak ada jabatan yang mencapai target tabungan ini di kota manapun.",
    minRoleEmptyStateMessage:
      "Masukkan target tabungan bulanan untuk melihat jabatan mana yang mencapainya di setiap kota.",
    seRolesCaption: "Jabatan: rekayasa perangkat lunak (IC + manajemen)",
    qualifyingDivider: "— jabatan di bawah tidak mencapai target tabungan —",
    moreBelowBar: "pasangan (kota, jabatan) lain di bawah ambang Anda (tidak ditampilkan)",
    colRole: "Jabatan",
    colTrack: "Jalur",
    colBestCity: "Kota terbaik",
    colP25: "P25 (bulanan)",
    colMedian: "Median",
    colP75: "P75",
    colEssentialSavings: "Tabungan kebutuhan pokok",
    colNonSalaryCompInfo: "Kompensasi non-gaji",
    minimumMarker: "← min",
    // UWT-010: percentile gloss tooltips for the salary-distribution headers.
    tooltipP25: "Gaji bulanan persentil ke-25 — seperempat orang di jabatan ini berpenghasilan lebih rendah.",
    tooltipMedian: "Gaji bulanan median (persentil ke-50) untuk jabatan ini.",
    tooltipP75: "Gaji bulanan persentil ke-75 — seperempat orang di jabatan ini berpenghasilan lebih tinggi.",
    // UWT-013: expanded Track labels (the table renders these instead of bare "ic"/"mgmt").
    trackIc: "Kontributor individu",
    trackMgmt: "Manajemen",
    // UWT-003: gloss for the shortened "Non-salary comp" header.
    tooltipNonSalaryComp:
      "RSU/ekuitas + bonus — total tahunan, hanya informasi, tidak digunakan dalam perhitungan tabungan.",

    // IA navigation revamp — landing homepage + global nav
    heroHeading: "Belajar membangun perangkat lunak, dengan cara yang jelas.",
    heroIntro:
      "AyoKoding adalah pusat belajar terbuka dwibahasa untuk rekayasa perangkat lunak — panduan praktis, contoh nyata, dan alat gratis yang tumbuh bersama Anda.",
    heroCtaLearn: "Mulai belajar",
    heroCtaTools: "Jelajahi alat",
    navLearn: "Belajar",
    navTools: "Alat",
    browseTitle: "Jelajahi",
    browseIntro: "Jelajahi seluruh bagian AyoKoding dalam satu tempat.",
    sectionBlurbFallback: "Jelajahi bagian ini.",
    toolsTeaserKicker: "Alat",
    toolsTeaserTitle: "Kalkulator Biaya Hidup",
    toolsTeaserDesc: "Bandingkan biaya hidup bulanan, tabungan, dan peran minimum yang Anda butuhkan di berbagai kota.",
    toolsTeaserCta: "Buka kalkulator",
    footerLearn: "Belajar",
    footerTools: "Alat",
    footerAbout: "Tentang",
    footerBrowseAll: "Jelajahi semua",
    footerCalculator: "Kalkulator Biaya Hidup",
    footerAboutAyokoding: "Tentang AyoKoding",
    footerTerms: "Syarat & Ketentuan",
    footerProject: "Proyek",
    sectionExploreHeading: "Jelajahi",

    // Mobile nav drawer — preset width control
    mobileNavWidthLabel: "Lebar drawer",
    mobileNavWidthDefault: "Standar",
    mobileNavWidthWide: "Lebar",

    // Resizable docs sidebar — drag/keyboard handle accessible name
    resizableSidebarHandleLabel: "Ubah ukuran panel",
  },
};

export function t(locale: Locale, key: string): string {
  return translations[locale]?.[key] ?? key;
}
