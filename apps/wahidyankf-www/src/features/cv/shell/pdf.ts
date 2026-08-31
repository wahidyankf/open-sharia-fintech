import PDFDocument from "pdfkit";
import type { CvPdfDocumentModel, CvPdfSection } from "../core/pdf";

const COLORS = {
  heading: "#111827",
  subheading: "#374151",
  meta: "#4b5563",
  body: "#1f2937",
  rule: "#d1d5db",
};

const addSectionHeading = (pdf: PDFKit.PDFDocument, title: string): void => {
  pdf.moveDown(0.6);
  pdf.font("Helvetica-Bold").fontSize(13).fillColor(COLORS.heading).text(title.toUpperCase());
  pdf
    .moveTo(pdf.x, pdf.y)
    .lineTo(pdf.page.width - pdf.page.margins.right, pdf.y)
    .strokeColor(COLORS.rule)
    .stroke();
  pdf.moveDown(0.3);
};

const addSections = (pdf: PDFKit.PDFDocument, heading: string, entries: CvPdfSection[]): void => {
  if (entries.length === 0) return;

  addSectionHeading(pdf, heading);
  entries.forEach((entry) => {
    pdf.font("Helvetica-Bold").fontSize(11).fillColor(COLORS.heading).text(entry.title);
    const subtitle = [entry.organization, entry.period].filter(Boolean).join(" · ");
    if (subtitle) {
      pdf.font("Helvetica-Oblique").fontSize(9.5).fillColor(COLORS.meta).text(subtitle);
    }
    pdf.moveDown(0.2);
    pdf.font("Helvetica").fontSize(9.5).fillColor(COLORS.body);
    entry.details.forEach((bullet) => pdf.text(`•  ${bullet}`, { indent: 10 }));
    entry.meta.forEach((line) => pdf.fontSize(8.5).fillColor(COLORS.meta).text(line));
    pdf.moveDown(0.5);
  });
};

export const renderCvPdf = (document: CvPdfDocumentModel): PDFKit.PDFDocument => {
  const pdf = new PDFDocument({ size: "A4", margins: { top: 48, bottom: 48, left: 56, right: 56 } });

  pdf.font("Helvetica-Bold").fontSize(20).fillColor(COLORS.heading).text(document.name);
  pdf.font("Helvetica").fontSize(12).fillColor(COLORS.subheading).text(document.tagline);
  pdf.moveDown(0.3);
  pdf.font("Helvetica").fontSize(9).fillColor(COLORS.meta).text(document.contactLine);
  pdf.moveDown();

  if (document.summary.length > 0) {
    addSectionHeading(pdf, "Summary");
    pdf.font("Helvetica").fontSize(10).fillColor(COLORS.body);
    document.summary.forEach((paragraph) => {
      pdf.text(paragraph);
      pdf.moveDown(0.4);
    });
  }

  addSections(pdf, "Experience", document.experience);
  addSections(pdf, "Education", document.education);
  addSections(pdf, "Certifications", document.certifications);

  if (document.languages.length > 0) {
    addSectionHeading(pdf, "Languages");
    pdf.font("Helvetica").fontSize(9.5).fillColor(COLORS.body);
    document.languages.forEach(({ name, proficiency }) => pdf.text(`${name} — ${proficiency}`));
  }

  pdf.end();
  return pdf;
};
