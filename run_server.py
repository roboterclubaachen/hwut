#!/usr/bin/env python3
from hwut_server import create_app

app = create_app()

app.run(debug=True)
