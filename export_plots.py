import pandas as pd
import plotly.graph_objects as go
import os


def preprocess(path):
    
    district_data=pd.read_csv(path)
    district_data.drop(['State','District'],axis=1,inplace=True)
    district_data.set_index('Date',inplace=True)
    
    district_data=district_data.diff(1)
    
    district_data.drop([district_data.head(1).index[0],district_data.tail(1).index[0]],inplace=True)
    
    district_data.set_index(pd.DatetimeIndex(district_data.index),inplace=True)
    
    return district_data


def export_plot(filename):
    
    observed_path='./Dataset/Districts/'+filename
    forecast_path='./Dataset/Forecasts/'+filename
    
    output_path='./Dataset/Plots/'+filename[:-4]+".png"
    
    observed=preprocess(observed_path)
    
    forecast=pd.read_csv(forecast_path,header=None,names=['Date','Confirmed'])
    forecast.set_index(pd.DatetimeIndex(forecast['Date']),inplace=True)
    forecast.drop('Date',axis=1,inplace=True)
    
    fig=go.Figure()

    fig.add_trace(go.Scatter(
        x=observed.index,
        y=observed["Confirmed"],
        name="Observed"
    ))

    fig.add_trace(go.Scatter(
        x=forecast.index,
        y=forecast["Confirmed"],
        name="Forecast"
    ))

    fig.update_layout(
        title=filename[:-4],
        xaxis_title="Date",
        yaxis_title="New Confirmed Cases"
    )
    
    fig.write_image(output_path)

files=os.listdir('./Dataset/Forecasts/')

for file in files:
	print(file)
	export_plot(file)