from backend import app
import os

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', debug=True)
if __name__ == '__main__':  # Script executed directly?
    print("songs application.")
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "8081")), debug=False)
