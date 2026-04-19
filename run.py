from monitor.admin.app import app
from monitor.db import init_db

if __name__ == "__main__":
    init_db()
    app.run(debug=True)