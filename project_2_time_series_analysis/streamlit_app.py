import streamlit as st

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import plotly.express as px

individual_stocks_path = r"/Users/rubisc/workspace/data_analytics_real_world_projects/project_2_time_series_analysis/S&P_resources/individual_stocks_5yr/"

company_list = [individual_stocks_path + "AAPL_data.csv", 
                individual_stocks_path + "AMZN_data.csv",
                individual_stocks_path + "GOOG_data.csv",
                individual_stocks_path + "MSFT_data.csv",
               ]

all_data = pd.DataFrame()

for file in company_list:
    current_df = pd.read_csv(file)
    all_data = current_df.append(all_data, ignore_index=True)
    
all_data['date'] = pd.to_datetime(all_data['date'])

print(all_data)
print(all_data.columns)

st.set_page_config(page_title = "Stock Analysis Dashboard", layout= "wide")
st.title("Tech Stocks Analysis Dashboard")

tech_list = sorted(all_data['Name'].unique())
print(tech_list)
st.sidebar.title("Choose a Company:")

selected_company = st.sidebar.selectbox("Select a stock", tech_list)
print("~~~~~~~~~~ Selected company:")
print(selected_company)

company_df = all_data[all_data['Name'] == selected_company]
company_df.sort_values('date', inplace=True)

print("~~~~~~~~~~ Selected df:")
print(company_df)

# 1st plot
st.subheader(f"1. Closing Price of {selected_company} Over Time")
# fig1 = px.line(company_df, x="date", y="close", title=selected_company + " closing prices over time")
# st.plotly_chart(fig1, use_container_width=True)
chart_data = company_df.set_index('date')[['close']] 

st.line_chart(
    chart_data, 
    use_container_width=True
)

# 2nd plot
st.subheader("2. Moving Averages (10, 20, 50 days)")
ma_day = [10, 20, 50]

for ma in ma_day:
    company_df['close_' + str(ma)] = company_df['close'].rolling(ma).mean()

# fig2 = px.line(company_df, x="date", y=["close", "close_10", "close_20", "close_50"], 
#                title=selected_company + " closing prices with moving average")
# plot_df = company_df.dropna(subset=["close_10", "close_20", "close_50"])
# fig2 = px.line(plot_df, x="date", y=["close", "close_10", "close_20", "close_50"], 
#                    title=f"{selected_company} closing prices with moving average")
# st.plotly_chart(fig2, use_container_width=True)

# 2. Select the columns needed for the plot: the x-axis (date) and all y-axes.
#    Then, set 'date' as the index for st.line_chart.
chart_data = company_df.set_index('date')[["close", "close_10", "close_20", "close_50"]]

# 3. Use st.line_chart to display the graph. Streamlit automatically uses 
#    the index for the x-axis and column names for the legend/lines.
st.line_chart(
    chart_data,
    use_container_width=True
)

# 3rd plot
st.subheader(f"3. Daily returns for {selected_company}")
company_df["Daily return in %"] = company_df['close'].pct_change()*100

# fig3 = px.line(company_df, x="date", y="Daily return in %", 
#                title="Daily return in %")
# st.plotly_chart(fig3, use_container_width=True)
daily_return_df = company_df.dropna(subset=["Daily return in %"])
chart_data_daily_return = daily_return_df.set_index('date')[["Daily return in %"]]

st.line_chart(
    chart_data_daily_return,
    use_container_width=True
)

# 4th plot
st.subheader(f"4. Resampled Closing Price (Monthly, Quarterly, Yearly)")

company_df.set_index('date', inplace=True)
resample_option = st.radio("Select Resample Frequency", ["Monthly", "Quarterly", "Yearly"])

if resample_option == "Monthly":
    resampled = company_df['close'].resample('M').mean() 
elif resample_option == "Quarterly":
    resampled = company_df['close'].resample('Q').mean() 
else:
    resampled = company_df['close'].resample('Y').mean() 

# company_df["Daily return in %"] = company_df['close'].pct_change()*100

# fig4 = px.line(resampled,
#                title=f"{selected_company} {resample_option} Average Closing Price")
# st.plotly_chart(fig4, use_container_width=True)

st.line_chart(
    resampled,
    use_container_width=True
)

# 5th plot
aapl_data = pd.read_csv(company_list[0])
amzn_data = pd.read_csv(company_list[1])
goog_data = pd.read_csv(company_list[2])
msft_data = pd.read_csv(company_list[3])

closing_price = pd.DataFrame()

closing_price['apple_close'] = aapl_data['close']
closing_price['amzn_close'] = amzn_data['close']
closing_price['goog_close'] = goog_data['close']
closing_price['msft_close'] = msft_data['close']

fig5, ax = plt.subplots()
sns.heatmap(closing_price.corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig5)
st.markdown("---")
st.markdown("**Note:** This dashboard provides basic technical analysis of maojr tech stocks using Python and Streamlit.")