import reflex as rx
from typing import TypedDict, Optional
import logging
from sqlalchemy import text
import random
import string


class Author(TypedDict):
    au_id: str
    name: str
    phone: str
    address: str
    city: str
    state: str
    zip: str
    contract: bool


class Book(TypedDict):
    title_id: str
    title: str
    type: str
    price: float
    ytd_sales: int


class AuthorDetailState(rx.State):
    author: Optional[Author] = None
    books: list[Book] = []
    is_loading: bool = True

    @rx.var
    def author_id_from_route(self) -> str:
        return self.router.page.params.get("au_id", "")

    @rx.event(background=True)
    async def get_author_details(self):
        async with self:
            self.is_loading = True
            self.author = None
            self.books = []
        try:
            async with rx.asession() as session:
                author_res = await session.execute(
                    text(
                        "SELECT au_id, au_fname + ' ' + au_lname, phone, address, city, state, zip, contract FROM authors WHERE au_id = :au_id"
                    ),
                    {"au_id": self.author_id_from_route},
                )
                author_row = author_res.first()
                if not author_row:
                    async with self:
                        self.is_loading = False
                    return
                books_res = await session.execute(
                    text("""
                        SELECT t.title_id, t.title, RTRIM(t.type) as type, ISNULL(t.price, 0) as price, ISNULL(t.ytd_sales, 0) as ytd_sales
                        FROM titles t
                        JOIN titleauthor ta ON t.title_id = ta.title_id
                        WHERE ta.au_id = :au_id
                    """),
                    {"au_id": self.author_id_from_route},
                )
                books_rows = books_res.all()
            async with self:
                self.author = {
                    "au_id": author_row[0],
                    "name": author_row[1],
                    "phone": author_row[2],
                    "address": author_row[3],
                    "city": author_row[4],
                    "state": author_row[5],
                    "zip": author_row[6],
                    "contract": author_row[7],
                }
                self.books = [
                    {
                        "title_id": row[0],
                        "title": row[1],
                        "type": row[2],
                        "price": float(row[3]),
                        "ytd_sales": row[4],
                    }
                    for row in books_rows
                ]
        except Exception as e:
            logging.exception(f"Failed to fetch author details: {e}")
        finally:
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def add_book(self, form_data: dict):
        try:
            title_id = f"BU{random.randint(1000, 9999)}"
            async with rx.asession() as session:
                async with session.begin():
                    await session.execute(
                        text(
                            "INSERT INTO titles (title_id, title, type, price) VALUES (:title_id, :title, :type, :price)"
                        ),
                        {
                            "title_id": title_id,
                            "title": form_data["title"],
                            "type": form_data["type"],
                            "price": float(form_data["price"]),
                        },
                    )
                    await session.execute(
                        text(
                            "INSERT INTO titleauthor (au_id, title_id) VALUES (:au_id, :title_id)"
                        ),
                        {"au_id": self.author_id_from_route, "title_id": title_id},
                    )
        except Exception as e:
            logging.exception(f"Failed to add book: {e}")
        async with self:
            return AuthorDetailState.get_author_details

    @rx.event(background=True)
    async def update_book(self, form_data: dict):
        try:
            async with rx.asession() as session:
                async with session.begin():
                    await session.execute(
                        text(
                            "UPDATE titles SET title = :title, type = :type, price = :price WHERE title_id = :title_id"
                        ),
                        {
                            "title": form_data["title"],
                            "type": form_data["type"],
                            "price": float(form_data["price"]),
                            "title_id": form_data["title_id"],
                        },
                    )
        except Exception as e:
            logging.exception(f"Failed to update book: {e}")
        async with self:
            return AuthorDetailState.get_author_details