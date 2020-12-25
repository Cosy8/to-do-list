from gui import gui
from database import database
import os

def main():
    data = database()
    data.info()
    gui(data)
    data.close()

if __name__ == "__main__":
    main()