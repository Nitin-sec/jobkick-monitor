from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from monitor.admin.app import app
from monitor.db import init_db
from monitor.config import Config

if __name__ == "__main__":
    init_db()
    app.run(host=Config.HOST, port=Config.APP_PORT, debug=Config.DEBUG)