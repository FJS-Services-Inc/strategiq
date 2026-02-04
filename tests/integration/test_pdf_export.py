"""
Integration tests for PDF export functionality.

Tests: PDF generation → Caching → Download
"""

from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from backend.core.core import SwotAnalysis
from backend.core.pdf_cache import pdf_cache
from backend.core.pdf_service import SwotPDFGenerator, generate_swot_pdf
from backend.site.consts import result_store


@pytest.mark.integration
@pytest.mark.pdf
class TestPDFGeneration:
    """Test PDF generation with ReportLab"""

    def test_pdf_generator_creates_valid_pdf(self, sample_swot_analysis: SwotAnalysis):
        """
        Test that PDF generator produces a valid PDF BytesIO buffer.

        Regression: Ensure BytesIO returned, not int.
        """
        pdf_buffer = generate_swot_pdf(sample_swot_analysis)

        assert isinstance(pdf_buffer, BytesIO)
        assert pdf_buffer.tell() > 0  # Buffer has content
        pdf_buffer.seek(0)
        content = pdf_buffer.read(4)
        assert content == b"%PDF"  # Valid PDF magic bytes

    def test_pdf_generator_no_reserved_style_names(
        self, sample_swot_analysis: SwotAnalysis
    ):
        """
        Regression test: Ensure no ReportLab reserved style name conflicts.

        Bug: KeyError: "Style 'BodyText' already defined"
        Fix: Renamed to "ReportBodyText"
        """
        # Should not raise KeyError
        generator = SwotPDFGenerator(sample_swot_analysis)
        assert "ReportBodyText" in generator.styles
        # Original BodyText should exist as built-in
        assert "BodyText" in generator.styles

    def test_pdf_contains_swot_data(self, sample_swot_analysis: SwotAnalysis):
        """Verify PDF contains SWOT analysis data"""
        pdf_buffer = generate_swot_pdf(sample_swot_analysis)

        # Read PDF as text (simplified - real PDF parsing would use PyPDF2)
        pdf_buffer.seek(0)
        pdf_bytes = pdf_buffer.read()

        # Check for entity name and category keywords
        # Note: PDF encoding may make this fragile; consider using PyPDF2
        assert b"Google" in pdf_bytes or sample_swot_analysis.primary_entity.encode() in pdf_bytes


@pytest.mark.integration
@pytest.mark.pdf
class TestPDFCaching:
    """Test PDF caching system"""

    def test_cache_stores_and_retrieves_pdf(
        self, sample_swot_analysis: SwotAnalysis, mock_session_id: str
    ):
        """Test basic cache storage and retrieval"""
        pdf_buffer = generate_swot_pdf(sample_swot_analysis)

        # Store in cache
        pdf_cache.set(mock_session_id, sample_swot_analysis, pdf_buffer)

        # Retrieve from cache
        cached_pdf = pdf_cache.get(mock_session_id, sample_swot_analysis)

        assert cached_pdf is not None
        assert isinstance(cached_pdf, BytesIO)
        # Should be a copy, not same object
        assert cached_pdf is not pdf_buffer

    def test_cache_miss_returns_none(
        self, sample_swot_analysis: SwotAnalysis
    ):
        """Cache miss should return None"""
        cached_pdf = pdf_cache.get("nonexistent_session", sample_swot_analysis)

        assert cached_pdf is None

    def test_cache_invalidation(
        self, sample_swot_analysis: SwotAnalysis, mock_session_id: str
    ):
        """Test cache invalidation for a session"""
        pdf_buffer = generate_swot_pdf(sample_swot_analysis)
        pdf_cache.set(mock_session_id, sample_swot_analysis, pdf_buffer)

        # Invalidate
        pdf_cache.invalidate(mock_session_id)

        # Should return None after invalidation
        cached_pdf = pdf_cache.get(mock_session_id, sample_swot_analysis)
        assert cached_pdf is None


@pytest.mark.integration
@pytest.mark.pdf
@pytest.mark.api
class TestPDFDownloadEndpoint:
    """Test PDF download endpoint"""

    def test_download_pdf_without_result_returns_404(
        self, test_client: TestClient, mock_session_id: str
    ):
        """
        PDF download should return 404 if no result available.

        Tests error handling for missing result.
        """
        with test_client:
            test_client.cookies.set("analysis_id", mock_session_id)

            response = test_client.get("/download-pdf")

            assert response.status_code == 404
            assert b"Analysis not complete" in response.content

    def test_download_pdf_returns_pdf_file(
        self, test_client: TestClient, mock_session_id: str, sample_swot_analysis
    ):
        """
        Test PDF download returns valid PDF file.

        Regression: Ensure StreamingResponse works with BytesIO iterator.
        Bug: AttributeError: 'int' object has no attribute 'encode'
        Fix: Use iterfile() generator for BytesIO chunks
        """
        # Set up result
        result_store[mock_session_id] = sample_swot_analysis

        with test_client:
            test_client.cookies.set("analysis_id", mock_session_id)

            response = test_client.get("/download-pdf")

            assert response.status_code == 200
            assert response.headers["content-type"] == "application/pdf"
            assert "attachment" in response.headers["content-disposition"]
            assert "swot-analysis" in response.headers["content-disposition"]

            # Verify it's a valid PDF
            content = response.content
            assert content.startswith(b"%PDF")
            assert len(content) > 1000  # PDF should have substantial content

    def test_download_pdf_uses_cache(
        self, test_client: TestClient, mock_session_id: str, sample_swot_analysis
    ):
        """Test that PDF download uses cache when available"""
        # Set up result
        result_store[mock_session_id] = sample_swot_analysis

        with test_client:
            test_client.cookies.set("analysis_id", mock_session_id)

            # First request - generates PDF and caches
            response1 = test_client.get("/download-pdf")
            assert response1.status_code == 200

            # Second request - should use cache
            response2 = test_client.get("/download-pdf")
            assert response2.status_code == 200

            # Both should return identical content
            assert response1.content == response2.content

    def test_download_pdf_filename_format(
        self, test_client: TestClient, mock_session_id: str, sample_swot_analysis
    ):
        """Test PDF filename follows expected format"""
        result_store[mock_session_id] = sample_swot_analysis

        with test_client:
            test_client.cookies.set("analysis_id", mock_session_id)

            response = test_client.get("/download-pdf")

            assert response.status_code == 200
            disposition = response.headers["content-disposition"]
            # Format: swot-analysis-{session_id[:8]}.pdf
            assert f"swot-analysis-{mock_session_id[:8]}.pdf" in disposition
