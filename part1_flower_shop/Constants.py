#the capacity of the florists
florist_max_capacity = 4
florist_min_capacity = 1

#florist salary per hour and working time per month
florist_salary = 15.50
florist_working_hours = 80

#the greenhouse capacity of the roses,daisies and greenery
greenhouse_max_capacity = {
    "roses": 200,
    "daisies": 250,
    "greenery": 400
}

#the depreciation of the roses,daisies and greenery
depreciation_pm = {
    "roses": 0.4,
    "daisies": 0.15,
    "greenery": 0.05
}

#the greenhouse Costs of the roses,daisies and greenery
greenhouse_cost_pm = {
    "roses": 1.5,
    "daisies": 0.8,
    "greenery": 0.2
}

#the suppliers of the roses,daisies and greenery
suppliers = {
    'Evergreen Essentials': {'roses': 2.80 , 'daisies': 1.50 , 'greenery': 0.95 },
    'FloraGrow Distributors': {'roses': 1.60 , 'daisies': 1.20 , 'greenery': 1.0}
}

#Materials required for each product
recipe = {
    "Fern-tastic" :{'roses': 0 , 'daisies': 2 , 'greenery': 4 },
    "Be-Leaf in Yourself":{'roses': 1 , 'daisies': 3 , 'greenery': 2 },
    "You Rose to the Occasion":{'roses': 4 , 'daisies': 2 , 'greenery': 2 }
}

#Bouquet demand per month
bouquet_demand = {
    "Fern-tastic":175,
    "Be-Leaf in Yourself":100,
    "You Rose to the Occasion": 250
}

#Bouquet sale price
bouquet_price = {
    "Fern-tastic":18.5,
    "Be-Leaf in Yourself":17.75,
    "You Rose to the Occasion": 32.5
}

