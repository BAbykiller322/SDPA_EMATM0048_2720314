
from Constants import *
from Inventory import Inventory, Procurement
from FlowerShop import FlowerShop

def month_int(prompt:str, allow_zero=False, positive_only=True):
    """Robust integer input with error handling."""
    while True:
        value = input(prompt).strip()
        if value == '':
            value = month_value_default
            return value
        if not value.isdigit():
            print("please enter a positive integer.")
            continue
        value = int(value)
        if positive_only and value < 0: 
            """reject negitive number"""
            print("please enter a non-negative integer.")
            continue
        elif not allow_zero and value == 0: 
            """reject zero"""
            print("zero not allowed here.")
            continue
        else:
            if value > 60:
                print("month should less than 60")
            else:
                return value

def talent_int(prompt:str):
    """
    Input an integer whthin [0,3] to indicate
    whether you have a special skill
    waht is the type of the skill
    """
    while True:
        value = input(prompt).strip()
        if value == "":
            print("input cannot be empty.")
            continue
        if not value.isdigit():
            print("please enter an integer in [0,3].")
            continue
        num = int(value)
        if 0 <= num <= 3:
            return num
        else:
            print("please enter a number in [0,3].")

def talent_float(prompt: str):
    """Input a float as talent ratio, in the range (0,1)"""
    while True:
        value = input(prompt).strip()
        try:
            num = float(value)
        except ValueError:
            print("please enter a number in (0,1).")
            continue
        if 0 < num < 1:
            return num
        else:
            print("number must be in (0,1).")

def supplier_input(prompt: str):
    """Input an integer: 0 or 1"""
    while True:
        value = input(prompt).strip()
        if value == '0':
            return 0
        elif value == '1':
            return 1
        else:
            print("please enter the integer :0 or 1.")

def other_int_input(prompt:str, positive_only=True):
    """Robust integer input with error handling."""
    while True:
        value = input(prompt).strip()
        if not value.isdigit():
            print("please enter a positive integer.")
            continue
        value = int(value)
        if positive_only and value < 0:
            print("please enter a non-negative integer.")
            continue
        else:
            return value


inv = Inventory()
procurement = Procurement()
flowershop = FlowerShop(inv)

"""Welcome title"""
print(
    "------------------------------------\n\n"
    "Welcome to the FlowerShop Simulator!\n\n"
    "------------------------------------"
)

