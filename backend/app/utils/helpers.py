from datetime import datetime
from typing import List, Dict
import re

def clean_text(text: str) -> str:
    """
    Cleans text by removing extra whitespace and special characters
    """
    # Remove LaTeX commands
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_authors(authors_str: str) -> List[str]:
    """
    Parses a comma-separated author string into a list of names
    """
    return [author.strip() for author in authors_str.split(',')]

def format_date(date: datetime) -> str:
    """
    Formats a datetime object into a consistent string format
    """
    return date.strftime("%Y-%m-%d %H:%M:%S")

def calculate_time_ago(date: datetime) -> str:
    """
    Calculates a human-readable time difference from now
    """
    now = datetime.utcnow()
    diff = now - date
    
    if diff.days > 365:
        years = diff.days // 365
        return f"{years} year{'s' if years != 1 else ''} ago"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months} month{'s' if months != 1 else ''} ago"
    elif diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "just now"

def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncates text to a maximum length while preserving whole words
    """
    if len(text) <= max_length:
        return text
        
    truncated = text[:max_length].rsplit(' ', 1)[0]
    return truncated + "..."

def parse_categories(categories_str: str) -> List[str]:
    """
    Parses a space-separated category string into a list
    """
    return categories_str.split() 