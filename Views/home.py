from flet import (UserControl, ElevatedButton, Column)


class Home(UserControl):
    def __init__(self, username, password):
        super().__init__()
        print(username+"-->"+password)
        self.username = username
        self.password = password

    def build(self):
        return Column(
            controls=[
                ElevatedButton("BA", on_click=self.open_ba,
                               width=200, height=50),
                ElevatedButton("PDI", on_click=self.open_pdi,
                               width=200, height=50)
            ],
        )

    def open_ba(self, e):
        self.page.go("BA")

    def open_pdi(self, e):

        self.page.go("PDIHome")
