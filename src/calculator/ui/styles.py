DARK_THEME_STYLE = """
QMainWindow {
    background-color: #121214;
}

QWidget {
    color: #e2e8f0;
    font-family: "Segoe UI", -apple-system, Roboto, Helvetica, Arial, sans-serif;
    font-size: 13px;
}

QGroupBox {
    border: 1px solid #2a2a30;
    border-radius: 4px;
    margin-top: 12px;
    padding-top: 16px;
    background-color: #18181c;
    font-weight: bold;
    color: #94a3b8;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 8px;
    padding: 0 4px;
}

QLineEdit {
    background-color: #202024;
    border: 1px solid #2a2a30;
    border-radius: 4px;
    padding: 6px 10px;
    color: #e2e8f0;
}

QLineEdit:focus {
    border: 1px solid #4f46e5;
    background-color: #22222a;
}

QLineEdit:disabled {
    background-color: #151518;
    color: #64748b;
    border: 1px solid #1a1a20;
}

QPushButton {
    background-color: #25252b;
    border: 1px solid #2a2a30;
    border-radius: 4px;
    padding: 6px 12px;
    color: #e2e8f0;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2d2d35;
    border-color: #3f3f46;
}

QPushButton:pressed {
    background-color: #1a1a20;
}

QPushButton:disabled {
    background-color: #151518;
    color: #64748b;
    border-color: #1a1a20;
}

QPushButton#calculateButton {
    background-color: #4f46e5;
    border: 1px solid #4338ca;
}

QPushButton#calculateButton:hover {
    background-color: #6366f1;
}

QPushButton#calculateButton:pressed {
    background-color: #3730a3;
}

QTabWidget::pane {
    border: 1px solid #2a2a30;
    background-color: #18181c;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #121214;
    border: 1px solid #2a2a30;
    border-bottom: none;
    padding: 8px 16px;
    color: #94a3b8;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}

QTabBar::tab:hover {
    background-color: #18181c;
    color: #e2e8f0;
}

QTabBar::tab:selected {
    background-color: #18181c;
    border-color: #2a2a30;
    color: #e2e8f0;
    border-bottom: 2px solid #4f46e5;
}

QTableWidget {
    background-color: #18181c;
    alternate-background-color: #202024;
    border: 1px solid #2a2a30;
    gridline-color: #2a2a30;
    border-radius: 4px;
    color: #e2e8f0;
}

QTableWidget::item {
    padding: 6px;
}

QTableWidget::item:selected {
    background-color: #2d2d3f;
    color: #e2e8f0;
}

QHeaderView::section {
    background-color: #202024;
    color: #94a3b8;
    padding: 6px;
    border: 1px solid #2a2a30;
    font-weight: bold;
}

QScrollBar:vertical {
    border: none;
    background-color: #121214;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #2a2a30;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background-color: #3f3f46;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background-color: #121214;
    height: 10px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background-color: #2a2a30;
    min-width: 20px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #3f3f46;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QSplitter::handle {
    background-color: #2a2a30;
}

QComboBox {
    background-color: #202024;
    border: 1px solid #2a2a30;
    border-radius: 4px;
    padding: 6px 10px;
    color: #e2e8f0;
}

QComboBox:focus {
    border: 1px solid #4f46e5;
}

QComboBox QAbstractItemView {
    background-color: #202024;
    border: 1px solid #2a2a30;
    selection-background-color: #4f46e5;
    selection-color: #e2e8f0;
}

QScrollArea {
    border: none;
    background-color: #121214;
}

#rightScrollWidget {
    background-color: #121214;
}

#errorLabel {
    color: #f87171;
    font-weight: bold;
}

#appTitle {
    font-size: 18px;
    font-weight: bold;
    color: #e2e8f0;
}

#appSubtitle {
    color: #64748b;
    font-size: 11px;
}
"""
