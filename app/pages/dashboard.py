import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.header import header
from app.components.sales_chart import sales_chart
from app.components.tables import books_table, authors_table


def loading_skeleton() -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name="h-8 w-1/3 bg-gray-200 rounded-lg"),
        rx.el.div(class_name="h-4 w-1/4 bg-gray-200 rounded-lg mt-2"),
        rx.el.div(
            rx.foreach(
                [1, 2, 3, 4],
                lambda _: rx.el.div(class_name="h-24 bg-gray-200 rounded-2xl"),
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-6",
        ),
        rx.el.div(class_name="h-80 bg-gray-200 rounded-2xl mt-8"),
        rx.el.div(class_name="h-64 bg-gray-200 rounded-2xl mt-8"),
        rx.el.div(class_name="h-64 bg-gray-200 rounded-2xl mt-8"),
        class_name="animate-pulse w-full",
    )


def dashboard_content() -> rx.Component:
    return rx.el.div(
        header(),
        rx.el.div(sales_chart(), class_name="mt-8"),
        rx.el.div(
            books_table(),
            authors_table(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8",
        ),
        class_name="w-full",
    )


def dashboard_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.cond(DashboardState.is_loading, loading_skeleton(), dashboard_content()),
            class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        class_name="font-['Raleway'] bg-gray-50 min-h-screen",
    )