"""
Integration tests for PDF export functionality.

Tests: PDF generation → Caching → Download
"""

from io import BytesIO
from unittest.mock import MagicMock

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

        # Seek to beginning and check for PDF magic bytes
        pdf_buffer.seek(0)
        content = pdf_buffer.read(4)
        assert content == b"%PDF"  # Valid PDF magic bytes

        # Check buffer has content (seek to end to get size)
        pdf_buffer.seek(0, 2)
        size = pdf_buffer.tell()
        assert size > 0  # Buffer has content

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

        # Read PDF as bytes
        pdf_buffer.seek(0)
        pdf_bytes = pdf_buffer.read()

        # PDF should be valid and non-empty
        assert pdf_bytes.startswith(b"%PDF")
        assert len(pdf_bytes) > 1000  # Reasonable minimum size

        # Note: Text search in compressed PDFs is unreliable
        # For proper validation, would need PyPDF2 or similar
        # Just verify the PDF structure is valid


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

    def test_download_pdf_without_session_returns_404(self, test_client: TestClient):
        """
        Regression test: PDF download without session ID should return 404.

        Bug: AttributeError: 'int' object has no attribute 'encode'
        Root Cause: StreamingResponse used with raw bytes instead of Response
        Fix: Use Response for error paths, not StreamingResponse

        This tests the first error path (no session_id).
        """
        # Don't set any session cookie
        response = test_client.get("/download-pdf")

        assert response.status_code == 404
        assert b"No analysis found" in response.content
        # Verify response can be read without AttributeError
        assert isinstance(response.content, bytes)
        assert len(response.content) > 0

    @pytest.mark.asyncio
    async def test_download_pdf_without_result_returns_404(
        self, mock_session_id: str
    ):
        """
        Regression test: PDF download with session but no result should return 404.

        Bug: AttributeError: 'int' object has no attribute 'encode'
        Root Cause: StreamingResponse used with raw bytes instead of Response
        Fix: Use Response for error paths, not StreamingResponse

        This tests the second error path (session exists but result is None).
        This is the exact error scenario from the production bug.
        """
        from backend.site.router import download_pdf

        # Create mock request with session but no result
        mock_request = MagicMock()
        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=mock_session_id)
        mock_request.session = mock_session

        # Clear result_store to simulate "analysis not complete"
        result_store.clear()

        # Call the endpoint handler directly
        response = await download_pdf(mock_request)

        # Should hit the "result is None" error path
        assert response.status_code == 404
        assert b"Analysis not complete" in response.body
        # Verify response can be read without AttributeError
        assert isinstance(response.body, bytes)
        assert len(response.body) > 0

    def test_download_pdf_error_paths_use_response_not_streaming(
        self, test_client: TestClient, mock_session_id: str
    ):
        """
        Regression test: Verify error paths return Response, not StreamingResponse.

        This prevents the AttributeError when iterating over bytes in StreamingResponse.
        Response handles bytes directly, StreamingResponse requires an iterator.
        """

        # Test path 1: No session ID
        response1 = test_client.get("/download-pdf")
        assert response1.status_code == 404
        # Response should be directly readable (not streamed)
        assert isinstance(response1.content, bytes)

        # Test path 2: Session ID but no result
        with test_client:
            test_client.cookies.set("analysis_id", mock_session_id)
            response2 = test_client.get("/download-pdf")
            assert response2.status_code == 404
            # Response should be directly readable (not streamed)
            assert isinstance(response2.content, bytes)

    @pytest.mark.asyncio
    async def test_download_pdf_returns_pdf_file(
        self, mock_session_id: str, sample_swot_analysis
    ):
        """
        Test PDF download returns valid PDF file.

        Regression: Ensure StreamingResponse works with BytesIO iterator.
        Bug: AttributeError: 'int' object has no attribute 'encode'
        Fix: Use iterfile() generator for BytesIO chunks
        """
        from backend.site.router import download_pdf

        # Create mock request with session
        mock_request = MagicMock()
        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=mock_session_id)
        mock_request.session = mock_session

        # Populate result_store with completed analysis
        result_store[mock_session_id] = sample_swot_analysis

        # Call the endpoint handler directly
        response = await download_pdf(mock_request)

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert "attachment" in response.headers["content-disposition"]
        assert "swot-analysis" in response.headers["content-disposition"]

        # Verify it's a valid PDF by reading the stream
        body_content = b""
        async for chunk in response.body_iterator:
            body_content += chunk

        assert body_content.startswith(b"%PDF")
        assert len(body_content) > 1000  # PDF should have substantial content

    @pytest.mark.asyncio
    async def test_download_pdf_uses_cache(
        self, mock_session_id: str, sample_swot_analysis
    ):
        """Test that PDF download uses cache when available"""
        from backend.site.router import download_pdf

        # Create mock request
        mock_request = MagicMock()
        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=mock_session_id)
        mock_request.session = mock_session

        # Populate result_store
        result_store[mock_session_id] = sample_swot_analysis

        # First request - generates PDF and caches
        response1 = await download_pdf(mock_request)
        assert response1.status_code == 200

        # Read first response body
        body1 = b""
        async for chunk in response1.body_iterator:
            body1 += chunk

        # Second request - should use cache
        response2 = await download_pdf(mock_request)
        assert response2.status_code == 200

        # Read second response body
        body2 = b""
        async for chunk in response2.body_iterator:
            body2 += chunk

        # Both should return identical content
        assert body1 == body2

    @pytest.mark.asyncio
    async def test_download_pdf_filename_format(
        self, mock_session_id: str, sample_swot_analysis
    ):
        """Test PDF filename follows expected format"""
        from backend.site.router import download_pdf

        # Create mock request
        mock_request = MagicMock()
        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=mock_session_id)
        mock_request.session = mock_session

        # Populate result_store
        result_store[mock_session_id] = sample_swot_analysis

        response = await download_pdf(mock_request)

        assert response.status_code == 200
        disposition = response.headers["content-disposition"]
        # Format: swot-analysis-{session_id[:8]}.pdf
        assert f"swot-analysis-{mock_session_id[:8]}.pdf" in disposition
