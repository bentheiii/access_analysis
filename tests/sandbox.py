from accessanalysis import read, find_invalid_access

g = read(
"""
f0:(u0,r)
f1:(u0,w)->(u1,r)
""".splitlines()
)
ia = find_invalid_access(g)
print('->'.join(ia))