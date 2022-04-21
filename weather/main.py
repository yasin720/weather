from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from request_timeout import Ui_Dialog
from geopy.geocoders import Nominatim
import sys
import requests
import ipinfo
import socket



class Ui_Form(object):
    def __init__(self, Form):
        # objects
        self.error = Ui_Dialog()
        self.dialog = QtWidgets.QDialog()
        # resize window
        Form.setObjectName("Form")
        Form.resize(420, 520)
        # set font
        font = QtGui.QFont()
        font_bigger = QtGui.QFont()
        font_bigger.setPointSize(14)
        font.setPointSize(10)
        # set layout
        self.layout = QtWidgets.QGridLayout()
        Form.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # add label image
        self.label_img = QtWidgets.QLabel(Form)
        # self.image = QtGui.QPixmap('icons\sun.png')
        # self.label_img.setPixmap(self.image)
        self.layout.addWidget(self.label_img, 0, 9, 1, 1)
        # add label
        self.label_1 = QtWidgets.QLabel(Form)
        self.label_1.setText('Locattion:')
        self.layout.addWidget(self.label_1, 1,0,1,1)
        self.label_1.setFont(font)
        # 2
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setText('Temp:')
        self.layout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_2.setFont(font)
        # 3
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setText('Humidity:')
        self.layout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_3.setFont(font)
        # 4
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setText('MAX Temp:')
        self.layout.addWidget(self.label_4, 4, 0, 1, 1)
        self.label_4.setFont(font)
#         5
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setText('MIN Temp:')
        self.layout.addWidget(self.label_5, 5, 0, 1, 1)
        self.label_5.setFont(font)
#         6
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setText('Pressure:')
        self.layout.addWidget(self.label_10, 6, 0, 1, 1)
        self.label_10.setFont(font)

#         add frame
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.layout.addWidget(self.line, 1, 1, 6, 1)
        self.line.show()
#         add lineEdit
        self.line_edit = QtWidgets.QLineEdit(Form)
        self.layout.addWidget(self.line_edit, 1, 2, 1, 1)
#         2
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setFont(font_bigger)
        self.layout.addWidget(self.label_6, 2, 2, 1, 1)
#         3
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setFont(font_bigger)
        self.layout.addWidget(self.label_7, 3, 2, 1, 1)
#         4
        self.label_8= QtWidgets.QLabel(Form)
        self.label_8.setFont(font_bigger)
        self.layout.addWidget(self.label_8, 4, 2, 1, 1)
#         5
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setFont(font_bigger)
        self.layout.addWidget(self.label_9, 5, 2, 1, 1)
        # 6
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setFont(font_bigger)
        self.layout.addWidget(self.label_11, 6, 2, 1, 1)
#         push buttons
        self.pushbutton = QtWidgets.QPushButton(Form)
        self.pushbutton.setText('Search')
        self.layout.addWidget(self.pushbutton, 1, 9, 1, 9)
#         check box
        self.checkbox = QtWidgets.QCheckBox(Form)
        self.checkbox.setText('Use Location')
        self.layout.addWidget(self.checkbox, 0, 0, 1, 1)
        # signals
        self.checkbox.stateChanged.connect(self.set_readonly_location)
        self.pushbutton.clicked.connect(self.find_location_name)
        self.pushbutton.clicked.connect(self.weather)
        self.pushbutton.clicked.connect(self.set_label)


    def set_readonly_location(self):
        if self.checkbox.isChecked():
            self.line_edit.clear()
            self.line_edit.setReadOnly(True)
            self.find_location_id()
        else:
            self.line_edit.setReadOnly(False)

    def weather(self):
        url = 'https://api.openweathermap.org/data/2.5/weather'
        if not self.checkbox.isChecked():
            city = self.line_edit.text().title()
            params = {'city':city, 'appid': 'ff828edb087ffc5215105153d6b6a89b', 'lat': self.lat_2, 'lon': self.lon_2}
        else:
            params = {'appid': 'ff828edb087ffc5215105153d6b6a89b', 'lat': self.lat, 'lon': self.lon}
        try:
            request_weather = requests.get(url=url, params=params)
            request_weather = request_weather.json()
            weather_mode = request_weather['weather']
            weather_main = request_weather['main']
            icon_code = weather_mode[0]['icon']
            image_url = f'http://openweathermap.org/img/wn/{icon_code}.png'
            self.load_icon_url(image_url)
            self.temp_list = [weather_main['temp'], weather_main['temp_min'],
                              weather_main['temp_max'], weather_main['pressure'], weather_main['humidity']]
        except:
            self.error.setupUi(self.dialog)
            self.dialog.show()


    def load_icon_url(self, img_url):
        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self.set_image_label)
        self.nam.get(QNetworkRequest(QtCore.QUrl(img_url)))

    def find_location_id(self):
        access_token = '02e296e662fad4'
        try:
            handler = ipinfo.getHandler(access_token)
            ip = self.find_ip()
            details = handler.getDetails(ip)
            locaction = details.loc
            list_loc = locaction.split(',')
            ok = True
        except:
            self.error.setupUi(self.dialog)
            self.dialog.show()
            ok = False
        if ok:
            self.lat = float(list_loc[0])
            self.lon = float(list_loc[1])

    def set_image_label(self, http_response):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(http_response.readAll())
        icon = QtGui.QPixmap(pixmap)
        self.label_img.setPixmap(icon)

    def set_label(self):
        try:
            self.label_6.setText(str(self.temp_list[0]-273))
            self.label_7.setText(str(self.temp_list[-1]))
            self.label_8.setText(str(self.temp_list[2]-273))
            self.label_9.setText(str(self.temp_list[1]-273))
            self.label_11.setText(str(self.temp_list[-2]))
        except:
            pass

    def find_ip(self):
        ip = requests.get('https://api.ipify.org').text
        return ip

    def find_location_name(self):
        geolocator = Nominatim(user_agent='yasin123456')
        city_name = self.line_edit.text().title()
        try:
            location = geolocator.geocode(city_name)
            self.lat_2 = location.latitude
            self.lon_2 = location.longitude
        except:
            self.lat_2 = None
            self.lon_2 = None




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    # form_file = QtWidgets.QMainWindow()
    ui = Ui_Form(Form)
    Form.show()
    sys.exit(app.exec_())