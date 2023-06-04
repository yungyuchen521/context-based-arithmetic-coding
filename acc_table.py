import dataclasses
from typing import Dict, Tuple

from define import ESC


@dataclasses.dataclass
class UpdateInfo:
    left_bound: int
    right_bound: int
    total: int
    esc: bool


class BaseAccTable:
    def __init__(self, word_len: int):
        self._max_total: int = 2 ** (word_len-2)
        self._total: int

    @property
    def total(self):
        return self._total

    def get_update_info(self, symbol: str) -> UpdateInfo:
        raise NotImplementedError


class StaticAccTable(BaseAccTable):
    def __init__(self, word_len: int, cnt_table: Dict[str, int]):
        super().__init__(word_len)

        self._total: int = 0
        self._acc_table: Dict[str, Tuple[int, int]] = {}
        # {symbol: (left bound, right bound)}

        for s in sorted(cnt_table.keys()):
            left = self._total
            self._total += cnt_table[s]
            self._acc_table[s] = (left, self._total)

        assert self._total <= self._max_total

    def get_update_info(self, symbol: str) -> UpdateInfo:
        l, r = self._acc_table[symbol]
        return UpdateInfo(
            left_bound=l,
            right_bound=r,
            total=self._total,
            esc=False,
        )


class AdaptiveAccTable(BaseAccTable):
    def __init__(self, word_len: int, init_cnts: Dict[str, int]={}):
        super().__init__(word_len)

        self._cnt_table: Dict[str, int] = init_cnts
        self._cnt_table[ESC] = 1
        self._total: int = sum(self._cnt_table.values())

    def get_update_info(self, symbol: str) -> UpdateInfo:
        # return tuple(escaped_or_not, UpdateInfo)
        assert len(symbol) == 1

        if symbol not in self._cnt_table:
            info = UpdateInfo(
                left_bound=self._total-1,
                right_bound=self._total,
                total=self._total,
                esc=True,
            )  # ESC

            self._total += 1
            self._cnt_table[symbol] = 1

            return info

        acc = 0
        for key in sorted(self._cnt_table.keys()):
            if key == ESC:
                continue

            cnt = self._cnt_table[key]
            if symbol == key:
                info = UpdateInfo(
                    left_bound=acc,
                    right_bound=acc+cnt,
                    total=self._total,
                    esc=False,
                )
                self._increment_cnt(symbol)
                return info

            acc += cnt
        
        raise AssertionError

    def _increment_cnt(self, symbol):
        if symbol not in self._cnt_table:
            raise AssertionError
        
        self._cnt_table[symbol] += 1    
        self._total += 1
        if self._total > self._max_total:
            for key, val in self._cnt_table.items():
                new_val = max(1, val//2)
                self._cnt_table[key] = new_val
                self._total -= (val - new_val)