months = month_int("How many months would you like to run the game for?\n")
for month in range(months):
    print(
        "------------------------------------\n"
        f"month: {month+1}\n"
        "------------------------------------"
    )
    print(
        "Before the month starts, there are some oner actions for you to carry out. First, review the number of the stuff,"
        "then decide how many bouquets to sell.\n"
    )
    print(f"Current number of florists: {len(flowershop.florist_status())}\n"
          f"current staff: {[florist.name for florist in flowershop.florists]}")

    max_hire = florist_max_capacity - len(flowershop.florists)
    if month == 0:# require hiring at least one florist in the first month
        min_hire = 1  
    else:
        min_hire = 0  
    if max_hire < min_hire:
        print("Staff is already at maximum.")
        florist_hire_qty = 0
    else:
        while True:
            florist_hire_qty = other_int_input(
                f"How many florists would you like to hire? ({min_hire}~{max_hire})\n"
            )
            if min_hire <= florist_hire_qty <= max_hire:
                break
            print(f"Please enter a number between {min_hire} and {max_hire}.")

    hired = 0
    while hired < florist_hire_qty:
        florist_name = input("please input florist name (one at a time):\n").strip()
        if florist_name == "":
            print("name cannot be empty. Skipping.")
            continue
        
        """talents input -> {bouquet_name: ratio}"""
        talents = {}
        while True:
            speciality_choice = talent_int(
                "Does the florist have a speciality?\n"
                "0: No more specialities / Stop\n"
                "1: Yes :Fern-tastic\n"
                "2: Yes :Be-Leaf in Yourself\n"
                "3: Yes :You Rose to the Occasion\n"
                "Your choice: "
            )
            if speciality_choice == 0:
                break
            ratio = talent_float("Enter speciality time ratio (0~1): ")
            talents[bouquet_map[speciality_choice]] = ratio
        if len(talents) == 0:
            talents = None
            
        add_result = flowershop.add_florist(florist_name, talents)
        if add_result is not True:
            print(f"{add_result}\n")
        else:
            hired += 1
    print(f"current staff: {[florist.name for florist in flowershop.florists]}")

    # optionally remove florists with bounds checking
    removable = len(flowershop.florists) - florist_min_capacity
    if removable > 0:
        while True:
            remove_qty = other_int_input(
                f"How many florists would you like to remove? (0~{removable})\n"
            )
            if 0 <= remove_qty <= removable:
                break
            print(f"Please enter a number between 0 and {removable}.")
        for _ in range(remove_qty):
            name_to_remove = input("please input florist name to remove:\n").strip()
            if name_to_remove == "":
                print("name cannot be empty. Skipping.")
                continue
            print(flowershop.remove_florist(name_to_remove))
    else:
        print("Staff is already at minimum; cannot remove more florists.")

    print("How much of each bouquet would you like to sell?")
    while True:
        sale_plan = {}
        for bouquet in bouquet_map.values():
            sale_plan[bouquet] = other_int_input(f"{bouquet}:\n")
        """Check if the sales plan exceeds customer demand."""
        cd_check_answer,exceeded = flowershop.check_customer_demand(sale_plan)
        if not cd_check_answer:
            print(f"This exceeds the demand for {exceeded}.")
            continue
        """Check if the sales plan exceeds the maximum workload of existing employees."""
        fc_check_answer,workload= flowershop.check_florist_capacity(sale_plan)
        if not fc_check_answer:
            print(f"This exceeds the maximum workload:\n {workload}.")
            continue
        """check if the sale_plan exceeded the inventory capacity"""
        ic_check_answer,shortages = flowershop.check_inventory_capacity(sale_plan)
        if not ic_check_answer:
            continue
        break

    print(
        "----------------------------------------\n"
        "Month in progress...\n"
        "----------------------------------------\n"
    )

    """sale the bouquet as sale_plan"""
    consumption = inv.consume_plants(sale_plan)
    current_stock,loss = inv.apply_depreciation()
    optional_consumption_loss = other_int_input(
        "press '1' if you would like know the consumption and depreciation of raw materials this month\n"
        "press '0' to continue\n"
    )
    if optional_consumption_loss == 1:
        print(
            f"consumption:{consumption}\n"
            f"loss:{loss}\n"
        )

    """print current flowershop status"""
    print(
        "Current shop status:\n"
        f"current staff: {[florist.name for florist in flowershop.florists]}\n\n"
        "Greenhouse quantity:\n"
        f"{current_stock}"
    )

    """select supplier and restock"""
    restock_cost = 0.0
    if sale_plan: # sale plan is not empty.
        restock_needed = inv.restock_needed()
        if restock_needed:
            supplier_selection_method = supplier_input(
                "The greenhouse has spare capacity and needs to be restocked...\n\n"
                "0.manually select supplier\n"
                "1.automatically select the best supplier\n"
            )
            if supplier_selection_method == 1:
                inv.restock_needed_dict = restock_needed
                restock_cost = inv.auto_restock()
            else:
                supplier_choice = {}
                for plant in restock_needed.keys():
                    while True:
                        print (
                            f"\nDo you want to purchase {plant} from Evergreen Essentials (0), "
                            f"or FloraGrow Distributors (1)?\n"
                            "Press (i) if you would like to see price information from either supplier."
                        )
                        choice = input("Input: ").strip().lower()

                        """show price information"""
                        if choice == "i":
                            for sup_name, price_dict in suppliers.items():
                                print(f"{sup_name}: £{price_dict[plant]:.2f} per bunch")
                            continue

                        if choice in ("0", "1"):
                            supplier_choice[plant] = ("Evergreen Essentials" if choice == "0" else "FloraGrow Distributors")
                            break
                        print("Please enter 0, 1 or i.")
                restock_cost = procurement.restock_cost(restock_needed,supplier_choice)
                for plant in restock_needed.keys():
                    inv.current_stock[plant] = inv.capacity[plant]

    """Calculate the income and outgoings of the flowershop"""
    print(f"Cash Balance:\n Month Start:{flowershop.cash_status()}\n"
          f"Income:{flowershop.calculate_revenue(sale_plan)}")
    total_cost, inventory_cost, employee_costs, rent = flowershop.calculate_cost(restock_cost)
    print(
        "Outgoings:\n"
        f"  Employee costs:{employee_costs}\n"
        f"  Greenhouse costs:{inventory_cost - restock_cost}\n"
        f"  Restock costs:{restock_cost}\n"
        f"  Rent:{rent}\n"
    )
    print(f"End of month Cash Balance:{flowershop.cash_status()}\n")
    if flowershop.cash_status() <= 0:
        print("Sorry, your flower shop has gone bankrupt.")
        break
print(
    "***********************************************************************\n"
    "Congratulations! You have completed the simulation!"
)
