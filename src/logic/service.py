from src.models.base import XRepository as REPO, Progress
from src.logic.calculator import Xplus, to_list_xs


def organize_nodes(repo: REPO, border: Progress = Progress.story_clear):
    data = {x: Xplus(x) for x in repo}

    while True:
        updated = False

        for x in data:

            synthesis, score = data[x].best_synthesis(data, border)

            if not synthesis:
                continue

            current_score = (data[x].show.effort, data[x].show.rank)
            if data[x].synthesis and score >= current_score:
                continue

            data[x].update_status(synthesis, data)
            updated = True

        if not updated:
            break

    for x in data:
        xp = data[x]
        if not xp.is_valid:
            continue

        for ys in xp.synthesis.xs:
            ys.is_root = False

    return data


def arrange_list_xs(repo: REPO, border: Progress):
    return to_list_xs(organize_nodes(repo, border))
