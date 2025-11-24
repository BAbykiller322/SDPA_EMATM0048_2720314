# SDPA_EMATM0048_2720314
This repository contains my solution for **part 1** and **part 2** of the SDPA coursework.  
Part 1 implements a **text based flower shop simulation** using an **object oriented design** in Python.  

---

# Part 1: Flower Shop Simulation
The program models a small flower shop which    
 - **employs florists** to **assemble bouquets**  
 - manages a greenhouse with **limited storage** and **monthly depreciation**  
 - buys plants from different **suppliers**  
 - sells bouquets to customers within **monthly demand** and **capacity limits**  
 - tracks the shop cash flow and detects bankruptcy  

## 1. How to Run

### Requirements
Python 3.10 or newer  
Standard library only 

### Running the simulation
From the root of the repository  
```bash
python main.py
```

You will be prompted to  
 - Enter the number of months to run the simulation  
   - Press Enter with no input to use the default of 6 months.  
 - For each month  
   - Hire or fire florists and optionally give them **specialties**.  
   - Enter the quantity of each type of bouquet you wish to sell to form a **sales plan**.  
 - The program then simulates the month and displays in the following order  
   - current florists and their specialties  
   - sales and costs for the month  
   - greenhouse stock levels  
   - cash balance  
 - The simulation ends when  
   - the chosen number of months has been completed  
   - the shop goes bankrupt  


## 2. Coursework Part 1 Summary
Part 1 requires a text based simulation of a flower shop which:  
 - offers three bouquet types with recipes and preparation times  
 - stores *roses, daisies and greenery in a greenhouse with  
   - a maximum capacity per item  
   - monthly depreciation of stock  
   - a **monthly running cost**  
 - starts with a **full greenhouse** and an *initial cash balance of 7,500 pounds    
 - employs between one and four florists, each providing a **number of working hours** and a fixed wage  

Each month the owner must  
 - **decide how many florists** to employ in capacity limits  
 - **decide how many bouquets** of each type to sell  

The program must  
 - *respect customer demand for each bouquet type  
 - ensure the sales plan fits within florist capacityand available stock  
 - update inventory using stock usage, depreciation, and restocking to full capacity  
 - update cash using sales revenue and all costs  
 - stop when all months have been simulated or the shop becomes bankrupt  

## 3. Program Design and Structure

### 3.1 Modules
The solution is divided into several modules.

 - `Constants.py`  
   Holds all configuration values used by the simulation such as bouquet recipes, preparation times, greenhouse capacity and depreciation, supplier prices, customer demand, bouquet prices, florist working hours and wages.

 - `Florist.py`  
   Defines the `Florist` class which stores the florist name, optional bouquet specific talents and methods to compute labour capacity and time required to make bouquets.

 - `Inventory.py`  
   Defines the `Inventory` class which tracks current greenhouse stock, applies monthly depreciation and calculates how many items are needed to restock to full capacity.  
   Defines the `Procurement` class which compares supplier prices, selects the cheapest supplier for each item and calculates restocking cost.

 - `FlowerShop.py`  
   Defines the `FlowerShop` class which holds the list of florists, owns the inventory and procurement objects, tracks the cash balance, checks whether a monthly sales plan is feasible and calculates monthly revenue and costs.

 - `main.py`  
   Contains the main program loop.  
   It handles all user interaction, calls the methods of the classes above and does not define any classes itself.

### 3.2 Responsibilities & relationships
Separation of responsibilities keeps the design clear and easier to maintain:  
 - FlowerShop acts as the central controller and coordinates florists, inventory and procurement.  
 - Florist represents individual workers and only handles labour related logic.  
 - Inventory encapsulates all stock and greenhouse behaviour.  
 - Procurement focuses on suppliers and prices and can be changed without touching other modules.  

## 4. Workflow

The simulation runs in month steps.

### 4.1 Initial settings
 - The greenhouse is at **maximum capacity** after replenishment.  
 - The *initial cash balance is set to 7,500 pounds.  
 - Users must hire **at least one florist in the first month**  

### 4.2 Monthly loop
For each month the following steps occur.

1. **Staff and sales decisions**  
   - Print the current number of florists and their specialties.  
   - Allow the user to hire or fire florists with minimum and maximum limits.  
   - When hiring, ask for the florist name and any talents for specific bouquet types.  
   - Reject empty names and duplicate names.  
   - Ask the user how many bouquets of each type to sell this month.

2. **Plan validation**  
   - Check that the requested quantities do not exceed customer demand.  
   - Use the **scheduling algorithm** to check that the plan fits within total florist working hours.  
   - Check that the required roses, daisies and greenery do not exceed current inventory.  
   - If any check fails, explain the reasons and ask the users to enter a new plan.

