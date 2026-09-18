"""Create small, reproducible synthetic leaf images for a runnable demo."""

from pathlib import Path

import cv2
import numpy as np


def create_leaf(kind: str, output: Path) -> None:
    canvas = np.full((420, 520, 3), (235, 235, 235), dtype=np.uint8)
    center, axes, angle = (260, 230), (125, 190), 22
    colour = {"healthy": (45, 150, 35), "stressed": (35, 175, 185), "diseased": (25, 105, 130)}[kind]
    cv2.ellipse(canvas, center, axes, angle, 0, 360, colour, -1)
    cv2.ellipse(canvas, center, axes, angle, 0, 360, (35, 90, 20), 3)
    cv2.line(canvas, (205, 385), (300, 65), (180, 235, 185), 3)

    if kind == "stressed":
        for point in [(215, 175), (280, 250), (245, 300)]:
            cv2.circle(canvas, point, 25, (30, 185, 215), -1)
    if kind == "diseased":
        for point, radius in [((210, 170), 38), ((290, 245), 43), ((250, 310), 28), ((300, 130), 22)]:
            cv2.circle(canvas, point, radius, (25, 65, 100), -1)
            cv2.circle(canvas, point, max(5, radius - 10), (20, 40, 70), -1)
    cv2.imwrite(str(output), canvas)


def main() -> None:
    folder = Path("samples")
    folder.mkdir(exist_ok=True)
    for kind in ("healthy", "stressed", "diseased"):
        create_leaf(kind, folder / f"{kind}_leaf.png")
        print(f"Created samples/{kind}_leaf.png")


if __name__ == "__main__":
    main()
