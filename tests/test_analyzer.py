import numpy as np

from src.analyzer import analyze_image


def test_green_image_is_mostly_healthy():
    image = np.full((100, 100, 3), (40, 160, 40), dtype=np.uint8)
    result, _ = analyze_image(image)
    assert result.label == "Mostly healthy-looking"
    assert result.green_percent > 95


def test_brown_image_is_flagged():
    image = np.full((100, 100, 3), (20, 60, 100), dtype=np.uint8)
    result, _ = analyze_image(image)
    assert result.label == "Likely diseased or severely stressed"
    assert result.brown_percent > 95


def test_blank_image_has_no_leaf_region():
    image = np.full((100, 100, 3), 240, dtype=np.uint8)
    result, _ = analyze_image(image)
    assert result.label == "No leaf region detected"
