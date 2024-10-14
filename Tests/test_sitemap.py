import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
import requests
import xml.etree.ElementTree as ET

# Import the functions to be tested from the main module
from Sitemap_parse.Sitemap_parse_for_pytest import extract_sitemap_urls, parse_sitemap

# Mock data for the sitemap index and URLs (with domain-specific loc)
SITEMAP_INDEX_XML = '''
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <sitemap>
        <loc>https://watchesofmayfair.com/sitemaps/general/sitemap_01.xml</loc>
    </sitemap>
</sitemapindex>
'''

SITEMAP_AU_INDEX_XML = '''
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <sitemap>
        <loc>https://watchesofmayfair.com.au/sitemaps/general/sitemap_01.xml</loc>
    </sitemap>
</sitemapindex>
'''

SITEMAP_HK_INDEX_XML = '''
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <sitemap>
        <loc>https://watchesofmayfair.com.hk/sitemaps/general/sitemap_01.xml</loc>
    </sitemap>
</sitemapindex>
'''

SITEMAP_COM_XML = '''
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
    <url>
        <loc>https://watchesofmayfair.com/</loc>
        <xhtml:link rel="alternate" hreflang="en" href="https://watchesofmayfair.hk.com"/>
        <xhtml:link rel="alternate" hreflang="en" href="https://watchesofmayfair.au.com"/>
    </url>
</urlset>
'''

SITEMAP_AU_XML = '''
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
    <url>
        <loc>https://watchesofmayfair.au.com/</loc>
        <xhtml:link rel="alternate" hreflang="en" href="https://watchesofmayfair.hk.com"/>
        <xhtml:link rel="alternate" hreflang="en" href="https://watchesofmayfair.com"/>
    </url>
</urlset>
'''

SITEMAP_HK_XML = '''
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
    <url>
        <loc>https://watchesofmayfair.hk.com/</loc>
        <xhtml:link rel="alternate" hreflang="en" href="https://watchesofmayfair.au.com"/>
        <xhtml:link rel="alternate" hreflang="en" href="https://watchesofmayfair.com"/>
    </url>
</urlset>
'''


@pytest.fixture
def mock_requests(requests_mock):
    """Fixture to mock requests for sitemap fetching."""
    # Mock the requests for the sitemap index files
    requests_mock.get("https://watchesofmayfair.com/sitemaps/general/sitemap_com_index.xml", text=SITEMAP_INDEX_XML)
    requests_mock.get("https://watchesofmayfair.com.au/sitemaps/general/sitemap_au_index.xml",
                      text=SITEMAP_AU_INDEX_XML)
    requests_mock.get("https://watchesofmayfair.com.hk/sitemaps/general/sitemap_hk_index.xml",
                      text=SITEMAP_HK_INDEX_XML)

    # Mock the requests for the individual sitemap files based on the domain
    requests_mock.get("https://watchesofmayfair.com/sitemaps/general/sitemap_01.xml", text=SITEMAP_COM_XML)
    requests_mock.get("https://watchesofmayfair.com.au/sitemaps/general/sitemap_01.xml", text=SITEMAP_AU_XML)
    requests_mock.get("https://watchesofmayfair.com.hk/sitemaps/general/sitemap_01.xml", text=SITEMAP_HK_XML)


def test_sitemap_com(mock_requests):
    """Test for watchesofmayfair.com sitemap."""
    global_domain = "watchesofmayfair.com"
    regional_domains = ["watchesofmayfair.hk.com", "watchesofmayfair.au.com", "watchesofmayfair.com"]

    sitemap_urls = extract_sitemap_urls("https://watchesofmayfair.com/sitemaps/general/sitemap_com_index.xml")
    for url in sitemap_urls:
        parse_sitemap(url, global_domain, regional_domains)


def test_sitemap_au(mock_requests):
    """Test for watchesofmayfair.au.com sitemap."""
    global_domain = "watchesofmayfair.au.com"
    regional_domains = ["watchesofmayfair.hk.com", "watchesofmayfair.com", "watchesofmayfair.au.com"]

    sitemap_urls = extract_sitemap_urls("https://watchesofmayfair.com.au/sitemaps/general/sitemap_au_index.xml")
    for url in sitemap_urls:
        parse_sitemap(url, global_domain, regional_domains)


def test_sitemap_hk(mock_requests):
    """Test for watchesofmayfair.hk.com sitemap."""
    global_domain = "watchesofmayfair.hk.com"
    regional_domains = ["watchesofmayfair.hk.com", "watchesofmayfair.au.com", "watchesofmayfair.com"]

    sitemap_urls = extract_sitemap_urls("https://watchesofmayfair.com.hk/sitemaps/general/sitemap_hk_index.xml")
    for url in sitemap_urls:
        parse_sitemap(url, global_domain, regional_domains)