# Energy Consumption Dashboard (for UNCG)

This app displays the actual and predicted energy consumption values for different buildings/meters at University of North Carolina, Greensboro. User can provide various inputs as per the requirement, and the pulled out data is presented in highly interactive graphs. This app is built using python, plotly and Dash.

![demo](images/dash-energy-app-demo.gif)

## Table of Contents
* [Team Members](#team-members)
* [Introduction](#introduction)
* [Dataset](#dataset)
* [Pre-Requisites](#pre-requisites)
* [Setting up the app](#setting-up-the-app)
* [Start the app](#start-the-app)

## Team Members

Ritu Joshi and Shravya Muttineni, Computer Science Graduate Students at UNCG 
  

## Introduction
The purpose of this dashboard app is to display total or average energy consumption or average hourly consumption over various hours of the day, days of the week or over months of the year at UNCG. This app enables you to see the actual energy consumption by each building meter and then lets you compare it to the predicted values. Predictions are performed by using the statistical and machine learning models by team "Green Fund" and provided to us to create a dashboard. We can visualise the margin of error in the predictions (95% confidence interval) and it is represented in grey shade along the prediction line in graph 1.

Predictions are represented by dashed lines, and actual energy consumption values are presented by solid lines in the plots. 

## Datasets

The dataset containing the actual consumption, predicted consumption, margin of error lower and upper bounds, Meter Names and labels are provided to us as part of the Green Fund Hack-a-thon at UNCG which was held from November 16,2020 to November 23, 2020. The dataset is available in Data folder.

## Pre-Requisites
* Python 3
* Jupyter Notebook
* Git
* Plotly
* Dash
* Detailed requirements are provided in requirements.txt

## Setting up the app

First clone this repo:
```
git clone https://github.com/UNCG-CSE/Hackathon-Team4.git
cd Hackathon-Team4/src/dash-energy-app
```

Create a conda env (or venv) and install the requirements:
```
conda create -n dash-energy-app python=3.6.7
conda activate dash-energy-app
pip install -r requirements.txt
```


## Start the app

In a separate terminal window, you can now run the app:
```
python dash-energy-app.py
```

and visit http://127.0.0.1:8050/ or http://127.0.0.1:3004/.