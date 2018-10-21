import sys,random,os
from copy import deepcopy
import numpy as np
import pandas as pd
from pyecharts import Bar,Scatter,Line
from PyQt5 import QtCore, QtGui
#from PyQt5.QtWebKitWidgets import QWebViews
'''
some pyqt5 version only support QtWebKitWidgets, some only support QtWebEngineWidgets.
i dont know why. so just change the import when occur error.
'''
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton, QGridLayout, QLabel, QComboBox, QFrame, QVBoxLayout, QSlider, QGraphicsView

class TVL(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self)
        self.capitalLog = []
        self.luckyLog = []
        self.unluckyLog = []
        self.lucky = []
        self.unlucky = []
        self.capital = []
        self.sitex = []
        self.sitey = []
        self.talent = []
        self.displayTarget = ""
        self.epochs = 0
        self.displayGrand = 0
        self.outdir = "file:///"+os.getcwd().replace('\\','/')+"/data/"
        self.setWindowTitle('Talent vs Luck')
        self.setWindowIcon(QtGui.QIcon('title.ico'))
        self.resize(851, 535)
        self.setMinimumSize(851, 535)
        self.setMaximumSize(851, 535)
        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 191, 511))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.M_lab = QLabel("地图规模",self.gridLayoutWidget)
        self.M_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.M_lab, 0, 0, 1, 1)
        self.T_avg = QComboBox(self.gridLayoutWidget)
        for i in range(1,10):
            self.T_avg.addItem(str(i/10))
        self.gridLayout_2.addWidget(self.T_avg, 5, 1, 1, 1)
        self.avg_lab = QLabel("talent均值",self.gridLayoutWidget)
        self.avg_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.avg_lab, 5, 0, 1, 1)
        self.T_std = QComboBox(self.gridLayoutWidget)
        for i in range(1,10):
            self.T_std.addItem(str(i/10))
        self.gridLayout_2.addWidget(self.T_std, 6, 1, 1, 1)
        self.std_lab = QLabel("talent标准差",self.gridLayoutWidget)
        self.std_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.std_lab, 6, 0, 1, 1)
        self.grand_lab = QLabel("图表粒度",self.gridLayoutWidget)
        self.grand_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.grand_lab, 7, 0, 1, 1)
        self.grand = QComboBox(self.gridLayoutWidget)
        for i in range(1,5):
            self.grand.addItem(str(i*10))
        self.gridLayout_2.addWidget(self.grand, 7, 1, 1, 1)
        self.luck = QComboBox(self.gridLayoutWidget)
        for i in range(1,10):
            self.luck.addItem(str(i*100))
        self.gridLayout_2.addWidget(self.luck, 2, 1, 1, 1)
        self.step = QComboBox(self.gridLayoutWidget)
        for i in range(1,7):
            self.step.addItem(str(i*50))
        self.gridLayout_2.addWidget(self.step, 4, 1, 1, 1)
        self.map = QComboBox(self.gridLayoutWidget)
        for i in range(1,7):
            self.map.addItem(str(i*100)+"x"+str(i*100))
        self.gridLayout_2.addWidget(self.map, 0, 1, 1, 1)
        self.unluck = QComboBox(self.gridLayoutWidget)
        for i in range(1,10):
            self.unluck.addItem(str(i*100))
        self.gridLayout_2.addWidget(self.unluck, 3, 1, 1, 1)
        self.N_lab = QLabel("人数",self.gridLayoutWidget)
        self.N_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.N_lab, 1, 0, 1, 1)
        self.unluck_lab = QLabel("不幸事件",self.gridLayoutWidget)
        self.unluck_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.unluck_lab, 3, 0, 1, 1)
        self.luck_lab = QLabel("幸运事件",self.gridLayoutWidget)
        self.luck_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.luck_lab, 2, 0, 1, 1)
        self.s_lab = QLabel("迭代次数",self.gridLayoutWidget)
        self.s_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.s_lab, 4, 0, 1, 1)
        self.N = QComboBox(self.gridLayoutWidget)
        for i in range(1,7):
            self.N.addItem(str(i*500))
        self.gridLayout_2.addWidget(self.N, 1, 1, 1, 1)
        self.line = QFrame(self)
        self.line.setGeometry(QtCore.QRect(210, 10, 20, 511))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line_2 = QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(340, 10, 20, 511))
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(230, 10, 101, 511))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.start = QPushButton("Start",self.verticalLayoutWidget)
        self.verticalLayout_2.addWidget(self.start)
        self.TN = QPushButton("T-N",self.verticalLayoutWidget)
        self.verticalLayout_2.addWidget(self.TN)
        self.LN = QPushButton("L-N",self.verticalLayoutWidget)
        self.verticalLayout_2.addWidget(self.LN)
        self.CN = QPushButton("C-N",self.verticalLayoutWidget)
        self.verticalLayout_2.addWidget(self.CN)
        self.CT = QPushButton("C-T",self.verticalLayoutWidget)
        self.verticalLayout_2.addWidget(self.CT)
        self.TC = QPushButton("T-C",self.verticalLayoutWidget)
        self.verticalLayout_2.addWidget(self.TC)
        self.LC = QPushButton("L-C",self.verticalLayoutWidget)
        self.verticalLayout_2.addWidget(self.LC)
        self.CL = QPushButton("C-L",self.verticalLayoutWidget)
        self.verticalLayout_2.addWidget(self.CL)
        self.UC = QPushButton("U-C",self.verticalLayoutWidget)
        self.verticalLayout_2.addWidget(self.UC)
        self.CU = QPushButton("C-U",self.verticalLayoutWidget)
        self.verticalLayout_2.addWidget(self.CU)
        self.CmaxTime = QPushButton("Cmax-Time",self.verticalLayoutWidget)
        self.verticalLayout_2.addWidget(self.CmaxTime)
        self.CmaxEvent = QPushButton("Cmax-Event",self.verticalLayoutWidget)
        self.verticalLayout_2.addWidget(self.CmaxEvent)
        self.verticalLayoutWidget_2 = QWidget(self)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(360, 10, 471, 511))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.slider = QSlider(self.verticalLayoutWidget_2)
        self.slider.setMinimum(0)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.verticalLayout_3.addWidget(self.slider)
        self.screen = QWebEngineView(self.verticalLayoutWidget_2)
        self.verticalLayout_3.addWidget(self.screen)
        self.start.clicked.connect(self.startAction)
        self.TN.clicked.connect(self.TNAction)
        self.LN.clicked.connect(self.LNAction)
        self.CN.clicked.connect(self.CNAction)
        self.CT.clicked.connect(self.CTAction)
        self.TC.clicked.connect(self.TCAction)
        self.LC.clicked.connect(self.LCAction)
        self.CL.clicked.connect(self.CLAction)
        self.UC.clicked.connect(self.UCAction)
        self.CU.clicked.connect(self.CUAction)
        self.CmaxTime.clicked.connect(self.CmaxTimeAction)
        self.CmaxEvent.clicked.connect(self.CmaxEventAction)
        self.slider.valueChanged[int].connect(self.sliderAction)
        self.TN.setEnabled(False)
        self.LN.setEnabled(False)
        self.CN.setEnabled(False)
        self.CT.setEnabled(False)
        self.TC.setEnabled(False)
        self.LC.setEnabled(False)
        self.CL.setEnabled(False)
        self.UC.setEnabled(False)
        self.CU.setEnabled(False)
        self.CmaxTime.setEnabled(False)
        self.CmaxEvent.setEnabled(False)
        self.slider.setEnabled(False)
        self.screen.setHtml("please set configuration")

    def sliderAction(self,value):
        self.slider.setValue(value)
        if self.displayTarget=="TN":
            self.screen.load(QtCore.QUrl(self.outdir+"TN"+str((value+1)*10)+".html"))
        elif self.displayTarget=="LN":
            self.screen.load(QtCore.QUrl(self.outdir+"LN"+str(value)+".html"))
        elif self.displayTarget=="CN":
            self.screen.load(QtCore.QUrl(self.outdir+"CN"+str(value)+".html"))
        elif self.displayTarget=="CT":
            self.screen.load(QtCore.QUrl(self.outdir+"CT"+str(value)+".html"))
        elif self.displayTarget=="TC":
            self.screen.load(QtCore.QUrl(self.outdir+"TC"+str(value)+".html"))
        elif self.displayTarget=="LC":
            self.screen.load(QtCore.QUrl(self.outdir+"LC"+str(value)+".html"))
        elif self.displayTarget=="CL":
            self.screen.load(QtCore.QUrl(self.outdir+"CL"+str(value)+".html"))
        elif self.displayTarget=="UC":
            self.screen.load(QtCore.QUrl(self.outdir+"UC"+str(value)+".html"))
        elif self.displayTarget=="CU":
            self.screen.load(QtCore.QUrl(self.outdir+"CU"+str(value)+".html"))
        
    def renderBar(self,source,xname,yname,times,path):
        for i in range(times):
            index = pd.cut(source[i],bins=self.displayGrand).categories.values
            index = [round(i.mid,4) for i in index]
            bar = Bar(width=450,height=450,is_animation=False)
            bar.add(xname,index,pd.value_counts(source[i],bins=self.displayGrand,sort=False),xaxis_name=xname,yaxis_name=yname,is_legend_show=False,is_toolbox_show=False)
            bar.render("data/"+path+str(i)+".html")

    def renderScatter(self,xname,yname,ax,ay,times,path,op):
        for i in range(times):
            sc = Scatter(width=450,height=450,is_animation=False)
            if op==0:
                sc.add(xname,ax[i],ay[i],xaxis_name=xname,yaxis_name=yname,is_legend_show=False,is_toolbox_show=False)
            elif op==-1:
                sc.add(xname,ax[i],ay,xaxis_name=xname,yaxis_name=yname,is_legend_show=False,is_toolbox_show=False)
            else:
                sc.add(xname,ax,ay[i],xaxis_name=xname,yaxis_name=yname,is_legend_show=False,is_toolbox_show=False)
            sc.render("data/"+path+str(i)+".html")

    def startAction(self):
        #init
        self.capitalLog = []
        self.luckyLog = []
        self.unluckyLog = []
        mapsize = int(self.map.currentText()[:3])
        num = int(self.N.currentText())
        lucknum = int(self.luck.currentText())
        unlucknum = int(self.unluck.currentText())
        self.epochs = int(self.step.currentText())
        self.displayGrand = int(self.grand.currentText())
        std = float(self.T_std.currentText())
        avg = float(self.T_avg.currentText())
        self.talent = np.random.normal(avg, std, num)
        self.capital = [10]*num
        self.sitex = np.random.uniform(0,mapsize,num)
        self.sitey = np.random.uniform(0,mapsize,num)
        self.lucky = [0]*num
        self.unlucky = [0]*num
        self.capitalLog.append(deepcopy(self.capital))
        self.luckyLog.append(deepcopy(self.lucky))
        self.unluckyLog.append(deepcopy(self.unlucky))
        #simulate
        for i in range(self.epochs):
            goodx = np.random.uniform(0,mapsize,lucknum)
            goody = np.random.uniform(0,mapsize,lucknum)
            badx = np.random.uniform(0,mapsize,unlucknum)
            bady = np.random.uniform(0,mapsize,unlucknum)
            for j in range(num):
                for k in range(lucknum):
                    disx = abs(goodx[k]-self.sitex[j])
                    disy = abs(goody[k]-self.sitey[j])
                    if (disx<=2 or disx>=mapsize-1) and (disy<=2 or disy>=mapsize-1):
                        self.lucky[j]+=1
                        r = random.random()
                        if r<self.talent[j]:
                            self.capital[j]*=2
                for k in range(unlucknum):
                    disx = abs(badx[k]-self.sitex[j])
                    disy = abs(bady[k]-self.sitey[j])
                    if (disx<=2 or disx>=mapsize-1) and (disy<=2 or disy>=mapsize-1):
                        self.unlucky[j]+=1
                        self.capital[j]/=2
            self.capitalLog.append(deepcopy(self.capital))
            self.luckyLog.append(deepcopy(self.lucky))
            self.unluckyLog.append(deepcopy(self.unlucky))   
        if os.path.exists("./data")==False:
            os.mkdir("data") 
        #draw TN and Cmax
        for i in [10,20,30,40,50]:
            index = pd.cut(self.talent,bins=i).categories.values
            index = [round(i.mid,4) for i in index]
            bar = Bar(width=450,height=450,is_animation=False)
            bar.add("talent",index,pd.value_counts(self.talent,bins=i,sort=False),xaxis_name="talent",yaxis_name="individuals",is_legend_show=False,is_toolbox_show=False)
            bar.render("data/TN"+str(i)+".html")
        cmax = np.argmax(self.capital)
        ctime = [k[cmax] for k in self.capitalLog]
        cstep = list(range(self.epochs+1))
        line = Line(width=450,height=450,is_animation=False)
        line.add("captial",cstep,ctime,xaxis_name="time",yaxis_name="captial",is_legend_show=False,is_toolbox_show=False)
        line.render("data/CmaxTime.html")
        cevent = [0]
        for i in range(1,self.epochs+1):
            cevent.append((self.luckyLog[i][cmax]-self.luckyLog[i-1][cmax])-(self.unluckyLog[i][cmax]-self.unluckyLog[i-1][cmax]))
        line = Line(width=450,height=450,is_animation=False)
        line.add("event",cstep,cevent,xaxis_name="time",yaxis_name="event",is_legend_show=False,is_toolbox_show=False)
        line.render("data/CmaxEvent.html")
        #draw others
        self.renderBar(self.luckyLog,"lucky","individuals",self.epochs,"LN")
        self.renderBar(self.capitalLog,"captial","individuals",self.epochs,"CN")
        self.renderScatter("captial","talent",self.capitalLog,self.talent,self.epochs,"CT",-1)
        self.renderScatter("talent","captial",self.talent,self.capitalLog,self.epochs,"TC",1)
        self.renderScatter("lucky","captial",self.luckyLog,self.capitalLog,self.epochs,"LC",0)
        self.renderScatter("captial","lucky",self.capitalLog,self.luckyLog,self.epochs,"CL",0)
        self.renderScatter("unlucky","captial",self.unluckyLog,self.capitalLog,self.epochs,"UC",0)
        self.renderScatter("captial","unlucky",self.capitalLog,self.unluckyLog,self.epochs,"CU",0)
        self.TN.setEnabled(True)
        self.LN.setEnabled(True)
        self.CN.setEnabled(True)
        self.CT.setEnabled(True)
        self.TC.setEnabled(True)
        self.LC.setEnabled(True)
        self.CL.setEnabled(True)
        self.UC.setEnabled(True)
        self.CU.setEnabled(True)
        self.CmaxTime.setEnabled(True)
        self.CmaxEvent.setEnabled(True)
        self.screen.setHtml("finished")

    def displayInit(self,t,m,p):
        self.displayTarget = t
        self.slider.setEnabled(True)
        self.slider.setValue(0)
        self.slider.setMaximum(m)
        self.screen.load(QtCore.QUrl(self.outdir+p))
        
    def TNAction(self):
        self.displayInit("TN",4,"TN10.html")

    def LNAction(self):
        self.displayInit("LN",self.epochs,"LN0.html")

    def CNAction(self):
        self.displayInit("CN",self.epochs,"CN0.html")

    def CTAction(self):
        self.displayInit("CT",self.epochs,"CT0.html")

    def TCAction(self):
        self.displayInit("TC",self.epochs,"TC0.html")

    def LCAction(self):
        self.displayInit("LC",self.epochs,"LC0.html")
    
    def CLAction(self):
        self.displayInit("CL",self.epochs,"CL0.html")

    def UCAction(self):
        self.displayInit("UC",self.epochs,"UC0.html")

    def CUAction(self):
        self.displayInit("CU",self.epochs,"CU0.html")

    def CmaxTimeAction(self):
        self.slider.setEnabled(False)
        self.slider.setValue(0)
        self.screen.load(QtCore.QUrl(self.outdir+"CmaxTime.html"))

    def CmaxEventAction(self):
        self.slider.setEnabled(False)
        self.slider.setValue(0)
        self.screen.load(QtCore.QUrl(self.outdir+"CmaxEvent.html"))

app = QApplication(sys.argv)
qb = TVL()
qb.show()
sys.exit(app.exec_())