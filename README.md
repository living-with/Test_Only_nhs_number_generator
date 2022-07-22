# Test Only NHS Number Generator

Generate test NHS numbers in Python 2.7+ and 3.

## To use as a script

Generate five (-n 5) sequential (-d) formatted (-f) nhs numbers:

```
$ python3 generate_nhs_numbers.py -n 5 -d -f
400 000 0004
400 000 0012
400 000 0020
400 000 0039
400 000 0047
```

Use the -h flag for help:

```
$ python3 generate_nhs_numbers.py -h
usage: generate_nhs_numbers.py [-h] [-n N] [-d] [-f]

Generate 10-digit NHS numbers.

optional arguments:
  -h, --help           show this help message and exit
  -n N                 the amount to generate
  -d, --deterministic  generate predictably, starting at 4000000004
  -f, --format         format using spaces e.g. 565 228 3297
  ```

## To use as a library

```python
import generate_nhs_numbers

for nhs_number in generate_nhs_numbers.random_nhs_number_generator([(999000000, 999999999)]):
    print(nhs_number)
```
