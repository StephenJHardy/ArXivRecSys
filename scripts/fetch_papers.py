#!/usr/bin/env python3

import arxiv
import argparse
from datetime import datetime, timedelta
import sys
import os
import json
from typing import List, Dict, Any

# Add the server directory to the Python path so we can import the database modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))

from database import SessionLocal
from models import Paper

def get_categories() -> List[str]:
    """Get all CS and Stats categories from arXiv."""
    cs_categories = [
        'cs.AI', 'cs.AR', 'cs.CC', 'cs.CE', 'cs.CG', 'cs.CL', 'cs.CR', 'cs.CV',
        'cs.CY', 'cs.DB', 'cs.DC', 'cs.DL', 'cs.DM', 'cs.DS', 'cs.ET', 'cs.FL',
        'cs.GL', 'cs.GR', 'cs.GT', 'cs.HC', 'cs.IR', 'cs.IT', 'cs.LG', 'cs.LO',
        'cs.MA', 'cs.MM', 'cs.MS', 'cs.NA', 'cs.NE', 'cs.NI', 'cs.OH', 'cs.OS',
        'cs.PF', 'cs.PL', 'cs.RO', 'cs.SC', 'cs.SD', 'cs.SE', 'cs.SI', 'cs.SY'
    ]
    
    stats_categories = [
        'stat.AP', 'stat.CO', 'stat.ML', 'stat.ME', 'stat.OT', 'stat.TH'
    ]
    
    return cs_categories + stats_categories

def format_authors(authors: List[Any]) -> str:
    """Format the list of authors into a string."""
    return ', '.join(str(author) for author in authors)

def fetch_papers_for_date(target_date: datetime) -> List[Dict[str, Any]]:
    """Fetch papers from arXiv for a specific date."""
    categories = get_categories()
    
    # Create the date range for the search
    date_str = target_date.strftime('%Y%m%d')
    next_date = (target_date + timedelta(days=1)).strftime('%Y%m%d')
    
    all_papers = []
    
    # Search for each category
    for category in categories:
        search = arxiv.Search(
            query=f'cat:{category} AND submittedDate:[{date_str}0000 TO {next_date}0000]',
            max_results=100,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        try:
            results = list(search.results())
            
            for paper in results:
                paper_dict = {
                    'arxiv_id': paper.entry_id.split('/')[-1],
                    'title': paper.title,
                    'abstract': paper.summary,
                    'authors': format_authors(paper.authors),
                    'categories': ' '.join(paper.categories),
                    'published_date': paper.published.strftime('%Y-%m-%d'),
                    'score': 0.0
                }
                
                # Only add if we haven't seen this paper before
                if not any(p['arxiv_id'] == paper_dict['arxiv_id'] for p in all_papers):
                    all_papers.append(paper_dict)
            
        except Exception as e:
            print(f"Error fetching papers for category {category}: {str(e)}", file=sys.stderr)
    
    return all_papers

def fetch_papers_for_date_range(start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
    """Fetch papers from arXiv for a range of dates."""
    all_papers = []
    current_date = start_date
    
    while current_date <= end_date:
        print(f"Fetching papers for {current_date.strftime('%Y-%m-%d')}...")
        papers = fetch_papers_for_date(current_date)
        print(f"Found {len(papers)} papers")
        all_papers.extend(papers)
        current_date += timedelta(days=1)
    
    return all_papers

def save_to_database(papers: List[Dict[str, Any]]) -> None:
    """Save the papers to the database."""
    db = SessionLocal()
    try:
        for paper_dict in papers:
            # Check if paper already exists
            existing_paper = db.query(Paper).filter(Paper.arxiv_id == paper_dict['arxiv_id']).first()
            if not existing_paper:
                paper = Paper(**paper_dict)
                db.add(paper)
        db.commit()
    except Exception as e:
        print(f"Error saving to database: {str(e)}", file=sys.stderr)
        db.rollback()
    finally:
        db.close()

def parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print(f"Error: Date '{date_str}' must be in YYYY-MM-DD format", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Fetch papers from arXiv for a specific date or date range')
    date_group = parser.add_mutually_exclusive_group()
    date_group.add_argument('--date', type=str, help='Single date to fetch papers for (YYYY-MM-DD format)')
    date_group.add_argument('--start-date', type=str, help='Start date of range (YYYY-MM-DD format)')
    parser.add_argument('--end-date', type=str, help='End date of range (YYYY-MM-DD format, required if --start-date is used)')
    parser.add_argument('--output', type=str, help='Output JSON file (optional)')
    parser.add_argument('--save-db', action='store_true', help='Save papers to database')
    
    args = parser.parse_args()
    
    # Validate date arguments
    if args.start_date and not args.end_date:
        parser.error("--end-date is required when using --start-date")
    if args.end_date and not args.start_date:
        parser.error("--start-date is required when using --end-date")
    
    # Set default date if neither option is provided
    if not args.date and not args.start_date:
        args.date = datetime.now().strftime('%Y-%m-%d')
    
    # Fetch papers based on date options
    if args.date:
        target_date = parse_date(args.date)
        print(f"Fetching papers for {args.date}...")
        papers = fetch_papers_for_date(target_date)
        print(f"Found {len(papers)} papers")
    else:
        start_date = parse_date(args.start_date)
        end_date = parse_date(args.end_date)
        
        # Validate date range
        if end_date < start_date:
            print("Error: End date must be after start date", file=sys.stderr)
            sys.exit(1)
        
        # Warn if range is more than 7 days
        date_diff = (end_date - start_date).days
        if date_diff > 7:
            print(f"Warning: Fetching papers for {date_diff} days. This might take a while.", file=sys.stderr)
            response = input("Do you want to continue? [y/N] ")
            if response.lower() != 'y':
                sys.exit(0)
        
        papers = fetch_papers_for_date_range(start_date, end_date)
        print(f"Found total of {len(papers)} papers")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(papers, f, indent=2)
        print(f"Saved papers to {args.output}")
    
    if args.save_db:
        print("Saving papers to database...")
        save_to_database(papers)
        print("Done saving to database")

if __name__ == '__main__':
    main() 