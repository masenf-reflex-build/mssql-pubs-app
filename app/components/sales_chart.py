import reflex as rx
from app.states.dashboard_state import DashboardState


def sales_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Monthly Sales (Last 6 Months)",
            class_name="text-xl font-semibold text-gray-800",
        ),
        rx.el.div(
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(
                    vertical=False, class_name="stroke-gray-200"
                ),
                rx.recharts.graphing_tooltip(
                    cursor={"fill": "#f3f4f6"},
                    content_style={
                        "background": "white",
                        "border": "1px solid #e5e7eb",
                        "borderRadius": "0.75rem",
                    },
                ),
                rx.recharts.x_axis(
                    data_key="month",
                    tick_line=False,
                    axis_line=False,
                    class_name="text-xs font-medium text-gray-500",
                ),
                rx.recharts.y_axis(
                    tick_line=False,
                    axis_line=False,
                    class_name="text-xs font-medium text-gray-500",
                ),
                rx.recharts.bar(data_key="sales", fill="#3b82f6", radius=[4, 4, 0, 0]),
                data=DashboardState.sales_by_month,
                height=300,
                width="100%",
                margin={"top": 20, "right": 20, "left": -10, "bottom": 5},
            ),
            class_name="mt-4",
        ),
        class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
    )