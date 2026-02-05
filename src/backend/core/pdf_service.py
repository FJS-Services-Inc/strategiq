"""
PDF Generation Service for SWOT Analysis Reports

Generates professional, branded PDF reports using ReportLab.
Follows StrategIQ brand guidelines with WCAG accessibility considerations.
"""

import hashlib
from io import BytesIO
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.doctemplate import BaseDocTemplate

from backend.core.core import SwotAnalysis
from backend.logger import logger

# Brand Colors (from _variables.scss)
BRAND_PRIMARY = colors.HexColor("#8B5CF6")
BRAND_PRIMARY_DARK = colors.HexColor("#7C3AED")
SWOT_STRENGTH = colors.HexColor("#10B981")
SWOT_WEAKNESS = colors.HexColor("#F59E0B")
SWOT_OPPORTUNITY = colors.HexColor("#3B82F6")
SWOT_THREAT = colors.HexColor("#EF4444")
NEUTRAL_700 = colors.HexColor("#374151")
NEUTRAL_100 = colors.HexColor("#F3F4F6")
WHITE = colors.white


def compute_content_hash(analysis: SwotAnalysis) -> str:
    """
    Compute SHA-256 hash of SWOT analysis content for caching.

    :param analysis: SwotAnalysis object
    :return: Hexadecimal hash string
    """
    content = f"{analysis.primary_entity}{analysis.comparison_entities}{analysis.strengths}{analysis.weaknesses}{analysis.opportunities}{analysis.threats}{analysis.analysis}"
    return hashlib.sha256(content.encode()).hexdigest()


