import reflex as rx
from typing import TypedDict
import logging
from sqlalchemy import text
import random


class Author(TypedDict):
    au_id: str
    name: str
    phone: str
    city: str
    state: str
    contract: bool


class AuthorState(rx.State):
    authors: list[Author] = []
    is_loading: bool = True

    @rx.event(background=True)
    async def get_all_authors(self):
        async with self:
            self.is_loading = True
        try:
            async with rx.asession() as session:
                res = await session.execute(
                    text("""
                        SELECT au_id, au_fname + ' ' + au_lname as name, phone, city, state, contract
                        FROM authors
                        ORDER BY au_lname, au_fname
                    """)
                )
                rows = res.all()
            async with self:
                self.authors = [
                    {
                        "au_id": row[0],
                        "name": row[1],
                        "phone": row[2],
                        "city": row[3],
                        "state": row[4],
                        "contract": row[5],
                    }
                    for row in rows
                ]
        except Exception as e:
            logging.exception(f"Failed to fetch authors: {e}")
        finally:
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def add_author(self, form_data: dict):
        try:
            au_id = f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
            async with rx.asession() as session:
                async with session.begin():
                    await session.execute(
                        text("""
                            INSERT INTO authors (au_id, au_fname, au_lname, phone, address, city, state, zip, contract)
                            VALUES (:au_id, :au_fname, :au_lname, :phone, :address, :city, :state, :zip, :contract)
                        """),
                        {
                            "au_id": au_id,
                            "au_fname": form_data["au_fname"],
                            "au_lname": form_data["au_lname"],
                            "phone": form_data["phone"],
                            "address": form_data.get("address", ""),
                            "city": form_data.get("city", ""),
                            "state": form_data.get("state", ""),
                            "zip": form_data.get("zip", ""),
                            "contract": 1 if form_data.get("contract") else 0,
                        },
                    )
        except Exception as e:
            logging.exception(f"Failed to add author: {e}")
        async with self:
            return AuthorState.get_all_authors