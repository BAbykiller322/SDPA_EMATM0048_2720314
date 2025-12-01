from Inventory import Inventory
from Florist import Florist
from Constants import *

class FlowerShop:
    """Coordinate sales, inventory, staffing, and cash flow for the shop."""
    def __init__(self,inventory: Inventory):
        self.inventory = inventory
        self.florists = []
        self.supplier_choice = None
        self.cash = initial_cash

    def add_florist(self, name: str, talents: dict = None):
        """
        Add a florist if under capacity.

        Inputs:
        name: string identifier.
        talents: optional {bouquet: time_ratio} passed to Florist.

        Output:
        True if added; otherwise error string when duplicate or over max capacity.
        """
        for florist in self.florists:
            if florist.name == name:
                return f"ERROR: florist '{name}' exists."
        if len(self.florists) >= florist_max_capacity:
            return f"ERROR: reached maximum capacity(4)."
        else:
            new_florist = Florist(name, talents)
            self.florists.append(new_florist)
            return True

    def remove_florist(self, name: str):
        """
        Remove a florist if above minimum capacity.

        Input:
        name: florist name to remove.

        Output:
        updated staff list or error message.
        """
        if len(self.florists) <= florist_min_capacity:
            return f"reached minimum capacity(1)."
        else:
            for florist in self.florists:
                if florist.name == name:
                    self.florists.remove(florist)
                    return f"current staff: {[f.name for f in self.florists]}"
            return f"no florist named '{name}'."

    def check_customer_demand(self,sale_plan: dict[str, int],bouquet_demands = bouquet_demand):
        """
        Validate sale plan against demand limits.

        Inputs:
        sale_plan: {bouquet: qty}
        bouquet_demands: {bouquet: max_monthly_demand}

        Output:
        (ok: bool, exceeded_list: list of bouquets that exceed demand)
        """
        exceeded = []
        for bouquet,qty in bouquet_demands.items():
            planned = sale_plan.get(bouquet, 0)
            if qty < planned:
                exceeded.append(bouquet)
        if len(exceeded) > 0:
            return False, exceeded
        return True,exceeded

    def check_florist_capacity(self,sale_plan: dict[str, int]):
        """
        Check if current florists can craft the sale_plan within monthly hours.

        Input:
        sale_plan: {bouquet: qty}

        Algorithm:
        Expand tasks list with one entry per bouquet unit, sorted by descending base time.
        For each task, pick the florist who can finish fastest; tie-breaker by remaining time.

        Output:
        bool,structured_assignment: dict
        When ok=False, assignment shows partial attempted counts per florist.
        """
        florist_max_time = florist_working_hours * 60 # the max working time for each florist
        remaining_time = {f.name: florist_max_time for f in self.florists} # the remaining working time for each florist
        assignment = {f.name: [] for f in self.florists} # tasks each florist complete
        tasks: list[tuple[str, int]] = []
        for bouquet, qty in sale_plan.items():
            base_time = bouquet_time_required[bouquet]
            for i in range(qty):
                tasks.append((bouquet, base_time))
        tasks.sort(key=lambda x: x[1], reverse=True) # sort by task time in descending order
        for bouquet, base_time in tasks: # choose the best_florist who makes the bouquet in the shortest time.
            best_florist = None
            best_time = None
            for florist in self.florists:
                time = florist.time_required(bouquet)
                if remaining_time[florist.name] < time: # the florist did not have enough time to complete the task.
                    continue
                if best_time is None or time < best_time: # select the best_time and best_florist
                    best_time = time
                    best_florist = florist
                elif time == best_time: # when time is equal to best_time, choose the florist with the most remaining time.
                    if remaining_time[florist.name] >= remaining_time[best_florist.name]:
                        best_florist = florist
            if best_florist is None: # task failed
                structured_assignment = {} # structured output
                for florist, tasks in assignment.items():
                    counter = {}
                    for task in tasks:
                        counter[task] = counter.get(task, 0) + 1
                    structured_assignment[florist] = counter
                return False, structured_assignment
            remaining_time[best_florist.name] -= best_time #assign the task to the best florist
            assignment[best_florist.name].append(bouquet)
        structured_assignment = {} # structured output
        for florist, tasks in assignment.items():
            counter = {}
            for task in tasks:
                counter[task] = counter.get(task, 0) + 1
            structured_assignment[florist] = counter
        return True, structured_assignment

    def check_inventory_capacity(self,sale_plan: dict[str, int]):
        """
        Check whether planned bouquets exceed greenhouse raw material capacity.

        Input:
        sale_plan: {bouquet: qty}

        Output:
        bool, shortages: {plant: units_over_capacity}
        
        tips: Since plants are fully restocked by default each month,
        'greenhouse_max_capacity' is used instead of 'current_stock' here.This avoids creating class Inventory in method.
        """
        needed_plants = {plant:0 for plant in greenhouse_max_capacity}
        shortages = {}
        for bouquet, bouquet_qty in sale_plan.items():
            if bouquet not in recipe:
                continue
            for plant, plant_qty in recipe[bouquet].items():
                needed_plants[plant] += bouquet_qty * plant_qty
        for plant in needed_plants:
            if needed_plants[plant] > greenhouse_max_capacity[plant]:
                shortages[plant] = needed_plants[plant] - greenhouse_max_capacity[plant]
        if shortages:
            print(f"Lack of raw plants {shortages}")
            return False,shortages
        return True,shortages

    def cash_status(self):
        """Return current cash balance (float)."""
        return self.cash

    def florist_status(self):
        """Return current florist list (objects)."""
        return self.florists

    def calculate_revenue(self,sale_plan):
        """
        Calculate and add monthly revenue.

        Input:
        sale_plan: {bouquet: qty}

        Output:
        revenue = sum(qty * bouquet_price); also increments cash.
        """
        revenue = 0.0
        for bouquet, bouquet_qty in sale_plan.items():
            price = bouquet_price.get(bouquet, 0.0)
            revenue += bouquet_qty * price
        self.cash += revenue
        return round(revenue,2)

    def calculate_cost(self,restock_cost : float):
        """
        Calculate monthly costs and deduct from cash.

        Input:
        restock_cost: restock cost for this month.

        Calculation:
        labor_cost = sum(florist.monthly_cost())
        rent = rent_pm
        inventory_cost = inventory.inventory_cost(restock_cost)
        total_cost = labor + rent + inventory
        cash decreased by total_cost

        Output:
        total_cost, inventory_cost, labor_cost, rent
        """
        labor_cost = 0.0
        rent = rent_pm
        inventory_cost = self.inventory.inventory_cost(restock_cost)
        for florist in self.florists:
            labor_cost += florist.monthly_cost()
        total_cost = labor_cost + rent + inventory_cost
        self.cash -= total_cost
        return round(total_cost,2),round(inventory_cost,2),round(labor_cost,2),round(rent,2)


