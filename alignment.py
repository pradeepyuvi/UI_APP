import flet
from flet import Container, Page, Row, Text, alignment, colors

def main(page: Page):
    page.title = "Containers - clickable and not"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    from flet import alignment

    container_1.alignment = alignment.center
    container_2.alignment = alignment.top_left
    container_3.alignment = alignment.Alignment(-0.5, -0.5)

flet.app(target=main)