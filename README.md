# Warehouse Store User Spending

This repository contains the code, data processing scripts, and model training code for our project, Warehouse Store User Spending. Our goal is to develop a robust object detection pipeline for counting cars in parking lots of warehouse stores (e.g., Costco) in Northeast USA. We achieve this by using Google Maps APIs (Text Search API and Street View API) to gather parking lot images and then applying a deep learning model (YOLOv5) to count cars. The car counts serve as an indicator of store traffic and can be used to infer user spending patterns.

Repository: [https://github.com/aryamonani/warehouse-store-user-spending.git](https://github.com/aryamonani/warehouse-store-user-spending.git)

---

## Table of Contents

- [Overview](#overview)
- [Dataset and Data Acquisition](#dataset-and-data-acquisition)
- [Training Process](#training-process)
- [Output Files Explanation](#output-files-explanation)
- [Challenges and Limitations](#challenges-and-limitations)
- [Infrastructure and Resource Choices](#infrastructure-and-resource-choices)
- [Repository Structure](#repository-structure)
- [Future Work](#future-work)
- [References](#references)

---

## Overview

This project aims to gather information about warehouse stores like Costco in Northeast USA using Google Maps APIs (such as the Text Search API and Street View API) to get images of parking lots at these stores. We then apply a deep learning model (YOLOv5) to count the number of cars in those parking lots. The car counts serve as an indicator of store traffic and potentially user spending patterns.

---

## Dataset and Data Acquisition

### Google Maps APIs
- **Text Search API:**  
  Utilized to search for warehouse store locations in the Northeast USA.
- **Street View API:**  
  Employed to obtain images of parking lots for these locations.

### Aerial Cars Dataset
- We incorporated the publicly available [Aerial Cars Dataset](https://github.com/jekhor/aerial-cars-dataset), which provides aerial images and annotations.
- The dataset was reorganized into two folders:
  - **images/** – Contains the aerial images.
  - **labels/** – Contains the annotation files converted into YOLO format.
- A custom YAML configuration file (`aerial_data.yaml`) was created to define the dataset paths and class names:
  ```yaml
  train: /content/drive/MyDrive/DSCI_511_Project/aerial-cars-dataset/images
  val: /content/drive/MyDrive/DSCI_511_Project/aerial-cars-dataset/images
  nc: 1
  names: ['car']

---

## Training Process

### 1. Environment Setup

- **Google Colab Free GPU:**  
  Initially used for rapid prototyping with a free GPU. However, limitations such as runtime disconnects and slow I/O (due to Google Drive) proved challenging.

- **Drexel’s TUX Server:**  
  For extended and stable training sessions, we migrated to Drexel’s TUX server. This environment provided dedicated computational resources and stability needed for fine-tuning our YOLOv5 model.

### 2. Data Preparation

- The Aerial Cars Dataset was reorganized into separate folders for images and labels.
- Annotations were converted to YOLO format as needed.
- A custom YAML file (`aerial_data.yaml`) was configured to reflect the dataset paths.

### 3. Model Training

- We fine-tuned a pretrained YOLOv5s model on our dataset.
- Training began on Colab for initial experiments but was eventually shifted to Drexel’s TUX server to avoid free GPU session limitations.
- The final checkpoint (e.g., `best.pt` stored under `runs/train/exp14`) is used for inference.

### 4. Inference and Post-Processing

- After training, the model is applied to new parking lot images (collected via Google Maps APIs) to detect and count cars.
- The inference scripts generate several JSON files:

  - **`records.json`:**  
    Contains detailed metadata and raw detection results for each image (e.g., timestamps, store identifiers, bounding box coordinates, and confidence scores). This file serves as a comprehensive log of the detection process.

  - **`car_counts.json`:**  
    Provides a simplified summary mapping each store (identified by its image filename, stored as `store_code`) to the number of detected cars (`no of cars`). This is used for quick evaluation and further analysis.

  - **`final_results.json`:**  
    Combines the car count data with additional post-processing metrics and aggregated statistics. This file is intended as the final deliverable for the analysis pipeline, supporting further business insights and decision-making.

---

## Output Files Explanation

- **`records.json`:**  
  This file logs detailed information for each processed image. It includes raw detection outputs such as bounding box coordinates, confidence levels, and other metadata from the inference process. Researchers can use this file to analyze detection performance, adjust thresholds, and identify potential issues in the detection pipeline.

- **`car_counts.json`:**  
  This file summarizes the detections by mapping each store’s image filename (as `store_code`) to the total number of cars detected (`no of cars`). It provides a quick, high-level overview of parking lot occupancy for further statistical analysis.

- **`final_results.json`:**  
  After additional post-processing and validation, this file aggregates the results (including potential error metrics and other derived statistics) to produce a final summary. It represents the end result of the inference pipeline, ready for integration with other business analytics tools.

---

## Challenges and Limitations

### Code Files and Integration Challenges

- **Integration of Multiple Code Files:**  
  Our codebase includes three key files: `image_server.py`, `run.py`, and `server.py`, which handle location searching, map retrieval, and API-based data processing.

  - **`image_server.py`:**  
    Implements a Flask server that provides a `/mapview` API endpoint.
    Uses `Google Maps Geocoding API` to obtain latitude and longitude from a given text query (e.g., a city or store name).
    Constructs a `Google Static Maps API` URL to fetch a satellite image of the location.
    Returns the location’s coordinates and a URL to the static map image.

  - **`run.py`:**  
    Retrieves a list of counties from a` U.S. Census Bureau` data source.
    Uses the `/ggmap` API (from `server.py`) to search for stores with parking in a given county.
    Calls the `/mapview` API (from `image_server.py`) to obtain a static map of the store locations.
    Saves results in `records.json` and downloads the map images.

  - **`server.py`:**  
    Implements a Flask server providing a `/ggmap` API endpoint.
    Uses `Google Places Text Search API` to find store locations based on text queries.
    Returns a list of store names, addresses, latitude/longitude coordinates, and place IDs.
    
  - **`car_counter.ipynb`:**  
    The `car_counter.ipynb` notebook provides an end-to-end demonstration of how to detect and count cars in a set of images using a pre-trained YOLOv5 model. This notebook is particularly useful if you want to quickly evaluate parking lot occupancy or run inference on a custom folder of images.
      
      1. *Model Loading:*  
         - Automatically downloads or loads a YOLOv5 model (e.g., `best.pt`) trained on the aerial-cars-dataset or any other relevant dataset.
         - Optionally sets the confidence threshold to filter out low-confidence detections.
      
      2. *Image Inference:*  
         - Iterates through all images in a specified folder (e.g., `/content/drive/MyDrive/images`) and runs YOLOv5 inference.
         - Outputs bounding boxes, class labels, and confidence scores for each detection.
      
      3. *Car Counting:*  
         - Aggregates the number of detections labeled as "car" for each image.
         - Saves the results to a JSON file (e.g., `car_counts.json`), mapping image filenames to their respective car counts.
      
      4. *Visualization:*  
         - Optionally renders bounding boxes on images to help visually verify detection results.
         - Displays a subset of images in the notebook with bounding boxes drawn around detected cars.


  These files posed challenges in terms of asynchronous processing, error handling, and ensuring compatibility across different environments (Google Colab and Drexel’s TUX server).

### API and Infrastructure Challenges

- **Google Maps API Rate Limits:**  
  The Google Maps APIs have strict rate limits, which can affect the speed and reliability of location queries and image retrieval. Implementing request throttling and handling rate limit errors is necessary to ensure stable execution.

- **Google Maps API Rate Limits:**  
When retrieving paginated results from the Google Places Text Search API, the next page token is not immediately valid after being issued. If the next request is made too quickly, it may result in an empty response. To avoid this, we introduce a delay before requesting the next page of results to ensure the token becomes active.

- **Data Storage and Processing Efficiency:**
The collected data, including store locations, static map URLs, and related metadata, must be structured efficiently for downstream processing. Ensuring a well-defined storage format and handling potential data inconsistencies is an ongoing challenge.

- **Google Colab Free GPU:**  
  Although convenient for rapid prototyping, Colab’s free GPU sessions are time-limited and can disconnect unexpectedly. This led to interruptions during long training sessions.

- **Drexel’s TUX Server:**  
  To overcome Colab’s limitations, we transitioned extended training to Drexel’s TUX server. While this environment provided stability, it also required additional configuration, particularly regarding file I/O operations and environment-specific optimizations.

- **Model Generalization:**  
  Aerial images pose unique challenges—cars appear very small compared to the overall scene. This sometimes resulted in under-detection, highlighting the need for further dataset refinement and model tuning.

---

## Infrastructure and Resource Choices

- **Google Colab Free GPU:**  
  Utilized for initial experiments and model prototyping. Despite its convenience, Colab’s free GPU environment suffers from session timeouts and slower I/O performance when interacting with Google Drive.

- **Drexel’s TUX Server:**  
  Adopted for extended, stable training runs. Its dedicated computational resources and stable runtime environment enabled us to fine-tune our YOLOv5 model without interruption, though at the cost of additional configuration complexity.

---

## Repository Structure

<pre>
DSCI_511_Project/
+-- aerial-cars-dataset/
|   +-- images/           # Aerial images from the dataset
|   +-- labels/           # YOLO-format label files
+-- aerial_data.yaml      # Custom YAML configuration for YOLOv5 training
+-- yolov5_new/           # Modified YOLOv5 repository for our project
|   +-- train.py
|   +-- detect.py
|   +-- ... (other YOLOv5 code)
+-- run.py                # Script to run inference and count cars, outputs records.json and car_counts.json
+-- image_server.py       # Code to process and serve images with detection boxes
+-- server.py             # Additional server/API code for integration and generating final_results.json
+-- README.md             # This file
</pre>

---

## Future Work

- **Data Enhancement:**  
  Expand the dataset by incorporating additional parking lot images via Google Maps APIs, and improve the quality of annotations to better capture small vehicles.

- **Model Optimization:**  
  Experiment with larger YOLOv5 variants (e.g., YOLOv5m, YOLOv5l) and further hyperparameter tuning to improve detection accuracy.

- **Deployment:**  
  Develop a robust REST API using Flask or FastAPI for real-time inference on new parking lot images, integrating the detection pipeline with business analytics systems.

- **Multi-Source Data Integration:**  
  Combine parking lot occupancy data with additional metrics (e.g., store size, location demographics, historical spending) to refine predictions of warehouse store performance.

---

## References

- **YOLOv5 GitHub Repository:**  
  [https://github.com/ultralytics/yolov5](https://github.com/ultralytics/yolov5)

- **Aerial Cars Dataset:**  
  [https://github.com/jekhor/aerial-cars-dataset](https://github.com/jekhor/aerial-cars-dataset)

- **Research Paper – Counting Cars in Aerial Images:**  
  [https://ieeexplore.ieee.org/abstract/document/8658300/authors#authors](https://ieeexplore.ieee.org/abstract/document/8658300/authors#authors)

- **Google Maps APIs Documentation:**  
  [https://developers.google.com/maps/documentation](https://developers.google.com/maps/documentation)

- **Drexel’s TUX Server:**  
  Internal resource used for extended training sessions
