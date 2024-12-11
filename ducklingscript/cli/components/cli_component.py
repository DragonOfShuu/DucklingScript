from __future__ import annotations

from abc import ABC, abstractmethod


class CliComponent(ABC):
    _component = None

    @classmethod
    @abstractmethod
    def get(cls) -> CliComponent:
        pass
