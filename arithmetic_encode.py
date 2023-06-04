from typing import Dict
import sys

from define import IO_MODE_BIT, IO_MODE_BYTE
from bit_io_stream import BitInStream, BitOutStream
from acc_table import StaticAccTable
from arithmetic_encoder import ArithmeticEncoder


def _get_distribution(src: str, mode: str, max_total: int) -> Dict[str, int]:
    dist = {}
    total = 0

    with open(src, "rb") as f:
        stream = BitInStream(f, mode)

        while True:
            symbol = stream.read(1)
            if not symbol:
                break

            total += 1
            if symbol in dist:
                dist[symbol] += 1
            else:
                dist[symbol] = 1

    if total > max_total:
        for key, val in dist.items():
            dist[key] = max(1, val*max_total//total)

    return dist


if __name__ == "__main__":
    kwargs = dict([arg.split("=") for arg in sys.argv[1:]])

    src = kwargs["src"]
    out = kwargs["out"]

    if kwargs["mode"] == "b":
        mode = IO_MODE_BIT
    elif kwargs["mode"] == "B":
        mode = IO_MODE_BYTE
    else:
        raise AssertionError

    word_len = int(kwargs["len"])
    assert word_len > 2
    max_total = 2 ** (word_len-2)

    dist = _get_distribution(src=src, mode=mode, max_total=max_total)
    acc_table = StaticAccTable(word_len=word_len, cnt_table=dist)
    encoder = ArithmeticEncoder(length=word_len)

    with open(src, "rb") as src_file, open(out, "wb") as out_file:
        istream = BitInStream(src_file, mode)
        ostream = BitOutStream(out_file, IO_MODE_BIT)

        while True:
            symbol = istream.read()
            if not symbol:
                break

            info = acc_table.get_update_info(symbol)
            code = encoder.encode(info)

            for b in code:
                ostream.write(b)
        
        eos = encoder.flush()
        for b in eos:
            ostream.write(b)
    
        ostream.flush()
