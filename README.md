# String-encrypt

String encryption parser

## Information

- Python 3 compatible

- Encrypts string input with randomized functions

  - i.e. XOR, NEG, ADD, SUB, INC, DEC

  - Increase variability using index of decryption loop

- Supported languages:

  - C/C++
  
  - Python

  - Javascript

  - Java

## Usage

### ![Help](img/1.png)

## Example commands

```shell
> ./parser.py -s hello -e 10 -l py -o hello.py
```

### ![Output](img/2.png)

## Issues

- Uses `import signal` to set timeout for running function, which only works on UNIX.

  - **Remove timeout code to run on Windows**

## References

- [Stringencrypt](https://www.stringencrypt.com)

### Note: Program is made without reference to the executable from the website. The python program here is written from scratch with reference solely to the outputs of the string encryption there
