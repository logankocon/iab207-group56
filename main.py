from website import create_app

#starts flask server
if __name__ == '__main__':
    app = create_app()
    app.run()