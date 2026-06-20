def kg_to_lbs(weight: float) -> float:
    """
    This convert kilogram to pounds
    :param weight: kg
    :return: lbs
    """
    return round(weight * 2.20462, 2)


def lbs_to_kg(weight: float) -> float:
    """
    This convert pounds to kilogram
    :param weight: lbs
    :return: kg
    """
    return round(weight / 2.20462, 2)
