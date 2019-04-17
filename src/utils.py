import math

millnames = ['', ' thousand', ' million', ' billion', ' trillion']


def millify(n):
    """Human-readable large numbers

    Reference
    ---------
    https://stackoverflow.com/questions/3154460/python-human-readable-large-numbers

    """
    n = float(n)
    millidx = max(
        0,
        min(len(millnames)-1,
            int(
                math.floor(0 if n == 0 else math.log10(abs(n))/3)
            )
        )
    )

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])
