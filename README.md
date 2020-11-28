# sqlalchemy-challenge

The SQLalchemy challenge was completed by developing a juputer notebook for the climate analysis and a flask python application for the api.

The climate.ipynb jupyter notebook performs the following:
1. Connects to the hawaii.sqlite file found in the Resources folder.
2. Reflects the hawaii.sqlite database 
3. Returns the table names in the database
4. Returns the field and data types for each table.
5. Queries the database for the last 12 months of pprecipitation data and plots the results with pandas plotting and matplotlib.
6. Calculates the summary stats for the precipitation data.
7. Runs a query that returns the number of stations in the dataset.
8. Lists the stations by total number of measurements in the dataset.
9. Calculates the min, max, and avg temp for the most active station.
10. Queries the date and tobs for the most active station.
11. Generates a historgram for the dates and tobs queires in the previous step.
12. Displays the average temp for June months and the average temp for December months from the dataset.
13. Performs a t-test on the average temp for June months and the average temp for December months.
14. Uses the function calc_temps to calculate tmin, tavg, and tmax for a set of vacation dates.
15. Plots the previous step's results as a bar chart using peak-to-peak value as the y error bar.
16. Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates.
17. Calculates the daily normals for he vacation trip
18. Creates a dataframe of the daily normals.
19. Plots the daily normals as an area plot with stacked=false.

