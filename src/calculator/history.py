import json
import os
from datetime import datetime
from typing import List
from pathlib import Path
from calculator.models import HistoryItem

class HistoryManager:
    def __init__(self, filepath: str = None):
        if filepath is None:
            app_dir = Path.home() / ".ip_address_calculator"
            app_dir.mkdir(parents=True, exist_ok=True)
            self.filepath = str(app_dir / "history.json")
        else:
            self.filepath = filepath
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

    def load_history(self) -> List[HistoryItem]:
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
                return [
                    HistoryItem(
                        timestamp=item["timestamp"],
                        ip_address=item["ip_address"],
                        cidr=item["cidr"],
                        ip_version=item["ip_version"],
                        network_address=item["network_address"]
                    )
                    for item in data
                ]
        except Exception:
            return []

    def add_item(self, ip_address: str, cidr: int, ip_version: int, network_address: str) -> None:
        history = self.load_history()
        
        history = [item for item in history if not (item.ip_address == ip_address and item.cidr == cidr)]
        
        new_item = HistoryItem(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ip_address=ip_address,
            cidr=cidr,
            ip_version=ip_version,
            network_address=network_address
        )
        history.insert(0, new_item)
        history = history[:50]
        self._save_history(history)

    def clear_history(self) -> None:
        self._save_history([])

    def _save_history(self, history: List[HistoryItem]) -> None:
        try:
            with open(self.filepath, "w") as f:
                json.dump([
                    {
                        "timestamp": item.timestamp,
                        "ip_address": item.ip_address,
                        "cidr": item.cidr,
                        "ip_version": item.ip_version,
                        "network_address": item.network_address
                    }
                    for item in history
                ], f, indent=4)
        except Exception:
            pass
