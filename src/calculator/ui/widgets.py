from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QGuiApplication

class OverviewCard(QFrame):
    def __init__(self, title: str, value: str = "", parent: QWidget = None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e24;
                border: 1px solid #2a2a30;
                border-radius: 6px;
            }
        """)
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(12, 10, 12, 10)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; text-transform: uppercase;")
        
        self.value_label = QLabel(value if value else "-")
        self.value_label.setStyleSheet("color: #e2e8f0; font-size: 15px; font-weight: bold;")
        self.value_label.setWordWrap(True)
        
        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.value_label)
        
        self.layout.addLayout(text_layout)
        self.layout.addStretch()
        
        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setFixedWidth(50)
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #25252b;
                border: 1px solid #2a2a30;
                border-radius: 4px;
                color: #94a3b8;
                font-size: 11px;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #2d2d35;
                color: #e2e8f0;
            }
        """)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.layout.addWidget(self.copy_btn)

    def set_value(self, value: str) -> None:
        self.value_label.setText(value if value else "-")

    def copy_to_clipboard(self) -> None:
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.value_label.text())


class BinaryVisualizer(QFrame):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #18181c;
                border: 1px solid #2a2a30;
                border-radius: 6px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)
        
        title_layout = QHBoxLayout()
        title = QLabel("IPv4 Binary Visualization")
        title.setStyleSheet("color: #94a3b8; font-weight: bold;")
        
        legend = QLabel(
            '<span style="color: #6366f1;">■</span> Network Bits  '
            '<span style="color: #94a3b8;">■</span> Host Bits'
        )
        legend.setStyleSheet("color: #64748b; font-size: 11px;")
        
        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(legend)
        layout.addLayout(title_layout)
        
        self.binary_text = QLabel("Enter an IPv4 address to visualize...")
        self.binary_text.setAlignment(Qt.AlignCenter)
        self.binary_text.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.binary_text.setStyleSheet("""
            QLabel {
                font-family: "Consolas", "Courier New", monospace;
                font-size: 20px;
                background-color: #121214;
                border: 1px solid #2a2a30;
                border-radius: 4px;
                padding: 16px;
            }
        """)
        layout.addWidget(self.binary_text)

    def visualize(self, binary_str: str, cidr: int) -> None:
        raw_bits = binary_str.replace(".", "")
        net_bits = raw_bits[:cidr]
        host_bits = raw_bits[cidr:]
        
        formatted_net = ""
        bit_counter = 0
        for bit in net_bits:
            formatted_net += bit
            bit_counter += 1
            if bit_counter % 8 == 0 and bit_counter < 32:
                formatted_net += "."
                
        formatted_host = ""
        for bit in host_bits:
            if bit_counter % 8 == 0 and bit_counter > 0 and bit_counter < 32:
                formatted_host += "."
            formatted_host += bit
            bit_counter += 1
            
        html = (
            f'<span style="color: #6366f1;">{formatted_net}</span>'
            f'<span style="color: #64748b;">{formatted_host}</span>'
        )
        self.binary_text.setText(html)

    def clear(self) -> None:
        self.binary_text.setText("Enter an IPv4 address to visualize...")
