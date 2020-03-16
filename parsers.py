def parse_dues(due_query) :
    if due_query.plus > 999.9:
        due_plus = '+999.9'
    else:
        due_plus = '+' + str(due_query.plus)
    if due_query.minus > 999.9:
        due_minus = '-999.9'
    else:
        due_minus = '-' + str(due_query.minus)
    if due_query.net > 999.9:
        due_net = 999.9
    else:
        due_net = due_query.net
    if due_query.net < 0:
        due_net = '-' + str(due_net)
    else:
        due_net = '+' + str(due_net)
    parsed_dues = {
        'plus' : due_plus,
        'minus' : due_minus,
        'net' : due_net
    }
    return parsed_dues