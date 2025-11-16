# SDPA_EMATM0048_2720314
This repository contains my solution for part 1 and part 2 of SDPA coursework.
In part 1, the program implements a **text-based flower shop simulation** using an object-oriented design in Python.
# Part 1: Flower Shop Simulation
The program models a small flower shop which:
    employs florists to assemble bouquets
    manages a greenhouse with limited storage and monthly depreciation
    buys supplies from different suppliers
    sells bouquets to customers within monthly demand and capacity constraints
    tracks the shop’s cash flow and detects bankruptcy
## 1. How to Run
### Requirements
Python 3.14 or 3.14+
Standard library only: math
### Running the simulation
From the root of the repository:
- bash
python main.py

You will be prompted to:
    1.Enter the number of months to run the simulation:
        Press Enter with no input to use the default of 6 months.
    2.For each month:
        Hire or fire florists(with any specialties).
        Enter the quantity of each type of bouquet you wish to sell to develop a sales plan.
The program then simulates the month and displays by following ordering:
    1.current florists
    2.sales and costs for the month
    3.greenhouse stock levels
    4.updated cash balance
The simulation ends when:
    1.the chosen number of months has been completed
    2.the shop goes bankrupt (cash is insufficient to pay monthly expenses)