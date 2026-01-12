"""Constants and enums."""

from enum import StrEnum, auto


class State(StrEnum):
    WAITING_TEXT = auto()
    CONFIRMING = auto()


EXTRACTION_PROMPT = """
Extract opportunity information and return ONLY valid JSON:

{text}

Format:
{{
    "name": "opportunity name",
    "deadline": "YYYY-MM-DD",
    "tags": ["tag1", "tag2"],
    "link": "full URL or null",
    "description": "description or null"
}}

Tags should be categories like: "scholarship", "internship", "competition", "grant", "research", country names, institutions, etc.
"""