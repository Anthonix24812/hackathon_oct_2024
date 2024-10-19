
import matplotlib.pyplot as plt

data = {
    "recycled_metals": {
        "2021": {
            "average_recycled_content": {
                "value": 30,
                "unit": "%"
            },
            "recycled_tin": {
                "value": 30,
                "unit": "%"
            },
            "recycled_gold": {
                "value": 1,
                "unit": "%"
            }
        },
        "2022": {
            "average_recycled_content": {
                "value": 20,
                "unit": "%"
            },
            "recycled_tin": {
                "value": 38,
                "unit": "%"
            },
            "recycled_gold": {
                "value": 4,
                "unit": "%"
            }
        }
    }
}

years = list(data["recycled_metals"].keys())
recycled_tin_values = [data["recycled_metals"][year]["recycled_tin"]["value"] for year in years]
recycled_gold_values = [data["recycled_metals"][year]["recycled_gold"]["value"] for year in years]

# Creating bar chart for recycled tin and recycled gold values
plt.figure(figsize=(10, 6))
bar_width = 0.35
index = range(len(years))
bar1 = plt.bar(index, recycled_tin_values, bar_width, label='Recycled Tin', color='b')
bar2 = plt.bar([i + bar_width for i in index], recycled_gold_values, bar_width, label='Recycled Gold', color='g')

plt.xlabel('Year')
plt.ylabel('Percentage')
plt.title('Reported Levels of Recycled Metals in Apple Products (2021-2022)')
plt.xticks([i + bar_width/2 for i in index], years)
plt.legend()
plt.tight_layout()

plt.savefig('result.png')
  