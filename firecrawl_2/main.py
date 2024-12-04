# Getting a bit fancier
# Creating a function to do our crawl and specifying paramatwers

import warnings

# Filter out UserWarning: Field name 'schema' in "FirecrawlApp.ExtractParams" shadows an attribute in parent
# "BaseModel" from pydantic.main
warnings.filterwarnings("ignore", category=UserWarning)

import os
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import requests

# Load environment variables from the .env file
load_dotenv()

# Initialize the Firecrawl client with the local API URL
app = FirecrawlApp(
    api_key=os.getenv("FIRECRAWL_API_KEY"), api_url="http://localhost:3002"
)


def crawl_url(url, params=None):
    try:
        if params is None:
            params = {
                "limit": 5,
                "scrapeOptions": {
                    "formats": ["markdown", "html"],
                    "waitFor": 1000,  # wait for a second for pages to load
                    "timeout": 10000,  # timeout after 10 seconds
                },
            }
        return app.crawl_url(url, params=params)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 402:  # Payment Required
            # Get credit usage from the API
            try:
                credit_info = app.get_credit_usage()
                return f"Out of Token credits. Credits used: {credit_info.get('total_credits_used', 'Unknown')}"
            except Exception as credit_error:
                return f"Out of Token credits. Unable to fetch credit usage: {str(credit_error)}"
        raise e


def main():
    base_url = "https://books.toscrape.com/"
    crawl_result = crawl_url(url=base_url)

    # Check if we got an error message string instead of the usual dictionary
    if isinstance(crawl_result, str):
        print(crawl_result)
        return

    # did the crawl succeed?
    print("Crawl status:", crawl_result["status"])

    # If we got here, we have a successful crawl result
    # Get the data
    print("Available keys in response: ", crawl_result.keys())

    # how many pages did we get?
    print("Total pages crawled:", crawl_result["total"])

    # Display token usage information
    if "creditsUsed" in crawl_result:
        print("\nToken Usage Information:")
        token_usage = crawl_result["creditsUsed"]
        print(f"Total tokens used: ", token_usage)

    # Display the extracted content. This isnt pretty, just
    # a bunch of text scrolling up the screen up the screen.
    # We will make this prettier in another example.
    if "data" in crawl_result:
        print("\nExtracted Content:")
        for page_number, page_data in enumerate(crawl_result["data"], 1):
            print(f"\nPage {page_number}:")
            for key, value in page_data.items():
                print(f"  {key}: {value}")
    else:
        print("No extracted content found.")


if __name__ == "__main__":
    main()
