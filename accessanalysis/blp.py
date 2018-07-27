from collections import namedtuple
from accessanalysis.find_invalid_access import invalid_access
from accessanalysis.graph import AccessGraph
from accessanalysis.__util import *
import itertools as it


@cache_attr('blp')
def blp(graph: AccessGraph):
    if invalid_access(graph) is not None:
        return None  # if there is an invalid access there is no BLP

    equal_groups = create_equal_groups(graph)
    merged_groups = merge_groups(equal_groups, graph)
    sorted_groups = sort_groups(merged_groups, graph)

    nodes_levels = {}
    for level in sorted_groups:
        for node in sorted_groups[level]:
            nodes_levels[node] = level

    return nodes_levels


def create_equal_groups(graph):
    equal_groups = {}

    for f in graph.nodes():  # iterate through files
        if f in graph.users:
            continue

        file_group = []

        for u in graph.nodes():  # iterate through users
            if u not in graph.users:
                continue

            if graph[f, u] and graph[u, f]:
                file_group.append(u)

        equal_groups[f] = file_group

    return equal_groups


def merge_groups(equal_groups, graph):
    merged_groups = []
    for f0, f1 in it.combinations(equal_groups, 2):
        for u0 in equal_groups[f0]:
            for u1 in equal_groups[f1]:
                if u0 == u1:
                    if equal_groups[f0] == equal_groups[f1]:
                        add_to_merged_groups(merged_groups, equal_groups, f0, f1)
                    else:
                        return None  # No BLP

    add_rest_of_groups(merged_groups, equal_groups, graph)

    tuples_merged_groups = []
    for g in merged_groups:
        tuples_merged_groups.append(tuple(g))

    return tuples_merged_groups


def add_to_merged_groups(merged_groups, equal_groups, f0, f1):
    for group in merged_groups:
        if f0 in group and f1 in group:
            return
        if f0 in group:
            group.append(f1)
            return
        if f1 in group:
            group.append(f0)
            return

    temp_group = [f0, f1]
    temp_group = temp_group + equal_groups[f0]
    merged_groups.append(temp_group)


def add_rest_of_groups(merged_groups, equal_groups, graph):
    for file in equal_groups:
        flag = True
        for group in merged_groups:
            if file in group:
                flag = False
                break
        if flag:
            temp_group = [file]
            temp_group = temp_group + equal_groups[file]
            merged_groups.append(temp_group)

    for node in graph.nodes():
        flag = True
        for group in merged_groups:
            if node in group:
                flag = False
                break

        if flag:
            temp_group = [node]
            merged_groups.append(temp_group)


def sort_groups(merged_groups, graph):
    ratio_dict = {}
    for g0, g1 in it.combinations(merged_groups, 2):
        ratio_dict[(g0, g1)] = find_classification_ratio(g0, g1, graph)

    sorted_list = {}
    for i in range(len(merged_groups)):
        if len(ratio_dict) is 1:
            last_item = ratio_dict.popitem()
            if last_item[1] == "<":
                sorted_list[2] = last_item[0][1]
                sorted_list[1] = last_item[0][0]
            else:
                sorted_list[2] = last_item[0][0]
                sorted_list[1] = last_item[0][1]
            break
        sorted_list[len(merged_groups) - i] = find_biggest(ratio_dict)
        ratio_dict = create_new_ration_list(ratio_dict, sorted_list[len(merged_groups) - i])

    return sorted_list


def find_classification_ratio(g0, g1, graph):
    for n in g0:
        for m in g1:
            if (n in graph.users) == (m in graph.users):
                continue  # we are not interested in file-file or user-user connections
            if graph[n, m]:
                if check_all_connected(g0, g1, graph):
                    return '<'
            elif graph[m, n]:
                if check_all_connected(g1, g0, graph):
                    return '>'
            else:
                return None


def check_all_connected(g0, g1, graph):
    for n in g0:
        for m in g1:
            if (n in graph.users) == (m in graph.users):
                continue  # we are not interested in file-file or user-user connections
            if graph[n, m] is None:
                return False

    return True


def find_biggest(ratio_dict):
    biggest = None
    for t in ratio_dict:
        if ratio_dict[t] == ">":
            if biggest is None:
                biggest = t[0]
            elif biggest == t[0]:
                continue
            elif ((t[0], biggest) in ratio_dict and ratio_dict[(t[0], biggest)] is ">") or ((biggest, t[0]) in ratio_dict and ratio_dict[(biggest, t[0])] is "<"):
                biggest = t[0]
        elif ratio_dict[t] == "<":
            if biggest is None:
                biggest = t[1]
            elif biggest == t[1]:
                continue
            elif ((t[1], biggest) in ratio_dict and ratio_dict[(t[1], biggest)] is ">") or ((biggest, t[1]) in ratio_dict and ratio_dict[(biggest, t[1])] is "<"):
                biggest = t[1]

    return biggest


def create_new_ration_list(ratio_dict, x):
    new_ratio_dict = {}
    for t in ratio_dict:
        if t[0] != x and t[1] != x:
            new_ratio_dict[t] = ratio_dict[t]

    return new_ratio_dict
