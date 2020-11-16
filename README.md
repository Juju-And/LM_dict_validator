# LM dict validation

This script allows user to input dictionary and receive verified version of it for partially manual validation.


## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Install all required modules running pip with the provided file:

```
pip install -r requirements.txt
```

## Running locally

```
$ python3 main.py <input.dict>
```

## Output files

> duplicates_ort_vs_disp.dict

File containing only lines with duplicate values between `ort word` and `disp word`, requiring manual selection of valid versions.