def convert_to_number(value):
    if isinstance(value, str):
        if 'B' in value:
            return float(value.replace('B', '')) * 1e9
        elif 'T' in value:
            return float(value.replace('T', '')) * 1e12
        elif 'M' in value:
            return float(value.replace('M', '')) * 1e6
        elif 'K' in value:
            return float(value.replace('K', '')) * 1e3
        elif '%' in value:
            return float(value.replace('%', '')) / 100
    return float(value)