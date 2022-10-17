from re import U
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


conn = sqlite3.connect('handicapDatabase.db')
cur = conn.cursor()
#cur.execute("drop table handicapLog")
cur.execute('create table if not exists handicapLog (userName text, handicap text)')
cur.execute('create unique index if not exists idx_userName on handicapLog (userName)')



class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(544, 433)
        self.submitBtn = QtWidgets.QPushButton(Form, clicked = lambda: self.show_tool())
        self.submitBtn.setGeometry(QtCore.QRect(430, 370, 81, 41))
        self.submitBtn.setObjectName("submitBtn")
        self.userNameEntry = QtWidgets.QLineEdit(Form)
        self.userNameEntry.setGeometry(QtCore.QRect(270, 50, 131, 41))
        self.userNameEntry.setObjectName("userNameEntry")
        self.courseParEntry = QtWidgets.QLineEdit(Form)
        self.courseParEntry.setGeometry(QtCore.QRect(270, 220, 61, 41))
        self.courseParEntry.setObjectName("courseParEntry")
        self.courseSlopeEntry = QtWidgets.QLineEdit(Form)
        self.courseSlopeEntry.setGeometry(QtCore.QRect(270, 310, 61, 41))
        self.courseSlopeEntry.setObjectName("courseSlopeEntry")
        self.usernameLabel = QtWidgets.QLabel(Form)
        self.usernameLabel.setGeometry(QtCore.QRect(100, 60, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.usernameLabel.setFont(font)
        self.usernameLabel.setObjectName("usernameLabel")
        self.couseParLabel = QtWidgets.QLabel(Form)
        self.couseParLabel.setGeometry(QtCore.QRect(90, 210, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.couseParLabel.setFont(font)
        self.couseParLabel.setObjectName("couseParLabel")
        self.couseParDetailedLabel = QtWidgets.QLabel(Form)
        self.couseParDetailedLabel.setGeometry(QtCore.QRect(30, 250, 211, 21))
        self.couseParDetailedLabel.setObjectName("couseParDetailedLabel")
        self.courseSlopeLabel = QtWidgets.QLabel(Form)
        self.courseSlopeLabel.setGeometry(QtCore.QRect(80, 300, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.courseSlopeLabel.setFont(font)
        self.courseSlopeLabel.setObjectName("courseSlopeLabel")
        self.courseSlopeDetailedLabel = QtWidgets.QLabel(Form)
        self.courseSlopeDetailedLabel.setGeometry(QtCore.QRect(20, 340, 231, 21))
        self.courseSlopeDetailedLabel.setObjectName("courseSlopeDetailedLabel")
        self.playerScoreEntry = QtWidgets.QLineEdit(Form)
        self.playerScoreEntry.setGeometry(QtCore.QRect(270, 130, 61, 41))
        self.playerScoreEntry.setObjectName("playerScoreEntry")
        self.playerScore = QtWidgets.QLabel(Form)
        self.playerScore.setGeometry(QtCore.QRect(70, 120, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.playerScore.setFont(font)
        self.playerScore.setObjectName("playerScore")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)



    def show_tool(self):
            userName = self.userNameEntry.text()
            userScore = self.playerScoreEntry.text()
            handicap = ""
            coursePar = self.courseParEntry.text()
            courseSlope = self.courseSlopeEntry.text()

            try:
                if(isinstance(float(userScore), float) and isinstance(float(coursePar), float) and isinstance(float(courseSlope),float)):
                    handicap = (float(userScore) - float(coursePar))*113/float(courseSlope)
                    
                    cur.execute(f'select handicap from handicapLog where userName ="{userName}"')
                    result = cur.fetchone()
                    if result:
                        for row in cur.execute(f'select handicap from handicapLog where userName ="{userName}"'):
                            handicapAvg = row[0]
        
                        handicap = (float(handicapAvg) + float(handicap))/2
                        handicap = float(round(handicap,1))
                        #cur.execute("insert or replace into handicapLog (userName, handicap) values ((select userName from handicapLog where userName = userName), handicap)")
                        
                    else:
                        handicap = float(round(handicap,1))

                else:
                    flogMsg = QMessageBox()
                    flogMsg.setWindowTitle("hanidcapTool")
                    flogMsg.setText(f"somehthing went wrong recheck your values")
                    q = flogMsg.exec_()
                    print(userScore)
            except ValueError:
                print(ValueError)
                flagMsg = QMessageBox()
                flagMsg.setWindowTitle("hanidcapTool")
                flagMsg.setText(f"somehthing went wrong recheck your values")
                q = flagMsg.exec_()


            cur.execute("replace into handicapLog values (?,?)", (userName, handicap))
            conn.commit()
            msg = QMessageBox()
            msg.setWindowTitle("hanidcapTool")
            msg.setText(f"{userName} your handicap is {handicap}")
            x = msg.exec_()



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "handicap tracker"))
        self.submitBtn.setText(_translate("Form", "submit"))
        self.usernameLabel.setText(_translate("Form", "UserName"))
        self.couseParLabel.setText(_translate("Form", "Course Par"))
        self.couseParDetailedLabel.setText(_translate("Form", "typically between 34-36 for 9 70-23 for 18"))
        self.courseSlopeLabel.setText(_translate("Form", "course slope"))
        self.courseSlopeDetailedLabel.setText(_translate("Form", "Range from 55 to 155 average is 113 to 130"))
        self.playerScore.setText(_translate("Form", "Strokes This Round"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
