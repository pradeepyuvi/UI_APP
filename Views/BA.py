from flet import *
from flet import colors, dropdown
import requests
from base64 import b64encode
import urllib.parse
import os
import xmltodict


class BA(UserControl):

    def __init__(self, username: str, password: str):
        super().__init__()
        print(username, password)
        self.username = username
        self.password = password

    def clearAll(self, e):

        self.url = ""
        self.attributesvalue = ""
        self.extension = ".xml"
        self.radiobuttonsvalue = False
        self.mainText.current.color = colors.WHITE
        self.mainText.current.value = "Please Enter Attribute Value"
        self.attributes.current.value = ""
        self.attributes.current.focus()
        self.dropdown_ds.current.value = "Environment"
        self.radiobuttons.current.value = ""
        self.typeof.current.value = ""
        self.update()

    def updateTextHolder(self):
        self.mainText.current.value = self.url + self. attributesvalue
        self.update()

    def addError(self, val):
        self.errorText.current.value = val
        self.errorText.current.color = colors.RED
        self.attributes.current.focus()
        self.update()
        self.errorText.current.color = colors.WHITE
        self.errorText.current.value = ""

    def set_DEVandSIT(self, e):

        print(e.data)
        if (e.data == "SIT"):
            self.url = "https://rpt.dwh.sit2.ea.la.gov:8443/"
        else:
            self.url = "https://rpt.dwh.dev2.ea.la.gov:18443/"
        self.typeof.current.value = e.data + " -"
        self.updateTextHolder()

    def checkFileds(self):

        if (str(self.attributes.current.value) == ""):
            self.addError("Please Enter File Name")
            return True
        if (str(self.url) == ""):
            self.addError("Please Select Environment")
            return True
        if (not self.radiobuttonsvalue):
            self.addError("Please Select type of file to download")
            return True
        return False

    def set_Data_UrlWithAttribute(self, e):

        vals = self.attributes.current.value
        self.checkFileds()

        if (e.data == "Anlaysis"):
            self.  attributesvalue = "pentaho/plugin/data-access/api/datasource/analysis/catalog/{0}".format(
                self.attributes.current.value)
        elif (e.data == "DataSource"):
            self.  attributesvalue = "pentaho/plugin/data-access/api/datasource/metadata/{0}/download".format(
                self. attributes.current.value)
        elif (e.data == "Report"):
            self.attributesvalue = "pentaho/api/repo/files/{0}/download".format(
                urllib.parse.quote(self.attributes.current.value.encode('utf8')))
            self.extension = ".zip"
        self.radiobuttonsvalue = True
        self.updateTextHolder()

    def sendGetRequestAndDownloadFile(self, e):
        try:
            if (self.checkFileds()):
                return
            dis = os.getcwd()
            mainurl = self.url+self.attributesvalue
            mainurl = mainurl.strip()
            print(mainurl)
            s = requests.Session()
            s.verify = False
            usrpass = b64encode(
                bytes(f"{self.username}:{self.password}", 'utf-8'))
            usrpass = usrpass.decode("utf-8")
            headers = {'Authorization': f'Basic {usrpass}'}
            print(headers, "-->"+self.username)
            file_data = s.get(mainurl, headers=headers).content
            with open(urllib.parse.quote(self.attributes.current.value.encode('utf8'))+self.extension, "wb") as file:
                file.write(file_data)
            self.mainText.current.value = f"Downloaded {self.attributes.current.value.strip()+self.extension} succesfully at {dis}\\{self.attributes.current.value.strip()+self.extension} "
            self.mainText.current.color = colors.GREEN
            self.update()
        except Exception as e:
            self.errorText.current.value = "Downloaded Failed"
            self.errorText.current.color = colors.RED
            self.update()
            print(e)
            return

    def build(self):
        self.url = ""
        self.attributesvalue = ""
        self.extension = ".xml"
        self.radiobuttonsvalue = False
        self.mainText = Ref[Text]()
        self.typeof = Ref[Text]()
        self.errorText = Ref[Text]()
        self.attributes = Ref[TextField]()
        self.dropdown_ds = Ref[Dropdown]()
        self.radiobuttons = Ref[RadioGroup]()
        return Container(


            content=Column(
                controls=[
                    ElevatedButton(
                        "Clear", on_click=self.clearAll),
                    Column(
                        controls=[
                            Row(
                                controls=[
                                    TextField(label="File Name",
                                              ref=self.attributes,),
                                    Dropdown(
                                        label="Environment",
                                        options=[
                                            dropdown.Option(
                                                "DEV"),
                                            dropdown.Option(
                                                "SIT"),

                                        ],
                                        on_change=self.set_DEVandSIT, ref=self.dropdown_ds,
                                    )

                                ]
                            ),
                            Divider(height=20, thickness=0,
                                    color=colors.TRANSPARENT),
                            Text("What to Download",
                                 color=colors.WHITE, size=20),
                            Divider(height=10, thickness=0,
                                    color=colors.TRANSPARENT),
                            RadioGroup(
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
                                on_change=self.set_Data_UrlWithAttribute,
                                ref=self. radiobuttons,
                            ),

                            Divider(height=20, thickness=0,
                                    color=colors.TRANSPARENT),
                            Column(
                                controls=[
                                    Text(
                                        size=20,
                                        weight="w100",
                                        color=colors.WHITE,
                                        ref=self.typeof
                                    ),
                                    Container(
                                        content=Text(
                                            "Please Enter Attribute Value",
                                            size=20,
                                            weight="w100",
                                            color=colors.WHITE,
                                            ref=self.mainText
                                        ),
                                        padding=5,
                                    ),
                                    Container(
                                        content=Text(
                                            "",
                                            size=20,
                                            weight="w100",
                                            color=colors.RED,
                                            ref=self.errorText,
                                        ),
                                        padding=5,
                                    ),

                                ]
                            ),
                            ElevatedButton(
                                "Download", on_click=self.sendGetRequestAndDownloadFile)

                        ]
                    )
                ]
            ),
        )
