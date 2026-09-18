# Project Report: Leaf Condition Analyzer

## 1. Project title

Leaf Condition Analyzer Using Computer Vision

## 2. Problem statement

Leaves can show visual signs of stress through yellowing and browning. Manual inspection is slow and subjective. This project demonstrates how computer vision can quantify visible colour changes in a leaf photograph and produce a simple, reproducible screening result.

## 3. Objective

To build a command line application that accepts a leaf image, detects approximate green, yellow, and brown regions, classifies the visible condition, and saves an annotated output image.

## 4. Scope

The system categorizes a visible leaf as mostly healthy looking, possibly stressed/early disease, likely diseased/severely stressed, or no leaf region detected. It does not diagnose plant species or a particular disease.

## 5. Tools and technologies

- Python 3
- OpenCV: image loading, HSV conversion, thresholding, morphology, annotation
- NumPy: matrix and array operations
- unittest: automated verification

## 6. Methodology

The input BGR image is converted to HSV, because HSV separates colour from brightness more clearly than raw RGB/BGR values. Predefined HSV thresholds generate green, yellow, and brown masks. Their union estimates the visible leaf. Morphological opening removes isolated noise pixels. The program then calculates each colour mask as a percentage of the leaf mask and applies documented rules:

| Condition | Rule |
| --- | --- |
| Likely diseased/severely stressed | brown ≥ 20% or yellow + brown ≥ 45% |
| Possible stress/early disease | yellow + brown ≥ 15% |
| Mostly healthy looking | otherwise |

The output image shows the estimated leaf contour and analysis values.

## 7. Implementation and execution

The source code is split into a reusable analysis module (`src/analyzer.py`), a command line interface (`src/main.py`), and a demo image generator (`src/generate_demo_images.py`). The project is executed with:

```bash
python -m src.generate_demo_images
python -m src.main --image samples/healthy_leaf.png --output results/healthy_annotated.png
```

## 8. Testing

Automated tests validate three core cases: a green image is classified as mostly healthy looking, a brown image is flagged as likely diseased/severely stressed, and a blank image produces no leaf detection. Run them with:

```bash
python -m unittest discover -s tests -v
```

## 9. Results

The included sample generator creates healthy, stressed, and diseased style synthetic leaf images. The analyzer produces a console classification and an annotated PNG for each. These samples make the application reproducible even without a downloaded dataset.

## 10. Limitations and future work

The HSV thresholds are sensitive to illumination, background objects, and crop type. Future work could use a labelled public dataset, leaf segmentation with a trained model, and a CNN classifier to distinguish named diseases. A calibration stage for camera and crop type could also improve reliability.

## 11. Conclusion

This project demonstrates an end to end computer vision workflow: image input, colour space conversion, segmentation, feature measurement, transparent classification, visual output, and automated tests. It is lightweight, explainable, and executable entirely from the terminal.
