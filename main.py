from PySide6 import (
    QtWidgets,
    QtCore,
    QtGui,
)
from pydub import AudioSegment
from ui_main import Ui_Form
import random
import json
import sys
import os

if not os.path.isfile("settings.json"):
    open("settings.json", "w").write(
            json.dumps({
                    "theme": "white",
                })
        )

with open("settings.json") as settings:
    settings = json.load(settings)

class TCBPP(QtWidgets.QWidget):
    def __init__(self):
        super(TCBPP, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        app.setStyle("Fusion")

        self.white_palette = QtGui.QPalette()
        self.dark_palette = QtGui.QPalette()

        self.dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        self.dark_palette.setColor(QtGui.QPalette.WindowText, QtGui.Qt.white)
        self.dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
        self.dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        self.dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.Qt.white)
        self.dark_palette.setColor(QtGui.QPalette.ToolTipText, QtGui.Qt.white)
        self.dark_palette.setColor(QtGui.QPalette.Text, QtGui.Qt.white)
        self.dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        self.dark_palette.setColor(QtGui.QPalette.ButtonText, QtGui.Qt.white)
        self.dark_palette.setColor(QtGui.QPalette.BrightText, QtGui.Qt.red)
        self.dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
        self.dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
        self.dark_palette.setColor(QtGui.QPalette.HighlightedText, QtGui.Qt.black)
        
        match settings["theme"]:
            case "white":
                self.set_theme(False)
                self.ui.dark_checkbox.setChecked(False)
                self.ui.light_checkbox.setChecked(True)
            case "dark":
                self.set_theme(True)
                self.ui.dark_checkbox.setChecked(True)
                self.ui.light_checkbox.setChecked(False)
        
        if not os.path.isdir("clickpacks"):
            os.mkdir("clickpacks")
        
        self.clickpacks = os.listdir("clickpacks") if os.listdir("clickpacks") != [] else ["No clickpacks!"]
        self.ui.clickpack_combo.clear()
        self.ui.clickpack_combo.addItems(self.clickpacks)
        
        self.connect()
        app.setWindowIcon(QtGui.QIcon(self.get_qpix_from_filename("assets/tcb-col.png")))
        
        self.log_print("[INFO] Initialized")
        self.log_warn("Softclicks and Hardclicks not avaible yet")
    
    def connect(self) -> None:
        self.ui.dark_checkbox.clicked.connect(lambda: self.set_theme(True))
        self.ui.light_checkbox.clicked.connect(lambda: self.set_theme(False))
        self.ui.hc_checkbox.clicked.connect(lambda: self.ui.hc_spinbox.setEnabled(self.ui.hc_checkbox.isChecked()))
        self.ui.sc_checkbox.clicked.connect(lambda: self.ui.sc_spinbox.setEnabled(self.ui.sc_checkbox.isChecked()))
        self.ui.browse_button.clicked.connect(self.browse_replay)
        self.ui.render_button.clicked.connect(self.render_audio)
        self.ui.update_button.clicked.connect(self.fetch_clickpacks)
        self.ui.about_button.clicked.connect(self.about)
    
    def about(self) -> None:
        msg = QtWidgets.QMessageBox()
        msg.setText('Оригинальный TCB - TobyAdd\nTCB++ - acid (aka cosmo aka ignitedoreo)')
        msg.setWindowTitle("О TCB++")
        msg.exec()
    
    def fetch_clickpacks(self) -> None:
        self.clickpacks = os.listdir("clickpacks") if os.listdir("clickpacks") != [] else ["No clickpacks!"]
        self.ui.clickpack_combo.clear()
        self.ui.clickpack_combo.addItems(self.clickpacks)
    
    def set_theme(self, theme: bool) -> None:
        match theme:
            case False:
                app.setPalette(self.white_palette)
                app.setStyleSheet("")
                settings["theme"] = "white"
                self.ui.icon.setPixmap(self.get_qpix_from_filename("assets/tcb-bl-transp-2-1.png").scaled(64, 32, mode=QtCore.Qt.SmoothTransformation))
            case True:
                app.setPalette(self.dark_palette)
                app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
                settings["theme"] = "dark"
                self.ui.icon.setPixmap(self.get_qpix_from_filename("assets/tcb-col-transp-2-1.png").scaled(64, 32, mode=QtCore.Qt.SmoothTransformation))
        with open("settings.json", "w") as file:
            file.write(json.dumps(settings))
    
    def render_audio(self) -> None:  
        if self.clickpacks == ["No clickpacks!"]:
            self.log_error("No clickpacks!")
            return
        
        self.ui.progress_bar.setValue(0)
        ms_duration = ((float(self.ui.replay_table.item(self.ui.replay_table.rowCount() - 1, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
        output = AudioSegment.silent(duration=ms_duration + self.ui.ed_spinbox.value() * 1000)
        self.ui.progress_bar.setMaximum(self.ui.replay_table.rowCount())
        
        holds = os.listdir("clickpacks/" + self.ui.clickpack_combo.currentText() + "/holds")
        releases = os.listdir("clickpacks/" + self.ui.clickpack_combo.currentText() + "/releases")
        self.log_info(f"Rendering {self.ui.replay_table.rowCount()} actions")
        for i in range(self.ui.replay_table.rowCount()):
            self.ui.progress_bar.setValue(self.ui.progress_bar.value() + 1)
            if self.ui.replay_table.item(i, 1).text() == "Hold":
                output = output.overlay(AudioSegment.from_wav("clickpacks/" + self.ui.clickpack_combo.currentText() + "/holds/" + holds[random.randrange(len(holds))]), position=(int(self.ui.replay_table.item(i, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
            elif self.ui.replay_table.item(i, 1).text() == "Release":
                output = output.overlay(AudioSegment.from_wav("clickpacks/" + self.ui.clickpack_combo.currentText() + "/releases/" + releases[random.randrange(len(releases))]), position=(int(self.ui.replay_table.item(i, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
        
        out_path, ok = QtWidgets.QFileDialog.getSaveFileName(None, f"Save to... (default - 'rendered.{'mp3' if self.ui.mp3_checkbox.isChecked() else 'wav'}')", None, f"Audio ({'*.mp3' if self.ui.mp3_checkbox.isChecked() else '*.wav'})")
        if not ok:
            out_path = f"rendered.{'mp3' if self.ui.mp3_checkbox.isChecked() else 'wav'}"
            
        if self.ui.mp3_checkbox.isChecked():
            output.export(out_path, format="mp3", bitrate="320k")
        else:
            output.export(out_path, format="wav", bitrate="320k")
        self.log_info("Done!")
    
    def browse_replay(self) -> None:
        path, ok = QtWidgets.QFileDialog.getOpenFileName(None, "Select Replay...", None, "Supported Macros (*.txt *.echo *.json)")
        if path and ok:
            self.ui.replay_lineedit.setText(os.path.basename(path))
            if os.path.basename(path).split(".")[-1] == "echo":
                self.load_replay(path, 1)
            if os.path.basename(path).split(".")[-1] == "json":
                self.load_replay(path, 2)
            else:
                self.log_warn("Could not determine macro type. Defaulting to \"Plain Text\"")
                self.load_replay(path, 0)
                
            self.log_info("Replay loaded")
        else:
            self.log_error("Replay not loaded, something went wrong")
    
    def load_replay(self, path: str, macro_type: int) -> None:
        if macro_type == 0:
            replay_list = open(path).readlines()
            self.ui.fps_spinbox.setValue(float(replay_list[0].replace("\n", "")))

            self.ui.replay_table.setRowCount(len(replay_list) - 1)
            
            for k, i in list(enumerate(replay_list))[1:]:
                splited = i.split()
                self.ui.replay_table.setItem(k - 1, 0, QtWidgets.QTableWidgetItem(splited[0]))
                if splited[1] == "0":
                    self.ui.replay_table.setItem(k - 1, 1, QtWidgets.QTableWidgetItem("Release"))
                elif splited[1] == "1":
                    self.ui.replay_table.setItem(k - 1, 1, QtWidgets.QTableWidgetItem("Hold"))
                if splited[2] == "0":
                    self.ui.replay_table.setItem(k - 1, 2, QtWidgets.QTableWidgetItem("Release"))
                elif splited[2] == "1":
                    self.ui.replay_table.setItem(k - 1, 2, QtWidgets.QTableWidgetItem("Hold"))
            
            self.log_info("Successfully decoded \"Plain Text\" replay!")
        elif macro_type == 1:
            json_data = json.load(open(path))
            self.ui.fps_spinbox.setValue(json_data["FPS"])
            
            replay = self.convert([i["Hold"] for i in json_data["Echo Replay"]])
            
            self.ui.replay_table.setRowCount(len(replay) - 1)
            
            for k, i in enumerate(replay):
                self.ui.replay_table.setItem(k, 0, QtWidgets.QTableWidgetItem(str(i[0])))
                if i[1] == False:
                    self.ui.replay_table.setItem(k, 1, QtWidgets.QTableWidgetItem("Release"))
                elif i[1] == True:
                    self.ui.replay_table.setItem(k, 1, QtWidgets.QTableWidgetItem("Hold"))
            
            self.log_info("Successfully decoded \"EchoBot\" replay!")
        elif macro_type == 2:
            json_data = json.load(open(path))
            self.ui.fps_spinbox.setValue(json_data["fps"])
            
            replay = [[i["frame"], i["player_1"]["click"], i["player_2"]["click"]] for i in json_data["macro"]]
            
            self.ui.replay_table.setRowCount(len(replay) - 1)
            
            for k, i in enumerate(replay):
                self.ui.replay_table.setItem(k, 0, QtWidgets.QTableWidgetItem(str(i[0])))
                if i[1] == 0:
                    self.ui.replay_table.setItem(k, 1, QtWidgets.QTableWidgetItem("None"))
                elif i[1] == 1:
                    self.ui.replay_table.setItem(k, 1, QtWidgets.QTableWidgetItem("Release"))
                elif i[1] == 2:
                    self.ui.replay_table.setItem(k, 1, QtWidgets.QTableWidgetItem("Hold"))
                if i[2] == 0:
                    self.ui.replay_table.setItem(k, 2, QtWidgets.QTableWidgetItem("None"))
                elif i[2] == 1:
                    self.ui.replay_table.setItem(k, 2, QtWidgets.QTableWidgetItem("Release"))
                elif i[2] == 2:
                    self.ui.replay_table.setItem(k, 2, QtWidgets.QTableWidgetItem("Hold"))
            
            self.log_info("Successfully decoded \"TasBot\" replay!")
    
    def convert(self, array: list) -> list:
        old = array[0]
        res = [[0, old]]
        for k, i in enumerate(array):
            if i != old:
                res.append([k, i])
            old = i
        return res
    
    def log_info(self, text: str) -> None:
        self.ui.log.setPlainText(self.ui.log.toPlainText() + f"\n[INFO] {text}")
    
    def log_warn(self, text: str) -> None:
        self.ui.log.setPlainText(self.ui.log.toPlainText() + f"\n[WARNING] {text}")
    
    def log_error(self, text: str) -> None:
        self.ui.log.setPlainText(self.ui.log.toPlainText() + f"\n[ERROR] {text}")
    
    def log_debug(self, text: str) -> None:
        self.ui.log.setPlainText(self.ui.log.toPlainText() + f"\n[DEBUG] {text}")
    
    def log_print(self, text: str) -> None:
        self.ui.log.setPlainText(self.ui.log.toPlainText() + text)

    def get_qpix_from_filename(self, path):
        data_str = open(path, "rb").read()
        qpix = QtGui.QPixmap()
        qpix.loadFromData(data_str)
        return qpix


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = TCBPP()
    window.show()

    sys.exit(app.exec())
