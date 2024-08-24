from utilities.dice import roll

def roll_tuple_to_string(res_tuple: tuple) ->str:
    """
    convert roll results to a string representation
    @param res_tuple: Tuple of 2 or 3 elements: d20 result, success (bool), and tp (optional)
    @return: String representation
    """
    
    res = res_tuple[0]
    suc = res_tuple[1]

    if suc == roll.SUCCESS:
        suc_str = ":white_check_mark:"
        if len(res_tuple) == 3:
            tp = f"TP: {res_tuple[2]}"
        else:
            tp = ""
    elif suc == roll.CRIT:
        suc_str = "🎯"
        if len(res_tuple) == 3:
            tp = f"TP: {res_tuple[2]}"
        else:
            tp = ""
    elif suc == roll.CRIT_CONF:
        suc_str = "🎯‼️"
        if len(res_tuple) == 3:
            tp = f"TP: {res_tuple[2]*2}"        
        else:
            tp = ""
    elif suc == roll.FAIL:
        suc_str = "❌"
        tp = ""
    elif suc == roll.FAIL_CONF:
        suc_str = "❌‼️"
        tp = ""


    return f'{suc_str}:{res} ' + tp

def life_points_correction(lep: int) -> int:
    if lep < 0:
        return 0
    else:
        return lep
