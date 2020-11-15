# Machine learning models evaluation web-service
A web service for visually comparing the performance of machine learning models.

## Features
- Online model evaluation
- Comparison with other models
- Possible different datasets and models for one task

## Web interface
### Authorization
1. Enter login and password, which the service administrator gave you. (default: admin:admin)
2. Click "Login"

### Main menu
There you can see 3 columns:
1. *Models* — models uploaded to the service. You can add your model by clicking "+".
2. *Datasets* — test data used to evaluate models. You can add one more dataset by clicking "+".
3. *Experiments* — result of evaluationg models on corresponding datasets. There you can see models comparison: histograms, diagrams based on calculated metrics.

## API

Used to upload test dataset.

### Requirements

- Python 3.6

### Usage
1. Download *update_dataset.py*
2. Open *cmd*
3. Change the working direcory to the script folder using ```cd path```
4. ```python update_dataset.py url file_path info```, where `url` is *URL to API*, `file_path` — *path to test dataset*, `info` — *any text*
5. Done. Dataset uploaded.
