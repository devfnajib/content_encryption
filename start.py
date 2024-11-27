import sys
from app import create_application

app = create_application()

if __name__ == '__main__':
    app.run(debug=True, port=int(sys.argv[2]))
