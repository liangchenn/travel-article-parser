# Klook Article Parser

## Guide
1. Provide your `OPENAI_API_KEY` in `.env` file follow `.env.template` 
2. Build and Run the app from docker with following commands:

    ```
    # build docker image and run 
    $ make all

    # if image already exists
    $ make run
    ```
3. Use `docker container ls -a` to check current status
4. Open the app via `localhost:8501` link
5. Run following command to stop the app

    ```
    $ make stop
    ```