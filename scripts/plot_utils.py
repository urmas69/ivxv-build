def _avg_rgb_from_image(path_img):
    try:
        import matplotlib.image as mpimg
    except Exception:
        return None
    try:
        img = mpimg.imread(path_img)
    except Exception:
        return None
    if img is None or img.size == 0:
        return None
    if img.max() > 1.0:
        img = img / 255.0
    if img.shape[-1] == 4:
        img = img[..., :3]
    r, g, b = img[..., 0].mean(), img[..., 1].mean(), img[..., 2].mean()
    return (r, g, b)


def plot_seat_pies(path_out, party_name_by_code, seats_paper, seats_actual, seats_e):
    import matplotlib.pyplot as plt

    parties = sorted(set(seats_paper) | set(seats_actual) | set(seats_e))

    def values(d):
        return [d.get(p, 0) for p in parties]

    labels = [party_name_by_code.get(p, p) or p for p in parties]

    ee200_color = _avg_rgb_from_image("e200.jpg")
    colors_by_party = {
        "REF": "#f4d03f",
        "EKRE": "#000000",
        "KESK": "#2e7d32",
        "EE200": ee200_color or "#6fa8dc",
        "SDE": "#d32f2f",
        "IE": "#1565c0",
    }
    colors = [colors_by_party.get(p, "#b0b0b0") for p in parties]

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle("RK 2023 – Seat distribution (paper / actual / e-votes)")

    for ax, title, data in [
        (axes[0], "Paper ballots", seats_paper),
        (axes[1], "Actual", seats_actual),
        (axes[2], "Electronic votes", seats_e),
    ]:
        vals = values(data)
        vals2 = [v for v in vals if v > 0]
        ax_colors = [c for v, c in zip(vals, colors) if v > 0]
        _, _, autotexts = ax.pie(
            vals2,
            labels=None,
            colors=ax_colors,
            autopct=lambda p: f"{int(round(p/100*sum(vals2)))}" if p > 0 else "",
        )
        for t in autotexts:
            t.set_color("white")
        ax.set_title(title)
        ax.axis("equal")

    fig.legend(labels, loc="lower center", ncol=min(len(labels), 6))
    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    fig.savefig(path_out, dpi=200)
    plt.close(fig)
