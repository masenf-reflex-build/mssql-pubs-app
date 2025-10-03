import reflex as rx
from app.states.dashboard_state import DashboardState


def stat_card(icon: str, title: str, value: rx.Var[str]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(tag=icon, class_name="size-6 text-blue-500"),
            class_name="p-3 bg-blue-100 rounded-xl",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-semibold text-gray-800"),
            class_name="flex flex-col",
        ),
        class_name="flex items-center gap-4 p-4 bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300",
    )


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Publisher Dashboard", class_name="text-3xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Sales, book, and author insights.", class_name="text-gray-500 mt-1"
                ),
                class_name="flex-1",
            ),
            rx.el.nav(
                rx.link(
                    "Dashboard",
                    href="/",
                    class_name="text-sm font-medium text-gray-600 hover:text-blue-500",
                ),
                rx.link(
                    "Authors",
                    href="/authors",
                    class_name="text-sm font-medium text-gray-600 hover:text-blue-500",
                ),
                class_name="flex items-center gap-4",
            ),
        ),
        rx.el.div(
            stat_card(
                "book-open",
                "Total Books",
                DashboardState.stats["total_books"].to_string(),
            ),
            stat_card("trending-up", "YTD Sales", DashboardState.formatted_total_sales),
            stat_card(
                "dollar-sign", "Avg. Book Price", DashboardState.formatted_avg_price
            ),
            stat_card(
                "users",
                "Total Authors",
                DashboardState.stats["total_authors"].to_string(),
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-6",
        ),
        class_name="w-full",
    )