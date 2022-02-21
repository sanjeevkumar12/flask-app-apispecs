from app import create_app

try:
    app = create_app()
    if __name__ == "__main__":
        app.run()
except ImportError as e:
    print(e)
