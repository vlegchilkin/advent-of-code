from typing import Optional


def cyk(rules, text, rule_weights=None, backtrack=False) -> [dict, Optional[dict]]:
    """
    https://en.wikipedia.org/wiki/CYK_algorithm
    """
    n = len(text)
    weights = [[dict() for _ in range(n)] for _ in range(n)]
    paths = [[dict() for _ in range(n)] for _ in range(n)] or None

    for j in range(0, n):  # end pos

        for lhs, rule in rules.items():  # terminals
            for rhs in rule:
                if len(rhs) == 1 and rhs[0] == text[j]:
                    weights[j][j][lhs] = 0
                    if backtrack:
                        paths[j][j][lhs] = [lhs]

        for i in range(j - 1, -1, -1):  # start pos
            for k in range(i, j):
                for lhs, rule in rules.items():
                    for rhs in rule:
                        if (
                            len(rhs) == 2
                            and (l_weight := weights[i][k].get(rhs[0])) is not None
                            and (r_weight := weights[k + 1][j].get(rhs[1])) is not None
                        ):
                            weight = l_weight + r_weight + ((rule_weights.get(lhs) or 0) if rule_weights else 0)
                            best_weight = weights[i][j].get(lhs)
                            if best_weight is None or best_weight > weight:
                                weights[i][j][lhs] = weight
                                if backtrack:
                                    paths[i][j][lhs] = [lhs, paths[i][k].get(rhs[0]), paths[k + 1][j].get(rhs[1])]

    return weights[0][n - 1], paths[0][n - 1] if paths else None


def make_cnf(rules) -> dict:
    doubles = {v: rep for rep, val in rules.items() for v in val if len(v) == 2}
    mapping = {}

    def get_mapped(st) -> str:
        if st not in mapping:
            mapping[st] = chr(len(mapping) + ord("А"))
        return mapping[st]

    def split(st):
        nonlocal doubles

        if len(st) > 2:
            x = st
            while len(x) != 2:
                if len(x) > 3:
                    x = split(x[:2]) + split(x[2:])
                else:
                    x = x[0] + split(x[1:])
            return x

        if st not in doubles:
            x = get_mapped(st)
            doubles[st] = x
            rules[x] = [st]

        return doubles[st]

    for rep in list(rules):
        new_val = []
        for v in rules[rep]:
            if len(v) <= 2:
                new_val.append(v)
            else:
                new_val.append(split(v))
        rules[rep] = new_val

    return rules
