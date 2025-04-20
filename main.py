import os
import sys

from PyQt6.QtWidgets import QApplication

import settings
from gui import MainWindow
from server.requests_handler import handler
from server.tcp_server import TCPServer


def main():
    # launch part
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    server = TCPServer(handler)
    server.start()

    # executing part
    exit_status = app.exec()

    # exit part
    server.stop()
    if settings.DELETE_FILTERS_PARAMS_ON_EXIT:
        try:
            os.remove(settings.FILTERS_PARAMS_PATH)
        except Exception:
            pass
    sys.exit(exit_status)


if __name__ == "__main__":
    main()
