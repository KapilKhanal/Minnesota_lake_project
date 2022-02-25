# Minnesota_lake_project
Lake Quality and Taxation data interaction and prediction of median sale value

This project is the deployment part of the citizen science project about the water quality of lake data. This project is for developing restAPI for batch prediction

Data pipeline is deployed locally and the file will be uploaded to another cloud service probaly s3
and then the script in this package will look for new files in the location and then run the ci/cd pipeline for machine learning delivery

The predictions at the moment are not that great but this is just an exercise for learning how to deliver a data product in buisnness settings. 

All the tools that are used in commercial application are used: 
Heroku
CD/CI
Test Intergration
RESTapi

train.csv and test.csv from https://github.com/KapilKhanal/lake_project

This puts the model in a server to which another web dashboard posts test dataset for predictions. The architecture of the machine learning deployment was inspired by the excellent course/tutorial by https://christophergs.com/







