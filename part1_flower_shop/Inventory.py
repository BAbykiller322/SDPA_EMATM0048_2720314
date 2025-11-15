from Constants import greenhouse_max_capacity,depreciation_pm,greenhouse_cost_pm,suppliers,recipe
import math

class Procurement:
    """Handles supplier-related logic: choosing cheapest supplier and calculating restock cost."""
    def __init__(self, supplier_prices: dict = suppliers):
        self.supplier_prices = supplier_prices

    def choose_best_supplier(self,restock_needed: dict[str, int])-> dict[str, str]:
        """Additional method: automatically select the cheapest supplier for each plant."""
        best_choice = {}
        for plant in restock_needed.keys():
            best_supplier = min(
                list(self.supplier_prices.keys()),
                key=lambda s: self.supplier_prices[s].get(plant)
            )
            best_choice[plant] = best_supplier
        return best_choice

    def restock_cost(self,restock_needed: dict[str, int],supplier_choice: dict[str, str]) -> float:
        """Calculate total restock cost based on supplier choice."""
        restock_cost = 0.0
        for plant, qty in restock_needed.items():
            supplier = supplier_choice.get(plant)
            if supplier:
                unit_price = self.supplier_prices[supplier].get(plant, 0.0)
                restock_cost += qty * unit_price
        return round(restock_cost, 2)


class Inventory:
    """Manages the greenhouse stock lifecycle with four steps: consumption，depreciation，restocking，cost."""
    def __init__(
        self,
        supplier_choice: dict[str, str],
        sales_plan: dict[str, int],
        best_choice = None
    ):
        """Initialize inventory with capacity, cost, and procurement system."""
        self.capacity = greenhouse_max_capacity
        self.depreciation = depreciation_pm
        self.greenhouse_cost = greenhouse_cost_pm
        self.recipe = recipe
        self.current_stock = self.capacity.copy()
        self.supplier_choice = supplier_choice
        self.sale_plan = sales_plan
        self.restock_needed = {}

    def consume_plants(self) -> dict[str, int]:
        """
        Deduct plant quantities from current stock based on sales plan.
        Tips：`self.current_stock`reflects monthly sales consumption.
        """
        consumption = {plant: 0 for plant in self.capacity}
        for bouquet, qty in self.sale_plan.items():
            if bouquet not in self.recipe:
                continue
            for plant, need in self.recipe[bouquet].items():
                consumption[plant] += qty * need
        for plant in self.current_stock:
            self.current_stock[plant] = max(0, self.current_stock[plant] - consumption[plant])
        return consumption

    def apply_depreciation(self)-> tuple[dict[str, int], dict[str, int]]:
        """Calculate the depreciation of various plants per month.return current_stock and loss"""
        loss = {}
        for plant, rate in self.depreciation.items():
            loss[plant] = math.ceil(self.current_stock[plant] * rate) # must round up to ensure the loss is an integer
            self.current_stock[plant] = max(0, self.current_stock[plant] - loss[plant])
        return self.current_stock,loss

    def restock_needed(self) -> dict[str, int]:
        """Calculate restock needed for each plant."""
        for plant, capacity in self.capacity.items():
            if self.current_stock[plant] < capacity:
                self.restock_needed[plant] = capacity - self.current_stock[plant]
        return self.restock_needed

    def auto_restock(self) -> float:
        """Additional coupling method: automatically select the best plan and restock to full capacity."""
        procurement = Procurement(suppliers) # best choice by default
        best_choice =  procurement.choose_best_supplier(self.restock_needed)
        restock_cost = procurement.restock_cost(self.restock_needed, best_choice)
        for plant in self.restock_needed:
            self.current_stock[plant] = self.capacity[plant]
        return restock_cost

    def inventory_cost(self,restock_cost:float) -> float:
        """Calculate total monthly inventory cost (maintenance + restocking)."""
        maintenance_cost = sum(self.greenhouse_cost[plant] * self.capacity[plant] for plant in self.capacity)
        return restock_cost + maintenance_cost

    def get_stock_status(self) -> str:
        """Additional method: return current stock."""
        return (
            f"Current Stock — Roses: {self.current_stock['roses']}, "
            f"Daisies: {self.current_stock['daisies']}, "
            f"Greenery: {self.current_stock['greenery']}"
        )




