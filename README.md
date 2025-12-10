# Async Django Book Scraper API

This project is an **asynchronous web scraper API** built with **Django**, **ADRF (Asynchronous Django REST Framework)**, and **BeautifulSoup**.
It scrapes book information (title and price) from [Books to Scrape](https://books.toscrape.com/) and saves it in a Django model.

---

## Features

* Async scraping of multiple pages concurrently using `httpx` and `asyncio`.
* Stores scraped book data in the Django database.
* Avoids duplicate entries by checking existing titles.
* Fully asynchronous API endpoint using `adrf`.

---

## Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd <repo-folder>
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

**Requirements:**

```txt
adrf==0.1.12
Django==5.2.7
djangorestframework==3.16.1
httpx==0.28.1
beautifulsoup4==4.14.3
asgiref==3.10.0
```

---

## Usage

1. **Add the app to `INSTALLED_APPS` in `settings.py`**

```python
INSTALLED_APPS = [
    ...
    'your_app_name',
    'rest_framework',
]
```

2. **Run migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Start the Django server**

```bash
python manage.py runserver
```

4. **Access the scraping API**

* URL: `/scraping/`
* Method: `GET`
* Response example:

```json
{
    "pages": [
        {
            "url": "https://books.toscrape.com/catalogue/page-1.html",
            "total_books": 20,
            "books": [
                {
                    "title": "A Light in the Attic",
                    "price": "£51.77"
                },
                ...
            ]
        },
        ...
    ]
}
```

---

## About httpx and asyncio

* **httpx**: An async HTTP client library used to make concurrent HTTP requests to web pages. It allows non-blocking network calls, which makes your scraping faster by fetching multiple pages at the same time.

* **asyncio**: Python's built-in library for writing asynchronous code. It provides the event loop and tools like `async def`, `await`, and `asyncio.gather()` to run multiple tasks concurrently.

**Example Usage:**

```python
import httpx
import asyncio

async def fetch(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text

async def main():
    urls = ["https://books.toscrape.com/page-1.html", "https://books.toscrape.com/page-2.html"]
    tasks = [fetch(u) for u in urls]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

---

## Project Structure

```
project/
│
├── your_app_name/
│   ├── models.py          # Book model
│   ├── views.py           # Async scraping API
│   ├── urls.py            # API endpoint routing
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## Notes

* **Async DB operations:** Uses `sync_to_async` to safely insert data using Django ORM.
* **Avoiding duplicates:** Checks existing book titles before inserting.
* **Headers:** The scraper uses a User-Agent header to avoid basic blocks.


