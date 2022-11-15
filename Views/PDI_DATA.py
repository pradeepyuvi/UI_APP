from flet import *
from flet import colors, radio_group
import requests
import requests
from base64 import b64encode
import urllib.parse
import os
import xmltodict


class PDI_DATA(UserControl):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.sessionWithAuth = requests.session()
        self.url = ""
        self.typeof = ""
        self.fileNameTextField = Ref[TextField]()
        self.mainText = Ref[Text]()
        self.errorText = Ref[Text]()
        self.radiobuttons = Ref[RadioGroup]

    def updateTextHolder(self):
        self.mainText.current.value = self.url
        self.update()

    def set_Data_UrlWithAttribute(self, e):

        vals = self.fileNameTextField.current.value
        if (vals == ''):
            self.errorText.current.value = "Please Enter File Name"
            self.fileNameTextField.current.focus()
            self.update()
            return

        if (e.data == "Download"):
            self.fileNameTextFieldValue = self.fileNameTextField.current.value.replace(
                "/", ':')
            self. url = "http://10.12.89.133:19080/pentaho/api/repo/files/:public:{0}.kjb/download".format(
                self.fileNameTextFieldValue)
        elif (e.data == "Execute"):

            self.url = "http://10.12.89.133:19080/pentaho/kettle/executeJob/?rep=pentaho-di&job=/public/{0}.kjb&level=INFO".format(
                self.fileNameTextField.current.value)
        self.typeof = e.data
        self.errorText.current.value = ""
        self.updateTextHolder()

    def clearAll(self, e):

        self.fileNameTextField.current.value = ""
        self.radiobuttons.current.value = ""
        self.mainText.current.value = ""
        self.errorText.current.value = ""
        self.url = ""
        self.typeof = ""
        self.update()

    def downloadPdiFileOrExecute(self, e):

        if (self.fileNameTextField.current.value == ""):
            self.fileNameTextField.current.focus()
            self.errorText.current.value = "Please Enter File Name"
            self.update()
            return
        if (self.typeof == ""):
            self.errorText.current.value = "Please Select type of Excution"
            self.update()
            return
        if (not "Authorization" in self.sessionWithAuth.headers.keys()):
            self.sessionWithAuth.verify = False
            usrpass = b64encode(
                bytes(f"{self.username}:{self.password}", 'utf-8'))
            usrpass = usrpass.decode("utf-8")
            headers = {'Authorization': f'Basic {usrpass}'}
            print(headers)
            loginUrl = "http://10.12.89.133:19080/pentaho/home"
            try:
                result = self.sessionWithAuth.post(
                    loginUrl, headers=headers)
                if result.status_code == 200:
                    print(self.sessionWithAuth.headers)
            except Exception as ex:
                self.errorText.current.value = ex
                self.update()
                # self.showSanckBar(val=ex, error=True)
        try:
            if (self.typeof == "Download"):
                filename = self.fileNameTextField.current.value.replace(
                    "/", ':').replace(".kjb", "")
                file_data = self.sessionWithAuth.get(self.url).content
                with open(urllib.parse.quote(filename)+".zip", "wb") as file:
                    file.write(file_data)
                self.mainText.current.value = f"Downloaded {filename}.zip succesfully at {os.getcwd()}\\{filename+'.zip'} "
                self.mainText.current.color = colors.GREEN
                self.update()
            elif (self.typeof == 'Execute'):
                result = self.sessionWithAuth.get(self.url).content
                result = xmltodict.parse(result)
                print(result)
                jodid = result["webresult"]["id"]
                self.mainText.current.value = f"Job Started Succefully id-{jodid}"
                self.update()
        except Exception as e:
            self.errorText.current.value = e
            self.update()

    def build(self):
        return Column(
            controls=[
                ListView(),
                TextField(label="File Name", ref=self.fileNameTextField,),
                RadioGroup(
                    content=Row(
                        controls=[
                            Radio(
                                label="Download", value="Download"),
                            Radio(
                                label="Execute", value="Execute"),
                        ]
                    ),
                    on_change=self.set_Data_UrlWithAttribute,
                    ref=self. radiobuttons,
                ),
                Row(
                    controls=[ElevatedButton(
                        text="Clear", on_click=self.clearAll),
                        ElevatedButton(
                        text="Submit", on_click=self.downloadPdiFileOrExecute), ]
                ),
                Text(
                    ref=self.mainText,
                    value="",
                    size=20,
                    weight="w100",
                    color=colors.WHITE
                ),
                Text(value="", size=20, weight="w100",
                     color=colors.RED, ref=self.errorText)

            ]
        )
