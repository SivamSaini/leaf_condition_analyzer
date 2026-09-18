"""Image-analysis functions for simple leaf-condition screening.

The classifier intentionally uses transparent HSV colour rules rather than a
pretrained black-box model.  It is suitable for a classroom demonstration,
not for agricultural or medical decision-making.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


@dataclass(frozen=True)
class AnalysisResult:
    label: str
    confidence: float
    green_percent: float
    yellow_percent: float
    brown_percent: float
    leaf_percent: float
    message: str


def _percent(mask: np.ndarray, denominator: int) -> float:
    return round(100.0 * int(np.count_nonzero(mask)) / max(denominator, 1), 2)


def analyze_image(image: np.ndarray) -> tuple[AnalysisResult, np.ndarray]:
    """Classify a BGR image and return the result plus an annotated copy."""
    if image is None or image.size == 0:
        raise ValueError("The image is empty or could not be decoded.")

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Saturated plant-like colours.  The union is our estimated leaf region.
    green = cv2.inRange(hsv, np.array([35, 45, 35]), np.array([90, 255, 255]))
    yellow = cv2.inRange(hsv, np.array([18, 55, 50]), np.array([35, 255, 255]))
    brown = cv2.inRange(hsv, np.array([5, 45, 20]), np.array([18, 255, 210]))
    leaf = cv2.bitwise_or(cv2.bitwise_or(green, yellow), brown)

    # Remove isolated pixel noise from the colour masks.
    kernel = np.ones((3, 3), np.uint8)
    leaf = cv2.morphologyEx(leaf, cv2.MORPH_OPEN, kernel)
    leaf_pixels = int(np.count_nonzero(leaf))
    total_pixels = image.shape[0] * image.shape[1]
    leaf_percent = _percent(leaf, total_pixels)

    if leaf_percent < 2.0:
        result = AnalysisResult(
            "No leaf region detected", 0.0, 0.0, 0.0, 0.0, leaf_percent,
            "Use a well-lit photo with one leaf occupying a larger part of the frame.",
        )
        return result, _annotate(image, leaf, result)

    green_percent = _percent(cv2.bitwise_and(green, leaf), leaf_pixels)
    yellow_percent = _percent(cv2.bitwise_and(yellow, leaf), leaf_pixels)
    brown_percent = _percent(cv2.bitwise_and(brown, leaf), leaf_pixels)

    damaged = yellow_percent + brown_percent
    if brown_percent >= 20 or damaged >= 45:
        label = "Likely diseased or severely stressed"
        confidence = min(99.0, 55 + damaged)
        message = "Large yellow/brown areas were found. Inspect the plant and consult a local expert."
    elif damaged >= 15:
        label = "Possible stress or early disease"
        confidence = min(95.0, 50 + damaged * 1.5)
        message = "Some yellow/brown colour is present. Check watering, nutrients, and pests."
    else:
        label = "Mostly healthy-looking"
        confidence = min(99.0, 60 + green_percent * 0.4)
        message = "The detected leaf area is predominantly green. Continue regular monitoring."

    result = AnalysisResult(label, round(confidence, 2), green_percent, yellow_percent,
                            brown_percent, leaf_percent, message)
    return result, _annotate(image, leaf, result)


def analyze_path(path: str | Path) -> tuple[AnalysisResult, np.ndarray]:
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"Could not read image: {path}")
    return analyze_image(image)


def _annotate(image: np.ndarray, leaf_mask: np.ndarray, result: AnalysisResult) -> np.ndarray:
    annotated = image.copy()
    contours, _ = cv2.findContours(leaf_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(annotated, contours, -1, (255, 255, 255), 2)
    lines = [
        result.label,
        f"Confidence: {result.confidence:.1f}%",
        f"Green {result.green_percent:.1f}% | Yellow {result.yellow_percent:.1f}% | Brown {result.brown_percent:.1f}%",
    ]
    y = 28
    for line in lines:
        cv2.putText(annotated, line, (12, y), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(annotated, line, (12, y), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    (255, 255, 255), 1, cv2.LINE_AA)
        y += 25
    return annotated
