import reflex as rx
from app.states.author_state import AuthorState


def authors_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.h1("Authors", class_name="text-3xl font-bold text-gray-900"),
            rx.el.div(
                rx.el.h2("Add New Author", class_name="text-xl font-semibold"),
                rx.el.form(
                    rx.el.div(
                        rx.el.input(
                            placeholder="First Name",
                            name="au_fname",
                            class_name="p-2 border rounded-md",
                        ),
                        rx.el.input(
                            placeholder="Last Name",
                            name="au_lname",
                            class_name="p-2 border rounded-md",
                        ),
                        rx.el.input(
                            placeholder="Phone (e.g., 415 555-1212)",
                            name="phone",
                            class_name="p-2 border rounded-md",
                        ),
                        rx.el.input(
                            placeholder="Address",
                            name="address",
                            class_name="p-2 border rounded-md",
                        ),
                        rx.el.input(
                            placeholder="City",
                            name="city",
                            class_name="p-2 border rounded-md",
                        ),
                        rx.el.input(
                            placeholder="State (2 chars)",
                            name="state",
                            class_name="p-2 border rounded-md",
                            max_length=2,
                        ),
                        rx.el.input(
                            placeholder="ZIP Code",
                            name="zip",
                            class_name="p-2 border rounded-md",
                        ),
                        rx.el.label(
                            rx.el.input(
                                type="checkbox", name="contract", class_name="mr-2"
                            ),
                            "Under Contract",
                        ),
                        rx.el.button(
                            "Add Author",
                            type="submit",
                            class_name="bg-blue-500 text-white p-2 rounded-md",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 items-end",
                    ),
                    on_submit=AuthorState.add_author,
                    reset_on_submit=True,
                    class_name="mt-4 p-4 border rounded-lg bg-white",
                ),
                class_name="my-8",
            ),
            rx.el.div(
                rx.el.h2("All Authors", class_name="text-xl font-semibold mb-4"),
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th("Name"),
                            rx.el.th("Location"),
                            rx.el.th("Phone"),
                            rx.el.th("Contract"),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            AuthorState.authors,
                            lambda author: rx.el.tr(
                                rx.el.td(
                                    rx.link(
                                        author["name"],
                                        href=f"/authors/{author['au_id']}",
                                        class_name="text-blue-600 hover:underline",
                                    )
                                ),
                                rx.el.td(f"{author['city']}, {author['state']}"),
                                rx.el.td(author["phone"]),
                                rx.el.td(rx.cond(author["contract"], "Yes", "No")),
                            ),
                        )
                    ),
                    class_name="w-full text-left table-auto",
                ),
                class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
            ),
            class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        class_name="font-['Raleway'] bg-gray-50 min-h-screen",
    )