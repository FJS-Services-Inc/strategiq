"""
PDF Caching Service with Time-Based Expiration

Implements composite caching with 5-minute TTL for PDF reports.
Cache key: result_id + content_hash for efficient lookups.
"""

import time
from io import BytesIO
from typing import Any

from backend.core.core import SwotAnalysis
from backend.core.pdf_service import compute_content_hash
from backend.logger import logger
from backend.settings.consts import PDF_CACHE_TTL_SECONDS

# Cache configuration
CACHE_TTL_SECONDS = PDF_CACHE_TTL_SECONDS  # Imported from settings
CLEANUP_INTERVAL_SECONDS = 60  # Run cleanup every minute


class PDFCacheEntry:
    """
    Represents a cached PDF with metadata.
    """

    def __init__(self, pdf_buffer: BytesIO, content_hash: str):
        self.pdf_buffer = pdf_buffer
        self.content_hash = content_hash
        self.created_at = time.time()
        self.accessed_at = time.time()
        self.access_count = 0

    def is_expired(self, ttl_seconds: int = CACHE_TTL_SECONDS) -> bool:
        """Check if cache entry has expired"""
        return (time.time() - self.created_at) > ttl_seconds

    def access(self):
        """Update access metadata"""
        self.accessed_at = time.time()
        self.access_count += 1

    def get_age_seconds(self) -> float:
        """Get age of cache entry in seconds"""
        return time.time() - self.created_at


class PDFCacheManager:
    """
    In-memory cache manager for PDF reports with composite key strategy.

    Cache key format: f"{session_id}:{content_hash}"
    - session_id: Unique identifier for the analysis session
    - content_hash: SHA-256 hash of SWOT content

    This ensures:
    - Same session + same content = cache hit
    - Same session + different content = cache miss (content changed)
    - Different session + same content = separate cache entry
    """

    def __init__(self):
        self._cache: dict[str, PDFCacheEntry] = {}
        self._last_cleanup = time.time()

    def _make_cache_key(self, session_id: str, content_hash: str) -> str:
        """Generate composite cache key"""
        return f"{session_id}:{content_hash}"

    def get(self, session_id: str, analysis: SwotAnalysis) -> BytesIO | None:
        """
        Retrieve cached PDF if available and not expired.

        :param session_id: Session identifier
        :param analysis: SwotAnalysis object for content hash computation
        :return: BytesIO buffer if cache hit, None if cache miss
        """
        content_hash = compute_content_hash(analysis)
        cache_key = self._make_cache_key(session_id, content_hash)

        # Auto-cleanup on every get
        self._cleanup_expired()

        if cache_key in self._cache:
            entry = self._cache[cache_key]

            if entry.is_expired():
                logger.info(f"PDF cache expired for key: {cache_key}")
                del self._cache[cache_key]
                return None

            # Update access metadata
            entry.access()
            logger.info(
                f"PDF cache HIT for key: {cache_key} "
                f"(age: {entry.get_age_seconds():.1f}s, accesses: {entry.access_count})"
            )

            # Return a copy of the buffer to avoid mutation
            buffer_copy = BytesIO(entry.pdf_buffer.getvalue())
            return buffer_copy

        logger.info(f"PDF cache MISS for key: {cache_key}")
        return None

    def set(self, session_id: str, analysis: SwotAnalysis, pdf_buffer: BytesIO):
        """
        Store PDF in cache with composite key.

        :param session_id: Session identifier
        :param analysis: SwotAnalysis object for content hash computation
        :param pdf_buffer: BytesIO buffer containing PDF
        """
        content_hash = compute_content_hash(analysis)
        cache_key = self._make_cache_key(session_id, content_hash)

        # Store a copy to prevent external mutation
        buffer_copy = BytesIO(pdf_buffer.getvalue())
        entry = PDFCacheEntry(buffer_copy, content_hash)

        self._cache[cache_key] = entry
        logger.info(
            f"PDF cached with key: {cache_key} (TTL: {CACHE_TTL_SECONDS}s)"
        )

    def invalidate(self, session_id: str):
        """
        Invalidate all cache entries for a session.

        :param session_id: Session identifier
        """
        keys_to_delete = [
            key for key in self._cache if key.startswith(f"{session_id}:")
        ]

        for key in keys_to_delete:
            del self._cache[key]
            logger.info(f"Invalidated cache key: {key}")

    def _cleanup_expired(self):
        """Remove expired entries from cache"""
        # Avoid excessive cleanup calls
        if (time.time() - self._last_cleanup) < CLEANUP_INTERVAL_SECONDS:
            return

        expired_keys = [
            key for key, entry in self._cache.items() if entry.is_expired()
        ]

        for key in expired_keys:
            del self._cache[key]
            logger.debug(f"Cleaned up expired cache key: {key}")

        if expired_keys:
            logger.info(
                f"PDF cache cleanup: removed {len(expired_keys)} expired entries"
            )

        self._last_cleanup = time.time()

    def get_stats(self) -> dict[str, Any]:
        """
        Get cache statistics for monitoring.

        :return: Dictionary with cache stats
        """
        total_entries = len(self._cache)
        total_accesses = sum(
            entry.access_count for entry in self._cache.values()
        )
        avg_age = (
            sum(entry.get_age_seconds() for entry in self._cache.values())
            / total_entries
            if total_entries > 0
            else 0
        )

        return {
            "total_entries": total_entries,
            "total_accesses": total_accesses,
            "average_age_seconds": avg_age,
            "ttl_seconds": CACHE_TTL_SECONDS,
        }

    def clear(self):
        """Clear all cache entries (useful for testing)"""
        count = len(self._cache)
        self._cache.clear()
        logger.info(f"PDF cache cleared: removed {count} entries")


# Global cache instance
pdf_cache = PDFCacheManager()
