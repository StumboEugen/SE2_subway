import codecs
import json
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QWidget)


def findID(name, subway):
    for station in subway:
        if station["stationName"] == name:
            return station["stationID"]
    return "Notfind"

def findLine(ID, subway):
    for line in subway:
        if line["lineID"] == ID:
            temp = list()
            temp.append(line["lineColor"])
            temp.append(line["lineStationID"])
            return temp
    raise Exception("没有找到匹配的线路")

def findIDpos(ID,subway):
    for station in subway:
        if station["stationID"] == ID:
            return station["stationPos"]
    raise Exception("没有找到匹配的站坐标")

def findIDnext(ID,subway):
    for station in subway:
        if station["stationID"] == ID:
            return  station["nextStationID"]
    raise Exception("没有找到匹配的相邻站")

def findIDname(ID,subway):
    for station in subway:
        if station["stationID"] == ID:
            return station["stationName"]
    raise Exception("没有找到匹配的站名")

def findStationinPos(x,y,subway):
    for station in subway:
        Pos = station["stationPos"]
        xp = float(Pos['posX'])
        yp = float(Pos['posY'])
        if x-xp<=5 and x-xp>=-5 and y - yp <=5 and y - yp>=-5:
            return station["stationName"]
    return "..."


def findroutecolor(name1,name2,subway):
    name = name1+"-"+name2
    n = len(subway)
    for i in range (n):
        if subway[i]["routeName"] == name:
            return subway[i]["routeColor"]
    name = name2 + "-" + name1
    for i in range (n):
        if subway[i]["routeName"] == name:
            return subway[i]["routeColor"]
    raise Exception("没有找到匹配的线路")

def findroute(begin, end):
    # 读入地铁内容文件
    subway_str = codecs.open('MetroData_SH.json', encoding="utf-8").read()
    subway = json.loads(subway_str)
    stations = subway['station']

    # 判断是不是字符串
    if type(begin) == str:
        print("你输入了站名\n")
        begin = findID(begin, stations)
        end = findID(end, stations)
        if begin == "Notfind" or end == "Notfind":
            return "站名错误"
    else:
        return "站名错误"

    # 初始化队列
    movefrom = [-1] * len(stations)  # 存储上一个节点是哪里
    movefrom[begin] = begin
    queue = [begin]  # 查找的队列,广度搜索
    route = [end]  # 最后的结果路径

    while movefrom[end] == -1:  # 还没有找到路径时(终点前一个站点还没有找到)
        process_node = queue.pop(0)  # 队列中取出当前处理的站点
        tempset = set(stations[process_node]["nextStationID"])  # 去重,数据中存在重复
        for nextnode in tempset:  # 当前站点的相邻节点
            if movefrom[nextnode] == -1:  # 如果是-1, 说明还没有遍历到
                queue.append(nextnode)  # 入队
                movefrom[nextnode] = process_node  # 记录是从哪个节点找到的

    # 填充结果
    while True:
        if movefrom[route[-1]] == begin:
            route.append(begin)
            break
        route.append(movefrom[route[-1]])

    # print对应的站名
    #for n in route:
        #print(stations[n]["stationName"])

    # 返回倒序的路径点,按ID

    return list(reversed(route))

