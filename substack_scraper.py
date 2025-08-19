"""
Purpose:
    Scrape paid subscription articles from a Substack newsletter, saving both HTML and Markdown versions.
    You must edit BASE_URL and SITEMAP_STRING below to match your target newsletter.

Instructions:
    - Set BASE_URL to the newsletter's main URL (e.g., "https://newsletter.eng-leadership.com")
    - Set SITEMAP_STRING to the sitemap path (e.g., "/sitemap.xml")
    - Use --paid flag to enable scraping paid content (manual login required)
"""

import requests
from bs4 import BeautifulSoup
import lxml
import markdownify
import json
from selenium import webdriver
from time import sleep
import argparse

BASE_URL = "https://newsletter.eng-leadership.com"  # Change to your newsletter base URL
SITEMAP_STRING = "/sitemap.xml"  # Change if your sitemap path is different

SITEMAP_URL = BASE_URL + SITEMAP_STRING

OUTPUT_FILE = "articles.json"


def selenium_login():
    driver = webdriver.Chrome()
    driver.get("https://substack.com/sign-in")
    input("After you have logged in and see your account, press Enter here to continue...")
    print("Continuing with scraping...")
    return driver


def get_article_urls(sitemap_url):
    resp = requests.get(sitemap_url)
    soup = BeautifulSoup(resp.content, "xml")
    return [loc.text for loc in soup.find_all("loc")]


def extract_article_html_and_md(soup):
    # Prioritize content containers
    article = soup.find("div", class_="available-content")
    if not article:
        article = soup.find("div", class_="body markup")
    if not article:
        article = soup.find("article")
    if not article:
        article = soup.find("div", class_="body") or soup.find("div", class_="post-content")
    if not article:
        return None, None
    html_content = str(article)
    markdown_content = markdownify.markdownify(html_content, heading_style="ATX")
    return html_content, markdown_content


def scrape_article_selenium(driver, url):
    driver.get(url)
    sleep(0.3)
    soup = BeautifulSoup(driver.page_source, "lxml")
    return extract_article_html_and_md(soup)


def scrape_article_requests(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "lxml")
    return extract_article_html_and_md(soup)


def main():
    parser = argparse.ArgumentParser(description="Substack scraper")
    parser.add_argument("--paid", action="store_true", help="Enable scraping paid content (manual login required)")
    args = parser.parse_args()

    driver = None
    if args.paid:
        print("Paid mode enabled. Manual login required.")
        driver = selenium_login()
    else:
        print("Paid mode not enabled. Scraping free content only.")

    print("Fetching sitemap...")
    urls = get_article_urls(SITEMAP_URL)
    print(f"Found {len(urls)} articles.")
    with open("urls.txt", "w") as url_file:
        for url in urls:
            url_file.write(url + "\n")
    print(f"Saved URLs to urls.txt")
    # Create folders for html and md files, clearing them first
    import os
    import shutil

    html_dir = "html_files"
    md_dir = "md_files"
    # Remove all files in html_files and md_files if they exist
    for folder in [html_dir, md_dir]:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            os.makedirs(folder, exist_ok=True)
    results = []
    for url in urls[:5]:  # to test on less articles
        print(f"Scraping {url}")
        if args.paid:
            html, md = scrape_article_selenium(driver, url)
        else:
            html, md = scrape_article_requests(url)
        if html and md:
            # Use last part of URL as filename
            base_name = url.rstrip("/").split("/")[-1]
            html_path = os.path.join(html_dir, base_name + ".html")
            md_path = os.path.join(md_dir, base_name + ".md")
            with open(html_path, "w", encoding="utf-8") as f_html:
                f_html.write(html)
            with open(md_path, "w", encoding="utf-8") as f_md:
                f_md.write(md)
            results.append({"url": url, "html_file": html_path, "md_file": md_path})
    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved {len(results)} articles to {OUTPUT_FILE}")
    if driver:
        driver.quit()


if __name__ == "__main__":
    main()
