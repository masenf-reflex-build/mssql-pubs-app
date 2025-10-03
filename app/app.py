import reflex as rx
import reflex_enterprise as rxe
from reflex_azure_auth import register_auth_endpoints, AzureAuthState
from app.pages.dashboard import dashboard_page
from app.pages.authors import authors_page
from app.pages.author_detail import author_detail_page
from app.states.dashboard_state import DashboardState
from app.states.author_state import AuthorState
from app.states.author_detail_state import AuthorDetailState
from app.components.auth_layout import auth_layout

app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)


def index():
    return auth_layout(dashboard_page())


def authors():
    return auth_layout(authors_page())


def author_detail():
    return auth_layout(author_detail_page())


app.add_page(
    index,
    route="/",
    on_load=[AzureAuthState.check_if_iframed, DashboardState.get_dashboard_data],
)
app.add_page(
    authors,
    route="/authors",
    on_load=[AzureAuthState.check_if_iframed, AuthorState.get_all_authors],
)
app.add_page(
    author_detail,
    route="/authors/[au_id]",
    on_load=[AzureAuthState.check_if_iframed, AuthorDetailState.get_author_details],
)
register_auth_endpoints(app)