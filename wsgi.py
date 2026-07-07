"""Entry point WSGI per il deploy (PythonAnywhere, Render, gunicorn, ecc.).

Su PythonAnywhere: nel file di configurazione web che ti forniscono,
sostituisci il contenuto con:
    import sys
    path = '/home/TUO_USERNAME/bandi-militari-app'
    if path not in sys.path:
        sys.path.append(path)
    from wsgi import application
"""

import os

from app import create_app

application = create_app()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)))
