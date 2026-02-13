import httpx
from datetime import datetime
from typing import List, Dict
import xml.etree.ElementTree as ET
from app import schemas

async def fetch_daily_papers() -> List[Dict]:
    """
    Fetches the latest papers from arXiv using their API
    """
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": "cat:cs.AI",  # Example: AI papers
        "start": 0,
        "max_results": 100,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        response.raise_for_status()
        return parse_arxiv_response(response.text)

def parse_arxiv_response(xml_content: str) -> List[Dict]:
    """
    Parses the arXiv API response XML into a list of paper dictionaries
    """
    root = ET.fromstring(xml_content)
    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    papers = []
    
    for entry in root.findall("atom:entry", namespace):
        paper = {
            "arxiv_id": entry.find("atom:id", namespace).text.split("/")[-1],
            "title": entry.find("atom:title", namespace).text.strip(),
            "abstract": entry.find("atom:summary", namespace).text.strip(),
            "authors": ", ".join([author.find("atom:name", namespace).text 
                                for author in entry.findall("atom:author", namespace)]),
            "categories": entry.find("atom:category", namespace).get("term"),
            "published_date": datetime.strptime(
                entry.find("atom:published", namespace).text,
                "%Y-%m-%dT%H:%M:%SZ"
            )
        }
        papers.append(paper)
    
    return papers

def create_paper_object(paper_dict: Dict) -> schemas.PaperCreate:
    """
    Converts a paper dictionary into a PaperCreate schema object
    """
    return schemas.PaperCreate(
        arxiv_id=paper_dict["arxiv_id"],
        title=paper_dict["title"],
        abstract=paper_dict["abstract"],
        authors=paper_dict["authors"],
        categories=paper_dict["categories"],
        published_date=paper_dict["published_date"]
    ) 