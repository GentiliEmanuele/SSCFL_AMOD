class ProblemInstance:
    def __init__(self, facilities_opening_costs, transportation_costs, capacities, demands):
        self.facilities_opening_costs = facilities_opening_costs
        self.transportation_costs = transportation_costs
        self.capacities = capacities
        self.demands = demands

    def to_string(self):
        print(f"facilities_opening_costs: {self.facilities_opening_costs}")
        print(f"transportation_costs: {self.transportation_costs}")
        print(f"capacities: {self.capacities}")
        print(f"demands: {self.demands}")
