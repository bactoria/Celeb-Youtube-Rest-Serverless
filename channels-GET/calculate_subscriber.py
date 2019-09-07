def calculate_subscriber_string(value):
    valueStr = str(value)
    valueLen = str(len(valueStr))

    dic = {
        '1': lambda v: v,
        '2': lambda v: v,
        '3': lambda v: v,
        '4': lambda v: v[:1]+'.'+v[1:2]+'천',
        '5': lambda v: v[:1]+'.'+v[1:2]+'만',
        '6': lambda v: v[:2]+'만',
        '7': lambda v: v[:3]+'만',
        '8': lambda v: v[:4]+'만',
        '9': lambda v: v[:1]+'.'+v[1:2]+'억'
    }
    return dic[valueLen](valueStr)