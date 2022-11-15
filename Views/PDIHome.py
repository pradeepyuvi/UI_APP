from flet import *


class PDIHome(UserControl):

    def __init__(self):
        super().__init__()

    def build(self):
        return Row(
            controls=[
                ElevatedButton(
                    text="Download and Excute", on_click=lambda e:self.page.go("PDI")),
                ElevatedButton(text="B"),
            ],

        )
