from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QGroupBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QSplitter, QFileDialog, QMessageBox, QComboBox, QScrollArea,
    QFrame, QGridLayout
)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QKeySequence, QShortcut, QGuiApplication, QColor, QFont

from calculator.engine import NetworkEngine
from calculator.validators import InputValidator
from calculator.history import HistoryManager
from calculator.exporter import ResultExporter
from calculator.models import IPDetails
from calculator.ui.styles import DARK_THEME_STYLE
from calculator.ui.widgets import OverviewCard, BinaryVisualizer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Address Calculator")
        self.setMinimumSize(950, 700)
        self.setStyleSheet(DARK_THEME_STYLE)
        
        self.history_manager = HistoryManager()
        self.current_details = None
        
        self._init_ui()
        self._setup_shortcuts()
        self._load_initial_history()

    def _init_ui(self) -> None:
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        header_layout = QHBoxLayout()
        title_vbox = QVBoxLayout()
        title_vbox.setSpacing(2)
        
        app_title = QLabel("IP Address Calculator")
        app_title.setObjectName("appTitle")
        app_subtitle = QLabel("Professional Subnetting, Validation & Calculation Utility")
        app_subtitle.setObjectName("appSubtitle")
        
        title_vbox.addWidget(app_title)
        title_vbox.addWidget(app_subtitle)
        header_layout.addLayout(title_vbox)
        header_layout.addStretch()

        version_layout = QHBoxLayout()
        version_label = QLabel("IP Version:")
        version_label.setStyleSheet("color: #94a3b8; font-weight: bold;")
        self.ip_version_combo = QComboBox()
        self.ip_version_combo.addItems(["IPv4", "IPv6"])
        self.ip_version_combo.currentIndexChanged.connect(self._on_ip_version_changed)
        version_layout.addWidget(version_label)
        version_layout.addWidget(self.ip_version_combo)
        header_layout.addLayout(version_layout)
        
        main_layout.addLayout(header_layout)

        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        input_group = QGroupBox("Calculator Input")
        input_grid = QVBoxLayout(input_group)
        input_grid.setSpacing(10)
        input_grid.setContentsMargins(12, 16, 12, 12)

        ip_input_layout = QHBoxLayout()
        ip_label = QLabel("IP Address:")
        ip_label.setFixedWidth(80)
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("e.g. 192.168.1.1")
        ip_input_layout.addWidget(ip_label)
        ip_input_layout.addWidget(self.ip_input)
        input_grid.addLayout(ip_input_layout)

        mask_input_layout = QHBoxLayout()
        mask_label = QLabel("Mask / CIDR:")
        mask_label.setFixedWidth(80)
        self.mask_input = QLineEdit()
        self.mask_input.setPlaceholderText("e.g. 24 or 255.255.255.0")
        mask_input_layout.addWidget(mask_label)
        mask_input_layout.addWidget(self.mask_input)
        input_grid.addLayout(mask_input_layout)

        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
        self.error_label.setWordWrap(True)
        input_grid.addWidget(self.error_label)

        btn_layout = QHBoxLayout()
        self.calc_btn = QPushButton("Calculate")
        self.calc_btn.setObjectName("calculateButton")
        self.calc_btn.clicked.connect(self.calculate_ip)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_fields)
        
        btn_layout.addWidget(self.calc_btn)
        btn_layout.addWidget(self.clear_btn)
        input_grid.addLayout(btn_layout)

        left_layout.addWidget(input_group)

        self.tabs = QTabWidget()
        left_layout.addWidget(self.tabs)

        self.subnet_widget = QWidget()
        subnet_layout = QVBoxLayout(self.subnet_widget)
        subnet_layout.setSpacing(10)
        subnet_layout.setContentsMargins(8, 8, 8, 8)

        subnet_config_layout = QHBoxLayout()
        self.subnet_mode = QComboBox()
        self.subnet_mode.addItems(["Divide by Subnet Count", "Divide by Host Count"])
        self.subnet_param_input = QLineEdit()
        self.subnet_param_input.setPlaceholderText("Count")
        
        self.subnet_calc_btn = QPushButton("Divide")
        self.subnet_calc_btn.clicked.connect(self.calculate_subnets)
        
        subnet_config_layout.addWidget(self.subnet_mode)
        subnet_config_layout.addWidget(self.subnet_param_input)
        subnet_config_layout.addWidget(self.subnet_calc_btn)
        subnet_layout.addLayout(subnet_config_layout)

        self.subnet_table = QTableWidget(0, 7)
        self.subnet_table.setHorizontalHeaderLabels([
            "Idx", "Network Address", "Mask/CIDR", "Usable Range", "Broadcast", "Total Hosts", "Usable Hosts"
        ])
        self.subnet_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.subnet_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.subnet_table.verticalHeader().setVisible(False)
        subnet_layout.addWidget(self.subnet_table)
        
        self.tabs.addTab(self.subnet_widget, "Subnet Divider")

        self.history_widget = QWidget()
        history_layout = QVBoxLayout(self.history_widget)
        history_layout.setSpacing(10)
        history_layout.setContentsMargins(8, 8, 8, 8)
        
        self.history_table = QTableWidget(0, 4)
        self.history_table.setHorizontalHeaderLabels(["Timestamp", "IP Address", "CIDR", "Network Address"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.itemDoubleClicked.connect(self._on_history_item_double_clicked)
        history_layout.addWidget(self.history_table)
        
        history_actions = QHBoxLayout()
        self.load_history_btn = QPushButton("Load Selected")
        self.load_history_btn.clicked.connect(self._on_load_history_clicked)
        self.clear_history_btn = QPushButton("Clear History")
        self.clear_history_btn.clicked.connect(self._on_clear_history_clicked)
        history_actions.addWidget(self.load_history_btn)
        history_actions.addWidget(self.clear_history_btn)
        history_layout.addLayout(history_actions)
        
        self.tabs.addTab(self.history_widget, "History")

        main_splitter.addWidget(left_widget)

        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_widget = QWidget()
        right_widget.setObjectName("rightScrollWidget")
        right_scroll.setWidget(right_widget)
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        overview_group = QGroupBox("Overview")
        overview_grid = QGridLayout(overview_group)
        overview_grid.setSpacing(10)
        overview_grid.setContentsMargins(12, 16, 12, 12)
        
        self.card_network = OverviewCard("Network Address")
        self.card_broadcast = OverviewCard("Broadcast Address")
        self.card_first_usable = OverviewCard("First Usable")
        self.card_last_usable = OverviewCard("Last Usable")
        
        overview_grid.addWidget(self.card_network, 0, 0)
        overview_grid.addWidget(self.card_broadcast, 0, 1)
        overview_grid.addWidget(self.card_first_usable, 1, 0)
        overview_grid.addWidget(self.card_last_usable, 1, 1)
        right_layout.addWidget(overview_group)

        self.details_group = QGroupBox("Detailed Information")
        details_box = QVBoxLayout(self.details_group)
        details_box.setSpacing(10)
        details_box.setContentsMargins(12, 16, 12, 12)

        self.details_table = QTableWidget(0, 2)
        self.details_table.setHorizontalHeaderLabels(["Property", "Value"])
        self.details_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.details_table.horizontalHeader().setVisible(False)
        self.details_table.setAlternatingRowColors(True)
        self.details_table.verticalHeader().setVisible(False)
        details_box.addWidget(self.details_table)
        right_layout.addWidget(self.details_group)

        self.visualizer = BinaryVisualizer()
        right_layout.addWidget(self.visualizer)

        export_layout = QHBoxLayout()
        export_layout.addStretch()
        self.export_json_btn = QPushButton("Export JSON")
        self.export_json_btn.clicked.connect(self.export_json)
        self.export_txt_btn = QPushButton("Export TXT")
        self.export_txt_btn.clicked.connect(self.export_txt)
        export_layout.addWidget(self.export_json_btn)
        export_layout.addWidget(self.export_txt_btn)
        right_layout.addLayout(export_layout)

        main_splitter.addWidget(right_scroll)

        main_splitter.setSizes([450, 500])

    def _setup_shortcuts(self) -> None:
        self.shortcut_focus = QShortcut(QKeySequence("Ctrl+L"), self)
        self.shortcut_focus.activated.connect(self.ip_input.setFocus)
        
        self.shortcut_clear = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcut_clear.activated.connect(self.clear_fields)
        
        self.shortcut_copy_summary = QShortcut(QKeySequence("Ctrl+Shift+C"), self)
        self.shortcut_copy_summary.activated.connect(self.copy_calculation_summary)

    def _on_ip_version_changed(self) -> None:
        version = self.ip_version_combo.currentText()
        if version == "IPv4":
            self.ip_input.setPlaceholderText("e.g. 192.168.1.1")
            self.mask_input.setPlaceholderText("e.g. 24 or 255.255.255.0")
            self.card_broadcast.setVisible(True)
            self.visualizer.setVisible(True)
        else:
            self.ip_input.setPlaceholderText("e.g. 2001:db8::1")
            self.mask_input.setPlaceholderText("e.g. 64 or ffff:ffff::")
            self.card_broadcast.setVisible(False)
            self.visualizer.setVisible(False)

    @Slot()
    def calculate_ip(self) -> None:
        self.error_label.setText("")
        ip_text = self.ip_input.text()
        mask_text = self.mask_input.text()
        version = 4 if self.ip_version_combo.currentText() == "IPv4" else 6

        is_valid, ip, cidr, error_msg = InputValidator.validate_and_parse(ip_text, mask_text, version)
        if not is_valid:
            self.error_label.setText(error_msg)
            return

        try:
            details = NetworkEngine.calculate_ip_details(ip, cidr)
            self.current_details = details
            
            self.card_network.set_value(details.network_address)
            self.card_broadcast.set_value(details.broadcast_address)
            self.card_first_usable.set_value(details.first_usable)
            self.card_last_usable.set_value(details.last_usable)

            self.populate_details_table(details)

            if details.ip_version == 4:
                self.visualizer.visualize(details.binary_repr, details.cidr)
            else:
                self.visualizer.clear()

            self.history_manager.add_item(details.address, details.cidr, details.ip_version, details.network_address)
            self._load_initial_history()

        except Exception as e:
            self.error_label.setText(f"Calculation failed: {str(e)}")

    def populate_details_table(self, details: IPDetails) -> None:
        self.details_table.setRowCount(0)
        
        properties = [
            ("IP Address", details.address),
            ("CIDR Prefix", f"/{details.cidr}"),
            ("Netmask", details.netmask),
            ("Wildcard Mask", details.wildcard),
            ("Network Range", details.network_range),
            ("Host Range", details.host_range),
            ("Total Addresses", f"{details.total_addresses:,}"),
            ("Usable Host Count", f"{details.usable_hosts:,}"),
            ("Address Class", details.address_class),
            ("IP Type", details.ip_type),
            ("Private Network", "Yes" if details.is_private else "No"),
            ("Loopback Address", "Yes" if details.is_loopback else "No"),
            ("Multicast Address", "Yes" if details.is_multicast else "No"),
            ("Link-Local Address", "Yes" if details.is_link_local else "No"),
            ("Reserved Address", "Yes" if details.is_reserved else "No"),
            ("IPv4 Mapped", "Yes" if details.is_ipv4_mapped else "No"),
            ("Decimal Representation", str(details.decimal_repr)),
            ("Hexadecimal Representation", details.hex_repr),
            ("Reverse DNS PTR", details.reverse_dns),
            ("Binary Representation", details.binary_repr)
        ]

        self.details_table.setRowCount(len(properties))
        for row_idx, (prop_name, prop_val) in enumerate(properties):
            name_item = QTableWidgetItem(prop_name)
            name_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            name_item.setForeground(QColor("#94a3b8"))
            font = QFont()
            font.setBold(True)
            name_item.setFont(font)
            
            val_item = QTableWidgetItem(prop_val)
            val_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            
            self.details_table.setItem(row_idx, 0, name_item)
            self.details_table.setItem(row_idx, 1, val_item)

    @Slot()
    def calculate_subnets(self) -> None:
        if not self.current_details:
            QMessageBox.warning(self, "No Parent Network", "Please calculate an IP address first to set the parent network.")
            return

        param_text = self.subnet_param_input.text().strip()
        if not param_text.isdigit() or int(param_text) <= 0:
            QMessageBox.critical(self, "Invalid Input", "Please enter a valid positive integer.")
            return

        val = int(param_text)
        mode = self.subnet_mode.currentText()

        try:
            if mode == "Divide by Subnet Count":
                res = NetworkEngine.divide_by_subnet_count(
                    self.current_details.address,
                    self.current_details.cidr,
                    val
                )
            else:
                res = NetworkEngine.divide_by_host_count(
                    self.current_details.address,
                    self.current_details.cidr,
                    val
                )

            self.populate_subnet_table(res)
        except Exception as e:
            QMessageBox.critical(self, "Subnet Division Failed", str(e))

    def populate_subnet_table(self, res) -> None:
        self.subnet_table.setRowCount(0)
        self.subnet_table.setRowCount(len(res.subnets))
        
        for idx, sub in enumerate(res.subnets):
            self.subnet_table.setItem(idx, 0, QTableWidgetItem(str(sub.index)))
            self.subnet_table.setItem(idx, 1, QTableWidgetItem(sub.network_address))
            self.subnet_table.setItem(idx, 2, QTableWidgetItem(f"{sub.netmask} (/{sub.cidr})"))
            self.subnet_table.setItem(idx, 3, QTableWidgetItem(sub.usable_range))
            self.subnet_table.setItem(idx, 4, QTableWidgetItem(sub.broadcast_address))
            self.subnet_table.setItem(idx, 5, QTableWidgetItem(f"{sub.total_hosts:,}"))
            self.subnet_table.setItem(idx, 6, QTableWidgetItem(f"{sub.usable_hosts:,}"))

    @Slot()
    def clear_fields(self) -> None:
        self.ip_input.clear()
        self.mask_input.clear()
        self.error_label.setText("")
        self.card_network.set_value("")
        self.card_broadcast.set_value("")
        self.card_first_usable.set_value("")
        self.card_last_usable.set_value("")
        self.details_table.setRowCount(0)
        self.subnet_table.setRowCount(0)
        self.subnet_param_input.clear()
        self.visualizer.clear()
        self.current_details = None

    @Slot()
    def copy_calculation_summary(self) -> None:
        if not self.current_details:
            return
        
        d = self.current_details
        summary = (
            f"IP Address:        {d.address}/{d.cidr}\n"
            f"Netmask:           {d.netmask}\n"
            f"Wildcard Mask:     {d.wildcard}\n"
            f"Network Address:   {d.network_address}\n"
            f"Broadcast Address: {d.broadcast_address}\n"
            f"Usable Host Range: {d.host_range}\n"
            f"Total Addresses:   {d.total_addresses:,}\n"
            f"Usable Host Count: {d.usable_hosts:,}\n"
            f"IP Address Type:   {d.ip_type}\n"
            f"Binary Representation: {d.binary_repr}"
        )
        QGuiApplication.clipboard().setText(summary)

    @Slot()
    def export_json(self) -> None:
        if not self.current_details:
            QMessageBox.warning(self, "No Data", "No calculation results available to export.")
            return

        filepath, _ = QFileDialog.getSaveFileName(self, "Export to JSON", "", "JSON Files (*.json)")
        if filepath:
            try:
                ResultExporter.export_to_json(self.current_details, filepath)
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Could not export to JSON: {str(e)}")

    @Slot()
    def export_txt(self) -> None:
        if not self.current_details:
            QMessageBox.warning(self, "No Data", "No calculation results available to export.")
            return

        filepath, _ = QFileDialog.getSaveFileName(self, "Export to TXT", "", "Text Files (*.txt)")
        if filepath:
            try:
                ResultExporter.export_to_txt(self.current_details, filepath)
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Could not export to TXT: {str(e)}")

    def _load_initial_history(self) -> None:
        items = self.history_manager.load_history()
        self.history_table.setRowCount(0)
        self.history_table.setRowCount(len(items))
        
        for idx, item in enumerate(items):
            self.history_table.setItem(idx, 0, QTableWidgetItem(item.timestamp))
            self.history_table.setItem(idx, 1, QTableWidgetItem(item.ip_address))
            self.history_table.setItem(idx, 2, QTableWidgetItem(f"/{item.cidr}"))
            self.history_table.setItem(idx, 3, QTableWidgetItem(item.network_address))

    def _on_history_item_double_clicked(self, item: QTableWidgetItem) -> None:
        self._load_selected_history_row(item.row())

    def _load_selected_history_row(self, row: int) -> None:
        if row < 0:
            return
        items = self.history_manager.load_history()
        if row < len(items):
            hist = items[row]
            self.ip_version_combo.setCurrentText(f"IPv{hist.ip_version}")
            self.ip_input.setText(hist.ip_address)
            self.mask_input.setText(str(hist.cidr))
            self.calculate_ip()

    def _on_load_history_clicked(self) -> None:
        selected_indexes = self.history_table.selectionModel().selectedRows()
        if selected_indexes:
            self._load_selected_history_row(selected_indexes[0].row())
        else:
            QMessageBox.warning(self, "No Selection", "Please select a history entry first.")

    def _on_clear_history_clicked(self) -> None:
        self.history_manager.clear_history()
        self._load_initial_history()
