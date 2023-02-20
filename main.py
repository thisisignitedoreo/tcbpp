from PySide6 import (
    QtWidgets,
    QtCore,
    QtGui,
)
from pydub import AudioSegment
from pyunpack import Archive
from ui_main import Ui_Form
import requests
import struct
import random
import shutil
import json
import sys
import os
import io

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
        
        if settings["theme"] == "white":
            self.set_theme(False)
            self.ui.dark_checkbox.setChecked(False)
            self.ui.light_checkbox.setChecked(True)
        elif settings["theme"] == "dark":
            self.set_theme(True)
            self.ui.dark_checkbox.setChecked(True)
            self.ui.light_checkbox.setChecked(False)
        
        if not os.path.isdir("clickpacks"):
            os.mkdir("clickpacks")
        
        self.clickpacks = os.listdir("clickpacks") if os.listdir("clickpacks") != [] else ["No clickpacks!"]
        self.ui.clickpack_combo.clear()
        self.ui.clickpack_combo.addItems(self.clickpacks)
        
        self.connect()
        app.setWindowIcon(QtGui.QIcon(":/assets/tcb-col.png"))

        if shutil.which("ffmpeg") is None:
            if os.name == "nt":
                ret = QtWidgets.QMessageBox.warning(self, "No FFMPEG found.", "No FFMPEG found. Do you want to download it?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
                if ret == QtWidgets.QMessageBox.Yes:
                    if not os.path.isdir("temp"):
                        os.mkdir("temp")

                    response = requests.get("https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z", stream=True)
                    total_length = response.headers.get('content-length')
                    ffmpeg = b""

                    if total_length is None:
                        ffmpeg += response.content
                    else:
                        dl = 0
                        total_length = int(total_length)
                        ffmpeg_progressbar = QtWidgets.QProgressDialog("Downloading FFMPEG", "Abort", 0, total_length)
                        ffmpeg_progressbar.canceled.connect(app.quit)
                        ffmpeg_progressbar.setModal(True)
                        ffmpeg_progressbar.show()
                        for data in response.iter_content(chunk_size=65536):
                            app.processEvents()
                            dl += len(data)
                            ffmpeg += data
                            ffmpeg_progressbar.setValue(dl)
                        ffmpeg_progressbar.hide()

                    open("temp/ffmpeg.7z", "wb").write(ffmpeg)

                    if not os.path.isdir("temp/ffmpeg"):
                        os.mkdir("temp/ffmpeg")

                    Archive("temp/ffmpeg.7z").extractall("temp/ffmpeg/")
                    shutil.copy(f"temp/ffmpeg/{os.listdir('temp/ffmpeg')[0]}/bin/ffmpeg.exe", "ffmpeg.exe")
                    shutil.copy(f"temp/ffmpeg/{os.listdir('temp/ffmpeg')[0]}/bin/ffplay.exe", "ffplay.exe")
                    shutil.copy(f"temp/ffmpeg/{os.listdir('temp/ffmpeg')[0]}/bin/ffprobe.exe", "ffprobe.exe")
                    
                    shutil.rmtree("temp")
            else:
                QtWidgets.QMessageBox.warning(self, "No FFMPEG found.", "No FFMPEG found. You have to install it yourself.", QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)                
        
        self.log_print("[INFO] Initialized")
    
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
        if theme == False:
            app.setPalette(self.white_palette)
            app.setStyleSheet("")
            settings["theme"] = "white"
            self.ui.icon.setPixmap(QtGui.QPixmap(":/assets/tcb-bl-transp-2-1.png").scaled(64, 32, mode=QtCore.Qt.SmoothTransformation))
        elif theme == True:
            app.setPalette(self.dark_palette)
            app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
            settings["theme"] = "dark"
            self.ui.icon.setPixmap(QtGui.QPixmap(":/assets/tcb-col-transp-2-1.png").scaled(64, 32, mode=QtCore.Qt.SmoothTransformation))
        
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
        
        p1_overrides_p2 = False

        holds_p1 = os.listdir("clickpacks/" + self.ui.clickpack_combo.currentText() + "/p1/holds")
        releases_p1 = os.listdir("clickpacks/" + self.ui.clickpack_combo.currentText() + "/p1/releases")
        try:
            holds_p2 = os.listdir("clickpacks/" + self.ui.clickpack_combo.currentText() + "/p2/holds")
            releases_p2 = os.listdir("clickpacks/" + self.ui.clickpack_combo.currentText() + "/p2/releases")
        except FileNotFoundError:
            self.log_warn("No player 2 found in clickpack! Defaulting to player 1 clicks.")
            p1_overrides_p2 = True
            holds_p2 = os.listdir("clickpacks/" + self.ui.clickpack_combo.currentText() + "/p1/holds")
            releases_p2 = os.listdir("clickpacks/" + self.ui.clickpack_combo.currentText() + "/p1/releases")
        try:
            softclicks = os.listdir("clickpacks/" + self.ui.clickpack_combo.currentText() + "/softclicks")
        except FileNotFoundError:
            self.log_warn("No softclicks found in clickpack! Turning it off.")
            self.ui.sc_checkbox.setChecked(False)
        try:
            hardclicks = os.listdir("clickpacks/" + self.ui.clickpack_combo.currentText() + "/hardclicks")
        except FileNotFoundError:
            self.log_warn("No hardclicks found in clickpack! Turning it off.")
            self.ui.hc_checkbox.setChecked(False)
        self.log_info(f"Rendering {self.ui.replay_table.rowCount()} actions")
        for i in range(self.ui.replay_table.rowCount()):
            if i == 0:
                delay = -1
            else:
                delay = ((int(self.ui.replay_table.item(i, 0).text()) / self.ui.fps_spinbox.value()) * 1000) - ((int(self.ui.replay_table.item(i - 1, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
            self.ui.progress_bar.setValue(self.ui.progress_bar.value() + 1)
            if delay <= self.ui.sc_spinbox.value() and self.ui.sc_checkbox.isChecked():
                if self.ui.replay_table.item(i, 1).text() == "Hold":
                    output = output.overlay(AudioSegment.from_wav("clickpacks/" + self.ui.clickpack_combo.currentText() + "/softclicks/" + softclicks[random.randrange(len(softclicks))]),
                                            position=(int(self.ui.replay_table.item(i, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
                elif self.ui.replay_table.item(i, 1).text() == "Release":
                    output = output.overlay(AudioSegment.from_wav("clickpacks/" + self.ui.clickpack_combo.currentText() + "/p1/releases/" + releases_p1[random.randrange(len(releases_p1))]),
                                            position=(int(self.ui.replay_table.item(i, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
                if self.ui.replay_table.item(i, 2).text() == "Hold":
                    output = output.overlay(AudioSegment.from_wav("clickpacks/" + self.ui.clickpack_combo.currentText() + "/softclicks/" + softclicks[random.randrange(len(softclicks))]),
                                            position=(int(self.ui.replay_table.item(i, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
                elif self.ui.replay_table.item(i, 2).text() == "Release":
                    output = output.overlay(AudioSegment.from_wav("clickpacks/" + self.ui.clickpack_combo.currentText() + f"/p{'1' if p1_overrides_p2 else '2'}/releases/" + releases_p2[random.randrange(len(releases_p2))]),
                                            position=(int(self.ui.replay_table.item(i, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
            elif delay >= self.ui.hc_spinbox.value() and self.ui.hc_checkbox.isChecked():
                if self.ui.replay_table.item(i, 1).text() == "Hold":
                    output = output.overlay(AudioSegment.from_wav("clickpacks/" + self.ui.clickpack_combo.currentText() + "/hardclicks/" + hardclicks[random.randrange(len(hardclicks))]),
                                            position=(int(self.ui.replay_table.item(i, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
                elif self.ui.replay_table.item(i, 1).text() == "Release":
                    output = output.overlay(AudioSegment.from_wav("clickpacks/" + self.ui.clickpack_combo.currentText() + "/p1/releases/" + releases_p1[random.randrange(len(releases_p1))]),
                                            position=(int(self.ui.replay_table.item(i, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
                if self.ui.replay_table.item(i, 2).text() == "Hold":
                    output = output.overlay(AudioSegment.from_wav("clickpacks/" + self.ui.clickpack_combo.currentText() + "/hardclicks/" + hardclicks[random.randrange(len(hardclicks))]),
                                            position=(int(self.ui.replay_table.item(i, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
                elif self.ui.replay_table.item(i, 2).text() == "Release":
                    output = output.overlay(AudioSegment.from_wav("clickpacks/" + self.ui.clickpack_combo.currentText() + f"/p{'1' if p1_overrides_p2 else '2'}/releases/" + releases_p2[random.randrange(len(releases_p2))]),
                                            position=(int(self.ui.replay_table.item(i, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
            else:
                if self.ui.replay_table.item(i, 1).text() == "Hold":
                    output = output.overlay(AudioSegment.from_wav("clickpacks/" + self.ui.clickpack_combo.currentText() + "/p1/holds/" + holds_p1[random.randrange(len(holds_p1))]),
                                            position=(int(self.ui.replay_table.item(i, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
                elif self.ui.replay_table.item(i, 1).text() == "Release":
                    output = output.overlay(AudioSegment.from_wav("clickpacks/" + self.ui.clickpack_combo.currentText() + "/p1/releases/" + releases_p1[random.randrange(len(releases_p1))]),
                                            position=(int(self.ui.replay_table.item(i, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
                if self.ui.replay_table.item(i, 2).text() == "Hold":
                    output = output.overlay(AudioSegment.from_wav("clickpacks/" + self.ui.clickpack_combo.currentText() + f"/p{'1' if p1_overrides_p2 else '2'}/holds/" + holds_p2[random.randrange(len(holds_p2))]),
                                            position=(int(self.ui.replay_table.item(i, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
                elif self.ui.replay_table.item(i, 2).text() == "Release":
                    output = output.overlay(AudioSegment.from_wav("clickpacks/" + self.ui.clickpack_combo.currentText() + f"/p{'1' if p1_overrides_p2 else '2'}/releases/" + releases_p2[random.randrange(len(releases_p2))]),
                                            position=(int(self.ui.replay_table.item(i, 0).text()) / self.ui.fps_spinbox.value()) * 1000)
        
        out_path, ok = QtWidgets.QFileDialog.getSaveFileName(None, f"Save to... (default - 'rendered.{'mp3' if self.ui.mp3_checkbox.isChecked() else 'wav'}')", None, f"Audio ({'*.mp3' if self.ui.mp3_checkbox.isChecked() else '*.wav'})")
        if not ok:
            out_path = f"rendered.{'mp3' if self.ui.mp3_checkbox.isChecked() else 'wav'}"
            
        if self.ui.mp3_checkbox.isChecked():
            output.export(out_path, format="mp3", bitrate="320k")
        else:
            output.export(out_path, format="wav", bitrate="320k")
        self.log_info("Done!")
    
    def browse_replay(self) -> None:
        path, ok = QtWidgets.QFileDialog.getOpenFileName(None, "Select Replay...", None, "Supported Macros (*.txt *.echo *.json *.replay)")
        if path and ok:
            self.ui.replay_lineedit.setText(os.path.basename(path))
            if os.path.basename(path).endswith(".echo"): 
                self.load_replay(path, 1)
            elif os.path.basename(path).endswith(".mcb.json"):
                self.load_replay(path, 4)
            elif os.path.basename(path).endswith(".json"):
                file = json.loads(open(path).read())
                if file.get("actions") is None:
                    self.load_replay(path, 2)
                else:
                    self.load_replay(path, 5)
            elif os.path.basename(path).endswith(".replay"):
                self.load_replay(path, 3)
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
                self.ui.replay_table.setItem(k, 2, QtWidgets.QTableWidgetItem(""))
            
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
        elif macro_type == 3:
            with open(path, "rb") as f:
                length = os.path.getsize(path)
                magic = f.read(4)
                if magic != b"RPLY":
                    self.log_error("This macro is either too old or corrupted")
                    return
            
                version = int.from_bytes(f.read(1), "big")
                frames = False
                if version == 2:
                    frames = int.from_bytes(f.read(1), "big") == 1
                
                if frames:
                    fps = struct.unpack("f", f.read(4))[0]
                    self.ui.fps_spinbox.setValue(fps)
                    
                    self.ui.replay_table.setRowCount((length - f.tell()) / 5)
                    
                    for k, i in enumerate(range(0, (length - f.tell()), 5)):
                        frame = int.from_bytes(f.read(4), "little")
                        state = int.from_bytes(f.read(1), "little")
                        p1 = not not state & 0x1
                        p2 = not not state >> 1
                        self.ui.replay_table.setItem(k, 0, QtWidgets.QTableWidgetItem(str(frame)))
                        self.ui.replay_table.setItem(k, 1, QtWidgets.QTableWidgetItem("Hold" if p1 else "Release"))
                        self.ui.replay_table.setItem(k, 2, QtWidgets.QTableWidgetItem("Hold" if p2 else "Release"))
                        
                else:
                    self.log_error("This macro is not recorded with frames")
                    return
            self.log_info("Successfully decoded \"ReplayBot\" replay!")
        elif macro_type == 4:
            json_data = json.load(open(path))
            self.ui.fps_spinbox.setValue(json_data["fps"])
            
            replay = [[i["frame"], i["press"], i["player2"]] for i in json_data["actions"]]
            
            self.ui.replay_table.setRowCount(len(replay) - 1)
            
            for k, i in enumerate(replay):
                self.ui.replay_table.setItem(k, 0, QtWidgets.QTableWidgetItem(str(i[0])))
                self.ui.replay_table.setItem(k, 1, QtWidgets.QTableWidgetItem("Release" if i[1] else "Hold"))
                self.ui.replay_table.setItem(k, 2, QtWidgets.QTableWidgetItem("Release" if i[2] else "Hold"))
            
            self.log_info("Successfully decoded \"MacroBot\" replay!")
        elif macro_type == 5:
            json_data = json.load(open(path))
            self.ui.fps_spinbox.setValue(json_data["fps"])
            
            replay = self.convert([i["down"] for i in json_data["actions"]])
            
            self.ui.replay_table.setRowCount(len(replay) - 1)
            
            for k, i in enumerate(replay):
                self.ui.replay_table.setItem(k, 0, QtWidgets.QTableWidgetItem(str(i[0])))
                if i[1] == False:
                    self.ui.replay_table.setItem(k, 1, QtWidgets.QTableWidgetItem("Release"))
                elif i[1] == True:
                    self.ui.replay_table.setItem(k, 1, QtWidgets.QTableWidgetItem("Hold"))
                self.ui.replay_table.setItem(k, 2, QtWidgets.QTableWidgetItem(""))
            
            self.log_info("Successfully decoded \"DashReplay\" replay!")
    
    
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = TCBPP()
    window.show()

    sys.exit(app.exec())
