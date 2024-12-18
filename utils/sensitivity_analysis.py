import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

class EmissionsSensitivityAnalyzer:
    def __init__(self, base_values):
        """        
        Parameters: 
        base_values (dict): a dict containing Different emission factors and activity data
        """
        self.base_values = base_values
        self.results = {}
        self.Electricity_Factor = 0.4168           # Unit: kg CO2/kWh
        self.Natural_Gas_Factor = 2692.8           # Unit: kg CO2/t
        self.Water_Factor = 1.3                    # Unit: kg CO2/t
        self.Ferrous_Metal_Factor = -707.3592663   # Unit: kg CO2/t
        self.Paper_Cardboard_Factor = 5985.56917   # Unit: kg CO2/t
        self.Construction_Demolition_Factor = 97.79380174 # Unit: kg CO2/t
        self.Plastics_Factor = 2905.710927         # Unit: kg CO2/t
        self.Food_Factor = 3585.89118              # Unit: kg CO2/t
        self.Horticultural_Factor = -28.46620278   # Unit: kg CO2/t
        self.Wood_Factor = 1395.634268             # Unit: kg CO2/t
        self.Ash_Sludge_Factor = 86.9761           # Unit: kg CO2/t
        self.Textile_Leather_Factor = 4605.975149  # Unit: kg CO2/t
        self.Used_Slag_Factor = -6.342589587       # Unit: kg CO2/t
        self.Non_Ferrous_Metal_Factor = -707.3592663 # Unit: kg CO2/t
        self.Glass_Factor = 532.8208748            # Unit: kg CO2/t
        self.Scrap_Tyres_Factor = 3963.915656      # Unit: kg CO2/t
        self.Others_Factor = 38.17394179           # Unit: kg CO2/t
        self.Drive_Factor = 0.118                  # Unit: kg CO2/km
        self.Public_Factor = 0.0431                # Unit: kg CO2/km
        self.Walk_Factor = 0.0                     # Unit: kg CO2/km
         
        
    def calculate_emissions(self, params):
        """
        Calculate total GHG emissions 
        """
        Electricity_GHG_Emissions = (
            params['Electricity_Amount'] * 
            self.Electricity_Factor * 
            (1 - params['Renewable_Energy_Proportion'])
        )

        Natural_Gas_GHG_Emissions = (
            params['Natural_Gas_Amount'] * 
            self.Natural_Gas_Factor
        )

        Water_GHG_Emissions = (
            params['Water_Amount'] *
            self.Water_Factor
        )

        Waste_GHG_Emissions = (
            params['Ferrous_Metal_Amount'] * self.Ferrous_Metal_Factor +
            params['Paper_cardboard_Amount'] * self.Paper_Cardboard_Factor +
            params['Construction_Demolition_Amount'] * self.Construction_Demolition_Factor +
            params['Plastics_Amount'] * self.Plastics_Factor +
            params['Food_Amount'] * self.Food_Factor +
            params['Horticultural_Amount'] * self.Horticultural_Factor +
            params['Wood_Amount'] * self.Wood_Factor +
            params['Ash_sludge_Amount'] * self.Ash_Sludge_Factor +
            params['Textile_Leather_Amount'] * self.Textile_Leather_Factor +
            params['Used_Slag_Amount'] * self.Used_Slag_Factor +
            params['Non_Ferrous_Metal_Amount'] * self.Non_Ferrous_Metal_Factor +
            params['Glass_Amount'] * self.Glass_Factor +
            params['Scrap_Tyres_Amount'] * self.Scrap_Tyres_Factor +
            params['Others_Amount'] * self.Others_Factor
        )

        Commute_GHG_Emissions = (
            (params['Drive_Distance'] * self.Drive_Factor +
            params['Public_Distance'] * self.Public_Factor +
            params['Walk_Distance'] * self.Walk_Factor) *
            params['Work_Frequency']
        )

        return (Electricity_GHG_Emissions +
                Natural_Gas_GHG_Emissions +
                Water_GHG_Emissions +
                Waste_GHG_Emissions +
                Commute_GHG_Emissions)
    
    def perform_sensitivity_analysis(self, variation_percentage=10, steps=10):
        """
        Parameters:
        variation_percentage (float): variation percentage of given range 
        steps (int): times of variations
        """
        for param in self.base_values.keys():
            variations = []
            emissions = []
            base = self.base_values[param]
            
            # Calculate GUI variation in the given range
            if param == 'Work_Frequency':
                # Change the variation range of work_frequency based on its original value 
                lower_bound = max(0, base - 0.2)  # no less than 0
                upper_bound = min(1, base + 0.2)  # no more than 1
                discrete_values = [lower_bound, upper_bound]
                for value in discrete_values:
                    test_values = self.base_values.copy()
                    test_values[param] = value
                    
                    variations.append((value - base) * 100)  
                    emissions.append(self.calculate_emissions(test_values)) 
            else:
                # For other variables
                for i in np.linspace(-variation_percentage/100, variation_percentage/100, steps):
                    test_values = self.base_values.copy()
                    test_values[param] = base * (1 + i)
                    
                    variations.append(i * 100)  
                    emissions.append(self.calculate_emissions(test_values))
            
            # Calculate correlation coefficients
            correlation, _ = spearmanr(variations, emissions)
            
            self.results[param] = {
                'variations': variations,
                'emissions': emissions,
                'correlation': correlation
            }
    
    def plot_tornado_diagram(self):
        # Calculate range of variations of different parameters
        impacts = {}
        for param, data in self.results.items():
            emissions_range = max(data['emissions']) - min(data['emissions'])
            impacts[param] = emissions_range
        
        # Plot the ranges
        self.sorted_impacts = dict(sorted(impacts.items(), key=lambda x: x[1], reverse=True))
        
        plt.figure(figsize=(12, 8))
        y_pos = np.arange(len(self.sorted_impacts))
        
        plt.barh(y_pos, list(self.sorted_impacts.values()))
        plt.yticks(y_pos, list(self.sorted_impacts.keys()))
        plt.xlabel('Variation of Emissions (kgCO2e)')
        plt.title('Parameter Sensitivity Analysis (10% Variation)')
        
        return plt
    
    def analyze_top_3_impact(self,params):
        # Calculate the current GHG emissions for baseline parameters
        baseline_emissions = self.calculate_emissions(params)
        variable_contributions = {}
        improvement_suggestions = {}

        # Calculate the GHG emissions contribution of each parameter individually
        for var in list(self.sorted_impacts.keys())[:3]:
            # Test by reducing the parameter by 10%
            test_params = params.copy()
            if var == 'Work_Frequency':
                test_params[var] = test_params[var] - 0.2
            elif var == 'Renewable_Energy_Proportion':
                test_params[var] = test_params[var] * 1.1
            else:
                test_params[var] = test_params[var] * 0.9
                  
            emissions_after_reduction = self.calculate_emissions(test_params)
            contribution = baseline_emissions - emissions_after_reduction  
            variable_contributions[var] = round(contribution,2)
        
        for var, reduction in variable_contributions.items():
            if 'Electricity' in var:
                suggestion = "Promote the use of energy-efficient devices and smart lighting systems to reduce electricity consumption."
            elif 'Renewable_Energy_Proportion' in var:
                suggestion = "Increase the proportion of renewable energy usage, such as installing solar panels or utilizing wind energy."
            elif 'Natural_Gas' in var:
                suggestion = "Encourage the use of efficient natural gas heating systems to reduce waste and emissions."
            elif 'Water' in var:
                suggestion = "Install water-saving devices, such as low-flow faucets and smart water management systems."
            elif 'Ferrous_Metal' in var:
                suggestion = "Increase the recycling of ferrous metals to reduce the demand for new resources."
            elif 'Paper_Cardboard' in var:
                suggestion = "Promote digital office practices to reduce the use of paper and cardboard."
            elif 'Construction_Demolition' in var:
                suggestion = "Optimize demolition and recycling processes to increase the resource recovery of construction waste."
            elif 'Plastics' in var:
                suggestion = "Increase plastic recycling rates and promote the use of biodegradable materials."
            elif 'Food' in var:
                suggestion = "Implement office waste sorting and support food recovery to reduce food waste."
            elif 'Horticultural' in var:
                suggestion = "Use locally grown plants to reduce carbon emissions during transportation."
            elif 'Wood' in var:
                suggestion = "Use sustainable wood or alternative materials to prevent illegal deforestation."
            elif 'Ash_Sludge' in var:
                suggestion = "Promote the recycling of ash and sludge, such as using it in construction materials."
            elif 'Textile_Leather' in var:
                suggestion = "Increase the use of sustainable textiles and leather products to reduce environmental impact."
            elif 'Used_Slag' in var:
                suggestion = "Promote the reuse of waste slag, such as incorporating it into building materials."
            elif 'Non_Ferrous_Metal' in var:
                suggestion = "Increase the recycling of non-ferrous metals to reduce the negative impacts of mining activities."
            elif 'Glass' in var:
                suggestion = "Enhance glass recycling and reuse to reduce the need for new production."
            elif 'Scrap_Tyres' in var:
                suggestion = "Promote the recycling of scrap tires to reduce environmental pollution."
            elif 'Others' in var:
                suggestion = "Guide waste sorting and proper treatment and recycling of 'other waste'."
            elif 'Drive' in var or 'Public' in var or 'Walk' in var:
                suggestion = "Encourage employees to use public transportation or adopt electric vehicles to reduce commute-related emissions."
            else:
                suggestion = "Promote remote work or flexible working hours to reduce the frequency of commuting, thereby lowering transportation-related emissions."

            improvement_suggestions[var] = {
                'reduction_amount': reduction,
                'suggestion': suggestion
            }
            
        return improvement_suggestions
    
     