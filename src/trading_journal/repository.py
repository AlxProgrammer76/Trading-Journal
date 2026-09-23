"""Persistencia de operaciones en un archivo JSON local (v0.1)."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .models import Direction, Trade

_TRADE_KEYS = (
    "trade_datetime",
    "asset",
    "market",
    "direction",
    "entry_price",
    "exit_price",
    "quantity",
    "comment",
)


class JsonTradeRepository:
    """Guarda y recupera Trade en JSON. No calcula P&L."""

    def __init__(self, path: str | Path | None = None) -> None:
        if path is None:
            project_root = Path(__file__).resolve().parents[2]
            path = project_root / "data" / "trades.json"
        self._path = Path(path)

    def save(self, trade: Trade) -> None:
        records = self._load_records()
        records.append(self._trade_to_dict(trade))
        self._write_records(records)

    def list_all(self) -> list[Trade]:
        return [self._dict_to_trade(record) for record in self._load_records()]

    def _ensure_file(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._write_records([])

    def _load_records(self) -> list[dict]:
        self._ensure_file()
        try:
            raw_text = self._path.read_text(encoding="utf-8")
            payload = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid JSON in trade store '{self._path}': {exc}"
            ) from exc

        if not isinstance(payload, list):
            raise ValueError(
                f"Trade store '{self._path}' must contain a JSON list of operations, "
                f"got {type(payload).__name__}"
            )

        records: list[dict] = []
        for index, item in enumerate(payload):
            if not isinstance(item, dict):
                raise ValueError(
                    f"Trade store '{self._path}' item at index {index} must be an object, "
                    f"got {type(item).__name__}"
                )
            records.append(item)
        return records

    def _write_records(self, records: list[dict]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        serialized = json.dumps(records, indent=2, ensure_ascii=False)
        self._path.write_text(serialized + "\n", encoding="utf-8")

    @staticmethod
    def _trade_to_dict(trade: Trade) -> dict:
        return {
            "trade_datetime": trade.trade_datetime.isoformat(timespec="seconds"),
            "asset": trade.asset,
            "market": trade.market,
            "direction": trade.direction.value,
            "entry_price": trade.entry_price,
            "exit_price": trade.exit_price,
            "quantity": trade.quantity,
            "comment": trade.comment,
        }

    @staticmethod
    def _dict_to_trade(record: dict) -> Trade:
        missing = [key for key in _TRADE_KEYS if key not in record]
        if missing:
            raise ValueError(
                f"Trade record is missing required fields: {', '.join(missing)}"
            )

        try:
            trade_datetime = datetime.fromisoformat(record["trade_datetime"])
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Invalid trade_datetime '{record['trade_datetime']}': expected ISO 8601"
            ) from exc

        try:
            direction = Direction(record["direction"])
        except ValueError as exc:
            raise ValueError(
                f"Invalid direction '{record['direction']}': expected 'long' or 'short'"
            ) from exc

        return Trade(
            trade_datetime=trade_datetime,
            asset=record["asset"],
            market=record["market"],
            direction=direction,
            entry_price=record["entry_price"],
            exit_price=record["exit_price"],
            quantity=record["quantity"],
            comment=record["comment"],
        )
