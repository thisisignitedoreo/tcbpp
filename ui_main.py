# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QProgressBar, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTableWidget, QTableWidgetItem,
    QTextEdit, QToolButton, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(766, 403)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.theme_layout = QHBoxLayout()
        self.theme_layout.setObjectName(u"theme_layout")
        self.icon = QLabel(Form)
        self.icon.setObjectName(u"icon")

        self.theme_layout.addWidget(self.icon)

        self.spacer_1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.theme_layout.addItem(self.spacer_1)

        self.light_checkbox = QRadioButton(Form)
        self.light_checkbox.setObjectName(u"light_checkbox")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.light_checkbox.sizePolicy().hasHeightForWidth())
        self.light_checkbox.setSizePolicy(sizePolicy)
        self.light_checkbox.setChecked(True)

        self.theme_layout.addWidget(self.light_checkbox)

        self.dark_checkbox = QRadioButton(Form)
        self.dark_checkbox.setObjectName(u"dark_checkbox")
        sizePolicy.setHeightForWidth(self.dark_checkbox.sizePolicy().hasHeightForWidth())
        self.dark_checkbox.setSizePolicy(sizePolicy)

        self.theme_layout.addWidget(self.dark_checkbox)

        self.spacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.theme_layout.addItem(self.spacer_2)

        self.about_button = QToolButton(Form)
        self.about_button.setObjectName(u"about_button")

        self.theme_layout.addWidget(self.about_button)


        self.verticalLayout_3.addLayout(self.theme_layout)

        self.main_layout = QHBoxLayout()
        self.main_layout.setObjectName(u"main_layout")
        self.settings_layout = QVBoxLayout()
        self.settings_layout.setObjectName(u"settings_layout")
        self.replay_layout = QHBoxLayout()
        self.replay_layout.setObjectName(u"replay_layout")
        self.replay_label = QLabel(Form)
        self.replay_label.setObjectName(u"replay_label")

        self.replay_layout.addWidget(self.replay_label)

        self.replay_lineedit = QLineEdit(Form)
        self.replay_lineedit.setObjectName(u"replay_lineedit")
        self.replay_lineedit.setReadOnly(True)

        self.replay_layout.addWidget(self.replay_lineedit)

        self.browse_button = QPushButton(Form)
        self.browse_button.setObjectName(u"browse_button")

        self.replay_layout.addWidget(self.browse_button)


        self.settings_layout.addLayout(self.replay_layout)

        self.clickpack_layout = QHBoxLayout()
        self.clickpack_layout.setObjectName(u"clickpack_layout")
        self.clickpack_label = QLabel(Form)
        self.clickpack_label.setObjectName(u"clickpack_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.clickpack_label.sizePolicy().hasHeightForWidth())
        self.clickpack_label.setSizePolicy(sizePolicy1)

        self.clickpack_layout.addWidget(self.clickpack_label)

        self.clickpack_combo = QComboBox(Form)
        self.clickpack_combo.setObjectName(u"clickpack_combo")

        self.clickpack_layout.addWidget(self.clickpack_combo)

        self.update_button = QToolButton(Form)
        self.update_button.setObjectName(u"update_button")

        self.clickpack_layout.addWidget(self.update_button)


        self.settings_layout.addLayout(self.clickpack_layout)

        self.fps_layout = QHBoxLayout()
        self.fps_layout.setObjectName(u"fps_layout")
        self.fps_label = QLabel(Form)
        self.fps_label.setObjectName(u"fps_label")

        self.fps_layout.addWidget(self.fps_label)

        self.fps_spinbox = QDoubleSpinBox(Form)
        self.fps_spinbox.setObjectName(u"fps_spinbox")
        self.fps_spinbox.setReadOnly(True)
        self.fps_spinbox.setMaximum(10000.000000000000000)
        self.fps_spinbox.setValue(60.000000000000000)

        self.fps_layout.addWidget(self.fps_spinbox)


        self.settings_layout.addLayout(self.fps_layout)

        self.hardclicks_layout = QHBoxLayout()
        self.hardclicks_layout.setObjectName(u"hardclicks_layout")
        self.hc_checkbox = QCheckBox(Form)
        self.hc_checkbox.setObjectName(u"hc_checkbox")
        self.hc_checkbox.setEnabled(True)
        self.hc_checkbox.setChecked(True)

        self.hardclicks_layout.addWidget(self.hc_checkbox)

        self.hc_spinbox = QSpinBox(Form)
        self.hc_spinbox.setObjectName(u"hc_spinbox")
        self.hc_spinbox.setEnabled(False)
        self.hc_spinbox.setMaximum(10000)
        self.hc_spinbox.setSingleStep(10)
        self.hc_spinbox.setValue(500)

        self.hardclicks_layout.addWidget(self.hc_spinbox)


        self.settings_layout.addLayout(self.hardclicks_layout)

        self.softclicks_layout = QHBoxLayout()
        self.softclicks_layout.setObjectName(u"softclicks_layout")
        self.sc_checkbox = QCheckBox(Form)
        self.sc_checkbox.setObjectName(u"sc_checkbox")
        self.sc_checkbox.setEnabled(True)
        self.sc_checkbox.setChecked(True)

        self.softclicks_layout.addWidget(self.sc_checkbox)

        self.sc_spinbox = QSpinBox(Form)
        self.sc_spinbox.setObjectName(u"sc_spinbox")
        self.sc_spinbox.setEnabled(False)
        self.sc_spinbox.setMaximum(10000)
        self.sc_spinbox.setSingleStep(10)
        self.sc_spinbox.setValue(200)

        self.softclicks_layout.addWidget(self.sc_spinbox)


        self.settings_layout.addLayout(self.softclicks_layout)

        self.enddelay_layout = QHBoxLayout()
        self.enddelay_layout.setObjectName(u"enddelay_layout")
        self.ed_label = QLabel(Form)
        self.ed_label.setObjectName(u"ed_label")

        self.enddelay_layout.addWidget(self.ed_label)

        self.ed_spinbox = QSpinBox(Form)
        self.ed_spinbox.setObjectName(u"ed_spinbox")
        self.ed_spinbox.setMinimum(1)
        self.ed_spinbox.setMaximum(10000)

        self.enddelay_layout.addWidget(self.ed_spinbox)


        self.settings_layout.addLayout(self.enddelay_layout)

        self.mp3_checkbox = QCheckBox(Form)
        self.mp3_checkbox.setObjectName(u"mp3_checkbox")

        self.settings_layout.addWidget(self.mp3_checkbox)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.settings_layout.addItem(self.spacer)

        self.render_button = QPushButton(Form)
        self.render_button.setObjectName(u"render_button")

        self.settings_layout.addWidget(self.render_button)

        self.progress_bar = QProgressBar(Form)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setMaximum(1)
        self.progress_bar.setValue(0)

        self.settings_layout.addWidget(self.progress_bar)


        self.main_layout.addLayout(self.settings_layout)

        self.replay_table = QTableWidget(Form)
        if (self.replay_table.columnCount() < 3):
            self.replay_table.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.replay_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.replay_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.replay_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.replay_table.setObjectName(u"replay_table")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.replay_table.sizePolicy().hasHeightForWidth())
        self.replay_table.setSizePolicy(sizePolicy2)

        self.main_layout.addWidget(self.replay_table)

        self.log_layout = QVBoxLayout()
        self.log_layout.setObjectName(u"log_layout")
        self.log_label = QLabel(Form)
        self.log_label.setObjectName(u"log_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.log_label.sizePolicy().hasHeightForWidth())
        self.log_label.setSizePolicy(sizePolicy3)
        self.log_label.setAlignment(Qt.AlignCenter)

        self.log_layout.addWidget(self.log_label)

        self.log = QTextEdit(Form)
        self.log.setObjectName(u"log")
        sizePolicy2.setHeightForWidth(self.log.sizePolicy().hasHeightForWidth())
        self.log.setSizePolicy(sizePolicy2)
        self.log.setLineWrapMode(QTextEdit.NoWrap)
        self.log.setReadOnly(True)
        self.log.setTextInteractionFlags(Qt.TextSelectableByKeyboard)

        self.log_layout.addWidget(self.log)


        self.main_layout.addLayout(self.log_layout)


        self.verticalLayout_3.addLayout(self.main_layout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"tcb++", None))
        self.icon.setText("")
        self.light_checkbox.setText(QCoreApplication.translate("Form", u"Light", None))
        self.dark_checkbox.setText(QCoreApplication.translate("Form", u"Dark", None))
        self.about_button.setText(QCoreApplication.translate("Form", u"?", None))
        self.replay_label.setText(QCoreApplication.translate("Form", u"Replay:", None))
        self.browse_button.setText(QCoreApplication.translate("Form", u"Browse", None))
        self.clickpack_label.setText(QCoreApplication.translate("Form", u"Clickpack:", None))
        self.update_button.setText(QCoreApplication.translate("Form", u"Update", None))
        self.fps_label.setText(QCoreApplication.translate("Form", u"FPS:", None))
        self.fps_spinbox.setSuffix(QCoreApplication.translate("Form", u" FPS", None))
        self.hc_checkbox.setText(QCoreApplication.translate("Form", u"Hardclicks", None))
        self.hc_spinbox.setSuffix(QCoreApplication.translate("Form", u" ms", None))
        self.hc_spinbox.setPrefix("")
        self.sc_checkbox.setText(QCoreApplication.translate("Form", u"Softclicks", None))
        self.sc_spinbox.setSuffix(QCoreApplication.translate("Form", u" ms", None))
        self.ed_label.setText(QCoreApplication.translate("Form", u"End delay:", None))
        self.ed_spinbox.setSuffix(QCoreApplication.translate("Form", u" seconds", None))
        self.mp3_checkbox.setText(QCoreApplication.translate("Form", u"Save as MP3 (compressed)", None))
        self.render_button.setText(QCoreApplication.translate("Form", u"Render!", None))
        ___qtablewidgetitem = self.replay_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Frame", None));
        ___qtablewidgetitem1 = self.replay_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"P1", None));
        ___qtablewidgetitem2 = self.replay_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"P2", None));
        self.log_label.setText(QCoreApplication.translate("Form", u"LOG", None))
    # retranslateUi

