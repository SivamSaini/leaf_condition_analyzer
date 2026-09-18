# Leaf Condition Analyzer

A command line computer vision project that screens a leaf image for visible green, yellow, and brown regions. It estimates whether a leaf appears mostly healthy, possibly stressed, or likely diseased or severely stressed, and saves an annotated result image.


## Features

- Fully command line executable; no GUI or internet connection is required after installation.
- Uses OpenCV HSV colour segmentation and morphological filtering.
- Prints colour area measurements, classification, confidence, and a practical note.
- Saves an annotated image with the detected leaf contour.
- Includes a reproducible demo image generator and automated tests.

## Requirements

- Python 3.10 or newer
- pip

## Setup

Clone the repository and enter its root directory:

```bash
git clone https://github.com/SivamSaini/leaf_condition_analyzer.git
cd leaf_condition_analyzer
```

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the project

First generate the reproducible sample images:

```bash
python -m src.generate_demo_images
```

Analyze one of them:

```bash
python -m src.main --image samples/healthy_leaf.png --output results/healthy_annotated.png
```

Analyze your own image:

```bash
python -m src.main --image path/to/leaf.jpg --output results/annotated_leaf.png
```

For machine readable output, add `--json`:

```bash
python -m src.main --image samples/diseased_leaf.png --json
```

Use a close, well lit photo containing one leaf against a plain background for the most reliable result.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
src/analyzer.py              Core computer vision analysis
src/main.py                  Command line interface
src/generate_demo_images.py  Reproducible sample image generator
tests/test_analyzer.py        Automated tests
REPORT.md                    Structured project report
```

## Method

1. Convert the input image from BGR to HSV colour space.
2. Create masks for green, yellow, and brown colour ranges.
3. Combine masks to estimate the leaf region and remove small noise.
4. Calculate each colour's percentage of the detected leaf region.
5. Apply transparent rules to assign one of three condition categories.

## Limitations

Lighting, background colours, camera quality, and leaf species can affect results. The project uses generic colour heuristics rather than a trained disease recognition dataset; therefore its result is a visual screen, not a diagnosis.

## License

MIT License. Adapt and cite any external material you add before submitting coursework.
