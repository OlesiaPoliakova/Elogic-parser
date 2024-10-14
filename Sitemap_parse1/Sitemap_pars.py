
# import requests
# import xml.etree.ElementTree as ET
#
# # Define the global and regional domain variables
# global_domain = "watchesofmayfair.com"
# regional_domains = ["watchesofmayfair.hk.com", "watchesofmayfair.au.com"]
#
# # Single sitemap index URL
# sitemap_index_url = "https://watchesofmayfair.com/sitemaps/general/sitemap_com_index.xml"
#
# # Function to extract <loc> links from sitemap index
# def extract_sitemap_urls(sitemap_index_url):
#     print(f"Fetching sitemap index: {sitemap_index_url}")
#     response = requests.get(sitemap_index_url)
#     sitemap_urls = []
#     if response.status_code == 200:
#         print("Successfully fetched sitemap index.")
#         # Parse the sitemap index XML content with the correct namespace
#         root = ET.fromstring(response.content)
#         namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}  # Define the namespace
#
#         # Find all <sitemap> elements in the given namespace
#         sitemaps_found = root.findall('ns:sitemap', namespaces=namespace)
#         print(f"Found {len(sitemaps_found)} <sitemap> elements.")
#
#         # Iterate through each <sitemap> element and extract the <loc> URLs
#         for sitemap in sitemaps_found:
#             loc = sitemap.find('ns:loc', namespaces=namespace)
#             if loc is not None:
#                 loc_text = loc.text
#                 sitemap_urls.append(loc_text)
#             else:
#                 raise ValueError("No <loc> found in <sitemap>.")
#     else:
#         raise ConnectionError(f"Failed to fetch sitemap index: {response.status_code}")
#
#     return sitemap_urls
#
# # Define a function to parse a given sitemap URL
# def parse_sitemap(url):
#     print(f"Fetching sitemap: {url}")
#     response = requests.get(url)
#     if response.status_code == 200:
#         # Parse the XML content
#         root = ET.fromstring(response.content)
#
#         # Define the namespace for xhtml links
#         namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'xhtml': 'http://www.w3.org/1999/xhtml'}
#
#         # Iterate through each <url> in the sitemap
#         for url_elem in root.findall('ns:url', namespaces):
#             # Get the global domain from <loc>
#             loc_value = url_elem.find('ns:loc', namespaces).text
#
#             # Check if the global domain is correct
#             if global_domain not in loc_value:
#                 raise ValueError(f"Global domain does not point to {global_domain}: {loc_value}")
#
#             # Get the alternate regional domains from xhtml:link with hreflang attributes
#             for alt_link in url_elem.findall('xhtml:link', namespaces):
#                 regional_domain = alt_link.get('href')
#                 hreflang = alt_link.get('hreflang')
#
#                 # Ensure the href points to regional domains
#                 if not any(rd in regional_domain for rd in regional_domains):
#                     raise ValueError(f"Regional domain is incorrect: {regional_domain}")
#     else:
#         raise ConnectionError(f"Failed to fetch sitemap: {response.status_code} from {url}")
#
# # Step 1: Extract all sitemap URLs from the index
# sitemap_urls = extract_sitemap_urls(sitemap_index_url)
#
# # Step 2: Loop through the array of extracted sitemap URLs and parse each
# for sitemap_url in sitemap_urls:
#     parse_sitemap(sitemap_url)
#
# print("All sitemaps checked and passed validation.")

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



