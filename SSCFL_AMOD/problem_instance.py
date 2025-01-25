class ProblemInstance:
    def __init__(self, num_facilities, num_customers, facilities_opening_costs, transportation_costs, capacities, demands):
        self.num_facilities = num_facilities
        self.num_customers = num_customers
        self.facilities_opening_costs = facilities_opening_costs
        self.transportation_costs = transportation_costs
        self.capacities = capacities
        self.demands = demands

    def to_string(self):
        print(f"num_facilities: {self.num_facilities}")
        print(f"num_costumers: {self.num_customers}")
        print(f"facilities_opening_costs: {self.facilities_opening_costs}")
        print(f"transportation_costs: {self.transportation_costs}")
        print(f"capacities: {self.capacities}")
        print(f"demands: {self.demands}")
