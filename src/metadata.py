"""
Simple metadata extraction without LLM
Extracts title, summary, and keywords from content
"""
from hashlib import sha256
import re
from collections import Counter
from src.models import Metadata


def extract_metadata(content: str, user_tags: str = "") -> Metadata:
    """
    Extract simple metadata from content

    Args:
        content: Text content to analyze
        user_tags: Optional user-provided tags

    Returns:
        Metadata object with title, summary, tags, and hash
    """
    title = _extract_title(content)
    summary = _extract_summary(content)
    auto_tags = _extract_keywords(content)

    # Combine user tags with auto-extracted tags
    all_tags = f"{user_tags},{auto_tags}" if user_tags else auto_tags
    all_tags = all_tags.strip(",")

    # Compute content hash
    content_hash = "0x" + sha256(content.encode()).hexdigest()

    return Metadata(
        title=title,
        summary=summary,
        tags=all_tags,
        content_hash=content_hash
    )


def _extract_title(content: str, max_length: int = 100) -> str:
    """
    Extract title from content
    Looks for markdown headings first, then falls back to first line

    Args:
        content: Text content
        max_length: Maximum title length

    Returns:
        Extracted title
    """
    lines = content.strip().split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check for markdown heading (# Title)
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            return title[:max_length]

    # Fallback to first non-empty line
    for line in lines:
        line = line.strip()
        if line:
            return line[:max_length]

    return "Untitled"


def _extract_summary(content: str, max_length: int = 200) -> str:
    """
    Extract summary (first meaningful paragraph)

    Args:
        content: Text content
        max_length: Maximum summary length

    Returns:
        Content summary
    """
    # Remove markdown syntax
    text = re.sub(r'#{1,6}\s', '', content)  # Remove headings
    text = re.sub(r'[*_`\[\]]', '', text)     # Remove formatting

    # Get first paragraph
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    if not paragraphs:
        # Fallback: first N chars
        text = content.replace("\n", " ").strip()
        return text[:max_length]

    # Use first substantial paragraph
    for para in paragraphs:
        if len(para) > 20:  # Skip very short paragraphs
            summary = para.replace("\n", " ").strip()
            return summary[:max_length]

    # Fallback to first paragraph
    summary = paragraphs[0].replace("\n", " ").strip()
    return summary[:max_length]


def _extract_keywords(content: str, max_words: int = 5) -> str:
    """
    Simple keyword extraction via word frequency

    Args:
        content: Text content
        max_words: Maximum number of keywords to extract

    Returns:
        Comma-separated keywords
    """
    # Remove markdown syntax and convert to lowercase
    text = re.sub(r'[#*`\[\](){}]', '', content.lower())

    # Extract words (4+ characters)
    words = re.findall(r'\b\w{4,}\b', text)

    if not words:
        return ""

    # Common stopwords to skip
    stopwords = {
        'that', 'this', 'with', 'from', 'have', 'been', 'they',
        'would', 'their', 'there', 'about', 'which', 'when',
        'will', 'what', 'were', 'your', 'more', 'than', 'them',
        'some', 'into', 'other', 'then', 'also', 'only', 'over',
        'such', 'just', 'these', 'those', 'being', 'both', 'could'
    }

    # Filter stopwords
    words = [w for w in words if w not in stopwords]

    if not words:
        return ""

    # Get most frequent words
    freq = Counter(words).most_common(max_words)

    # Return as comma-separated string
    keywords = [word for word, count in freq]
    return ",".join(keywords)


# Quick test
if __name__ == "__main__":
    test_content = """# ZKML Verification

Jolt Atlas is a framework that enables zero-knowledge proofs for machine learning inference.
This allows you to verify that ML models produce correct outputs without revealing the model itself.

Key features:
- Verifiable inference
- Privacy-preserving
- Efficient proof generation
"""

    meta = extract_metadata(test_content, "zkml,research")
    print(f"Title: {meta.title}")
    print(f"Summary: {meta.summary}")
    print(f"Tags: {meta.tags}")
    print(f"Hash: {meta.content_hash}")
