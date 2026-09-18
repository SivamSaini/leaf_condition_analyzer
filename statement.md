# Project Statement: Leaf Condition Analyzer

## Problem Statement

Leaf colour changes such as yellowing and browning can indicate stress or disease. Manual visual inspection is subjective. This project uses computer vision to measure visible green, yellow, and brown regions in a leaf image and provide a transparent screening result.

## Scope

The application accepts a leaf image from the command line, segments relevant colours in HSV space, calculates colour percentages, classifies the visible condition, and saves an annotated output image. It does not identify plant species or diagnose a specific disease.

## Target Users

- Students learning computer vision and image processing
- Educators evaluating HSV segmentation and rule based classification
- Gardeners who want a simple educational leaf colour screening demonstration

## High Level Features

- Generate reproducible sample leaf images
- Accept JPG, JPEG, and PNG images through the command line
- Detect green, yellow, and brown regions using HSV colour masks
- Classify the visible condition using measured percentages
- Save an annotated image and print a clear terminal result
- Run automated tests for core classification cases
