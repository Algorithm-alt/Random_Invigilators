# 🏫 Random Invigilator System

This project is designed to help schools assign invigilators randomly to exam halls. By using automation, the system ensures a fair distribution of duties and removes any manual favoritism.

## 🚀 Features
* **Random Assignment:** Automatically pairs staff members with specific exam halls.
* **Fairness:** Ensures no manual bias in the selection process.
* **Django Powered:** Built using the Django 6.0 web framework for a robust backend.

## 🛠️ How it Works
The system uses **Python for loops** and randomization logic to:
1.  Iterate through a list of available staff members.
2.  Assign them to a list of available halls.
3.  Generate a final schedule for the exam period.

## 💻 Setup and Installation
To run this project locally:
1. Clone the repository: `git clone https://github.com/Algorithm-alt/Random_Invigilators.git`
2. Activate the virtual environment: `.\.venv\Scripts\activate`
3. Install dependencies: `pip install django`
4. Run the server: `python manage.py runserver`
