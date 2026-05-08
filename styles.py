def get_stylesheet():
    return """
        QWidget {
            background-color: #1e1e1e;
            color: #cccccc;
            font-family: 'Segoe UI', 'Inter', 'Roboto', sans-serif;
            font-size: 13px;
        }

        QLabel#Title {
            font-size: 22px;
            font-weight: 600;
            color: #ffffff;
        }

        QLabel#HeroTitle {
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
        }

        QLabel#StatusLabel {
            font-size: 14px;
            font-family: 'Consolas', monospace;
            color: #4EC9B0;
        }

        QFrame#Panel {
            background-color: #252526;
            border: 1px solid #333333;
            border-radius: 6px;
        }

        QLineEdit, QSpinBox {
            background-color: #3c3c3c;
            border: 1px solid #444444;
            border-radius: 4px;
            padding: 6px 10px;
            color: #ffffff;
        }

        QLineEdit:focus, QSpinBox:focus {
            border: 1px solid #007acc;
            background-color: #464646;
        }

        QPushButton {
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: 600;
        }

        QPushButton#PrimaryBtn {
            background-color: #0e639c;
            color: #ffffff;
        }
        QPushButton#PrimaryBtn:hover {
            background-color: #1177bb;
        }

        QPushButton#DangerBtn {
            background-color: #c53929;
            color: #ffffff;
        }
        QPushButton#DangerBtn:hover {
            background-color: #d84636;
        }

        QPushButton#MenuBtn {
            background-color: #0e639c;
            color: #ffffff;
            text-align: left;
            padding: 14px 18px;
        }
        QPushButton#MenuBtn:hover {
            background-color: #1177bb;
        }

        QTableWidget {
            background-color: #1e1e1e;
            alternate-background-color: #252526;
            border: 1px solid #333333;
            border-radius: 6px;
            outline: none;
        }

        QHeaderView::section {
            background-color: #2d2d30;
            color: #ffffff;
            padding: 8px;
            border: none;
            border-bottom: 1px solid #333333;
            font-weight: 600;
            text-align: left;
        }

        QTableWidget::item {
            padding: 4px 8px;
            border-bottom: 1px solid #2d2d30;
        }
    """
