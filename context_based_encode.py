import sys

from define import IO_MODE_BIT, IO_MODE_BYTE
from bit_io_stream import BitInStream, BitOutStream
from context_based_encoder import ContextBasedEncoder


if __name__ == "__main__":
    MAX_CONTEXT_ORDER = 2

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

    encoder = ContextBasedEncoder(word_len=word_len, mode=mode, max_context_order=MAX_CONTEXT_ORDER)

    with open(src, "rb") as src_file, open(out, "wb") as out_file:
        istream = BitInStream(src_file, mode)
        ostream = BitOutStream(out_file, IO_MODE_BIT)

        bits_cnt = 0
        symbols_cnt = 0

        context = ""
        while True:
            symbol = istream.read(1)
            if not symbol:
                break

            symbols_cnt += 1

            code = encoder.encode(context=context, symbol=symbol)
            for b in code:
                bits_cnt += 1
                ostream.write(b)

            context += symbol
            if len(context) > MAX_CONTEXT_ORDER:
                context = context[1:]

        eos = encoder.flush()
        for b in eos:
            bits_cnt += 1
            ostream.write(b)

        ostream.flush()
