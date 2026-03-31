from typing import List

from src.models.base_for_view import Xshow, SynthesisShow
from src.models.symbols import Symbols


def count_needed(xs: Xshow, data: dict[Xshow, int] | None = None):
    if data is None:
        data = {}

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


def describe_tree(xs: Xshow, list_process: List[SynthesisShow] | None = None):
    if list_process is None:
        list_process = []

    if xs.is_tip:
        return list_process
    else:
        synthesis = xs.synthesis
        list_process.append(synthesis)
        for ys in synthesis.xs:
            list_process = describe_tree(ys, list_process)
        return list_process


def describe_process(xs: Xshow):
    list_process = describe_tree(xs)
    return sorted(list_process, key=lambda synthesis: synthesis.ys.effort)


def build_mermaid_part(xs: Xshow, list_process: List[SynthesisShow] | None = None):
    if list_process is None:
        list_process = []

    if xs.is_tip:
        return list_process

    list_process = add_synthesis(list_process, xs.synthesis)
    for ys in xs.connect:
        list_process = build_mermaid_part(ys, list_process)
    return list_process


def add_synthesis(list_process: List[SynthesisShow], synthesis: SynthesisShow):
    if synthesis in list_process:
        return list_process
    list_process.append(synthesis)
    return list_process


def quote_dot_id(name: str) -> str:
    return f'"{name.replace("\"", "\\\"")}"'


def quote_dot_label(label: str) -> str:
    return f'"{label.replace("\"", "\\\"")}"'


def merge_text(list_process: List[SynthesisShow]):
    mm_code = "digraph {\n"
    mm_code += "layout=dot;\n"
    mm_code += 'rankdir="BT";\n'

    mm_code += "node [shape=point,width=0];\n"
    for synthesis in list_process:
        mm_code += f"{quote_dot_id('p' + synthesis.ys.name)}\n"

    mm_code += "node [shape=ellipse];\n"
    for synthesis in list_process:
        ys = synthesis.ys
        for xs in synthesis.xs:
            mm_code += f"    {quote_dot_id(xs.name)} -> {quote_dot_id('p' + ys.name)} [dir=none];\n"

        text_catalyst = (
            f" [label={quote_dot_label(synthesis.catalyst.label)}]"
            if synthesis.catalyst
            else ""
        )
        mm_code += f"    {quote_dot_id('p' + ys.name)} -> {quote_dot_id(ys.name)}{text_catalyst};\n"

    mm_code += "}"
    return mm_code


def build_mermaid_text(xs: Xshow):
    list_process = build_mermaid_part(xs)
    return merge_text(list_process)


def search_children(
    root: Xshow, xs: Xshow | None = None, list_children: List[Xshow] | None = None
):
    if list_children is None:
        list_children = []

    if not xs:
        xs = root

    if (xs != root) and (not xs in list_children):
        list_children.append(xs)

    if xs.is_tip:
        return list_children
    else:
        for ys in xs.connect:
            list_children = search_children(root, ys, list_children)
    return list_children


def decide_icon_for_page(xs: Xshow):
    if xs.is_root:
        return Symbols.flower
    elif xs.is_tip:
        return Symbols.bud
    else:
        return Symbols.middle


def name_for_show(xs: Xshow):
    icon = decide_icon_for_page(xs)
    return f"{icon.value} {xs.name}"