3. **Production and sales**  
   - Deduct the required quantities from inventory.  
   - Calculate total revenue from the bouquets sold.

4. **Depreciation and restocking**  
   - Apply **monthly depreciation** to each item in stock, rounding losses up to the next whole unit.  
   - Compute how many units of each item are needed to refill the greenhouse to maximum capacity.  
   - Let the user choose suppliers manually or let the program choose the **cheapest suppliers** automatically.  

5. **Costs, cash and termination**  
   - Calculate florist wages, greenhouse running cost and restocking cost.  
   - Update cash as previous cash plus revenue minus total costs.  
   - If cash is no longer sufficient, declare bankruptcy and stop the simulation.  
   - Otherwise print the updated status of cash, florists and stock and proceed to the next month.

## 5. Extensions and Design Highlights

 - **Flexible florist talents**  
   Each florist can have multiple talents represented as a time ratio for specific bouquet types.  
   The time required method applies these ratios to the base preparation times, so new bouquet types or different speed factors can be added by editing constants only.

 - **Scheduling algorithm**  
   When checking florist capacity the program breaks the plan into individual bouquet tasks, sorts them by preparation time and assigns each task to the florist who can complete it fastest and still has remaining hours.  
   This gives a realistic distribution of work.

 - **Supplier optimisation**  
   The procurement module compares supplier prices for each item, can automatically choose the cheapest supplier or allow the user to pick manually, and calculates the total restocking cost.  

 - **Config driven design**  
   All business parameters are stored in `Constants.py`, which makes it easy to understand the scenario and run different experiments by editing one file.

## 6. Assumptions & Limitations

 - Suppliers always maintain sufficient inventory and can ship immediately.    
 - Preparation time depends only on bouquet type and florist talents.  
 - No random changes in prices or demand are modelled.  


# Part 2: Data analysis projects


## 1. Project Overview
This project performs a comprehensive data analysis of the movie industry to identify key drivers of commercial success (ROI) and audience engagement.

The analysis follows the Data Science lifecycle:
 - Data Collection: Crawling real-world data from the TMDB (The Movie Database) API.

 - Preparation: Cleaning data, handling missing values, and feature engineering.

 - Exploration: Visualizing distributions and correlations.

 - Deep Dive: Answering a complex question regarding the relationship between genre, runtime, popularity, and profitability.

## 2. File Structure
analysis.ipynb: The main Jupyter Notebook containing all code, visualizations, and markdown explanations.
tmdb_movies_2020-2025.csv: The raw dataset extracted and saved during Step 1.
movie_schema.csv: explanations of movie features 
readme.md: This documentation file.

## 3. Dependencies & Setup
This project requires Python 3.14+ and the following external libraries: pandas, numpy, matplotlib, seaborn, and requests

## 4. Methodology & Logic

### 4.1: Data Collection:
Source: TMDB API  
Method:
 - Used requests to fetch data from the /discover/movie endpoint (pages 1-10).
 - Performed a second pass using /movie/{id} to fetch detailed financial data (Budget, Revenue) and Runtime, which are not available in the summary list.
 - Data Integration: Merged the discovery list with detailed metrics into a single DataFrame.

### 4.2: Data Preparation & Cleaning
Data Validity: Removed rows with 0 value in budget or revenue as they prevent accurate ROI calculation.

Feature Engineering:
 - Created ROI (Return on Investment) = Revenue / Budget. 
 - Applied Log Transformation (np.log1p) to vote_count and popularity to handle heavy-tailed distributions (long-tail effect).
 - Segmentation: Split the dataset into Main Movies (vote count > 50) and Cold Movies (vote count < 50) to analyze mainstream vs. niche market behaviors separately.

### 4.3: Exploratory Analysis (EDA)
Visualized the distribution of Runtime, Vote Average, and Budget.

Identified the "Head Effect" in popularity and the "Niche Effect" in ratings using Histograms and Boxplots.  

Key Insight: Niche movies (Cold Movies) show more polarized ratings compared to mainstream blockbusters.

### 4.4: Complex Question Analysis
Main Question: What are the key drivers of Movie ROI, and how do niche movies differ from blockbusters?

This was answered through some sub-questions, for example:
 - Genre Analysis: Which genres offer the best risk-reward ratio?
 - Quality vs. Popularity: Are high-rated movies always profitable?

## 5: Conclusion & Future Work
The analysis reveals that while high budget and popularity correlate with revenue, ROI is maximized by controlling budget (e.g., Horror genre).   
Future work could involve building a regression model to predict ROI based on these engineered features.

## 6. Acknowledgements
Data provided by The Movie Database (TMDB).
This product uses the TMDB API but is not endorsed or certified by TMDB

