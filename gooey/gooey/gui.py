import sys
import argparse
import asyncio
import stylesheet.qdarkstyle.pyqt5_style_rc
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt5.QtCore import QFile, QTextStream, Qt
from PyQt5.QtGui import QFontDatabase, QFont
from quamash import QEventLoop
from ui.widgets.mainwindow import CAND_MainWindow

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CAN-D Graphical User Interface GUI")

    parser.add_argument('-d', '--is-demo', action='store_true',
                        help='connect GUI to a CAN trace?')

    parser.add_argument('-t', '--trace-location',
                        help='location of the trace file in your directory')

    args = parser.parse_args()

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    # load font
    QFontDatabase.addApplicationFont(":/fonts/avenir.otf")
    font = QFont("Avenir Next LT Pro", 16)
    app.setFont(font)
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(
            Qt.AA_EnableHighDpiScaling, True)

    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(
            Qt.AA_UseHighDpiPixmaps, True)

    # set stylesheet
    f = QFile("stylesheet/qdarkstyle/style.qss")
    if not f.exists():
        print("Stylesheet not found.")
    else:
        f.open(QFile.ReadOnly | QFile.Text)
        ts = QTextStream(f)
        stylesheet = ts.readAll()
        app.setStyleSheet(stylesheet)

    cand = CAND_MainWindow(args.is_demo, args.trace_location)
    cand.showMaximized()

    with loop:
        loop.run_forever()
