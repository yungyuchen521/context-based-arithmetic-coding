from utils import BinaryNum, rescale_by
from acc_table import UpdateInfo


class ArithmeticEncoder:
    def __init__(self, length: int):
        assert length > 0

        self._low: BinaryNum = BinaryNum(is_high=False, length=length)
        self._high: BinaryNum = BinaryNum(is_high=True, length=length)
        self._e3_cnt: int = 0

    def encode(self, info: UpdateInfo) -> str:
        code = ""
        width = self._high.num - self._low.num + 1

        new_low = self._low.num + width * info.left_bound // info.total
        new_high = self._low.num + width * info.right_bound // info.total - 1

        self._low.set_num(new_low)
        self._high.set_num(new_high)

        while True:
            method = rescale_by(self._low, self._high)
            if method is None:
                break

            if method == BinaryNum.E1_RESCALE:
                code += "0"
                code += "1" * self._e3_cnt
                self._e3_cnt = 0
            elif method == BinaryNum.E2_RESCALE:
                code += "1"
                code += "0" * self._e3_cnt
                self._e3_cnt = 0
            elif method == BinaryNum.E3_RESCALE:
                self._e3_cnt += 1
            else:
                raise AssertionError

            self._low.rescale(method)
            self._high.rescale(method)

        return code

    def flush(self) -> str:
        low = self._low.bin
        code = low[0]

        if self._e3_cnt and code == "0":
            code += "1" * self._e3_cnt
        elif self._e3_cnt and code == "1":
            code += "0" * self._e3_cnt

        self._e3_cnt = 0
        return code + low[1:]
