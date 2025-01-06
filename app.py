from flask import Flask, jsonify, request, session
from flask_swagger_ui import get_swaggerui_blueprint
from flask_apispec import FlaskApiSpec, doc, use_kwargs
from marshmallow import Schema, fields
from linkedin_scraper import Person, Company, Job, JobSearch, actions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")


# Selenium WebDriver setup
driver = webdriver.Chrome()
email = os.getenv("LINKEDIN_USER")
password = os.getenv("LINKEDIN_PASSWORD")
actions.login(driver, email, password, timeout=100)


# print(Person("https://www.linkedin.com/in/jojojoseph/",
#       driver=driver,   close_on_complete=False, time_to_wait_after_login=2000))
# print(Company("https://ca.linkedin.com/company/google",
#               driver=driver, close_on_complete=False))


@ app.route('/person', methods=['GET'])
def get_person():

    profile_url = request.args.get('url')
    if not profile_url:
        return jsonify({"message": "Profile URL is required"}), 400

    try:
        person = Person(profile_url, driver=driver, close_on_complete=False)
        return jsonify({
            "name": person.name,
            "linkedin_url": person.linkedin_url,
            "about": person.about,
            "experiences": person.experiences,
            "interests": person.interests,
            "accomplishments": person.accomplishments,
            "also_viewed_urls": person.also_viewed_urls,
            "contacts": person.contacts,
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Serve the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
