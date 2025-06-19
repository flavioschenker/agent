I will upload data trading data related of different client who have an Investment Advisor helping them with their trading activities.
The table has information on the duration of the client relationship and data of the monthly trading activities.
For each month there is 1 column with the number of transactions and 1 column with the brokerage volume.
This provides a picture on the frequency and the transaction sizes of the various clients.

I will provide a table with the following data:

- Column A – Client ID: individual clients, 1 client has 1 Investment Advisor
- Column B: Investment Advisor name
- Column C: Location of investment Advisor , 1 Location: n Advisors
- Column D: Region: of Investment Advisor (IA): 1 region: n sub regions
- Column E: sub region of Investment Advisor: 1 sub region: n locations
- Column F: date, start of client relationship, can give an idea, how many new clients are acquired.
- Column G: date, end of client relationship, if empty the client is still with the bank. Can give an idea on the client attrition.
- From Column H: monthly data on number of transactions, format: month year “number of transactions”
- From Column I: monthly data on brokerage volume, format: month year “number of transactions”
etc

#### Role:
You are an analyst supporting the head of the Investment Advisors.

#### Task:
Analyze the brokerage volumes and number of transactions in the various locations and regions of the bank according to the specific question.
Base your analysis ONLY on the provided data.

#### Requirements:
Question:
Provide latest figures

To Do:
- Aggregate the figures by Investment Advisor, Location of Investment Advisor, Region of Investment Advisor, Subregion of Investment Advisor for:
    - Latest month
    - Latest month – 1
    - YTD (first month of current year until latest month)
    - PreviousYTD (first month of current year – 1 until latest month)
- Calculate the % change of the figures by Investment Advisor, Location of Investment Advisor, Region of Investment Advisor, Subregion of Investment Advisor for:
    - Current months vs. Latest month
    - YTD vs Previous YTD

Question:
Explain the MTD change (e.g. Brokerage Volume), current month vs previous month

To Do:
- Calculate the MTD change in absolute figures of the KPI by
    - Region
    - Location
    - Investment Advisors
- Calculate the standard deviation for KPI MTD change (e.g. Brokerage Volume) to measure equality:
    - Regions vs total
    - Clients within the locations
    - Locations within sub regions
    - Investment Advisors within location
- Calculate the Z-scores for KPI MTD change (e.g. Brokerage Volume) to find outliers:
    - Regions vs Total
    - Clients within the locations
    - Locations within sub regions
    - Investment Advisors within location
- Check if there was change in the number of clients (column F: Start date of relationship, column G; end date of relationship)
    - New client = Start date in latest month or latest month – 1
    - Lost client = end date in latest month
    - Aggregate KPIs (e.g. brokerage volume) of new clients in latest month to identify if a substantial part of the positive change is related to newer clients by
        - Investment Advisor
        - Location
        - Sub Region
        - Region
    - Aggregate KPIs of lost client of the last 6 months and calculate the monthly average to see if the change can be partly explained by lost clients by
        - Investment Advisor
        - Location
        - Sub Region
        - Region

Question:
Explain the YTD change (e.g. Brokerage Volume), current YTD vs previous YTD

To Do:

- Calculate the YTD change in absolute figures of the KPI by
    - Region
    - Location
    - Investment Advisors
- Calculate the standard deviation for KPI YTD change (e.g. Brokerage Volume) to measure equality:
    - Regions vs total
    - Clients within the locations
    - Locations within sub regions
    - Investment Advisors within location
- Calculate the Z-scores for KPI YTD change (e.g. Brokerage Volume) to find outliers:
    - Regions vs Total
    - Clients within the locations
    - Locations within sub regions
    - Investment Advisors within location
- Check if there was change in the number of clients (column F: Start date of relationship, column G; end date of relationship)
    - New client = Start date in current year
    - Lost client = end date in current year
    - Aggregate KPIs (e.g. brokerage volume) of new clients in current year to identify if a substantial part of the positive change is related to newer clients by
        - Investment Advisor
        - Location
        - Sub Region
        - Region
    - Aggregate KPIs of lost client of the last year and calculate a proportional average (if current month is March à x3) to see if the change can is related to lost clients, by
        - Investment Advisor
        - Location
        - Sub Region
        - Region

2. **Specific Examples:**
- "Monthly average trading volume in Location A has decreased in April because clients are trading less or lower transaction volumes than in March."
- "Location B has many new clients and thus reports an increase in trading volume."
- "Region XY has more active trading clients, while Region Z shows fewer trades but higher transaction sizes."


3. **Outliers:**
- Identify any significant outliers in trading patterns or brokerage volumes. These are data points that deviate significantly from the average pattern.

4. **Significant Changes:**
- Highlight relatively big changes, such as notable increases or decreases in transactions or brokerage volumes. For example, "Mexico City saw a significant increase in brokerage volumes due to new clients joining in 2024."

5. **Deliverables:**

- Key findings summarized in 5 key bullets.
- Detailed tables summarizing transactions and brokerage volumes by location and region.
- Analysis highlighting any significant deviations and notable changes impacting overall trends.