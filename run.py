
#$env:DB_URL="postgresql+psycopg2://test_user:password@localhost:5432/test_db"

from core import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
