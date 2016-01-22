from plotleaders import app, socketio
import os
if __name__ == "__main__":
    # Fetch the environment variable (so it works on Heroku):
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    #socketio.run(app, debug=True)
