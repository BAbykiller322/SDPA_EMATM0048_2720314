from Constants import greenhouse_max_capacity,depreciation_pm,greenhouse_cost_pm,suppliers,recipe
import math

class Procurement:
    #Handles supplier-related logic: choosing cheapest supplier and calculating restock cost.
    def __init__(self, supplier_prices: dict[str, dict[str, float]]):
        self.supplier_prices = supplier_prices
        self.supplier_names = list(supplier_prices.keys())

    def choose_best_supplier(self,restock_needed: dict[str, int])-> dict[str, str]:
        #Additional method: automatically select the cheapest supplier for each plant.
        best_choice = {}
        for plant in restock_needed:
            best_supplier = min(
                self.supplier_names,
                key=lambda s: self.supplier_prices[s].get(plant, float('inf'))
            )
            best_choice[plant] = best_supplier
        return best_choice

    def calculate_restock_cost(self, restock_needed: dict[str, int], supplier_choice: dict[str, str]) -> float:
        #Calculate total restock cost based on supplier choice.
        restock_cost = 0.0
        for plant, qty in restock_needed.items():
            supplier = supplier_choice.get(plant)
            if supplier:
                unit_price = self.supplier_prices[supplier].get(plant, 0.0)
                restock_cost += qty * unit_price
        return restock_cost


class Inventory:
    #Manages the greenhouse stock lifecycle with four steps: consumption，depreciation，restocking，cost.

    def __init__(
        self,
        capacity: dict = greenhouse_max_capacity,
        depreciation: dict = depreciation_pm,
        greenhouse_cost: dict = greenhouse_cost_pm,
        supplier: dict = suppliers,
    ):
        #Initialize inventory with capacity, cost, and procurement system.
        self.capacity = capacity
        self.depreciation = depreciation
        self.greenhouse_cost = greenhouse_cost
        self.recipe = recipe
        self.current_stock = capacity.copy()
        self.procurement = Procurement(supplier)

    def consume_plants(self,sales_plan: dict[str, int]) -> dict[str, int]:
        #Deduct plant quantities from current stock based on sales plan.
        #Tips：`self.current_stock`reflects monthly sales consumption.
        consumption = {'roses': 0 , 'daisies': 0 , 'greenery': 0}
        for bouquet, qty in sales_plan.items():
            if bouquet not in self.recipe:
                continue
            for plant, need in self.recipe[bouquet].items():
                consumption[plant] += qty * need
        for plant in self.current_stock:
            self.current_stock[plant] = max(0, self.current_stock[plant] - consumption[plant])
        return consumption

    def apply_depreciation(self)-> tuple[dict[str, int], dict[str, int]]:
        #Calculate the depreciation of various plants per month.return current_stock and loss
        loss = {}
        for plant, rate in self.depreciation.items():
            loss[plant] = math.ceil(self.current_stock[plant] * rate) # must round up to ensure the loss is an integer
            self.current_stock[plant] = max(0, self.current_stock[plant] - loss[plant])
        return self.current_stock,loss

    def calculate_restock_needed(self) -> dict[str, int]:
        #Calculate restock needed for each plant.
        restock_needed ={}
        for plant in self.capacity:
            if self.current_stock[plant] < self.capacity[plant]:
                restock_needed[plant] = self.capacity[plant] - self.current_stock[plant]
        return restock_needed

    def auto_restock(self) -> float:
        #Additional method: automatically select the best plan and restock to full capacity.
        restock_needed = self.calculate_restock_needed()
        supplier_choice = self.procurement.choose_best_supplier(restock_needed) #best choice by default
        restock_cost = self.procurement.calculate_restock_cost(restock_needed, supplier_choice)
        for plant in restock_needed:
            self.current_stock[plant] = self.capacity[plant]
        return restock_cost

    def calculate_monthly_cost(self,restock_cost:float) -> float:
        #Calculate total monthly inventory cost (maintenance + restocking).
        maintenance_cost = sum(
            self.greenhouse_cost[plant] * self.capacity[plant]
            for plant in self.capacity
        )
        return restock_cost + maintenance_cost

    def get_stock_status(self) -> str:
        #Additional method: return current stock.
        return (
            f"Current Stock — Roses: {self.current_stock['roses']}, "
            f"Daisies: {self.current_stock['daisies']}, "
            f"Greenery: {self.current_stock['greenery']}"
        )




