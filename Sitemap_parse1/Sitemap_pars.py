

import requests
import xml.etree.ElementTree as ET

# Global and regional domain variables
GLOBAL_DOMAIN = "watchesofmayfair.com"
REGIONAL_DOMAINS = ["watchesofmayfair.hk.com", "watchesofmayfair.au.com", "watchesofmayfair.com"]

# Sitemap index URL
SITEMAP_INDEX_URL = "https://watchesofmayfair.com/sitemaps/general/sitemap_com_index.xml"

# Namespaces
NAMESPACES = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'xhtml': 'http://www.w3.org/1999/xhtml'}
# Function to extract <loc> links from sitemap index
def extract_sitemap_urls(sitemap_index_url):
    print(f"Fetching sitemap index: {sitemap_index_url}")
    response = requests.get(sitemap_index_url)

    if response.status_code != 200:
        raise ConnectionError(f"Failed to fetch sitemap index: {response.status_code}")

    print("Successfully fetched sitemap index.")

    # Parse the sitemap index XML content
    root = ET.fromstring(response.content)

    # Find and return all <loc> URLs from <sitemap> elements
    sitemap_urls = [loc.text for loc in root.findall('ns:sitemap/ns:loc', namespaces=NAMESPACES)]
    print(f"Found {len(sitemap_urls)} sitemap URLs.")

    return sitemap_urls


# Function to parse a sitemap and validate domains
def parse_sitemap(url):
    print(f"Fetching and parsing sitemap: {url}")
    response = requests.get(url)

    if response.status_code != 200:
        raise ConnectionError(f"Failed to fetch sitemap: {response.status_code} from {url}")

    root = ET.fromstring(response.content)

    # Iterate through each <url> in the sitemap
    for url_elem in root.findall('ns:url', namespaces=NAMESPACES):
        # Check global domain in <loc>
        loc_value = url_elem.find('ns:loc', namespaces=NAMESPACES).text
        if GLOBAL_DOMAIN not in loc_value:
            raise ValueError(f"Global domain does not point to {GLOBAL_DOMAIN}: {loc_value}")

        # Check regional domains in xhtml:link
        for alt_link in url_elem.findall('xhtml:link', namespaces=NAMESPACES):
            regional_domain = alt_link.get('href')
            if not any(rd in regional_domain for rd in REGIONAL_DOMAINS):
                raise ValueError(f"Regional domain is incorrect: {regional_domain}")


# Main script execution
def main():
    # Step 1: Extract all sitemap URLs from the index
    sitemap_urls = extract_sitemap_urls(SITEMAP_INDEX_URL)

    # Step 2: Loop through the array of extracted sitemap URLs and parse each
    for sitemap_url in sitemap_urls:
        parse_sitemap(sitemap_url)

    print("All sitemaps checked and passed validation.")

if __name__ == "__main__":
    main()



