from pathlib import Path

import dash_bootstrap_components as dbc
import dash_html_components as html

from .components.alerts import alerts
from .components.badges import badges
from .components.buttons.simple import buttons as buttons_simple
from .components.buttons.outline import buttons as buttons_outline
from .components.buttons.group import buttons as buttons_group
from .components.layout.simple import row as layout_simple
from .components.layout.width import row as layout_width
from .components.layout.order_offset import row as layout_order_offset
from .components.layout.breakpoints import row as layout_breakpoints
from .components.layout.no_gutters import row as layout_no_gutters

from .helpers import ExampleContainer, HighlightedSource, load_source_with_app
from .api_doc import ApiDoc
from .metadata import load_metadata
from .sidebar import Sidebar, SidebarEntry


HERE = Path(__file__).parent
COMPONENTS = HERE / "components"

GITHUB_LINK = "https://github.com/ASIDataScience/dash-bootstrap-components"

component_metadata = load_metadata()

alerts_source = (COMPONENTS / "alerts.py").open().read()
badges_source = (COMPONENTS / "badges.py").open().read()
collapse_source = (COMPONENTS / "collapse.py").open().read()
buttons_simple_source = (COMPONENTS / "buttons" / "simple.py").open().read()
buttons_usage_source = (COMPONENTS / "buttons" / "usage.py").open().read()
buttons_outline_source = (COMPONENTS / "buttons" / "outline.py").open().read()
buttons_group_source = (COMPONENTS / "buttons" / "group.py").open().read()
layout_simple_source = (COMPONENTS / "layout" / "simple.py").open().read()
layout_width_source = (COMPONENTS / "layout" / "width.py").open().read()
layout_order_offset_source = (
    (COMPONENTS / "layout" / "order_offset.py").open().read()
)
layout_breakpoints_source = (
    (COMPONENTS / "layout" / "breakpoints.py").open().read()
)
layout_no_gutters_source = (
    (COMPONENTS / "layout" / "no_gutters.py").open().read()
)

NAVBAR = dbc.Navbar(
    brand="Dash Bootstrap Components",
    brand_href="/",
    brand_external_link=True,
    sticky="top",
    children=[dbc.NavItem(dbc.NavLink("GitHub", href=GITHUB_LINK))],
)


sidebar_entries = [
    SidebarEntry("alerts", "Alerts"),
    SidebarEntry("badges", "Badges"),
    SidebarEntry("buttons", "Buttons"),
    SidebarEntry("collapse", "Collapse"),
    SidebarEntry("layout", "Layout"),
]


def component_page(body_elements, active_item):
    sidebar_contents = Sidebar(sidebar_entries, active_item)
    body_column = dbc.Col(body_elements, md=9)
    sidebar_column = dbc.Col(sidebar_contents, md=3, className="docs-sidebar")
    page_body = dbc.Container(
        dbc.Row([body_column, sidebar_column]), className="docs-content"
    )
    return [NAVBAR, page_body]


class ComponentsPage:
    def __init__(self, app):
        self._app = app
        self._component_bodies = {
            "alerts": [
                ExampleContainer(alerts),
                HighlightedSource(alerts_source),
                ApiDoc(component_metadata.get("src/components/Alert.js")),
            ],
            "badges": [
                ExampleContainer(badges),
                HighlightedSource(badges_source),
                ApiDoc(component_metadata.get("src/components/Badge.js")),
            ],
            "buttons": [
                ExampleContainer(buttons_simple),
                HighlightedSource(buttons_simple_source),
                ExampleContainer(
                    load_source_with_app(
                        self._app, buttons_usage_source, "button"
                    )
                ),
                HighlightedSource(buttons_usage_source),
                ExampleContainer(buttons_outline),
                HighlightedSource(buttons_outline_source),
                ExampleContainer(buttons_group),
                HighlightedSource(buttons_group_source),
                ApiDoc(component_metadata.get("src/components/Button.js")),
            ],
            "collapse": [
                ExampleContainer(
                    load_source_with_app(
                        self._app, collapse_source, "collapse"
                    )
                ),
                HighlightedSource(collapse_source),
                ApiDoc(component_metadata.get("src/components/Collapse.js")),
            ],
            "layout": html.Div(
                [
                    layout_simple,
                    HighlightedSource(layout_simple_source),
                    layout_width,
                    HighlightedSource(layout_width_source),
                    layout_order_offset,
                    HighlightedSource(layout_order_offset_source),
                    layout_breakpoints,
                    HighlightedSource(layout_breakpoints_source),
                    layout_no_gutters,
                    HighlightedSource(layout_no_gutters_source),
                ],
                className="layout-demo",
            ),
        }

    def for_path(self, path_components):
        try:
            component_name = path_components[0]
            component_body = self._component_bodies[component_name]
            return component_page(component_body, component_name)
        except IndexError:
            return self.for_path(["alerts"])