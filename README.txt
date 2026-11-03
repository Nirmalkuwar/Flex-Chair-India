FLEX CHAIR WEBSITE - BEGINNER SETUP

1. Install Python from https://www.python.org/downloads/
   During Windows installation, tick "Add Python to PATH".

2. Install Visual Studio Code from https://code.visualstudio.com/

3. Extract this ZIP file to a folder, for example Desktop/flex_chair_website.

4. Open that folder in VS Code:
   File > Open Folder > choose flex_chair_website.

5. Open Terminal > New Terminal in VS Code.

6. Install Flask:
   python -m pip install flask
   If that does not work on Windows, try:
   py -m pip install flask

7. Run the website:
   python app.py
   Or on Windows:
   py app.py

8. Open your browser and visit:
   http://127.0.0.1:5000

IMPORTANT CUSTOMIZATION:
- Open app.py.
- Change PHONE, EMAIL and ADDRESS near the top.
- Change the PRODUCTS list to your real chair models and prices.
- Replace the sample text with your real business information.
- Add your own product photographs before publishing.

ORDER FORM:
When a customer submits an enquiry, it is saved in orders.csv in the project folder.
This starter project runs on your own computer. To receive customer enquiries over the internet,
you must deploy it to a Python hosting service and configure secure production settings.
Do not use Flask debug mode on a public website. Set a strong secret key before deployment.

This is an enquiry website, not a complete payment checkout. Add a trusted payment provider
and appropriate order, privacy and refund policies if you later want online payments.
