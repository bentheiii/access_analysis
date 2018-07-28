from accessanalysis import *
g = read(
    """
    f1:(u1,r)
    f2:(u1,w)->(u2,r)
    f3:(u1,w)
    """.splitlines()
)
ia = invalid_access(g)
print('->'.join(ia))
up = unix_permissions(g)
if isinstance(up, str):
    print(up)
else:
    print('\n'.join(f + ': ' + ' '.join(str(x) for x in r) for (f, r) in up.items()))
#dot(g).render('out.gv', view=True, cleanup=True)

g = read(
    """
    f1:(u1,rw)->(u2,r)->(u3,r)->(u4,r)
    f2:(u1,w)->(u2,rw)->(u3,w)->(u4,r)
    f3:(u1,w)->(u2,r)->(u3,rw)->(u4,r)
    f4:(u1,w)->(u2,rw)->(u3,w)->(u4,r)
    """.splitlines()
)
print(blp(g))
