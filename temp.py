
import matplotlib.pyplot as plt

data = {
    "recycled_tin": {
        "2021": {
            "percentage": 30,
            "unit": "%"
        },
        "2022": {
            "percentage": 38,
            "unit": "%"
        }
    }
}

years = list(data['recycled_tin'].keys())
percentages = [data['recycled_tin'][year]['percentage'] for year in years]

plt.figure(figsize=(8, 5))
plt.bar(years, percentages, color='skyblue')
plt.xlabel('Year')
plt.ylabel('Percentage')
plt.title('Reported Levels of Recycled Tin in Apple Products (2021-2022)')
plt.ylim(0, 50)

for i, percentage in enumerate(percentages):
    plt.text(i, percentage + 1, f'{percentage}%', ha='center', color='black')

plt.savefig('result.png')
