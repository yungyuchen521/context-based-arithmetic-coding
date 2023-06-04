from typing import Optional


class BinaryNum:
    E1_RESCALE = "E1"
    E2_RESCALE = "E2"
    E3_RESCALE = "E3"

    def __init__(self, is_high: bool, length: int):
        self._is_high: bool = is_high
        self._len: int = length
        self._num: int = (1 << self._len) - 1 if self._is_high else 0

        self._half = 1 << (self._len-1)
        self._quarter = self._half >> 1

    def __repr__(self):
        return f"{self.bin} ({self._num})"

    @property
    def bin(self) -> str:
        b = format(self._num, f"0{self._len}b")
        assert len(b) == self._len
        return b

    @property
    def num(self):
        return self._num

    @property
    def half(self):
        return self._half

    @property
    def quarter(self):
        return self._quarter

    def set_num(self, n):
        assert n < (self._half << 1)
        self._num = n

    def rescale(self, method: str):
        assert method in (self.E1_RESCALE, self.E2_RESCALE, self.E3_RESCALE)
        
        if method == self.E2_RESCALE:
            self._num -= self._half
        elif method == self.E3_RESCALE:
            self._num -= self._quarter

        self._num <<= 1
        self._num += int(self._is_high)

        assert self._num < (self._half << 1)


def rescale_by(low: BinaryNum, high: BinaryNum) -> Optional[str]:
    assert (not low._is_high) and high._is_high
    assert low.num <= high.num

    qtr = low.quarter
    half = low.half

    if high.num < half:
        return BinaryNum.E1_RESCALE
    elif low.num >= half:
        return BinaryNum.E2_RESCALE
    elif low.num >= qtr and high.num < half+qtr:
        return BinaryNum.E3_RESCALE
