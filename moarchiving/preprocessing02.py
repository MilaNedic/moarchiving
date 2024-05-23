import numpy as np
from hv_plus import clear_point, DLNode, setup_cdllist, hv3dplus
from sortedcontainers import SortedList

def outerDelimiterx(p, head, di):
    """Find the point with the smallest y > py such that qx < px"""
    current = head.next[di]
    candidate = None
    while current != head:
        if current.x[1] > p.x[1] and current.x[0] < p.x[0]:
            if candidate is None or current.x[1] < candidate.x[1]:
                candidate = current
        current = current.next[di]
    return candidate

def outerDelimitery(p, head, di):
    """Find the point with the largest x < px such that qy < py"""
    current = head.next[di]
    candidate = None
    while current != head:
        if current.x[0] < p.x[0] and current.x[1] < p.x[1]:
            if candidate is None or current.x[0] > candidate.x[0]:
                candidate = current
        current = current.next[di]
    return candidate

def preprocessing(head, d):
    di = d - 1
    current = head.next[di]
    stop = head.prev[di]

    # Initialize AVL-like sorted list to maintain order based on y-coordinate
    avl_tree = SortedList(key=lambda node: (node.x[1], node.x[0]))

    # Add sentinel nodes at the start and end
    avl_tree.add(head)  # head is the starting sentinel
    avl_tree.add(head.prev[di])  # head.prev[di] is the ending sentinel

    while current != stop:
        avl_tree.add(current)
        index = avl_tree.index(current)

        # Set closest[0] and closest[1] ensuring that current does not point to itself
        if index > 0 and avl_tree[index - 1] != current:
            current.closest[0] = avl_tree[index - 1]
        else:
            current.closest[0] = head

        if index + 1 < len(avl_tree) and avl_tree[index + 1] != current:
            current.closest[1] = avl_tree[index + 1]
        else:
            current.closest[1] = head.prev[di]

        # Remove dominated nodes
        dominated = [node for node in avl_tree if node != current and all(node.x[i] <= current.x[i] for i in range(3))]
        for node in dominated:
            avl_tree.remove(node)
            node.ndomr = 1

        current = current.next[di]

    # Clear AVL tree after processing
    avl_tree.clear()


data_points = [
    13, 3, 15,
    7, 15, 2,
    1, 17, 16,
    12, 9, 1,
    4, 5, 15
]
ref_point = [20, 20, 20]
n_points = int(len(data_points)/3)
dimension = 3

# Set up the circular doubly linked list
head = setup_cdllist(data_points, n_points, dimension, ref_point)

preprocessing(head, 3)

# Print results
current = head.next[2]  # Start from the first real node
print("Closest nodes after preprocessing")
while current != head:
    print(f"Node: {current.x}, \nClosest[0]: {current.closest[0].x if current.closest[0] else 'None'}, \nClosest[1]: {current.closest[1].x if current.closest[1] else 'None'}, \n")
    current = current.next[2]
print("---------------------------------------------")
print("\n")
hv3d = hv3dplus(head)
print("---------------------------------------------")
print("Hypervolume in 3d:", hv3d)