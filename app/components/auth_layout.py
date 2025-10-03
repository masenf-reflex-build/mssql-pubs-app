import reflex as rx
from reflex_azure_auth import AzureAuthState, azure_login_button


def auth_layout(page_content: rx.Component) -> rx.Component:
    """A layout that requires the user to be logged in."""
    return rx.el.div(
        rx.cond(
            AzureAuthState.is_hydrated,
            rx.cond(
                AzureAuthState.userinfo,
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                f"Welcome, {AzureAuthState.userinfo['name']}",
                                class_name="text-sm font-medium text-gray-600",
                            ),
                            rx.el.button(
                                "Logout",
                                on_click=AzureAuthState.redirect_to_logout,
                                class_name="text-sm font-medium text-blue-500 hover:text-blue-600",
                            ),
                            class_name="flex items-center gap-4",
                        ),
                        class_name="flex justify-end w-full p-2 bg-gray-100 border-b",
                    ),
                    page_content,
                    class_name="w-full",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Authentication Required",
                            class_name="text-2xl font-bold mb-4",
                        ),
                        rx.el.p(
                            "Please log in to access this page.", class_name="mb-8"
                        ),
                        azure_login_button(
                            rx.el.button(
                                "Log In with Microsoft",
                                class_name="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600",
                            )
                        ),
                        class_name="flex flex-col items-center justify-center p-8 bg-white rounded-2xl shadow-sm border",
                    ),
                    class_name="flex items-center justify-center min-h-screen bg-gray-50",
                ),
            ),
            rx.el.div(
                rx.icon(
                    tag="loader-circle", class_name="animate-spin size-12 text-blue-500"
                ),
                class_name="flex items-center justify-center min-h-screen",
            ),
        )
    )