# Compiler written in PLY
Compiler project written for _Formal Languages and Translation Techniques_ classes 2018/2019 conducted by Maciej Gębala at Wrocław University of Science and Technology.

# Requirements
* Python 3 (tested on _v3.7.0_)
* Python Pip (tested on _v18.1_)
* PLY (tested on _v3.11_)

# Build
## By command line
```
sudo apt update
sudo apt install python3-pip -y
pip install ply || pip3 install ply
```
## By running Make
Run `make` in root folder which should run above instructions automatically.

# Running
*NOTE: python **version 3** is required*.

`kompilator` script will use `python3` as fallback if default `python` version is 2.X.X.
```
kompilator <source_file> <out_file>
```
or manually
```
python kompilator.py <source_file> <out_file>
# python3 kompilator.py <source_file> <out_file>
```