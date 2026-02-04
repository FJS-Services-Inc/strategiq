"""
Unit tests for PDF generation service.

Tests individual components of the PDF service in isolation.
"""

from io import BytesIO

import pytest

from backend.core.core import SwotAnalysis
from backend.core.pdf_service import (
    SwotPDFGenerator,
    compute_content_hash,
    generate_swot_pdf,
)


@pytest.mark.unit
@pytest.mark.pdf
class TestContentHashing:
    """Test content hash generation for caching"""

    def test_compute_content_hash_is_consistent(
        self, sample_swot_analysis: SwotAnalysis
    ):
        """Same analysis should produce same hash"""
        hash1 = compute_content_hash(sample_swot_analysis)
        hash2 = compute_content_hash(sample_swot_analysis)

        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 produces 64 hex characters

    def test_compute_content_hash_changes_with_content(
        self, sample_swot_analysis: SwotAnalysis
    ):
        """Different content should produce different hash"""
        hash1 = compute_content_hash(sample_swot_analysis)

        # Modify analysis
        modified_analysis = SwotAnalysis(
            primary_entity="Microsoft",  # Changed
            comparison_entities=sample_swot_analysis.comparison_entities,
            strengths=sample_swot_analysis.strengths,
            weaknesses=sample_swot_analysis.weaknesses,
            opportunities=sample_swot_analysis.opportunities,
            threats=sample_swot_analysis.threats,
            analysis=sample_swot_analysis.analysis,
        )

        hash2 = compute_content_hash(modified_analysis)

        assert hash1 != hash2


@pytest.mark.unit
@pytest.mark.pdf
class TestPDFGeneratorInit:
    """Test PDF generator initialization"""

    def test_generator_initializes_styles(
        self, sample_swot_analysis: SwotAnalysis
    ):
        """Generator should create custom styles on init"""
        generator = SwotPDFGenerator(sample_swot_analysis)

        # Custom styles should exist
        assert "ReportTitle" in generator.styles
        assert "ReportSubtitle" in generator.styles
        assert "SectionHeader" in generator.styles
        assert "CategoryHeader" in generator.styles
        assert "ReportBodyText" in generator.styles
        assert "BulletItem" in generator.styles

    def test_generator_does_not_conflict_with_builtin_styles(
        self, sample_swot_analysis: SwotAnalysis
    ):
        """
        Regression: Ensure no conflicts with ReportLab built-in styles.

        Bug: "Style 'BodyText' already defined"
        Fix: Custom styles use "Report" prefix
        """
        generator = SwotPDFGenerator(sample_swot_analysis)

        # Built-in BodyText should still exist
        assert "BodyText" in generator.styles
        # Our custom style should exist separately
        assert "ReportBodyText" in generator.styles


@pytest.mark.unit
@pytest.mark.pdf
class TestPDFGeneration:
    """Test PDF generation logic"""

    def test_generate_returns_bytesio(self, sample_swot_analysis: SwotAnalysis):
        """
        generate_swot_pdf should return BytesIO buffer.

        Regression: Ensure BytesIO, not int or other type.
        """
        result = generate_swot_pdf(sample_swot_analysis)

        assert isinstance(result, BytesIO)

    def test_generate_creates_valid_pdf_header(
        self, sample_swot_analysis: SwotAnalysis
    ):
        """Generated PDF should have valid PDF header"""
        pdf_buffer = generate_swot_pdf(sample_swot_analysis)

        pdf_buffer.seek(0)
        header = pdf_buffer.read(4)

        assert header == b"%PDF"

    def test_generate_pdf_has_content(self, sample_swot_analysis: SwotAnalysis):
        """Generated PDF should have substantial content"""
        pdf_buffer = generate_swot_pdf(sample_swot_analysis)

        # Seek to end to get size
        pdf_buffer.seek(0, 2)
        size = pdf_buffer.tell()

        # PDF should be at least 10KB (very conservative)
        assert size > 10_000


@pytest.mark.unit
class TestSwotAnalysisModel:
    """Test SwotAnalysis data model"""

    def test_swot_analysis_dict_conversion(
        self, sample_swot_analysis: SwotAnalysis
    ):
        """SwotAnalysis should convert to dict properly"""
        result_dict = sample_swot_analysis.dict()

        assert "primary_entity" in result_dict
        assert "strengths" in result_dict
        assert "weaknesses" in result_dict
        assert "opportunities" in result_dict
        assert "threats" in result_dict
        assert "analysis" in result_dict

    def test_swot_analysis_requires_all_fields(self):
        """SwotAnalysis should require all critical fields"""
        with pytest.raises((TypeError, ValueError)):
            # Missing required fields should raise error
            SwotAnalysis(primary_entity="Test")
