from Inventory import Inventory
from Florist import Florist
from Constants import bouquet_demand

class FlowerShop():
    #management class that coordinates sales, inventory, and costs.
    def __init__(self,inventory: Inventory,florist: list[Florist],sales_plan: dict[str, int]):
        self.inventory = inventory
        self.florist = florist
        self.sale_plan = sales_plan

    def check_customer_demand(self,bouquet_demands = bouquet_demand) -> list[str]:
        #Return list of bouquets exceeding demand.
        exceeded = []
        for bouquet,qty in bouquet_demands.items():
            if qty < self.sale_plan[bouquet]:
                exceeded.append(bouquet)
        return exceeded

    def check_florist_capacity
