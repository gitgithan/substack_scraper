"""
Purpose:
    Scrape paid subscription articles from a Substack newsletter, saving both HTML and Markdown versions.
    You must edit BASE_URL, SITEMAP_STRING, USERNAME, and PASSWORD below to match your target newsletter and credentials.

Instructions:
    - Set BASE_URL to the newsletter's main URL (e.g., "https://newsletter.eng-leadership.com")
    - Set SITEMAP_STRING to the sitemap path (e.g., "/sitemap.xml")
    - Set USERNAME and PASSWORD to your Substack login credentials (if needed)
"""

import requests
from bs4 import BeautifulSoup
import lxml
import markdownify
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

USERNAME = ""  # Your Substack email
PASSWORD = ""  # Your Substack password
BASE_URL = "https://newsletter.eng-leadership.com"  # Change to your newsletter base URL
SITEMAP_STRING = "/sitemap.xml"  # Change if your sitemap path is different

SITEMAP_URL = BASE_URL + SITEMAP_STRING

OUTPUT_FILE = "articles.json"


def selenium_login(email, password, headless=True):
    options = Options()
    # Always use non-headless for manual login
    print("Launching browser for manual login. Please log in, then press Enter in the terminal to continue scraping.")
    driver = webdriver.Chrome(options=options)
    driver.get("https://substack.com/sign-in")
    input("After you have logged in and see your account, press Enter here to continue...")
    print("Continuing with scraping...")
    return driver


def get_article_urls(sitemap_url):
    resp = requests.get(sitemap_url)
    soup = BeautifulSoup(resp.content, "xml")
    return [loc.text for loc in soup.find_all("loc")]


def scrape_article_selenium(driver, url):
    driver.get(url)
    sleep(0.3)
    soup = BeautifulSoup(driver.page_source, "lxml")
    # Prioritize paid/full content containers
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


def main():
    print("Logging in with Selenium...")
    driver = selenium_login(USERNAME, PASSWORD, headless=False)
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

    for url in urls:
        print(f"Scraping {url}")
        html, md = scrape_article_selenium(driver, url)
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
    driver.quit()


if __name__ == "__main__":
    main()
