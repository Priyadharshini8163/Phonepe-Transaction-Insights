# Phonepe-Transaction-Insights
### Problem Statement:
With the increasing reliance on digital payment systems like PhonePe, understanding the dynamics of transactions, user engagement, and insurance-related data is crucial for improving services and targeting users effectively. This project aims to analyze and visualize aggregated values of payment categories, create maps for total values at state and district levels, and identify top-performing states, districts, and pin codes.

### Data Extraction:
Clone the GitHub repository containing PhonePe transaction data and load it into a SQL database.

### SQL Database and Table Creation:
- Set up a SQL database using a relational database management system (e.g., MySQL, PostgreSQL).
- Create tables to store data from the different folders:
### Aggregated Tables:
- Aggregated_user: Holds aggregated user-related data.
- Aggregated_transaction : Contains aggregated values for map-related data.
- Aggregated_insurance: Stores aggregated insurance-related data.
### Map Tables:
- Map_user: Contains mapping information for users.
- Map_map: Holds mapping values for total amounts at state and district levels.
- Map_insurance: Includes mapping information related to insurance.
### Top Tables:
- Top_user: Lists totals for the top users.
- Top_map: Contains totals for the top states, districts, and pin codes.
- Top_insurance: Lists totals for the top insurance categories.

### Technologies used:
 - Database: MySQL
 - Python Libraries: Pandas, matplotlib, seaborn, plotly expression
 - Visualization: Streamlit and PowerBI
   