class Widget(QWidget):

    def __init__(self, parent=None):
        #findroute("剑川路", "马当路")
        self.subway_str = codecs.open('MetroData_SH.json', encoding="utf-8").read()
        self.subway = json.loads(self.subway_str)
        self.stations = self.subway['station']
        self.line = self.subway['line']
        self.route = self.subway['route']
        _translate = QtCore.QCoreApplication.translate
        super(Widget, self).__init__(parent)
        self.pic_gray = 0
        self.pic_line = 0
        self.count = 0
        self.temp_count = 0
        self.mousefind = 0
        self.mousex = 0
        self.mousey = 0
        self.drawroute = 0

        self.text = ""
        self.stationName = ""
        self.resize(1200, 700)
        #self.move(100, 100)
        self.setWindowTitle("上海市地铁路线查询软件")
        #按钮1
        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setGeometry(QtCore.QRect(1050, 30, 133, 28))
        self.button1.setStyleSheet("*{\n""background-color:white;\n""border: 1px solid gray;\n""}")
        self.button1.setObjectName("pushButton")
        self.button1.setText(_translate("", "地铁线查询"))
        #按钮2
        self.button2 = QtWidgets.QPushButton(self)
        self.button2.setGeometry(QtCore.QRect(1060, 70, 83, 61))
        self.button2.setStyleSheet("*{\n""background-color:white;\n""border: 1px solid gray;\n""}")
        self.button2.setObjectName("pushButton_2")

        self.button3 = QtWidgets.QPushButton(self)
        self.button3.setGeometry(QtCore.QRect(1150, 70, 33, 61))
        self.button3.setStyleSheet("*{\n""background-color:white;\n""border: 1px solid gray;\n""}")
        self.button3.setObjectName("pushButton_2")

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(900, 30, 141, 28))
        self.comboBox.setObjectName("comboBox")
        for i in range(1,15):
            self.comboBox.addItem("")

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(952, 70, 101, 25))
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(952, 106, 101, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(900, 74, 51, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(900, 110, 51, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(900, 140, 300, 30))
        self.label_3.setObjectName("label_2")

        self.comboBox.setItemText(0, _translate("MainWindow", "一号线"))
        self.comboBox.setItemText(1, _translate("MainWindow", "二号线"))
        self.comboBox.setItemText(2, _translate("MainWindow", "三号线"))
        self.comboBox.setItemText(3, _translate("MainWindow", "四号线"))
        self.comboBox.setItemText(4, _translate("MainWindow", "五号线"))
        self.comboBox.setItemText(5, _translate("MainWindow", "六号线"))
        self.comboBox.setItemText(6, _translate("MainWindow", "七号线"))
        self.comboBox.setItemText(7, _translate("MainWindow", "八号线"))
        self.comboBox.setItemText(8, _translate("MainWindow", "九号线"))
        self.comboBox.setItemText(9, _translate("MainWindow", "十号线"))
        self.comboBox.setItemText(10, _translate("MainWindow", "十一号线"))
        self.comboBox.setItemText(11, _translate("MainWindow", "十二号线"))
        self.comboBox.setItemText(12, _translate("MainWindow", "十三号线"))
        self.comboBox.setItemText(13, _translate("MainWindow", "十六号线"))

        self.button2.setText(_translate("MainWindow", "起终站查询"))
        self.button3.setText(_translate("MainWindow", "复\n原"))
        self.label.setText(_translate("MainWindow", "起点站"))
        self.label_2.setText(_translate("MainWindow", "终点站"))
        self.label_3.setText(_translate("MainWindow", "------------途径站点列表-------------"))
        self.setMouseTracking(True)

        self.button1.clicked.connect(self.button1click)
        self.button2.clicked.connect(self.button2click)
        self.button3.clicked.connect(self.button3click)

    def paintEvent(self,event):
        text = self.text
        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        #背景画布
        painter.setPen(Qt.gray)
        painter.drawRect(30, 30, 830, 650)
        painter.drawRect(900, 170, 290, 510)
        painter.setBrush(Qt.white)
        painter.drawRect(30, 30, 830, 650)
        painter.drawRect(900, 170, 290, 510)
        # 画地图
        for i in range(1,14):
            self.drawSubLine(i, painter,0)
        self.drawSubLine(16, painter,0)
        if self.pic_line != 0:
            self.drawSubLine(self.pic_line, painter,1)
        #画查询路线
        if self.drawroute ==1:
            self.drawRoute(painter,self.route_draw)
        for st in self.stations:
            st = st["stationPos"]
            st_x = 170 + float(st['posX'])
            st_y = 40 + float(st['posY'])
            st_x = st_x * 0.65
            st_y = st_y * 0.75
            pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
            painter.setPen(pen)
            painter.drawEllipse(st_x, st_y, 4, 4)
            painter.setBrush(Qt.white)
            painter.drawEllipse(st_x, st_y, 4, 4)
        #画上方提示
        painter.setPen(Qt.black)
        painter.drawText(30,25, text)

        #画鼠标旁提示
        if self.mousefind ==1:
            painter.setBrush(Qt.white)
            painter.drawRect(self.mousex+17, self.mousey, len(self.stationName)*16, 20)
            painter.setPen(Qt.black)
            painter.drawText(self.mousex+17, self.mousey+15, self.stationName)



    def drawSubLine(self,Line_ID,painter,k):
        line_information = findLine(Line_ID, self.line)
        line_color = line_information[0]
        line_color = line_color.replace('#','')
        c1 = line_color[0]+line_color[1]
        c2 = line_color[2]+line_color[3]
        c3 = line_color[4]+line_color[5]
        c1 = int(c1, 16)
        c2 = int(c2, 16)
        c3 = int(c3, 16)
        line_station_ID = line_information[1]
        n = len(line_station_ID)
        for i in range(n):
            #获得当前站坐标
            Pos1 = findIDpos(line_station_ID[i], self.stations)
            x1 = 170 + float(Pos1['posX'])
            y1 = 40 + float(Pos1['posY'])
            x1 = x1*0.65
            y1 = y1*0.75
            points = findIDnext(line_station_ID[i],self.stations)
            for point in points:
                if point in line_station_ID:
                    Pos2 = findIDpos(point, self.stations)
                    x2 = 170 + float(Pos2['posX'])
                    y2 = 40 + float(Pos2['posY'])
                    x2 = x2 * 0.65
                    y2 = y2 * 0.75
                    pen = QtGui.QPen(QColor(c1, c2, c3), 3, QtCore.Qt.SolidLine)
                    if self.pic_gray == 1 and k == 0:
                        pen = QtGui.QPen(QColor(220, 220, 220), 3, QtCore.Qt.SolidLine)
                    painter.setPen(pen)
                    painter.drawLine(x1,y1,x2,y2)
            # Pos1 = findIDpos(line_station_ID[i], self.stations)
            # x1 = 170 + float(Pos1['posX'])
            # y1 = 40 + float(Pos1['posY'])
            # x1 = x1 * 0.65
            # y1 = y1 * 0.75
            pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
            painter.setPen(pen)
            painter.drawEllipse(x1,y1,4,4)
            #if i == n-1:
              #  painter.drawEllipse(x2, y2,4,4)
            painter.setBrush(Qt.white)
            painter.drawEllipse(x1, y1, 4, 4)
            #if i == n-1:
            #    painter.drawEllipse(x2, y2,4,4)
            if k==1:
                painter.setPen(Qt.black)
                sta_name = findIDname(line_station_ID[i], self.stations)
                if len(sta_name) > 6:
                    sta_2 = sta_name[5:]
                    sta_name = sta_name[0:5]
                    if self.count + self.temp_count <24:
                        painter.drawText(910, 185 + (self.count + self.temp_count) * 20, "{0}.".format(self.count) + sta_name)
                        self.temp_count = self.temp_count + 1
                        if self.count <10:
                            space = "  "
                        else:
                            space = "   "
                        painter.drawText(910, 185 + (self.count + self.temp_count) * 20, space+ sta_2)
                    else:
                        if self.count <10:
                            space = "  "
                        else:
                            space = "   "
                        painter.drawText(1050, 185 + (self.count + self.temp_count- 24) * 20, "{0}.".format(self.count) + sta_name)
                        self.temp_count = self.temp_count + 1
                        painter.drawText(1050, 185 + (self.count + self.temp_count-24) * 20, space+ sta_2)
                else:
                    if self.count + self.temp_count < 24:
                        painter.drawText(910, 185 + (self.count + self.temp_count) * 20, "{0}.".format(self.count) + sta_name)
                    else:
                        painter.drawText(1050, 185 + (self.count+ self.temp_count-24) * 20,"{0}.".format(self.count) + sta_name)
                self.count = self.count+1
        self.count = 0
        self.temp_count =0
        str = "{0}号线".format(Line_ID)
        if Line_ID == 16:
            Line_ID = 14
            str = "16号线"
        pen = QtGui.QPen(QColor(c1, c2, c3), 4, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.drawText(790, 40+15*Line_ID, str)
        painter.drawLine(740,40+15*Line_ID,780,40+15*Line_ID)

    def drawRoute(self,painter,route):
        n= len(route)
        for i in range(n):
            if i <= n-2:
                sta_name_draw = findIDname(route[i],self.stations)
                sta_pos_draw = findIDpos(route[i],self.stations)
                x1 = 170 + float(sta_pos_draw['posX'])
                x1 =x1*0.65
                y1 = 40 + float(sta_pos_draw['posY'])
                y1 = y1*0.75
                sta_name_draw2 = findIDname(route[i+1],self.stations)
                sta_pos_draw2 = findIDpos(route[i+1], self.stations)
                x2 = 170 + float(sta_pos_draw2['posX'])
                x2 = x2*0.65
                y2 = 40 + float(sta_pos_draw2['posY'])
                y2 = y2*0.75
                line_color = findroutecolor(sta_name_draw,sta_name_draw2,self.route)
                line_color = line_color.replace('#', '')
                c1 = line_color[0] + line_color[1]
                c2 = line_color[2] + line_color[3]
                c3 = line_color[4] + line_color[5]
                c1 = int(c1, 16)
                c2 = int(c2, 16)
                c3 = int(c3, 16)
                pen = QtGui.QPen(QColor(c1, c2, c3), 3, QtCore.Qt.SolidLine)
                painter.setPen(pen)
                painter.drawLine(x1, y1, x2, y2)
            else:
                sta_name_draw = findIDname(route[i], self.stations)
                sta_pos_draw = findIDpos(route[i], self.stations)
                x1 = 170 + float(sta_pos_draw['posX'])
                y1 = 40 + float(sta_pos_draw['posY'])
            painter.setPen(Qt.black)
            if len(sta_name_draw) > 6:
                sta_draw_2 = sta_name_draw[6:]
                sta_name_draw = sta_name_draw[1:6]
                if self.count + self.temp_count < 24:
                    painter.drawText(910, 185 + (self.count + self.temp_count) * 20,
                                     "{0}.".format(self.count) + sta_name_draw)
                    self.temp_count = self.temp_count + 1
                    if self.count < 10:
                        space = "  "
                    else:
                        space = "   "
                    painter.drawText(910, 185 + (self.count + self.temp_count) * 20, space + sta_draw_2)
                else:
                    if self.count < 10:
                        space = "  "
                    else:
                        space = "   "
                    painter.drawText(1050, 185 + (self.count + self.temp_count - 24) * 20,
                                     "{0}.".format(self.count) + sta_name_draw)
                    self.temp_count = self.temp_count + 1
                    painter.drawText(1050, 185 + (self.count + self.temp_count - 24) * 20, space + sta_draw_2)
            else:
                if self.count + self.temp_count < 24:
                    painter.drawText(910, 185 + (self.count + self.temp_count) * 20,
                                     "{0}.".format(self.count) + sta_name_draw)
                else:
                    painter.drawText(1050, 185 + (self.count + self.temp_count - 24) * 20,
                                     "{0}.".format(self.count) + sta_name_draw)
            self.count = self.count + 1
        self.count = 0
        self.temp_count = 0

    def button1click(self):
        self.pic_line = self.comboBox.currentIndex()+1
        if self.pic_line == 14:
            self.pic_line =16
        self.pic_gray =1
        self.drawroute =0
        self.update()

    def button2click(self):
        route = findroute(self.lineEdit.text(),self.lineEdit_2.text())
        if route == "站名错误":
            print("站名错误")
            reply = QtWidgets.QMessageBox.question(self, '警告', '地铁站名输入错误', QtWidgets.QMessageBox.Ok )
        else:
            self.route_draw = route
            self.pic_line = 0
            self.pic_gray = 1
            self.drawroute = 1

        self.update()

    def button3click(self):
        self.pic_line =0
        self.pic_gray =0
        self.drawroute =0
        self.update()

    def mouseMoveEvent(self, event):
        xFind = event.pos().x()/0.65-170
        yFind = event.pos().y()/0.75-40
        self.stationName = findStationinPos(xFind,yFind,self.stations)
        self.mousex = event.pos().x()
        self.mousey = event.pos().y()
        if self.stationName == "...":
            self.mousefind = 0
        else:
            self.mousefind = 1
        self.text = "x坐标：({0}) ，y坐标：({1}）".format(event.pos().x(),event.pos().y())
        self.text = self.text + "   地铁站："+self.stationName
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Widget()
    form.show()
    app.exec_()
