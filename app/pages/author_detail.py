import reflex as rx
from app.states.author_detail_state import AuthorDetailState, Book
import logging


def edit_book_form(book: Book) -> rx.Component:
    return rx.el.form(
        rx.el.input(type="hidden", name="title_id", value=book["title_id"]),
        rx.el.div(
            rx.el.label("Title", class_name="text-sm font-medium"),
            rx.el.input(
                name="title",
                default_value=book["title"],
                class_name="mt-1 w-full p-2 border rounded-md",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label("Type", class_name="text-sm font-medium"),
            rx.el.input(
                name="type",
                default_value=book["type"],
                class_name="mt-1 w-full p-2 border rounded-md",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label("Price", class_name="text-sm font-medium"),
            rx.el.input(
                name="price",
                type="number",
                step="0.01",
                default_value=book["price"].to_string(),
                class_name="mt-1 w-full p-2 border rounded-md",
            ),
            class_name="mb-4",
        ),
        rx.el.button(
            "Update Book",
            type="submit",
            class_name="w-full bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600",
        ),
        on_submit=AuthorDetailState.update_book,
        reset_on_submit=True,
    )


def author_detail_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.cond(
                AuthorDetailState.is_loading,
                rx.el.div("Loading..."),
                rx.el.div(
                    rx.cond(
                        AuthorDetailState.author,
                        rx.el.div(
                            rx.el.h1(
                                AuthorDetailState.author["name"],
                                class_name="text-3xl font-bold text-gray-900",
                            ),
                            rx.el.p(
                                f"{AuthorDetailState.author['address']}, {AuthorDetailState.author['city']}, {AuthorDetailState.author['state']} {AuthorDetailState.author['zip']}",
                                class_name="text-gray-600",
                            ),
                            rx.el.p(
                                f"Phone: {AuthorDetailState.author['phone']}",
                                class_name="text-gray-600",
                            ),
                            rx.el.p(
                                rx.cond(
                                    AuthorDetailState.author["contract"],
                                    "Under contract",
                                    "Not under contract",
                                ),
                                class_name="text-gray-600",
                            ),
                            rx.el.h2(
                                "Books",
                                class_name="text-2xl font-bold text-gray-900 mt-8",
                            ),
                            rx.el.div(
                                rx.foreach(
                                    AuthorDetailState.books,
                                    lambda book: rx.el.div(
                                        rx.el.h3(
                                            book["title"],
                                            class_name="text-lg font-semibold",
                                        ),
                                        rx.el.p(f"Type: {book['type']}"),
                                        rx.el.p(
                                            "Price: $"
                                            + book["price"].to_string().split(".")[0]
                                        ),
                                        rx.el.p(f"YTD Sales: {book['ytd_sales']}"),
                                        edit_book_form(book),
                                        class_name="p-4 border rounded-lg mt-4",
                                    ),
                                ),
                                class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                            ),
                            rx.el.h2(
                                "Add New Book",
                                class_name="text-2xl font-bold text-gray-900 mt-8",
                            ),
                            rx.el.form(
                                rx.el.div(
                                    rx.el.label(
                                        "Title", class_name="text-sm font-medium"
                                    ),
                                    rx.el.input(
                                        name="title",
                                        placeholder="Book Title",
                                        class_name="mt-1 w-full p-2 border rounded-md",
                                    ),
                                    class_name="mb-4",
                                ),
                                rx.el.div(
                                    rx.el.label(
                                        "Type", class_name="text-sm font-medium"
                                    ),
                                    rx.el.input(
                                        name="type",
                                        placeholder="e.g., business",
                                        class_name="mt-1 w-full p-2 border rounded-md",
                                    ),
                                    class_name="mb-4",
                                ),
                                rx.el.div(
                                    rx.el.label(
                                        "Price", class_name="text-sm font-medium"
                                    ),
                                    rx.el.input(
                                        name="price",
                                        type="number",
                                        step="0.01",
                                        placeholder="19.99",
                                        class_name="mt-1 w-full p-2 border rounded-md",
                                    ),
                                    class_name="mb-4",
                                ),
                                rx.el.button(
                                    "Add Book",
                                    type="submit",
                                    class_name="w-full bg-green-500 text-white p-2 rounded-md hover:bg-green-600",
                                ),
                                on_submit=AuthorDetailState.add_book,
                                reset_on_submit=True,
                                class_name="mt-4 p-4 border rounded-lg",
                            ),
                        ),
                        rx.el.div("Author not found."),
                    )
                ),
            ),
            class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        class_name="font-['Raleway'] bg-gray-50 min-h-screen",
    )