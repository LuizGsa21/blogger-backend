from app import create_app

if __name__ == '__main__':
    application = create_app()
    application.run('0.0.0.0', port=7001)
