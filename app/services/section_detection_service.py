"""Compatibility wrapper for CV section detection service functions."""

from app.services.section_detection import (
    classify_section_status,
    detect_contact_info,
    detect_sections,
    extract_section_blocks,
    generate_section_message,
)

__all__ = [
    "classify_section_status",
    "detect_contact_info",
    "detect_sections",
    "extract_section_blocks",
    "generate_section_message",
]
