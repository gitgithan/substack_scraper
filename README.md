# Substack Scraper

Scrape paid or free articles from a Substack newsletter, saving both HTML and Markdown versions.

## Setup

1. Clone the repository and enter the directory:
    ```bash
    git clone https://github.com/gitgithan/substack_scraper.git
    cd substack_scraper
    ```

2. (Recommended) Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```
    pip install requests beautifulsoup4 lxml markdownify selenium
    ```

4. Install ChromeDriver and ensure it's in your PATH.

5. Edit `substack_scraper.py`:
    - Set `BASE_URL` to your newsletter's main URL (e.g., `https://newsletter.eng-leadership.com`)
    - Set `SITEMAP_STRING` to the sitemap path (e.g., `/sitemap.xml`)

## Usage

- **Scrape free articles:**
    ```
    python substack_scraper.py
    ```

- **Scrape paid articles (manual login required):**
    ```
    python substack_scraper.py --paid
    ```
    This will launch a browser for you to log in manually (doesn't matter email OTP or with password). After logging in, press Enter in the terminal to continue scraping.

    **Note:** If paid content does not load correctly, you may need to increase the sleep duration in the script (see `sleep()` in `scrape_article_selenium`). Paid articles sometimes take longer to render after login.

## Output

- HTML files: `html_files/`
- Markdown files: `md_files/`
- Article metadata: `articles.json`
- List of URLs: `urls.txt`

