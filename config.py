import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGO_URI = "mongodb+srv://saiteja:saiteja@saidev.pmtwzvn.mongodb.net/?retryWrites=true&w=majority&appName=saidev"
#     app.secret_key = os.urandom(24)

# # MongoDB Configuration
# uri = "mongodb+srv://saiteja:saiteja@saidev.pmtwzvn.mongodb.net/?retryWrites=true&w=majority&appName=saidev"

# # Create a new client and connect to the server
# mongo = MongoClient(uri)

# # Send a ping to confirm a successful connection
# try:
#     mongo.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
