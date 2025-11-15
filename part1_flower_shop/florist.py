from Constants import florist_salary,florist_working_hours,bouquet_time_required
import math

class Florist:
    # Represent a single florist working in the shop.
    # Each florist may have talents which allow him to make certain bouquets faster.
    def __init__(self,name,talents:dict[str, int] = None):
        #Attribute:name
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Florist name must be non-empty string type.")
        self.name = name.strip()
        # Attribute:talent
        if talents:
            clean_talents = {}
            for bouquet, ratio in talents.items():
                if ratio <= 0 or ratio > 1:
                    raise ValueError(
                        f"Talent ratio for {bouquet} of {self.name} must be in (0, 1]"
                    )
                clean_talents[bouquet] = ratio
            self.talents = clean_talents
        else:
            self.talents = {}

    def monthly_cost(self):
        # monthly cost per florist
        return florist_salary * florist_working_hours

    def time_required(self,bouquet:str):
        # Calculate the required time for certain bouquet
        base_time = bouquet_time_required[bouquet]
        ratio = self.talents.get(bouquet, 1.0)
        return math.ceil(base_time * ratio)

