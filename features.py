"""
features.py - Feature Extraction for PhishGuard Lite.
Computes exactly 5 understandable lexical features from any URL string.
Used identically during training and web prediction.
"""

from urllib.parse import urlparse
import re

# The exact 5 feature names and their order
FEATURE_NAMES = [
    "url_length",
    "num_dots",
    "has_at_symbol",
    "num_hyphens_hostname",
    "is_https",
]


def extract_features(raw_url: str) -> dict:
    """
    Extract 5 simple, understandable features from a URL string:
    1. url_length: Total length of the URL.
    2. num_dots: Total count of dots (.) across the URL.
    3. has_at_symbol: 1 if '@' is present, else 0 (used to disguise target host).
    4. num_hyphens_hostname: Count of hyphens (-) inside the hostname.
    5. is_https: 1 if scheme is https://, else 0.
    """
    url = str(raw_url).strip()

    # If user did not type a scheme (e.g. 'google.com'), add 'http://' for safe parsing
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url):
        parsed = urlparse("http://" + url)
        # Note: If no scheme was typed originally, it wasn't https
        is_https = 1 if url.lower().startswith("https://") else 0
    else:
        parsed = urlparse(url)
        is_https = 1 if parsed.scheme.lower() == "https" else 0

    hostname = (parsed.hostname or "").lower()

    return {
        "url_length": len(url),
        "num_dots": url.count("."),
        "has_at_symbol": 1 if "@" in url else 0,
        "num_hyphens_hostname": hostname.count("-"),
        "is_https": is_https,
    }

