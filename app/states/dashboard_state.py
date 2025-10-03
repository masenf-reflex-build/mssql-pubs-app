import reflex as rx
from typing import TypedDict
import asyncio
import logging
from sqlalchemy import text


class Stat(TypedDict):
    total_books: int
    total_ytd_sales: int
    avg_price: float
    total_authors: int


class Sale(TypedDict):
    month: str
    sales: int


class Book(TypedDict):
    title: str
    type: str
    price: float
    ytd_sales: int


class Author(TypedDict):
    name: str
    city: str
    state: str
    book_count: int


class DashboardState(rx.State):
    stats: Stat = {
        "total_books": 0,
        "total_ytd_sales": 0,
        "avg_price": 0.0,
        "total_authors": 0,
    }
    sales_by_month: list[Sale] = []
    top_books: list[Book] = []
    top_authors: list[Author] = []
    is_loading: bool = True

    @rx.event(background=True)
    async def get_dashboard_data(self):
        async with self:
            self.is_loading = True
        try:
            async with rx.asession() as session:
                stats_res = await session.execute(
                    text("""
                        SELECT 
                            COUNT(DISTINCT t.title_id) as total_books,
                            ISNULL(SUM(t.ytd_sales), 0) as total_ytd_sales,
                            ISNULL(AVG(t.price), 0.0) as avg_price,
                            (SELECT COUNT(*) FROM authors) as total_authors
                        FROM titles t
                        """)
                )
                sales_res = await session.execute(
                    text("""
                        SELECT TOP 6
                            FORMAT(ord_date, 'MMM') as month,
                            SUM(qty) as total_sales
                        FROM sales
                        GROUP BY FORMAT(ord_date, 'MMM'), YEAR(ord_date), MONTH(ord_date)
                        ORDER BY YEAR(ord_date) DESC, MONTH(ord_date) DESC;
                        """)
                )
                books_res = await session.execute(
                    text("""
                        SELECT TOP 5
                            title,
                            RTRIM(type) as type,
                            ISNULL(price, 0) as price,
                            ISNULL(ytd_sales, 0) as ytd_sales
                        FROM titles
                        WHERE ytd_sales IS NOT NULL
                        ORDER BY ytd_sales DESC;
                        """)
                )
                authors_res = await session.execute(
                    text("""
                        SELECT TOP 5
                            a.au_fname + ' ' + a.au_lname as name,
                            ISNULL(a.city, 'Unknown') as city,
                            ISNULL(a.state, 'N/A') as state,
                            COUNT(ta.title_id) as book_count
                        FROM authors a
                        JOIN titleauthor ta ON a.au_id = ta.au_id
                        GROUP BY a.au_fname, a.au_lname, a.city, a.state
                        ORDER BY book_count DESC;
                        """)
                )
                stats_row = stats_res.first()
                sales_rows = sales_res.all()
                books_rows = books_res.all()
                authors_rows = authors_res.all()
            async with self:
                if stats_row:
                    self.stats = {
                        "total_books": stats_row[0],
                        "total_ytd_sales": stats_row[1],
                        "avg_price": float(stats_row[2]),
                        "total_authors": stats_row[3],
                    }
                self.sales_by_month = [
                    {"month": row[0], "sales": row[1]} for row in reversed(sales_rows)
                ]
                self.top_books = [
                    {
                        "title": row[0],
                        "type": row[1],
                        "price": float(row[2]),
                        "ytd_sales": row[3],
                    }
                    for row in books_rows
                ]
                self.top_authors = [
                    {
                        "name": row[0],
                        "city": row[1],
                        "state": row[2],
                        "book_count": row[3],
                    }
                    for row in authors_rows
                ]
        except Exception as e:
            logging.exception(f"Database Error: {e}")
        finally:
            async with self:
                self.is_loading = False

    @rx.var
    def formatted_total_sales(self) -> str:
        return f"${self.stats['total_ytd_sales']:,}"

    @rx.var
    def formatted_avg_price(self) -> str:
        return f"${self.stats['avg_price']:.2f}"