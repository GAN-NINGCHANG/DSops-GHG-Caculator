data = {
    'Building': ['Building A', 'Building B', 'Building C'],
    'SQFT': [10000, 20000, 15000],  
    'co2': [54000, 108000, 80000]
}
df = pd.DataFrame(data)

benchmark_emission_intensity = 6.4

df['Expected_CO2'] = df['SQFT'] * benchmark_emission_intensity
df['Difference'] = df['co2'] - df['Expected_CO2'] 

plt.figure(figsize=(8, 6))
colors = ['red' if diff > 0 else 'green' for diff in df['Difference']]

bar_width = 0.4
index = range(len(df))
plt.bar(index, df['co2'], width=bar_width, color='skyblue', label='Actual CO2 Emissions')
plt.bar([i + bar_width for i in index], df['Expected_CO2'], width=bar_width, color='lightgray', label='Benchmark CO2 Emissions')

plt.plot([i + bar_width / 2 for i in index], df['Difference'], color='black', marker='o', linestyle='--', linewidth=2, label='Difference from Benchmark')

for i, (diff, color) in enumerate(zip(df['Difference'], colors)):
    plt.text(i + bar_width / 2, df['co2'][i] + diff / 2, f'{diff:.0f} kg', color=color, ha='center', fontweight='bold')

plt.xlabel('Building')
plt.ylabel('CO2 Emissions (kg)')
plt.title('Actual vs. Benchmark CO2 Emissions with Differences')
plt.xticks([i + bar_width / 2 for i in index], df['Building'])
plt.legend()
plt.tight_layout()
plt.show()
