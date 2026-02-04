"""
Integration tests for the complete analyze flow.

Tests: Form submission → Background task → Status updates → Results
"""

import pytest
from fastapi.testclient import TestClient

from backend.site.consts import ANALYZING_MESSAGE, result_store, status_store


@pytest.mark.integration
@pytest.mark.api
class TestAnalyzeFlow:
    """Test the complete analysis workflow"""

    def test_analyze_endpoint_returns_success(
        self, test_client: TestClient, mock_analysis_data: dict
    ):
        """
        Regression test: Ensure analyze endpoint doesn't crash.

        Bug: TemplateNotFound after Jinjax refactor
        Fix: Return empty HTMLResponse instead of status.html
        """
        response = test_client.post("/analyze", data=mock_analysis_data)

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        # Should return empty response since HTMX polling handles rendering
        assert response.text.strip() == ""

    def test_analyze_creates_session(
        self, test_client: TestClient, mock_analysis_data: dict
    ):
        """Verify analyze endpoint creates session and initializes stores"""
        response = test_client.post("/analyze", data=mock_analysis_data)

        assert response.status_code == 200

        # Session should be created (stored in cookies)
        assert "session" in response.cookies

        # Note: Can't easily verify status_store without accessing session ID
        # This would require inspecting the session cookie or mocking

    def test_analyze_with_empty_comparison(self, test_client: TestClient):
        """Test analyze with no comparison entities"""
        data = {"primary_entity": "Apple", "comparison_entities": ""}

        response = test_client.post("/analyze", data=data)

        assert response.status_code == 200

    def test_analyze_with_multiple_comparisons(self, test_client: TestClient):
        """Test analyze with multiple comma-separated comparisons"""
        data = {
            "primary_entity": "Netflix",
            "comparison_entities": "Disney+, HBO Max, Amazon Prime",
        }

        response = test_client.post("/analyze", data=data)

        assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.api
class TestStatusPolling:
    """Test status polling endpoint with OOB swaps"""

    def test_status_endpoint_without_session(self, test_client: TestClient):
        """Status endpoint should return empty response without session"""
        response = test_client.get("/status")

        assert response.status_code == 200
        assert response.text.strip() == ""

    def test_status_endpoint_returns_oob_container_on_first_poll(
        self, test_client: TestClient, mock_session_id: str
    ):
        """
        First poll should return StatusTimeline container + initial items via OOB.

        This tests the Jinjax component rendering.
        """
        # Manually set up session state to simulate analyze_url
        status_store[mock_session_id] = [ANALYZING_MESSAGE]

        # Create session and make request
        with test_client:
            # Set session cookie
            test_client.cookies.set("analysis_id", mock_session_id)

            response = test_client.get("/status")

            assert response.status_code == 200
            assert "status-container" in response.text
            assert "status-timeline" in response.text
            assert ANALYZING_MESSAGE in response.text
            # Should have OOB swap attribute
            assert "hx-swap-oob" in response.text

    def test_status_endpoint_returns_empty_when_no_new_messages(
        self, test_client: TestClient, mock_session_id: str
    ):
        """Subsequent polls with no new messages return empty response"""
        from backend.site.consts import last_message_index

        # Set up state: already polled once
        status_store[mock_session_id] = [ANALYZING_MESSAGE]
        last_message_index[mock_session_id] = 1

        with test_client:
            test_client.cookies.set("analysis_id", mock_session_id)

            response = test_client.get("/status")

            assert response.status_code == 200
            assert response.text.strip() == ""

    def test_status_endpoint_returns_only_new_messages(
        self, test_client: TestClient, mock_session_id: str
    ):
        """Subsequent polls return only new messages via OOB"""
        from backend.site.consts import last_message_index

        # Set up state: first poll done, new messages added
        status_store[mock_session_id] = [
            ANALYZING_MESSAGE,
            "Using tool: Reddit Intelligence",
            "Generating SWOT analysis",
        ]
        last_message_index[mock_session_id] = 1

        with test_client:
            test_client.cookies.set("analysis_id", mock_session_id)

            response = test_client.get("/status")

            assert response.status_code == 200
            # Should NOT contain first message
            assert ANALYZING_MESSAGE not in response.text
            # Should contain new messages
            assert "Reddit Intelligence" in response.text
            assert "Generating SWOT" in response.text
            # Should have OOB swap for appending
            assert "hx-swap-oob" in response.text
            assert "status-timeline" in response.text


@pytest.mark.integration
@pytest.mark.api
class TestResultEndpoint:
    """Test result endpoint"""

    def test_result_endpoint_without_session(self, test_client: TestClient):
        """Result endpoint returns empty when no session"""
        response = test_client.get("/result")

        assert response.status_code == 200
        # Should render result.html with no result
        assert "result" not in response.text.lower() or response.text.strip() == ""

    def test_result_endpoint_with_result(
        self, test_client: TestClient, mock_session_id: str, sample_swot_analysis
    ):
        """Result endpoint returns SWOT analysis when available"""
        # Set up result in store
        result_store[mock_session_id] = sample_swot_analysis

        with test_client:
            test_client.cookies.set("analysis_id", mock_session_id)

            response = test_client.get("/result")

            assert response.status_code == 200
            # Should contain SWOT data
            assert "Google" in response.text
            assert "Strengths" in response.text
            assert "Weaknesses" in response.text
            assert "Opportunities" in response.text
            assert "Threats" in response.text
            assert "Executive Summary" in response.text
