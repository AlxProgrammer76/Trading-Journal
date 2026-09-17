"""Cálculo de P&L de una operación (v0.1, sin comisiones ni multiplicadores)."""

from .models import Direction


def calculate_pnl(
    direction: Direction,
    entry_price: float,
    exit_price: float,
    quantity: float,
) -> float:
    """Devuelve el P&L bruto: Long (salida − entrada) × cantidad; Short (entrada − salida) × cantidad."""
    if direction is Direction.LONG:
        return (exit_price - entry_price) * quantity
    if direction is Direction.SHORT:
        return (entry_price - exit_price) * quantity
    raise ValueError("direction must be Direction.LONG or Direction.SHORT")
