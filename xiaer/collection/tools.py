
def truncate_dot(value, size):
    if len(value) > size and size > 20:
        return value[0:(size-20)] + '..'
    else:
        return value[0:size]