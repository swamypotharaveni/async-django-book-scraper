from adrf.views import APIView
import asyncio
import httpx
from rest_framework.response import Response
from bs4 import BeautifulSoup
import httpx
import asyncio
from .models import Book
from asgiref.sync import sync_to_async
class scraping_site(APIView):

    async def featach_page(self, client, url):
        response = await client.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        find_all_book = soup.find_all("article", class_="product_pod")

        books_list = []
        for book in find_all_book:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text

            books_list.append({
                "title": title,
                "price": price
            })
        if(len(books_list)>0):
            existing_titles = await sync_to_async(lambda: set(Book.objects.values_list('title', flat=True)))()
            book_objects = [Book(title=b["title"], price=b["price"]) for b in books_list if b["title"] not in existing_titles]

            if book_objects:
             await sync_to_async(Book.objects.bulk_create)(book_objects, ignore_conflicts=True)
            
      
        return {
            "url": url,
            "total_books": len(books_list),
            "books": books_list
        }

    async def get(self, request):
        urls = [
            "https://books.toscrape.com/catalogue/page-1.html",
            "https://books.toscrape.com/catalogue/page-2.html",
            "https://books.toscrape.com/catalogue/page-3.html"
        ]

        async with httpx.AsyncClient(  headers={"User-Agent": "Mozilla/5.0"}) as client:
            tasks = [self.featach_page(client, u) for u in urls]
            results = await asyncio.gather(*tasks)

        return Response({"pages": results})


