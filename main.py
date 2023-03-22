from __init__ import app, config


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT)
