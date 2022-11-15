import flet
from flet import *
from flet.control import MainAxisAlignment
from flet import colors, dropdown, padding, icons
import requests
from requests.auth import HTTPBasicAuth
import traceback
from base64 import b64encode
import urllib.parse
import os
import xmltodict


def main(page: Page):

    page.title = "ETL_Reports"
    print("Initial route:", page.route)

    username = TextField(label="UserName")
    password = TextField(label="Password", password=True)

    def showSanckBar(val: str, error: bool):

        snackbar = SnackBar(
            content=Text(value=f"{val}", color=colors.RED if error else colors.GREEN),)
        page.snack_bar = snackbar
        page.snack_bar.open = True
        page.update()

    def route_change(e):
        print("Route change:", e.route)
        page.views.clear()

        def login(e):
            if (username.value == ''):
                username.focus()
                return
            if (password.value == ''):
                password.focus()
                return
            page.go("home")

        page.views.append(
            View(
                "/",
                [Row(
                    controls=[

                        Column(
                            controls=[username,
                                      password,
                                      ElevatedButton(
                                          text="Login", on_click=login),
                                      ]
                        )

                    ],
                    alignment="center"
                )],
                appbar=AppBar(title=Text("Login")),
                # padding=padding.symmetric(horizontal=10),
                vertical_alignment="center",
            )
        )

        if (page.route == 'home'):

            page.views.append(
                View(
                    "/home",
                    [
                        ElevatedButton("BA", on_click=open_ba,
                                       width=200, height=50),
                        ElevatedButton("PDI", on_click=open_pdi,
                                       width=200, height=50)
                    ],
                    appbar=AppBar(title=Text(
                        f"Home  logined by {username.value}")),
                    vertical_alignment="center",
                    horizontal_alignment="center"
                )
            )

        if page.route == "BA":
            url = ""
            attributesvalue = ""
            extension = ".xml"
            radiobuttonsvalue = False
            typeof = Text(size=20,
                          weight="w100",
                          color=colors.WHITE)

            def clearAll(e):
                nonlocal url, attributesvalue, extension, radiobuttonsvalue
                url = ""
                attributesvalue = ""
                extension = ".xml"
                radiobuttonsvalue = False
                mainText.color = colors.WHITE
                mainText.value = "Please Enter Attribute Value"
                attributes.value = ""
                attributes.focus()
                dropdown_ds.value = "Environment"
                radiobuttons.value = ""
                typeof.value = ""
                page.update()

            def updateTextHolder():
                mainText.value = url + attributesvalue
                page.update()

            def addError(val):
                errorText.value = val
                errorText.color = colors.RED
                attributes.focus()
                page.update()
                errorText.color = colors.WHITE
                errorText.value = ""

            def set_DEVandSIT(e):
                nonlocal url
                print(e.data)
                if (e.data == "SIT"):
                    url = "https://rpt.dwh.sit2.ea.la.gov:8443/"
                else:
                    url = "https://rpt.dwh.dev2.ea.la.gov:18443/"
                typeof.value = e.data + " -"
                updateTextHolder()

            def checkFileds():
                nonlocal url, attributesvalue, extension, radiobuttonsvalue
                if (str(attributes.value) == ""):
                    addError("Please Enter File Name")
                    return True
                if (str(url) == ""):
                    addError("Please Select Environment")
                    return True
                if (not radiobuttonsvalue):
                    addError("Please Select type of file to download")
                    return True
                return False

            def set_Data_UrlWithAttribute(e):
                nonlocal url, attributesvalue, extension, radiobuttonsvalue
                vals = attributes.value
                checkFileds()

                if (e.data == "Anlaysis"):
                    attributesvalue = "pentaho/plugin/data-access/api/datasource/analysis/catalog/{0}".format(
                        attributes.value)
                elif (e.data == "DataSource"):
                    attributesvalue = "pentaho/plugin/data-access/api/datasource/metadata/{0}/download".format(
                        attributes.value)
                elif (e.data == "Report"):
                    attributesvalue = "pentaho/api/repo/files/{0}/download".format(
                        urllib.parse.quote(attributes.value.encode('utf8')))
                    extension = ".zip"
                radiobuttonsvalue = True
                updateTextHolder()

            def sendGetRequestAndDownloadFile(e):
                try:
                    if (checkFileds()):
                        return
                    dis = os.getcwd()
                    mainurl = url+attributesvalue
                    mainurl = mainurl.strip()
                    print(mainurl)
                    s = requests.Session()
                    s.verify = False
                    usrpass = b64encode(
                        bytes(f"{username.value}:{password.value}", 'utf-8'))
                    usrpass = usrpass.decode("utf-8")
                    headers = {'Authorization': f'Basic {usrpass}'}
                    print(headers)
                    file_data = s.get(mainurl, headers=headers).content
                    with open(urllib.parse.quote(attributes.value.encode('utf8'))+extension, "wb") as file:
                        file.write(file_data)
                    mainText.value = f"Downloaded {attributes.value.strip()+extension} succesfully at {dis}\\{attributes.value.strip()+extension} "
                    mainText.color = colors.GREEN
                    page.update()
                except Exception as e:
                    errorText.value = "Downloaded Failed"
                    errorText.color = colors.RED
                    page.update()
                    print(e)
                    return

            mainText = Text(
                "Please Enter Attribute Value",
                size=20,
                weight="w100",
                color=colors.WHITE
            )
            errorText = Text(
                "",
                size=20,
                weight="w100",
                color=colors.RED
            )
            attributes = TextField(label="File Name")
            dropdown_ds = Dropdown(
                label="Environment",
                options=[
                    dropdown.Option(
                        "DEV"),
                    dropdown.Option(
                        "SIT"),

                ],
                on_change=set_DEVandSIT
            )
            radiobuttons = RadioGroup(
                content=Row(
                    controls=[
                        Radio(
                            label="Anlaysis", value="Anlaysis"),
                        Radio(
                            label="DataSource", value="DataSource"),
                        Radio(
                            label="Report", value="Report"),
                    ]
                ),
                on_change=set_Data_UrlWithAttribute
            )

            page.views.append(
                View(
                    "/BA",

                    [
                        Container(
                            content=Column(
                                controls=[
                                    ElevatedButton(
                                        "Clear", on_click=clearAll),
                                    Column(
                                        controls=[
                                            Row(
                                                controls=[
                                                    attributes,
                                                    dropdown_ds
                                                ]
                                            ),
                                            Divider(height=20, thickness=0,
                                                    color=colors.TRANSPARENT),
                                            Text("What to Download",
                                                 color=colors.WHITE, size=20),
                                            Divider(height=10, thickness=0,
                                                    color=colors.TRANSPARENT),
                                            radiobuttons,
                                            Divider(height=20, thickness=0,
                                                    color=colors.TRANSPARENT),
                                            Column(
                                                controls=[
                                                    typeof,
                                                    Container(
                                                        content=mainText,
                                                        padding=5,
                                                    ),
                                                    Container(
                                                        content=errorText,
                                                        padding=5,
                                                    ),

                                                ]
                                            ),
                                            ElevatedButton(
                                                "Download", on_click=sendGetRequestAndDownloadFile)

                                        ]
                                    )
                                ]
                            ),
                        )
                    ],
                    appbar=AppBar(title=Text(
                        f"BA  logined by {username.value}"), actions=[IconButton(icon=icons.POWER_SETTINGS_NEW, on_click=lambda e:page.go("/"))]),

                    padding=padding.symmetric(horizontal=200),
                    vertical_alignment="center",

                )
            )
        if page.route == 'PDIHome':
            page.views.append(
                View(
                    "/PDIHome",
                    controls=[
                        Row(
                            controls=[
                                ElevatedButton(
                                    text="A", on_click=lambda e:page.go("PDI")),
                                ElevatedButton(text="B"),
                            ],
                            alignment='center'
                        ),
                    ],
                    horizontal_alignment="center",
                    vertical_alignment="center"
                )
            )

        if page.route == "PDI":
            sessionWithAuth = requests.session()
            url = ""
            typeof = ""
            fileNameTextField = TextField(label="File Name")
            mainText = Text(
                "",
                size=20,
                weight="w100",
                color=colors.WHITE
            )
            errorText = Text("", size=20, weight="w100", color=colors.RED)

            def updateTextHolder():
                mainText.value = url
                page.update()

            def set_Data_UrlWithAttribute(e):
                nonlocal url, typeof, fileNameTextField
                vals = fileNameTextField.value
                if (vals == ''):
                    errorText.value = "Please Enter File Name"
                    fileNameTextField.focus()
                    page.update()
                    return

                if (e.data == "Download"):
                    fileNameTextFieldValue = fileNameTextField.value.replace(
                        "/", ':')
                    url = "http://10.12.89.133:19080/pentaho/api/repo/files/:public:{0}.kjb/download".format(
                        fileNameTextFieldValue)
                elif (e.data == "Execute"):

                    url = "http://10.12.89.133:19080/pentaho/kettle/executeJob/?rep=pentaho-di&job=/public/{0}.kjb&level=INFO".format(
                        fileNameTextField.value)
                typeof = e.data
                errorText.value = ""
                updateTextHolder()

            radiobuttons = RadioGroup(
                content=Row(
                    controls=[
                        Radio(
                            label="Download", value="Download"),
                        Radio(
                            label="Execute", value="Execute"),
                    ]
                ),
                on_change=set_Data_UrlWithAttribute
            )

            def clearAll(e):
                nonlocal typeof, url
                fileNameTextField.value = ""
                radiobuttons.value = ""
                mainText.value = ""
                errorText.value = ""
                url = ""
                typeof = ""
                page.update()

            def downloadPdiFileOrExecute(e):
                nonlocal url, typeof

                if (fileNameTextField.value == ""):
                    fileNameTextField.focus()
                    errorText.value = "Please Enter File Name"
                    page.update()
                    return
                if (typeof == ""):
                    errorText.value = "Please Select type of Excution"
                    page.update()
                    return
                if (not "Authorization" in sessionWithAuth.headers.keys()):
                    sessionWithAuth.verify = False
                    usrpass = b64encode(
                        bytes(f"{username.value}:{password.value}", 'utf-8'))
                    usrpass = usrpass.decode("utf-8")
                    headers = {'Authorization': f'Basic {usrpass}'}
                    print(headers)
                    loginUrl = "http://10.12.89.133:19080/pentaho/home"
                    try:
                        result = sessionWithAuth.post(
                            loginUrl, headers=headers)
                        if result.status_code == 200:
                            print(sessionWithAuth.headers)
                    except Exception as ex:
                        showSanckBar(val=ex, error=True)
                try:
                    if (typeof == "Download"):
                        filename = fileNameTextField.value.replace(
                            "/", ':').replace(".kjb", "")
                        file_data = sessionWithAuth.get(url).content
                        with open(urllib.parse.quote(filename)+".zip", "wb") as file:
                            file.write(file_data)
                        mainText.value = f"Downloaded {filename}.zip succesfully at {os.getcwd()}\\{filename+'.zip'} "
                        mainText.color = colors.GREEN
                        page.update()
                    elif (typeof == 'Execute'):
                        result = sessionWithAuth.get(url).content
                        result = xmltodict.parse(result)
                        print(result)
                        jodid = result["webresult"]["id"]
                        mainText.value = f"Job Started Succefully id:{jodid}"
                        mainText.color = colors.GREEN
                        page.update()
                        
                except Exception as e:
                    errorText.value = e
                    page.update()

            page.views.append(
                View(
                    "/PDI",
                    [
                        Column(
                            controls=[
                                fileNameTextField,

                                radiobuttons,
                                Row(
                                    controls=[ElevatedButton(
                                        text="Clear", on_click=clearAll),
                                        ElevatedButton(
                                        text="Submit", on_click=downloadPdiFileOrExecute), ]
                                ),
                                mainText,
                                errorText
                            ]
                        )
                    ],
                    appbar=AppBar(title=Text(
                        f"PDI  logined by {username.value}"), actions=[IconButton(icon=icons.POWER_SETTINGS_NEW, on_click=lambda e:page.go("/"))]),
                    horizontal_alignment="center",
                    vertical_alignment="center",
                    padding=padding.symmetric(horizontal=200),
                )
            )

        page.horizontal_alignment = "center"
        page.update()

    def view_pop(e):
        print("View pop:", e.view)
        page.views.pop()
        top_view = page.views[len(page.views)-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    def open_ba(e):
        page.go("BA")

    def open_pdi(e):

        page.go("PDIHome")

    page.go(page.route)


flet.app(target=main)
# flet.app(target=main, view=flet.WEB_BROWSER)
