import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from matplotlib.lines import Line2D


# Create the figure and dataset used for plotting
df = pd.DataFrame({
  'height': [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
  ,'animals': [0, 0.5, 1.1, 2.1, 4, 6, 9, 10, 10, 9, 6, 4, 2.6, 1.1, 0.5, 0, ]
})

df_lifeFindsAWay = pd.DataFrame({
  'height': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
  ,'animals': [0, 4, 5, 5, 4, 3, 7, 8, 8, 7, 5, 9, 10, 10, 9, 4, 2]
})

fig = plt.figure(figsize = (8, 4))
ax = fig.gca()

# Define variables
defaultFont = 'Arial'
defaultColor = '#070707'

# Set x Axis: ticks, format
ax.tick_params(length = 8, width = 1, direction = 'inout',
               labelsize = 9, color = defaultColor)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1.00))
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x}"))

# Set y Axis: ticks, labels, limit
ax.yaxis.set_major_locator(ticker.MultipleLocator(1.00))
ax.set_yticklabels(range(-1, 11, 1), rotation = 0,
                   ha = "center", va = "bottom",
                   size = 9, color = defaultColor)
ax.set_ylim(bottom = 0, top = 10.3)

# Set Axis font
for tick in ax.get_xticklabels():
    tick.set_fontname(defaultFont)
for tick in ax.get_yticklabels():
    tick.set_fontname(defaultFont)
    
# Set Axis titles and position
ax.set_xlabel('Height (cm)', labelpad = 8,
              color = defaultColor,  fontname = defaultFont)
ax.set_ylabel('A\nn\ni\nm\na\nl\ns', rotation = 0, labelpad = 20, va = 'center',
              color = defaultColor,  fontname = defaultFont)

# loop to create the grid
num = 0
for x in range(25, 42, 1):
  for y in range(0, 11, 1):
      num += 1
      plt.plot(x, y, marker = '*', markersize = 2, color = defaultColor)

# Remove the border
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add title
plt.title('JURASSIC PARK',
          size = 24, y=1.2, color = defaultColor,  fontname = defaultFont)
plt.suptitle('Height Distribution:    Procompsognathids',
          size = 12, y=1, color = defaultColor,  fontname = defaultFont)

# Add the legend
legend_elements = [Line2D([0], [0], label = 'animals',
                          marker = 'o', fillstyle = 'full',
                          color = 'white', markersize = 4,
                          markerfacecolor = 'white', markeredgecolor = defaultColor)]
ax.legend(handles = legend_elements, bbox_to_anchor = (0.11, -0.14),
          handletextpad = 0, edgecolor = 'w')

# Draw the plot
ax.plot(df.height, df.animals,
        marker = 'o', fillstyle = 'full',
        color = defaultColor, markersize = 4,
        markerfacecolor = 'white', markeredgecolor = defaultColor)

plt.show()