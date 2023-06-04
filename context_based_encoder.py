from typing import Dict

from define import IO_MODE_BIT, IO_MODE_BYTE
from context_table import NegContextTable, ContextTable
from arithmetic_encoder import ArithmeticEncoder


class ContextBasedEncoder:
    MODE_BIT = IO_MODE_BIT  # encode bit by bit
    MODE_BYTE = IO_MODE_BYTE # encode byte by byte

    def __init__(self, word_len: int, mode: str, max_context_order: int):
        assert mode in (self.MODE_BIT, self.MODE_BYTE)
        assert max_context_order >= 0

        self._word_len: int = word_len
        self._mode: str = mode
        self._max_context_order: int = max_context_order

        self._encoder: ArithmeticEncoder = ArithmeticEncoder(length=word_len)
        self._neg_context_table = NegContextTable(word_len=self._word_len, mode=self._mode)
        self._context_dict: Dict[str, ContextTable] = {}

    def encode(self, context: str, symbol: str) -> str:
        if len(context) > self._max_context_order:
            raise AssertionError

        code = ""
        while True:
            table = self._context_dict.get(context)
            if table:
                info = table.get_update_info(symbol)
                code += self._encoder.encode(info)
                if info.esc is False:
                    return code
            else:
                self._context_dict[context] = ContextTable(
                    word_len=self._word_len,
                    mode=self._mode,
                    init_cnts={symbol: 1},
                )

            if context == "":
                break
            context = context[1:]

        info = self._neg_context_table.get_update_info(symbol)
        code += self._encoder.encode(info)
        return code

    def flush(self) -> str:
        return self._encoder.flush()
