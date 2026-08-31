import PDFDocument from "pdfkit";
import type { CvPdfDocumentModel, CvPdfSection } from "../core/pdf";

// Matches the color palette used by the reference ATS resume in
// wkf-knowledge/career-materials/generate-cv-ats-pdf.py.
const COLORS = {
  navy: "#1F4E79",
  gray: "#6B7280",
  black: "#000000",
};

const FOOTER_MARGIN_FROM_BOTTOM = 34;

const addSectionHeading = (pdf: PDFKit.PDFDocument, title: string): void => {
  pdf.moveDown(0.8);
  pdf.font("Helvetica-Bold").fontSize(13).fillColor(COLORS.navy).text(title);
  pdf.moveDown(0.35);
};

const addSections = (pdf: PDFKit.PDFDocument, heading: string, entries: CvPdfSection[]): void => {
  if (entries.length === 0) return;

  addSectionHeading(pdf, heading);
  entries.forEach((entry) => {
    pdf.font("Helvetica-Bold").fontSize(11.5).fillColor(COLORS.black).text(entry.title);
    const subtitle = [entry.organization, entry.period].filter(Boolean).join(" · ");
    if (subtitle) {
      pdf.font("Helvetica-Bold").fontSize(10.5).fillColor(COLORS.black).text(subtitle);
    }
    pdf.moveDown(0.25);
    pdf.font("Helvetica").fontSize(10.5).fillColor(COLORS.black);
    entry.details.forEach((bullet) => {
      pdf.text(`-  ${bullet}`, { indent: 10, lineGap: 3 });
      pdf.moveDown(0.15);
    });
    entry.meta.forEach((line) => pdf.fontSize(9.5).fillColor(COLORS.gray).text(line, { lineGap: 2 }));
    pdf.moveDown(0.6);
  });
};

const addFooters = (pdf: PDFKit.PDFDocument, name: string): void => {
  const range = pdf.bufferedPageRange();
  for (let i = range.start; i < range.start + range.count; i += 1) {
    pdf.switchToPage(i);
    const { left, right, bottom } = pdf.page.margins;
    // Drawing this close to the bottom edge sits inside the page's normal bottom
    // margin band; pdfkit treats any text() beyond the margin-defined content
    // area as an overflow and silently starts a new page. Zero the bottom
    // margin for this one draw so it lands on the current page instead.
    pdf.page.margins.bottom = 0;
    pdf
      .font("Helvetica")
      .fontSize(9)
      .fillColor(COLORS.gray)
      .text(`${name} | Page ${i - range.start + 1}`, left, pdf.page.height - FOOTER_MARGIN_FROM_BOTTOM, {
        width: pdf.page.width - left - right,
        align: "right",
      });
    pdf.page.margins.bottom = bottom;
  }
};

export const renderCvPdf = (document: CvPdfDocumentModel): PDFKit.PDFDocument => {
  const pdf = new PDFDocument({
    size: "A4",
    bufferPages: true,
    margins: { top: 44, bottom: 54, left: 50, right: 50 },
  });

  pdf.font("Helvetica-Bold").fontSize(22).fillColor(COLORS.black).text(document.name, { align: "center" });
  pdf.moveDown(0.15);
  pdf.font("Helvetica-Bold").fontSize(13).fillColor(COLORS.navy).text(document.tagline, { align: "center" });
  pdf.moveDown(0.3);
  pdf.font("Helvetica").fontSize(10).fillColor(COLORS.black).text(document.contactLine, { align: "center" });
  pdf.moveDown(0.8);

  if (document.summary.length > 0) {
    addSectionHeading(pdf, "Summary");
    pdf.font("Helvetica").fontSize(10.5).fillColor(COLORS.black);
    document.summary.forEach((paragraph) => {
      pdf.text(paragraph, { lineGap: 3 });
      pdf.moveDown(0.4);
    });
  }

  addSections(pdf, "Experience", document.experience);
  addSections(pdf, "Education", document.education);
  addSections(pdf, "Honors & Awards", document.honors);

  if (document.languages.length > 0) {
    addSectionHeading(pdf, "Languages");
    pdf.font("Helvetica").fontSize(10.5).fillColor(COLORS.black);
    document.languages.forEach(({ name, proficiency }) => {
      pdf.text(`${name} — ${proficiency}`, { lineGap: 3 });
      pdf.moveDown(0.15);
    });
  }

  addFooters(pdf, document.name);
  pdf.end();
  return pdf;
};
