# Travel Article Parser

## Description
The Travel Article Parser could parse the article by providing the url.
Parsed results will be processed to extract the POI (point of interest) information.

## Guide
1. Provide your `OPENAI_API_KEY` in `.env` file follow the `.env.template` 
2. Build and Run the app from docker with following commands:

    ```
    # build docker image and run 
    $ make up

    # if docker image already exists
    $ make run

    ```
3. Use `docker container ls -a` to check current status
4. Open the app via `localhost:8501` link
5. Run following command to stop the app

    ```
    # stop the service
    $ make stop

    # stop the service and remove the image
    $ make down
    ```