from apps import create_app, db
from flask_migrate import Migrate


app = create_app()

Migrate(app=app, db=db)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, reload=True)
