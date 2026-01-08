from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class DashboardFilters:
    """사용자의 입력을 보관하는 데이터 클래스"""
    selected_year: int
    selected_cities: list[str]
    warn_threshold: int