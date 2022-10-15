# How to run
Use python 3.10+ to run
```
    # After cloning the github repository, cd into directory
    # create a venv
    > python -m venv ./venv
    # activating venv in windows
    > .\Venv\Scripts\Activate.ps1
    # install requirements
    > pip install -r requirements.txt
    # run development server
    > uvicorn main:app --reload --port 8001
```