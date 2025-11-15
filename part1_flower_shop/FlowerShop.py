from Inventory import Inventory, Procurement
from Florist import Florist
from Constants import *

class FlowerShop:
    #management class that coordinates sales, inventory, and costs.
    def __init__(self,inventory: Inventory,sales_plan: dict[str, int]):
        self.inventory = inventory
        self.sale_plan = sales_plan
        self.florists = []
        self.supplier_choice = None

    def set_supplier_choice(self,supplier_choice):
        self.supplier_choice = supplier_choice


    def add_florist(self, name: str, talents: dict = None):
        # Employee management: add florist
        for florist in self.florists:
            if florist.name == name:
                return f"[Error] florist '{name}' exists."
        if len(self.florists) >= florist_max_capacity:
            return f"[Error] reached maximum capacity(4)."
        else:
            new_florist = Florist(name, talents)
            self.florists.append(new_florist)
            return f"[Success] current staff: {[florist.name for florist in self.florists]}"


    def remove_florist(self, name: str):
        # Employee management: remove florist
        if len(self.florists) <= florist_min_capacity:
            return f"[Error] reached minimum capacity(1)."
        else:
            for florist in self.florists:
                if florist.name == name:
                    self.florists.remove(florist)
                    return f"current staff: {[f.name for f in self.florists]}"
            return f"[Error] no florist named '{name}'."

    def check_customer_demand(self,bouquet_demands = bouquet_demand):
        # Return list of bouquets exceeding demand.
        exceeded = []
        for bouquet,qty in bouquet_demands.items():
            planned = self.sale_plan.get(bouquet, 0)
            if qty < planned:
                exceeded.append(bouquet)
        return exceeded

    def check_florist_capacity(self):
        # check if total florists can complete the required sale_plan in the month
        # returns: bool,assignment_dict
        florist_max_time = florist_working_hours * 60 # the max working time for each florist
        remaining_time = {f.name: florist_max_time for f in self.florists} # the remaining working time for each florist
        assignment = {f.name: [] for f in self.florists} # tasks each florist complete
        tasks: list[tuple[str, int]] = []
        for bouquet, qty in self.sale_plan.items():
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
            remaining_time[best_florist.name] -= best_time # assign the task to the best florist
            assignment[best_florist.name].append(bouquet)
        structured_assignment = {} # structured output
        for florist, tasks in assignment.items():
            counter = {}
            for task in tasks:
                counter[task] = counter.get(task, 0) + 1
            structured_assignment[florist] = counter
        return True, structured_assignment

    def check_inventory_capacity(self):
        # check weather the sale_plan exceeded the inventory capacity
        needed_plants = {plant:0 for plant in greenhouse_max_capacity}
        shortages = {}
        for bouquet, bouquet_qty in self.sale_plan.items():
            if bouquet not in recipe:
                continue
            for plant, plant_qty in recipe[bouquet].items():
                needed_plants[plant] += bouquet_qty * plant_qty
        for plant in needed_plants:
            if needed_plants[plant] > greenhouse_max_capacity[plant]:
                shortages[plant] = needed_plants[plant] - greenhouse_max_capacity[plant]
        if shortages:
            print(f"Lack of raw plants {shortages}")
            return False
        return True

    def calculate_revenue(self):
        # calculate revenue this month
        revenue = 0.0
        for bouquet, bouquet_qty in self.sale_plan.items():
            price = bouquet_price.get(bouquet, 0.0)
            revenue += bouquet_qty * price
        return round(revenue,2)

    def calculate_cost(self,restock_cost : float):
        # calculate cost this month: return total_cost, inventory_cost, labor_cost and rent in order
        labor_cost = 0.0
        rent = rent_pm
        inventory_cost = self.inventory.inventory_cost(restock_cost)
        for florist in self.florists:
            labor_cost += florist.monthly_cost()
        total_cost = labor_cost + rent + inventory_cost
        return round(total_cost,2),round(inventory_cost,2),round(labor_cost,2),round(rent,2)

