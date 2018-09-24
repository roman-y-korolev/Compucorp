# Compucorp test task

This is from csv to CiviCRM data loader (events and participants). It uses aiohttp for api calls to increase the speed. To run the script on a schedule, you can use any schedule tool like rundeck or crontab.

## Howto

- Create virtual environment 

```
virtualenv -p python3.6 venv
source venv/bin/activate
```
- Install requirements

```
pip install -r rquirements.txt
```
- Run

```
python run.py
```

## How it works

1.  Reading all events data from the directory `csv/loaded/events/`
    
2.  Creating events in the CiviCRM system with API
    
3.  Getting all contacts data from the CiviCRM
    
4.  Reading all participants data from the directory `csv/loaded/participants`
    
5.  Matching participants data with events and contacts
    
6.  Creating participants in the CiviCRM with API
    
7.  Moving files from the loaded directory to the processed directory
    

## Assumptions

1.  Data always comes in the same format as in the example (date format, separators and etc.)
    
2.  The server will withstand the load from parallel data loading. No restrictions are required.




