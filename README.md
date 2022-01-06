# BRAW Face Authentication System

BRAW is a simple website that enables you to login with your face instead of the traditional email and password login. BRAW also enables you to cartoonize your profile picture to make look cooler 😎

---

**Prerequisites:**

You need [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) to be installed before you clone our code.

**How to use:**

Clone the repo:

`$ git clone https://github.com/abdullahalshawafi/Face-Authentication-System.git`

Open the project's folder:

`$ cd Face-Authentication-System`

Create a new conda environment and give it a name

`$ conda create --name <env> --file requirements.txt`

Activate the new conda environment that you just created

`$ conda activate <env>`

Open sqlite3

`$ sqlite3 database.db`

Populate the database

`$ .read schema.sql`

Exit from sqlite3 using `Ctrl + C` then start app.py

`$ python app.py`

The app should be running locally at <http://127.0.0.1:5000/>


# Explainer video

https://user-images.githubusercontent.com/58189568/148336412-1657ae27-4763-4c5f-a236-24a6372f5af6.mp4




