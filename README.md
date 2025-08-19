# Substack Scraper

## Quick Start

1. **Clone the repository and enter the project directory:**
   ```bash
   git clone https://github.com/gitgithan/substack_scraper.git
   cd substack_scraper
   ```

## Purpose

This project scrapes paid subscription articles from a Substack newsletter, saving both HTML and Markdown versions for offline use or analysis.

## Setup

1. **Edit Configuration**  
   Open `substack_scraper.py` and set the following at the top of the file:
   - `BASE_URL`: The main URL of the newsletter (e.g., `https://newsletter.eng-leadership.com`)
   - `SITEMAP_STRING`: The sitemap path (usually `/sitemap.xml`)
   - `USERNAME`: Your Substack email (if login is required)
   - `PASSWORD`: Your Substack password (if login is required)

2. **Create a virtual environment (.venv):**
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the virtual environment:**
   - On Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```cmd
     .venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt`, install manually:
   ```bash
   pip install requests beautifulsoup4 lxml markdownify selenium
   ```

5. **Run the Scraper**  
   The script will launch a browser for manual login. After logging in, scraping will begin.

## Output

- HTML files: Saved in `html_files/`
- Markdown files: Saved in `md_files/`
- Article metadata: Saved in `articles.json`

## Notes

- This tool is intended for personal use to archive paid content you have access to.
- You must have a valid subscription and login credentials for the target newsletter.

## Gotchas

- **Sleep Timing:**  
  If the script's sleep time after loading each article is too short, the full paid content may not be loaded yet. In this case, you may only scrape the non-subscriber (free) section of the article. If you notice missing content, try increasing the sleep duration in `substack_scraper.py` (see the `sleep()` call in `scrape_article_selenium`).

