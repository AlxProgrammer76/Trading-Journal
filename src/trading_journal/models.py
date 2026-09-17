"""Modelo de una operación de trading (v0.1)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Direction(Enum):
    """Sentido de la posición."""

    LONG = "long"
    SHORT = "short"


@dataclass
class Trade:
    """Operación cerrada. El P&L no se introduce: se deriva de precios, cantidad y dirección."""

    trade_datetime: datetime
    asset: str
    market: str
    direction: Direction
    entry_price: float
    exit_price: float
    quantity: float
    comment: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.direction, Direction):
            raise ValueError("direction must be a Direction value")

        if not self.asset.strip():
            raise ValueError("asset must not be empty")
        if not self.market.strip():
            raise ValueError("market must not be empty")

        self._require_positive_finite(self.entry_price, "entry_price")
        self._require_positive_finite(self.exit_price, "exit_price")
        self._require_positive_finite(self.quantity, "quantity")

    @staticmethod
    def _require_positive_finite(value: float, name: str) -> None:
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be a finite number greater than 0")

    @property
    def pnl(self) -> float:
        """P&L de la operación; delega en pnl.calculate_pnl."""
        from .pnl import calculate_pnl

        return calculate_pnl(
            self.direction,
            self.entry_price,
            self.exit_price,
            self.quantity,
        )
