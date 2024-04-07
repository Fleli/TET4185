# Power Markets Solver

This program solves general power market clearing problems with a given number of producers and consumers and their respective marginal costs and maximum/requested quantities.

The example currently found in `./sources/__init.pmax` is the following

Producer    | Qt    |   Price   |
------------|-------|-----------|
GE          | 250   | 200       |
Statkraft   | 75    | 240       |
TI          | 100   | 450       |
NVE         | 150   | 600       |
Trondheim   | 200   | 700       |

Consumer    |   Qt  |   Price   |
------------|-------|-----------|
Alpha       | 150   | 900       |
Beta        | 100   | 700       |
Elkraft     | 210   | 650       |
Omega       | 140   | 500       |
Indok       | 150   | 350       |

Since the virtual machine running the program only runs on 16 bits data widths and does not yet have access to printing, we get _either_ the system price _or_ the produced quantity as output. If the value of `__fetch_price` (a macro in `./sources/main.pmax`) is 0, the program returns the traded volume. Otherwise, the system price is returned.

The produced/bought quantity for each participant should then be inferred from these numbers.

To run the program, run `make` in this directory. Running requires
- that you have installed `make`
- the [PMax Development Kit](https://github.com/Fleli/PDK-Installer) (PDK), which includes the PMax compiler, assembler and virtual machine.
