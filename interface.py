"""いい感じにまとめる"""

from typing import List

from structure_for_synthesis import XRepository as REPO


class Xshow:
    def __init__(
        self,
        name: str,
        catalyst: str,
        connect: List["Xshow"],
        rank: int,
        effort: int,
        is_special: bool,
    ):
        self.name = name
        self.catalyst = catalyst
        self.connect = connect
        self.rank = rank
        self.effort = effort
        self.is_special = is_special


class Xplus:
    def __init__(
        self,
        is_completed: bool = False,
        rank: int = 0,
        effort: int = 1,
        is_root: bool = True,
        connect: Xshow = None,
    ):
        self.is_completed = is_completed
        self.rank = rank
        self.effort = effort
        self.connect = connect
        self.is_root = is_root


def arrange(repo: REPO):
    data = {key: Xplus() for key in repo}
    for x in data:
        if x.connect == []:
            data[x].rank = 0
            data[x].connect = Xshow(x.name, x.catalyst, [], 0, 1, True)

            data[x].is_completed = True

    while True:
        updated = False

        for x in data:
            if data[x].is_completed:
                continue
            else:
                if all(data[y].is_completed for y in x.connect):
                    data[x].rank = max([data[y].rank for y in x.connect]) + 1
                    data[x].effort = sum([data[y].effort for y in x.connect]) + 1
                    data[x].connect = Xshow(
                        x.name,
                        x.catalyst,
                        [data[y].connect for y in x.connect],
                        data[x].rank,
                        data[x].effort,
                        True,
                    )
                    data[x].is_completed = True
                    updated = True

        if not updated:
            break

    # 親子関係から非ルートノードを判定
    for x in data:
        # x の元の依存関係（親）を反復
        if x.connect:  # 依存関係がある = 子を持つ
            for child in x.connect:
                data[child].is_root = False
                data[child].connect.is_special = False

    if any(not data[x].is_completed for x in data):
        raise ValueError("未解決ノードあり（循環の可能性）")

    sorted_roots = sorted(
        [x for x in data if (data[x].is_root) or (x.connect)],
        key=lambda x: (data[x].effort, data[x].rank),
        reverse=True,
    )
    list_xs = [data[x].connect for x in sorted_roots]

    return list_xs


def count_needed(xs: Xshow, data: dict[Xshow, int]):
    if xs.connect == []:
        if xs in data:
            data[xs] += 1
        else:
            data[xs] = 1
        return data
    else:
        for ys in xs.connect:
            data = count_needed(ys, data)
        return data


def describe_tree(xs: Xshow, list_process: List[Xshow]):
    if xs.connect == []:
        return list_process
    else:
        list_process.append(xs)
        for ys in xs.connect:
            list_process = describe_tree(ys, list_process)
        return list_process


def describe_process(xs: Xshow):
    list_process = describe_tree(xs, [])
    return sorted(list_process, key=lambda xs: xs.rank)


def build_mermaid_part(
    xs: Xshow, list_text: List[tuple[str, str]], list_point: List[str]
) -> tuple[List[tuple[str, str]], List[str]]:
    if xs.connect == []:
        return list_text, list_point
    else:
        joint = f"p{xs.name}"
        for ys in xs.connect:
            list_text, list_point = build_mermaid_part(ys, list_text, list_point)
            if not ((f'"{ys.name}"', f"{joint} [dir=none]") in list_text):
                list_text.append((f'"{ys.name}"', f"{joint} [dir=none]"))
        text_catalyst = f' [label="{xs.catalyst}"]' if xs.catalyst else ""
        if not ((joint, xs.name + text_catalyst) in list_text):
            list_text.append((joint, xs.name + text_catalyst))
        list_point.append(joint)
        return list_text, list_point


def build_mermaid_text(xs: Xshow):
    list_text, list_point = build_mermaid_part(xs, [], [])
    return merge_text(list_text, list_point)


def merge_text(list_text: List[str], list_point: List[str], style: str = "dot"):

    mm_code = "digraph {\n"
    mm_code += f"layout={style};\n"

    mm_code += "node[shape=point,width=0]\n"
    for point in list_point:
        mm_code += f"{point}\n"

    mm_code += "node[shape=ellipse]"
    for start, end in list_text:
        mm_code += f"    {start} -> {end}\n"

    mm_code += "}"
    return mm_code


def search_children(root: Xshow, xs: Xshow, list_children: List[Xshow]) -> List[Xshow]:
    if xs.connect == []:
        return list_children
    else:
        if (xs != root) and (not xs in list_children):
            list_children.append(xs)
        for ys in xs.connect:
            list_children = search_children(root, ys, list_children)
    return list_children


def build_all_tree(list_xs: List[Xshow]):
    list_text, list_point = [], []
    for xs in list_xs:
        list_text, list_point = build_mermaid_part(xs, list_text, list_point)
    return merge_text(list_text, list_point)
