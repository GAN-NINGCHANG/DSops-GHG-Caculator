baseline_factors = {
    'electricity': 10000, 
    'water': new_prediction[0],          
    'natural_gas': total_gas_usage,    
    'waste': total_waste,         
    'transport': 1000    
}

emission_factors = {
    'electricity': 0.5,  
    'water': 0.3,        
    'natural_gas': 2.2,  
    'waste': 1.5,     
    'transport': 1.0   
}

def calculate_total_emissions(factors, emission_factors):
    return sum(factors[factor] * emission_factors[factor] for factor in factors)

baseline_emissions = calculate_total_emissions(baseline_factors, emission_factors)

def sensitivity_analysis(factor_name, change_percentage, baseline_factors, emission_factors):
    modified_factors = baseline_factors.copy()
    modified_factors[factor_name] *= (1 + change_percentage / 100)
    modified_emissions = calculate_total_emissions(modified_factors, emission_factors)
    impact = modified_emissions - baseline_emissions
    return impact

results = []
change_percentages = [10, -10] 
for factor in baseline_factors:
    for change in change_percentages:
        impact = sensitivity_analysis(factor, change, baseline_factors, emission_factors)
        results.append({
            'Factor': factor,
            'Change (%)': change,
            'Impact on Emissions (kg CO2e)': impact
        })
df_results = pd.DataFrame(results)

df_results['Absolute Impact'] = df_results['Impact on Emissions (kg CO2e)'].abs()
most_important_factor = df_results.loc[df_results['Absolute Impact'].idxmax()]

print("Most influential factor on emissions:")
print(most_important_factor[['Factor', 'Change (%)', 'Impact on Emissions (kg CO2e)']])

plt.figure(figsize=(10, 6))
for change in change_percentages:
    subset = df_results[df_results['Change (%)'] == change]
    plt.bar(subset['Factor'] + f' ({change}%)', subset['Impact on Emissions (kg CO2e)'], label=f'{change}% Change')

plt.axhline(0, color='gray', linewidth=0.8)
plt.xlabel('Factor and Change (%)')
plt.ylabel('Impact on Total Emissions (kg CO2e)')
plt.title('Sensitivity Analysis of Factors on Total Emissions')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
