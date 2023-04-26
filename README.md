# 🖥️ Computor v1

This project is a simple program that solves polynomial equations of degree up to 2. It has been written as part of the 42 school curriculum.

## 📦 Prerequisites

You will need to have Python 3.6 or higher installed on your machine.
An additional package named [PLY](https://www.dabeaz.com/ply) is also required.
You can install it by running the following command:
```
pip3 install -r requirements.txt
```

## 📖 Usage

To use the program, run the following command:
```sh
python3 computor.py
```

## 🔬 Examples

### Solve a linear equation

```sh
python3 computor.py -s '7 * X - 2'
```

- 💡 The *'-s'* option is used to show the intermediate steps of the resolution.

### Solve a quadratic equation

```sh
python3 computor.py -f '5 * X ^ 2 + 8 * X = -3'
```

- 💡 The *'-f'* option is used to force the program to use fractions when possible.

## ⚖️ License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
