from Constants import greenhouse_max_capacity,depreciation_pm,greenhouse_cost_pm,suppliers,recipe
import math

class Procurement:
    """Handle supplier-related logic: choose cheapest supplier and total restock cost."""
    def __init__(self, supplier_prices: dict = suppliers):
        self.supplier_prices = supplier_prices

    def choose_best_supplier(self,restock_needed: dict[str, int])-> dict[str, str]:
        """
        Pick the cheapest supplier per plant.

        Input:
        restock_needed: {plant: qty_needed}

        Output:
        best_choice:{plant: supplier_name} minimizing unit price for each plant.
        """
        best_choice = {}
        for plant in restock_needed.keys():
            best_supplier = min(
                list(self.supplier_prices.keys()),
                key=lambda s: self.supplier_prices[s].get(plant)
            )
            best_choice[plant] = best_supplier
        return best_choice

    def restock_cost(self,restock_needed: dict[str, int],supplier_choice: dict[str, str]) -> float:
        """
        Calculate total restock cost.

        Inputs:
        restock_needed: {plant: needed}
        supplier_choice: {plant: supplier_name} to buy from.

        Output:
        restock_cost: cost for all restock plants
        """
        restock_cost = 0.0
        for plant, qty in restock_needed.items():
            supplier = supplier_choice.get(plant)
            if supplier:
                unit_price = self.supplier_prices[supplier].get(plant, 0.0)
                restock_cost += qty * unit_price
        return round(restock_cost, 2)


class Inventory:
    """Manage greenhouse stock lifecycle: consumption → depreciation → restocking → cost."""
    def __init__(
        self,
    ):
        """
        Initialize inventory state.

        capacity, depreciation rates, greenhouse cost, recipes are loaded from constants.
        current_stock starts at full capacity.
        """
        self.capacity = greenhouse_max_capacity
        self.depreciation = depreciation_pm
        self.greenhouse_cost = greenhouse_cost_pm
        self.recipe = recipe
        self.current_stock = self.capacity.copy()
        self.restock_needed_dict = {}
        self.loss = {}

    def consume_plants(self,sale_plan) -> dict[str, int]:
        """
        Deduct plant quantities from current stock based on sales plan.

        Input:
        sale_plan: {bouquet_name: qty_to_sell}

        Calculation:
        For each bouquet, multiply qty by recipe requirement to get plant consumption.
        Reduce self.current_stock by consumption per plant (floors at 0).

        Output:
        {plant: consumed_qty_this_month}
        """
        consumption = {plant: 0 for plant in self.capacity}
        for bouquet, qty in sale_plan.items():
            if bouquet not in self.recipe:
                continue
            for plant, need in self.recipe[bouquet].items():
                consumption[plant] += qty * need
        for plant in self.current_stock:
            self.current_stock[plant] = max(0, self.current_stock[plant] - consumption[plant])
        return consumption

    def apply_depreciation(self)-> tuple[dict[str, int], dict[str, int]]:
        """
        Apply monthly depreciation to stock.

        Calculation:
        Take a snapshot `stock_before_depreciation`.
        loss[plant] = ceil(current_stock[plant] * depreciation_rate)
        current_stock[plant] -= loss (floors at 0).

        Output:
        (updated_current_stock_dict, loss_dict)
        """
        self.stock_before_depreciation = self.current_stock.copy()
        for plant, rate in self.depreciation.items():
            self.loss[plant] = math.ceil(self.current_stock[plant] * rate) # must round up to ensure the loss is an integer
            self.current_stock[plant] = max(0, self.current_stock[plant] - self.loss[plant])
        return self.current_stock,self.loss

    def restock_needed(self) -> dict[str, int]:
        """
        Calculate units required to refill to capacity.

        Output:
        {plant: capacity - current_stock} for plants below capacity.
        """
        self.restock_needed_dict = {}
        for plant, capacity in self.capacity.items():
            if self.current_stock[plant] < capacity:
                self.restock_needed_dict[plant] = capacity - self.current_stock[plant]
        return self.restock_needed_dict

    def auto_restock(self) -> float:
        """
        Auto-pick cheapest suppliers and refill to full capacity.

        Output:
        restock_cost; also mutates current_stock to capacity.
        """
        procurement = Procurement(suppliers) # best choice by default
        best_choice =  procurement.choose_best_supplier(self.restock_needed_dict)
        restock_cost = procurement.restock_cost(self.restock_needed_dict, best_choice)
        for plant in self.restock_needed_dict.keys():
            self.current_stock[plant] = self.capacity[plant]
        return restock_cost

    def inventory_cost(self,restock_cost:float) -> float:
        """
        Calculate total monthly inventory cost.

        Inputs:
        restock_cost: already computed for this month.

        Calculation:
        maintenance_cost = sum(greenhouse_cost[plant] * base_stock[plant])
        where base_stock is snapshot before depreciation.
        total = restock_cost + maintenance_cost.

        Output:
        total inventory cost for the month.
        """
        base_stock = getattr(self, "stock_before_depreciation", self.current_stock)
        maintenance_cost = sum(self.greenhouse_cost[plant] * base_stock[plant] for plant in self.current_stock.keys())
        return restock_cost + maintenance_cost





