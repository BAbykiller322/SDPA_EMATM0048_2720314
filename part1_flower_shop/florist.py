from Constants import florist_max_capacity,florist_min_capacity,florist_salary,florist_working_hours

class Florist:
    #Definition of the Florist class
    #Including methods for adding and removing florists
    #With enforced maximum and minimum capacity constraints

    florist_list = []
    def __init__(self,name,talents = None):
        #Add new florist to the florist list
        #Option: some florist has talent to make certain bouquet type with less time
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Florist name must be non-empty string type.")
        self.name = name.strip()
        self.talents = talents if talents else {}
        if self.name in Florist.florist_list:
            raise ValueError(f"Florist '{self.name}' already exists.")
        elif len(Florist.florist_list) < florist_max_capacity:
            Florist.florist_list.append(self.name)
            print(f'Current staff:',Florist.florist_list)
        else:
            raise ValueError("The number of florist exceeds maximum capacity, and the maximum capacity is 4.")

    def remove(self):
        #remove the florist of the florist list
        if len(Florist.florist_list) <= florist_min_capacity:
            raise ValueError("Cannot remove the last remaining florist. Minimum capacity is 1.")
        elif self.name in Florist.florist_list:
            Florist.florist_list.remove(self.name)
            print(f'Current staff:',Florist.florist_list)
        else:
            raise ValueError(f"{self.name} not found in florist list.")

    def florist_cost(self):
        #caculate the salary of the florists per month
        florist_cost = florist_working_hours * florist_salary * len(self.florist_list)
        return florist_cost

    def caculate_capacity(self):

