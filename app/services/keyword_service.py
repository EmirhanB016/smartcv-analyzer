"""Compatibility wrapper for keyword extraction and matching service functions."""

from app.services.keywords import (
    canonicalize_keyword,
    extract_keywords,
    match_keywords,
)

__all__ = [
    "canonicalize_keyword",
    "extract_keywords",
    "match_keywords",
]
