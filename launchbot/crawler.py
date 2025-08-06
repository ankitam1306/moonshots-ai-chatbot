import requests
import threading
import queue
from bs4 import BeautifulSoup
from langchain.schema import Document
from config import BASE_URL, DOMAIN
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
from urllib3.util.retry import Retry

lock = threading.Lock()

# create a request session with retry logic
session = requests.Session()
retries = Retry(
  total=3,  # Retry up to 3 times
  backoff_factor=1,  # Wait 1s, 2s, 4s between retries
  status_forcelist=[500, 502, 503, 504],  # Retry on these HTTP status codes
  allowed_methods=["HEAD", "GET", "OPTIONS"]  # Retry for safe HTTP methods
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

def get_all_documents(start_url, max_workers=10):
	visited = set()
	documents = []
	q = queue.Queue()
	q.put(start_url)

	def worker():
		while True:
			try:
				url = q.get(timeout=1)
			except queue.Empty:
				return
			crawl(url, visited, documents, q)
			q.task_done()

	with ThreadPoolExecutor(max_workers=max_workers) as executor:
			for _ in range(max_workers):
					executor.submit(worker)

	q.join()
	return documents


def crawl(url, visited, documents, q):
  with lock:
    if url in visited or not url.startswith(BASE_URL):
      return
    visited.add(url)

  try:
    print(f"[Queue size: {q.qsize()}] Fetching {url}")
    response = session.get(url, timeout=10)
    if response.status_code != 200:
      return
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.get_text(separator="\n")
    with lock:
      documents.append(Document(page_content=content, metadata={"source": url}))

    # Queue new links
    for link in soup.find_all("a", href=True):
      href = urljoin(url, link["href"])
      if DOMAIN in href and "#" not in href:
        with lock:
          if href not in visited:
            q.put(href)
      
  except Exception as e:
    print(f"Error fetching {url}: {e}")