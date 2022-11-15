from urllib.parse import parse_qs, urlparse

import flet
from flet import *
from flet import colors, dropdown, icons, padding

from Views import home, BA, PDIdownandexc, PDIHome, PDI_DATA


class Main(UserControl):
    def __init__(self):
        super().__init__()
        self.username = Ref[TextField]()
        self.password = Ref[TextField]()

    def login(self, e):
        if (self.username.current.value == ''):
            self.username.focus()
            return
        if (self.password.current.value == ''):
            self.password.focus()
            return
        self.page.go("home", username=self.username.current.value,
                     password=self.password.current.value)

    def build(self):

        return Row(
            vertical_alignment='center',
            controls=[
                Column(

                    controls=[TextField(ref=self.username, label="UserName"),
                              TextField(ref=self.password, label="Password",
                                        password=True),
                              ElevatedButton(
                        text="Login", on_click=self.login),
                    ],
                ),

            ],
            alignment="center"
        )


def main(page: Page):
    page.title = "ToDo App"
    page.horizontal_alignment = "center"
    page.update()
    page.appbar = AppBar(title=Text("Ran"))

    isusernameandpasswordSetted = False
    # create application instance
    app = Main()

    # add application's root control to the page
    page.add(app)

    username = ""
    password = ""

    def logout(e):
        toppage = page.views[0]
        page.views.clear()
        page.views.append(toppage)
        page.update()

    def onRouteChange(e):
        nonlocal isusernameandpasswordSetted, username, password

        parserdurl = urlparse(e.data)
        parameters = parse_qs(parserdurl.query)

        print(f"Navigate to /{parserdurl.path} with parameter of {parameters}")

        if (not isusernameandpasswordSetted and 'username' in parameters and 'password' in parameters):
            username = parameters["username"][0]
            password = parameters["password"][0]
            isusernameandpasswordSetted = False

        if (parserdurl.path == "home"):

            page.views.append(View(
                "/home",
                [
                    home.Home(username, password)
                ],
                appbar=AppBar(title=Text(f"Home logined by {username}"),),
                vertical_alignment="center",
                horizontal_alignment="center"
            ))

        if (e.data == "BA"):
            print(username+"--->"+password)
            page.views.append(View(
                "/home",
                [
                    BA.BA(username=username, password=password)
                ],
                appbar=AppBar(title=Text(
                    f"BA  logined by {username}"), actions=[IconButton(icon=icons.POWER_SETTINGS_NEW, on_click=logout)]),
                horizontal_alignment="center",
                vertical_alignment="center",
                # padding=padding.symmetric(horizontal=200),
            ),)
        if page.route == 'PDIHome':
            page.views.append(
                View(
                    "/PDIHome",
                    controls=[
                        PDIHome.PDIHome()
                    ],
                    appbar=AppBar(title=Text(
                        f"PDI  logined by {username}"), actions=[IconButton(icon=icons.POWER_SETTINGS_NEW, on_click=logout)]),
                    horizontal_alignment="center",
                    vertical_alignment="center",
                    padding=padding.symmetric(horizontal=200),
                )
            )
        if page.route == "PDI":

            page.views.append(
                View(
                    "/PDI",
                    [
                        PDIdownandexc.PDIdownAndExcue(
                            username=username, password=password)
                    ],
                    appbar=AppBar(title=Text(
                        f"PDI  logined by {username}"), actions=[IconButton(icon=icons.POWER_SETTINGS_NEW, on_click=logout)]),
                    horizontal_alignment="center",
                    vertical_alignment="center",
                    padding=padding.symmetric(horizontal=200),
                )
            )

        if page.route == "PDI":
    
            page.views.append(
                View(
                    "/PDI",
                    [
                        PDI_DATA.PDI_DATA(
                            username=username, password=password)
                    ],
                    appbar=AppBar(title=Text(
                        f"PDI  logined by {username}"), actions=[IconButton(icon=icons.POWER_SETTINGS_NEW, on_click=logout)]),
                    horizontal_alignment="center",
                    vertical_alignment="center",
                    padding=padding.symmetric(horizontal=200),
                )
            )

        page.update()

    def onViewPop(e):
        page.views.pop()
        top_view = page.views[len(page.views)-1]
        page.go(top_view.route)
    page.on_route_change = onRouteChange
    page.on_view_pop = onViewPop


flet.app(target=main)
