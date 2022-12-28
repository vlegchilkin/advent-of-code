def cyk(rules, text, weights=None, backtrack=False):
    """
    https://en.wikipedia.org/wiki/CYK_algorithm
    """
    n = len(text)
    props = [[dict() for _ in range(n)] for _ in range(n)]

    for j in range(0, n):  # end pos

        for lhs, rule in rules.items():  # terminals
            for rhs in rule:
                if len(rhs) == 1 and rhs[0] == text[j]:
                    props[j][j][lhs] = {"weight": 0, "path": [lhs] if backtrack else None}

        for i in range(j - 1, -1, -1):  # start pos
            for k in range(i, j):
                for lhs, rule in rules.items():
                    for rhs in rule:
                        if (
                            len(rhs) == 2
                            and (left := props[i][k].get(rhs[0]))
                            and (right := props[k + 1][j].get(rhs[1]))
                        ):
                            if weights:
                                weight = left["weight"] + right["weight"] + (weights.get(lhs) or 0)
                            else:
                                weight = 0

                            path = [lhs, left["path"], right["path"]] if backtrack else None

                            if lhs in props[i][j]:
                                lhs_props = props[i][j][lhs]
                                if lhs_props["weight"] > weight:
                                    lhs_props["weight"] = weight
                                    lhs_props["path"] = path
                            else:
                                props[i][j][lhs] = {"weight": weight, "path": path}

    return props[0][n - 1]
