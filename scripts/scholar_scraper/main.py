# import scholarly
from scholarly import scholarly
import time
import pandas as pd
from difflib import SequenceMatcher
import bibtexparser
from pathlib import Path
import logging
import argparse
from datetime import datetime
from easydict import EasyDict
import json

LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True, parents=True)
_log_path = LOG_DIR / f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'

def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(str(_log_path)),
            logging.StreamHandler()
        ]
    )

def similar(a, b):
    """Calculate string similarity ratio"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def clean_title(title):
    """Clean paper title for better matching"""
    return ' '.join(title.lower().split())

def search_paper(title, threshold=0.85):
    """
    Search for a paper on Google Scholar
    Args:
        title: Paper title to search for
        threshold: Minimum similarity ratio to consider a match
    Returns:
        Tuple of (bib_entry, similarity_score) or (None, 0)
    """
    try:
        # import ipdb; ipdb.set_trace()
        search_query = scholarly.search_pubs(title)
        best_match = None
        best_score = 0
        
        # Check first 3 results
        for i in range(3):
            try:
                result = next(search_query)
                # scholarly.pprint(result)
                result = EasyDict(result)
                cleaned_result_title = clean_title(result.bib.get('title', ''))
                cleaned_search_title = clean_title(title)
                score = similar(cleaned_result_title, cleaned_search_title)
                
                if score > best_score:
                    best_score = score
                    best_match = result
                
                if best_score > threshold:
                    break
                    
            except StopIteration:
                break
            
        if best_match and best_score > threshold:
            return best_match.bib, best_score
            # return best_match.bibtex, best_score
            
        return None, best_score
        
    except Exception as e:
        logging.error(f"Error searching for '{title}': {str(e)}")
        return None, 0

def process_title_list(input_file, output_file, delay=2):
    """
    Process a list of paper titles and save results
    Args:
        input_file: Path to file containing paper titles (one per line)
        output_file: Path to save BibTeX entries
        delay: Delay between requests in seconds
    """
    try:
        # Read titles
        titles = Path(input_file).read_text().splitlines()
        titles = [t.strip() for t in titles if t.strip()]
        
        results = []
        for i, title in enumerate(titles, 1):
            logging.info(f"Processing {i}/{len(titles)}: {title}")
            
            bib_entry, score = search_paper(title)
            if bib_entry:
                results.append(bib_entry)
                logging.info(f"Found match with score {score:.2f}")
            else:
                logging.warning(f"No good match found for: {title}")
            
            time.sleep(delay)  # Avoid too many requests
            
        # Save results
        if results:
            # convert EasyDict to dict to string
            _t = json.dumps(results, indent=4)
            Path(output_file).write_text(_t)
            logging.info(f"Saved {len(results)} BibTeX entries to {output_file}")
        else:
            logging.warning("No entries found")
            
    except Exception as e:
        logging.error(f"Error processing title list: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Fetch BibTeX entries from Google Scholar')
    parser.add_argument('input_file', help='File containing paper titles (one per line)')
    parser.add_argument('output_file', help='Output BibTeX file')
    parser.add_argument('--delay', type=float, default=2, help='Delay between requests in seconds')
    parser.add_argument('--threshold', type=float, default=0.85, help='Minimum similarity threshold')
    
    args = parser.parse_args()
    
    setup_logging()
    process_title_list(args.input_file, args.output_file, args.delay)

if __name__ == "__main__":
    main()