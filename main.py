from website import create_app
from website.events import socketio

app = create_app()

if __name__ == '__main__':
    socketio.init_app(app)
    app.run(debug=True)
