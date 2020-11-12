# LM dict verification

This script allows user to input dictionary and receive verified version of it for partially manual validation.

## Running locally

```
$ python3 main.py <input.dict>
```

## Output files

> general_report


> duplicates_ort_vs_disp.dict

File containing only lines with duplicate values between `ort word` and `disp word`, requiring manual selection of valid versions.