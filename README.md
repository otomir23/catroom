# catroom

This is a forum (image board), made in Python with Flask for Yandex Academy Lyceum 2022-2023.

## See the website

The website is currently hosted [here](https://cat.otomir23.me), but there are no guarantees that it will be up for long.

## Running from source

> NOTE: You will need PostgreSQL and Node.js installed.

1. Download the code using `git clone` or as a ZIP archive (don't forget to unpack it).
2. Create a new virtual environment using `python -m venv venv`
3. Activate it using activate scripts in the venv directory
4. Install Python dependencies using `pip install -r requirements.txt`
5. Install Node.js dependencies using `npm i`
6. Build TailwindCSS styles using `npm run build`
7. Configure the server using `.env` file or environment variables
    ```dotenv
    DB_NAME= # name of psql database that will be used by website
    DB_HOST=
    DB_PORT= # optional, default: 5432
    DB_USERNAME=
    DB_PASSWORD=
    HOST= # ip that server will be started on, default: localhost
    PORT= # port that will be used by the server, default: 80
    SECRET_KEY= # csrf token
    ```
8. Start the server using `python main.py`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.