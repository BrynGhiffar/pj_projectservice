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
## Attention
* When running this service with a `mongodb+srv` connection. You need to change the configuration in the `adapter/repository/config/config.py` to use the `tlsCAFile`.
# Using Docker Containers
If you are building using the docker container and have mongodb installed locally,
then you would want to change the `.env` file in the configuration and set 
`MONGO_URI=mongodb://host.docker.internal:27017/`. Then if you have docker installed,
you can do the following commands:
```
    # build docker image, after cd into directory.
    > docker image build -t pj-projectservice .
    # run the image as a docker container, in interactive terminal mode.
    # you can remove -it if you want to run it in background
    > docker container run -p 8000:8000 -it --name pj-projectservice-container pj-projectservice
```
## Restarting the container
```
    # stop the running container
    > docker container kill pj-projectservice-container
    # prune/remove the stopped container
    > docker container prune
    # check running containers
    > docker container ls -a
```