class SwotPDFGenerator:
    """
    Professional PDF generator for SWOT analysis reports.
    Uses StrategIQ brand colors and follows accessibility best practices.
    """

    def __init__(self, analysis: SwotAnalysis):
        self.analysis = analysis
        self.buffer = BytesIO()
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Configure custom paragraph styles matching brand guidelines"""
        # Title style
        self.styles.add(
            ParagraphStyle(
                name="ReportTitle",
                parent=self.styles["Heading1"],
                fontSize=28,
                textColor=BRAND_PRIMARY,
                spaceAfter=6,
                fontName="Helvetica-Bold",
                alignment=1,  # Center
            )
        )

        # Subtitle style
        self.styles.add(
            ParagraphStyle(
                name="ReportSubtitle",
                parent=self.styles["Normal"],
                fontSize=14,
                textColor=NEUTRAL_700,
                spaceAfter=20,
                fontName="Helvetica",
                alignment=1,  # Center
            )
        )

        # Section header style
        self.styles.add(
            ParagraphStyle(
                name="SectionHeader",
                parent=self.styles["Heading2"],
                fontSize=18,
                textColor=BRAND_PRIMARY_DARK,
                spaceBefore=16,
                spaceAfter=8,
                fontName="Helvetica-Bold",
            )
        )

        # Category header style
        self.styles.add(
            ParagraphStyle(
                name="CategoryHeader",
                parent=self.styles["Heading3"],
                fontSize=14,
                textColor=WHITE,
                spaceBefore=12,
                spaceAfter=8,
                fontName="Helvetica-Bold",
            )
        )

        # Body text style
        self.styles.add(
            ParagraphStyle(
                name="ReportBodyText",
                parent=self.styles["Normal"],
                fontSize=11,
                textColor=NEUTRAL_700,
                spaceAfter=8,
                fontName="Helvetica",
                leading=16,
            )
        )

        # Bullet list style
        self.styles.add(
            ParagraphStyle(
                name="BulletItem",
                parent=self.styles["Normal"],
                fontSize=10,
                textColor=NEUTRAL_700,
                leftIndent=20,
                spaceAfter=6,
                fontName="Helvetica",
                leading=14,
            )
        )

    def _add_header(self, story: list[Any]):
        """Add report header with title and entity information"""
        # Title
        title = Paragraph("SWOT Analysis Report", self.styles["ReportTitle"])
        story.append(title)
        story.append(Spacer(1, 0.1 * inch))

        # Entity information
        entity_text = f"<b>Primary Entity:</b> {self.analysis.primary_entity}"
        if self.analysis.comparison_entities:
            comparisons = ", ".join(self.analysis.comparison_entities)
            entity_text += f"<br/><b>Compared with:</b> {comparisons}"

        entity_para = Paragraph(entity_text, self.styles["ReportSubtitle"])
        story.append(entity_para)
        story.append(Spacer(1, 0.3 * inch))

    def _add_swot_section(
        self,
        story: list[Any],
        category: str,
        items: list[str],
        color: colors.HexColor,
    ):
        """
        Add a SWOT category section with colored header and bullet points.

        :param story: ReportLab story list
        :param category: Category name (e.g., "Strengths")
        :param items: List of SWOT items
        :param color: Brand color for the category
        """
        # Category header with colored background
        header_table = Table(
            [
                [
                    Paragraph(
                        f"<b>{category}</b> ({len(items)})",
                        self.styles["CategoryHeader"],
                    )
                ]
            ],
            colWidths=[6.5 * inch],
        )
        header_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), color),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ("ROUNDEDCORNERS", [8, 8, 0, 0]),
                ]
            )
        )
        story.append(header_table)

        # Items list with light background
        items_data = [
            [Paragraph(f"• {item}", self.styles["BulletItem"])]
            for item in items
        ]
        items_table = Table(items_data, colWidths=[6.5 * inch])
        items_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), NEUTRAL_100),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("ROUNDEDCORNERS", [0, 0, 8, 8]),
                ]
            )
        )
        story.append(items_table)
        story.append(Spacer(1, 0.25 * inch))

    def _add_executive_summary(self, story: list[Any]):
        """Add executive summary section"""
        if not self.analysis.analysis:
            return

        story.append(
            Paragraph("Executive Summary", self.styles["SectionHeader"])
        )
        story.append(Spacer(1, 0.1 * inch))

        # Wrap summary in a table for better styling
        summary_para = Paragraph(
            self.analysis.analysis, self.styles["ReportBodyText"]
        )
        summary_table = Table([[summary_para]], colWidths=[6.5 * inch])
        summary_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                    ("BOX", (0, 0), (-1, -1), 2, BRAND_PRIMARY),
                    ("LEFTPADDING", (0, 0), (-1, -1), 16),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 16),
                    ("TOPPADDING", (0, 0), (-1, -1), 16),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
                    ("ROUNDEDCORNERS", [8, 8, 8, 8]),
                ]
            )
        )
        story.append(summary_table)

    def _add_footer(self, canvas, doc):
        """Add footer with page numbers and branding"""
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(NEUTRAL_700)

        # Page number
        page_text = f"Page {doc.page}"
        canvas.drawRightString(7.5 * inch, 0.5 * inch, page_text)

        # Branding
        canvas.drawString(inch, 0.5 * inch, "Generated by StrategIQ")

        canvas.restoreState()

    def generate(self) -> BytesIO:
        """
        Generate PDF report and return as BytesIO buffer.

        :return: BytesIO buffer containing PDF
        """
        logger.info(f"Generating PDF report for {self.analysis.primary_entity}")

        # Create document with custom template
        doc = BaseDocTemplate(self.buffer, pagesize=letter)
        frame = Frame(
            doc.leftMargin,
            doc.bottomMargin,
            doc.width,
            doc.height,
            id="normal",
        )
        template = PageTemplate(
            id="main", frames=frame, onPage=self._add_footer
        )
        doc.addPageTemplates([template])

        # Build story (content)
        story = []

        # Header
        self._add_header(story)

        # Executive Summary (placed first for prominence)
        story.append(Spacer(1, 0.2 * inch))
        self._add_executive_summary(story)

        # SWOT Categories
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph("SWOT Analysis", self.styles["SectionHeader"]))
        story.append(Spacer(1, 0.15 * inch))

        self._add_swot_section(
            story, "Strengths", self.analysis.strengths, SWOT_STRENGTH
        )
        self._add_swot_section(
            story, "Weaknesses", self.analysis.weaknesses, SWOT_WEAKNESS
        )
        self._add_swot_section(
            story,
            "Opportunities",
            self.analysis.opportunities,
            SWOT_OPPORTUNITY,
        )
        self._add_swot_section(
            story, "Threats", self.analysis.threats, SWOT_THREAT
        )

        # Build PDF
        doc.build(story)

        # Reset buffer position
        self.buffer.seek(0)
        logger.info("PDF report generated successfully")

        return self.buffer


def generate_swot_pdf(analysis: SwotAnalysis) -> BytesIO:
    """
    Convenience function to generate SWOT PDF report.

    :param analysis: SwotAnalysis object
    :return: BytesIO buffer containing PDF
    """
    generator = SwotPDFGenerator(analysis)
    return generator.generate()
