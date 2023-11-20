from datetime import datetime

# Get the current date
current_date = datetime.now()

# Extract the year and month from the current date
year = current_date.year
month = current_date.month

# Convert the year and month to a string in the format 'YYYYMM'
formatted_date = f"{year}{month:02d}"

# Print the formatted date
print(formatted_date)
