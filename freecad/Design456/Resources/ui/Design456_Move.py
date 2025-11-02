# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Design456_Move.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dlgDesign456_Move(object):
    def setupUi(self, dlgDesign456_Move):
        dlgDesign456_Move.setObjectName("dlgDesign456_Move")
        dlgDesign456_Move.resize(443, 368)
        dlgDesign456_Move.setWindowOpacity(23.0)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlgDesign456_Move)
        self.buttonBox.setGeometry(QtCore.QRect(270, 340, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.dialX = QtWidgets.QDial(dlgDesign456_Move)
        self.dialX.setGeometry(QtCore.QRect(10, 20, 161, 151))
        self.dialX.setMaximum(360)
        self.dialX.setPageStep(5)
        self.dialX.setOrientation(QtCore.Qt.Vertical)
        self.dialX.setInvertedAppearance(True)
        self.dialX.setInvertedControls(False)
        self.dialX.setWrapping(True)
        self.dialX.setNotchesVisible(True)
        self.dialX.setObjectName("dialX")
        self.DialY = QtWidgets.QDial(dlgDesign456_Move)
        self.DialY.setGeometry(QtCore.QRect(240, 20, 161, 151))
        self.DialY.setMaximum(360)
        self.DialY.setPageStep(5)
        self.DialY.setOrientation(QtCore.Qt.Vertical)
        self.DialY.setInvertedAppearance(True)
        self.DialY.setInvertedControls(False)
        self.DialY.setWrapping(True)
        self.DialY.setNotchesVisible(True)
        self.DialY.setObjectName("DialY")
        self.DialZ = QtWidgets.QDial(dlgDesign456_Move)
        self.DialZ.setGeometry(QtCore.QRect(110, 170, 161, 151))
        self.DialZ.setMaximum(360)
        self.DialZ.setPageStep(5)
        self.DialZ.setOrientation(QtCore.Qt.Vertical)
        self.DialZ.setInvertedAppearance(True)
        self.DialZ.setInvertedControls(False)
        self.DialZ.setWrapping(True)
        self.DialZ.setNotchesVisible(True)
        self.DialZ.setObjectName("DialZ")
        self.lblX = QtWidgets.QLabel(dlgDesign456_Move)
        self.lblX.setGeometry(QtCore.QRect(60, 0, 54, 17))
        self.lblX.setObjectName("lblX")
        self.lblY = QtWidgets.QLabel(dlgDesign456_Move)
        self.lblY.setGeometry(QtCore.QRect(290, 0, 54, 17))
        self.lblY.setObjectName("lblY")
        self.lblZ = QtWidgets.QLabel(dlgDesign456_Move)
        self.lblZ.setGeometry(QtCore.QRect(160, 150, 54, 17))
        self.lblZ.setObjectName("lblZ")
        self.lblValueX = QtWidgets.QLabel(dlgDesign456_Move)
        self.lblValueX.setGeometry(QtCore.QRect(60, 180, 54, 17))
        self.lblValueX.setAlignment(QtCore.Qt.AlignCenter)
        self.lblValueX.setObjectName("lblValueX")
        self.lblValueY = QtWidgets.QLabel(dlgDesign456_Move)
        self.lblValueY.setGeometry(QtCore.QRect(290, 180, 54, 17))
        self.lblValueY.setAlignment(QtCore.Qt.AlignCenter)
        self.lblValueY.setObjectName("lblValueY")
        self.lblValueZ = QtWidgets.QLabel(dlgDesign456_Move)
        self.lblValueZ.setGeometry(QtCore.QRect(160, 320, 54, 17))
        self.lblValueZ.setAlignment(QtCore.Qt.AlignCenter)
        self.lblValueZ.setObjectName("lblValueZ")

        self.retranslateUi(dlgDesign456_Move)
        self.buttonBox.accepted.connect(dlgDesign456_Move.accept)
        self.buttonBox.rejected.connect(dlgDesign456_Move.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgDesign456_Move)

    def retranslateUi(self, dlgDesign456_Move):
        _translate = QtCore.QCoreApplication.translate
        dlgDesign456_Move.setWindowTitle(_translate("dlgDesign456_Move", "Design456 Move"))
        self.lblX.setText(_translate("dlgDesign456_Move", "X: Angle"))
        self.lblY.setText(_translate("dlgDesign456_Move", "Y: Angle"))
        self.lblZ.setText(_translate("dlgDesign456_Move", "Z: Angle"))
        self.lblValueX.setText(_translate("dlgDesign456_Move", "0"))
        self.lblValueY.setText(_translate("dlgDesign456_Move", "0"))
        self.lblValueZ.setText(_translate("dlgDesign456_Move", "0"))
