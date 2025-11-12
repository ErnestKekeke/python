def cm_to_inches(cm: float = 0) -> float:
    ans = cm * 0.393701
    ans = round(ans, 3)
    return ans


def inches_to_cm(inches: float = 0) -> float:
    ans = inches * 2.54
    ans = round(ans, 3)
    return ans
