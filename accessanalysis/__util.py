def cache_attr(attr_name):
    def ret(func):
        def ret(x):
            a = getattr(x, attr_name, ...)
            if a is not ...:
                return a
            ret = func(x)
            setattr(x, attr_name, ret)
            return ret

        return ret

    return ret


__all__ = ['cache_attr']
