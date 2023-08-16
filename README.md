# rssi-generator

## Prerequierements
- Python 3.10.x or above
- Install venv (Python Virtual Environment)

  Step to produce :

  ```
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
  if the process worked, there would be a sign of "(venv)" in front of the terminal line.
  
- Install required python library

  Step to Produce :
  ```
  pip install -r requirements.txt
  ```
  or
  ```
  python -m pip install -r requirements.txt
  ```
  wait and ensure all library installed.

## Usage
### Preprocess
- Curve Fitting
  Please aware to include or edit the "/path/to/file" according to your raw data directory in the ```--datapath``` parameter
  and preprocess output directory in the ```--destination``` parameter.

  - Node

    ```
    python -m preprocess.curve_fitting_node --datapath "/path/to/file" --destination "/path/to/destination"
    ```
  - Gateway


    ```
    python -m preprocess.curve_fitting_gw --datapath "/path/to/file" --destination "/path/to/destination" 
    ```
- Polynomial Fitting
  Please aware to include or edit the "/path/to/file" according to your raw data directory in the ```--datapath``` parameter
  and preprocess output directory in the ```--destination``` parameter.

  - Node

    ```
    python -m preprocess.polyfit_node --datapath "/path/to/file" --destination "/path/to/destination"
    ```
  - Gateway

    ```
    python -m preprocess.polyfit_gw --datapath "/path/to/file" --destination "/path/to/destination"
    ```
- Savitzky Golay
  Please aware to include or edit the "/path/to/file" according to your raw data directory in the ```--datapath``` parameter
  and preprocess output directory in the ```--destination``` parameter.

  - Node

    ```
    python -m preprocess.savitzky_golay_node --datapath "/path/to/file" --destination "/path/to/destination"
    ```
  - Gateway

    ```
    python -m preprocess.savitzky_golay_gw --datapath "/path/to/file" --destination "/path/to/destination"
    ```
### Quantization
- Two-Array
  Please aware to include or edit the "/path/to/file" according to your preprocess data directory in the ```--datapath``` parameter
  , change filename based on ```--filename``` parameter, and preprocess output directory in the ```--destination``` parameter.
  - Node

    ```
    python -m quantification.two_array_node --datapath "/path/to/file" --destination "/path/to/destination"
    ```
  - Gateway

    ```
    python -m quantification.two_array_gw --datapath "/path/to/file" --filename "preprocess.filename" --destination "/path/to/destination"
    ```
### Reconsiliation
- Reed Solomon
  Please aware to include or edit the "/path/to/file" according to your quantization data directory in the ```--datapath``` parameter
  and preprocess output directory in the ```--destination``` parameter.
  - Node

    ```
    python -m reconsiliation.reed_solomon_gateway --datapath "/path/to/file" --destination "/path/to/destination"
    ```
  - Gateway
