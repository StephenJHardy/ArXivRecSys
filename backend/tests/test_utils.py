from datetime import datetime, timedelta
from app.utils import helpers

def test_clean_text():
    # Test LaTeX command removal
    text = r"This is a \textbf{bold} text with \emph{emphasis}"
    cleaned = helpers.clean_text(text)
    assert cleaned == "This is a bold text with emphasis"
    
    # Test multiple whitespace removal
    text = "This    has    multiple    spaces"
    cleaned = helpers.clean_text(text)
    assert cleaned == "This has multiple spaces"
    
    # Test combined case
    text = r"Multiple  \textbf{spaces}  and  \emph{commands}"
    cleaned = helpers.clean_text(text)
    assert cleaned == "Multiple spaces and commands"

def test_parse_authors():
    # Test simple case
    authors = "John Doe, Jane Smith"
    parsed = helpers.parse_authors(authors)
    assert parsed == ["John Doe", "Jane Smith"]
    
    # Test with extra whitespace
    authors = "John Doe ,  Jane Smith  , Bob Johnson"
    parsed = helpers.parse_authors(authors)
    assert parsed == ["John Doe", "Jane Smith", "Bob Johnson"]
    
    # Test single author
    authors = "Single Author"
    parsed = helpers.parse_authors(authors)
    assert parsed == ["Single Author"]

def test_format_date():
    date = datetime(2024, 1, 15, 10, 30, 0)
    formatted = helpers.format_date(date)
    assert formatted == "2024-01-15 10:30:00"

def test_calculate_time_ago():
    now = datetime.utcnow()
    
    # Test years
    date = now - timedelta(days=400)
    assert "year" in helpers.calculate_time_ago(date)
    
    # Test months
    date = now - timedelta(days=40)
    assert "month" in helpers.calculate_time_ago(date)
    
    # Test days
    date = now - timedelta(days=5)
    assert "days" in helpers.calculate_time_ago(date)
    
    # Test hours
    date = now - timedelta(hours=5)
    assert "hours" in helpers.calculate_time_ago(date)
    
    # Test minutes
    date = now - timedelta(minutes=5)
    assert "minutes" in helpers.calculate_time_ago(date)
    
    # Test just now
    date = now - timedelta(seconds=30)
    assert helpers.calculate_time_ago(date) == "just now"

def test_truncate_text():
    # Test text shorter than max length
    text = "Short text"
    truncated = helpers.truncate_text(text, max_length=20)
    assert truncated == text
    
    # Test text longer than max length
    text = "This is a very long text that needs to be truncated"
    truncated = helpers.truncate_text(text, max_length=20)
    assert len(truncated) <= 23  # 20 + 3 for "..."
    assert truncated.endswith("...")
    assert truncated.rsplit(" ", 1)[0] in text  # Check that truncation happened at word boundary
    
    # Test exact length
    text = "Exactly twenty chars"
    truncated = helpers.truncate_text(text, max_length=20)
    assert truncated == text

def test_parse_categories():
    # Test single category
    categories = "cs.AI"
    parsed = helpers.parse_categories(categories)
    assert parsed == ["cs.AI"]
    
    # Test multiple categories
    categories = "cs.AI cs.LG math.ST"
    parsed = helpers.parse_categories(categories)
    assert parsed == ["cs.AI", "cs.LG", "math.ST"]
    
    # Test with extra whitespace
    categories = "cs.AI   cs.LG     math.ST"
    parsed = helpers.parse_categories(categories)
    assert parsed == ["cs.AI", "cs.LG", "math.ST"] 