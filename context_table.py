from typing import Dict

from define import BITS_PER_BYTE, IO_MODE_BIT, IO_MODE_BYTE
from acc_table import (
    AdaptiveAccTable,
    BaseAccTable,
    StaticAccTable,
    UpdateInfo,
)


class _BaseContextTable:
    MODE_BIT = IO_MODE_BIT  # encode bit by bit
    MODE_BYTE = IO_MODE_BYTE # encode byte by byte

    def __init__(self, word_len: int, mode: str):
        assert mode in (self.MODE_BIT, self.MODE_BYTE)

        self._word_len: int = word_len
        self._mode: str = mode
        self._acc_table: BaseAccTable

    def get_update_info(self, symbol: str) -> UpdateInfo:
        return self._acc_table.get_update_info(symbol)


class NegContextTable(_BaseContextTable):
    def __init__(self, word_len: int, mode: str):
        super().__init__(word_len=word_len, mode=mode)

        cnt_table = (
            {"0": 1, "1": 1}
            if self._mode == self.MODE_BIT
            else {chr(i): 1 for i in range(1 << BITS_PER_BYTE)}
        )
        self._acc_table: StaticAccTable = StaticAccTable(word_len=self._word_len, cnt_table=cnt_table)


class ContextTable(_BaseContextTable):
    def __init__(self, word_len: int, mode: str, init_cnts: Dict[str, int]={}):
        super().__init__(word_len=word_len, mode=mode)
        self._acc_table: AdaptiveAccTable = AdaptiveAccTable(word_len=word_len, init_cnts=init_cnts)
