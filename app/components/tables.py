import reflex as rx
from app.states.dashboard_state import DashboardState


def books_table() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Top 5 Books (YTD Sales)", class_name="text-xl font-semibold text-gray-800"
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Title",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Type",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Price",
                            class_name="px-4 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "YTD Sales",
                            class_name="px-4 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.top_books,
                        lambda book: rx.el.tr(
                            rx.el.td(
                                book["title"],
                                class_name="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-800",
                            ),
                            rx.el.td(
                                rx.el.span(
                                    book["type"]
                                    .to_string()
                                    .replace("_", " ")
                                    .capitalize(),
                                    class_name="px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800",
                                ),
                                class_name="px-4 py-4 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                f"${book['price']:.2f}",
                                class_name="px-4 py-4 whitespace-nowrap text-sm text-gray-500 text-right",
                            ),
                            rx.el.td(
                                book["ytd_sales"].to_string(),
                                class_name="px-4 py-4 whitespace-nowrap text-sm font-semibold text-gray-800 text-right",
                            ),
                            class_name="border-b border-gray-200 hover:bg-gray-50",
                        ),
                    )
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="mt-4 overflow-x-auto",
        ),
        class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
    )


def authors_table() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Top 5 Authors (by Books Published)",
            class_name="text-xl font-semibold text-gray-800",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Author",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Location",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Books",
                            class_name="px-4 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.top_authors,
                        lambda author: rx.el.tr(
                            rx.el.td(
                                rx.el.div(
                                    rx.image(
                                        src=f"https://api.dicebear.com/9.x/initials/svg?seed={author['name']}",
                                        class_name="size-8 rounded-full mr-3",
                                    ),
                                    rx.el.p(
                                        author["name"],
                                        class_name="text-sm font-medium text-gray-800",
                                    ),
                                    class_name="flex items-center",
                                ),
                                class_name="px-4 py-3 whitespace-nowrap",
                            ),
                            rx.el.td(
                                f"{author['city']}, {author['state']}",
                                class_name="px-4 py-3 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                author["book_count"].to_string(),
                                class_name="px-4 py-3 whitespace-nowrap text-sm font-semibold text-gray-800 text-right",
                            ),
                            class_name="border-b border-gray-200 hover:bg-gray-50",
                        ),
                    )
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="mt-4 overflow-x-auto",
        ),
        class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
    )