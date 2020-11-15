# Machine learning models evaluation web-service
A web service for visually comparing the performance of machine learning models.

## Features
- Online model evaluation
- Comparison with other models
- Possible different datasets and models for one task

## Usage
1) Install docker
2) docker-compose build
3) docker-compose up -d 
Service will be started on port 8080. See https://127.0.0.1:8080/

## Web interface
### Authorization
1. Enter login and password, which the service administrator gave you. (default: admin:admin)
2. Click "Login"

### Main menu
There you can see 3 columns:
1. *Models* — models uploaded to the service. You can add your model by clicking "+" button.
  - To add: type name of your model, description, as target type - type of model, as model file - file with model, as scheme file - JSON file with shape. 
2. *Datasets* — test data used to evaluate models. You can add one more dataset by clicking "+" button.
3. *Experiments* — result of testing and evaluating models on corresponding datasets. 

### Experiments

There you can see models comparison: histograms, diagrams based on calculated metrics.

#### How to make experiment:
1. Click "+" button in main menu.
2. Select parameters for your model, model and corresponding dataset.
3. Click "Ok" button.
4. Done.

- To *add new metrics*, you need to write *LaTeX code* and pass it through new *metrics adder*.

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
