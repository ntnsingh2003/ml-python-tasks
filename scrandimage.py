import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# 📥 Ask user for input URL
base_url = input("Enter the website URL (e.g., https://example.com): ").strip()
output_dir = "downloaded_site"
visited = set()

# ✅ Convert URL to safe filename
def sanitize_filename(url):
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path or path.endswith("/"):
        filename = "index.html"
    else:
        filename = path.replace("/", "_")
        if not filename.endswith(".html") and "." not in filename:
            filename += ".html"
    return filename

# ✅ Save any content to disk
def save_content(url, content):
    filename = sanitize_filename(url)
    if not filename:
        filename = "index.html"
    filepath = os.path.join(output_dir, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(content)

# ✅ Download static files like images, CSS, PDFs
def download_file(url):
    try:
        print(f"📥 Downloading file: {url}")
        r = requests.get(url)
        r.raise_for_status()
        save_content(url, r.content)
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")

# ✅ Crawl internal pages and resources
def crawl(url):
    if url in visited:
        return
    visited.add(url)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"⚠️ Failed to fetch {url}: {e}")
        return

    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        download_file(url)
        return

    save_content(url, response.content)
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup.find_all(["a", "img", "link", "script"]):
        attr = "href" if tag.name in ["a", "link"] else "src"
        file_url = tag.get(attr)
        if not file_url:
            continue

        full_url = urljoin(url, file_url)
        if urlparse(full_url).netloc != urlparse(base_url).netloc:
            continue  # skip external links

        crawl(full_url)

# 🏁 Run the crawler
if not base_url.startswith("http"):
    base_url = "https://" + base_url

os.makedirs(output_dir, exist_ok=True)
crawl(base_url)

print(f"\n✅ Website downloaded successfully to: {output_dir}/")
