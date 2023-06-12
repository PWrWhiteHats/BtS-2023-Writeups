from webapp import app
from webapp.db import create_db
from webapp.views import bp

if __name__ == "__main__":
    create_db()
    app.register_blueprint(bp)
    app.run(host='0.0.0.0', port=1337)
