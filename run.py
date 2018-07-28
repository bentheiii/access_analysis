import argparse

import accessanalysis

parser = argparse.ArgumentParser(__name__)
parser.add_argument('source_acl', type=open, help='a file containing the acl to use')
parser.add_argument('--onlydo', dest='only_do', default='ibud',
                    help='only do some parts of the program, must be a subset of iubd')


def main():
    args = parser.parse_args()
    graph = accessanalysis.read(args.source_acl)
    if 'i' in args.only_do:
        ia = accessanalysis.invalid_access(graph)
        if ia:
            print('Invalid access detected: ' + '->'.join(ia))
        else:
            print('No invalid access detected')
    if 'b' in args.only_do:
        w, assigned, order = accessanalysis.blp(graph)
        if w:
            print('BLP mapping:')
            for n, lv in assigned.items():
                print(f'{n}: {lv}')
            print()
            for x, ys in order.items():
                for y in ys:
                    print(f'{x} < {y}')
        else:
            print('no BLP mapping: '+assigned)
    if 'u' in args.only_do:
        umap = accessanalysis.unix_permissions(graph)
        if isinstance(umap, str):
            print('Could not find UNIX mapping: ' + umap)
        else:
            print('file\tpermissions\towner\tgroup')
            for f, r in umap.items():
                print(f'{f}\t{r.owner_perm} {r.group_perm} {r.other_perm}\t{r.owner}\t{r.group}')
    if 'd' in args.only_do:
        dot = accessanalysis.dot(graph)
        dot.render('out.gv', view=True, cleanup=True)


if __name__ == '__main__':
    main()
