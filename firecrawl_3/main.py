# Ensuring we do not re read a page that has already been read

# We import warnings before anything else as this allows us to filter out
# UserWarning: Field name 'schema' in "FirecrawlApp.ExtractParams" which
# clashes with an attribute in parent "BaseModel" from pydantic.main
import warnings

# HOUSEKEEPING:Filter out UserWarning: Field name 'schema' in "FirecrawlApp.ExtractParams"
# which clashes with an attribute in parent "BaseModel" from pydantic.main
warnings.filterwarnings("ignore", category=UserWarning)

# The rest of our imports
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

# Creating a function to do our crawl and specifying paramatwers
def crawl_url(url, params=None):
    """
    Crawl a specified URL using Firecrawl with optional parameters.

    Args:
        url (str): The target URL to crawl.
        params (dict, optional): Dictionary of crawling parameters. If None, uses default settings:
            - limit: 5 pages
            - scrapeOptions:
                - formats: ["markdown", "html"]
                - waitFor: 1000ms (wait time for page load)
                - timeout: 10000ms (maximum time before timeout)

    Returns:
        dict: Crawl results from Firecrawl if successful
        str: Error message if out of credits, including credit usage information if available

    Raises:
        requests.exceptions.HTTPError: For HTTP errors other than 402 (Payment Required)
        Exception: For other unexpected errors during the crawl

    Example:
        >>> result = crawl_url("https://example.com")
        >>> result = crawl_url("https://example.com",
        ...                   params={"limit": 10,
        ...                          "scrapeOptions": {"formats": ["markdown"]}})
    """
    try:
        if params is None:
            params = {
                # limit the number of pages to crawl
                "limit": 2,
                # Specify scrape options
                "scrapeOptions": {
                    "formats": ["markdown"],  # Return content as markdown only
                    "waitFor": 1000,  # wait for a second for pages to load
                    "timeout": 5000,  # timeout after 5 seconds
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

    # Did the crawl succeed?
    print("Crawl status:", crawl_result["status"])

    # How many pages did we get?
    print("Total pages crawled:", crawl_result["total"])


    # Display the extracted content.
    # This is the markdown that is returned
    # NOTE: This returns two pages of the same data. Why?
    # We will look at that next
    if "data" in crawl_result:
        print("\nExtracted Content:")
        # Iterate over the pages
        for page_number, page_data in enumerate(crawl_result["data"], 1):
            print(f"\nPage {page_number}:")
            # Iterate over the keys and values
            for key, value in page_data.items():
                print(f"  {key}: {value}")
    else:
       # And if we didnt get any extracted content
        print("No extracted content found.")


if __name__ == "__main__":
    main()
