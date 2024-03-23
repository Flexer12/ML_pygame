# Функция волнового алгоритма, позволяющая определить путь одной клетки к другой
def has_path(map_ai, x1, y1, x2, y2):
    d = {(x1, y1): 0}
    v = [(x1, y1)]
    parent = {}  # to store the parent of each visited node
    while len(v) > 0:
        x, y = v.pop(0)
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx * dy != 0:
                    continue
                if x + dx < 0 or x + dx >= len(map_ai[0]) or y + dy < 0 or y + dy >= len(map_ai):
                    continue
                if map_ai[y + dy][x + dx] == 0:
                    dn = d.get((x + dx, y + dy), -1)
                    if dn == -1:
                        d[(x + dx, y + dy)] = d.get((x, y), -1) + 1
                        v.append((x + dx, y + dy))
                        parent[(x + dx, y + dy)] = (x, y)  # store the parent of each visited node

    # backtracking to find the path
    if (x2, y2) not in parent:
        return [], False

    path = [(x2, y2)]
    while path[-1] != (x1, y1):
        path.append(parent[path[-1]])
    path.reverse()
    return path
