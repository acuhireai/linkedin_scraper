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
actions.login(driver, email, password)

# Swagger UI setup
SWAGGER_URL = '/swagger'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, '/swagger.json')
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Flask-APISpec setup
docs = FlaskApiSpec(app)

# Schema definitions


class LoginSchema(Schema):
    email = fields.String(required=True, description="LinkedIn email")
    password = fields.String(required=True, description="LinkedIn password")


print(Person("https://www.linkedin.com/in/jojojoseph/",
             driver=driver, close_on_complete=False))
# print(Company("https://ca.linkedin.com/company/google",
#       driver=driver, close_on_complete=False))


@app.route('/login', methods=['POST'])
@doc(description="Login the user and set session.", tags=["Authentication"])
@use_kwargs(LoginSchema, location="json")
def login(email, password):
    if 'user_logged_in' in session:
        return jsonify({"message": "Already logged in"}), 200

    if email == os.getenv("LINKEDIN_USER") and password == os.getenv("LINKEDIN_PASSWORD"):
        session['user_logged_in'] = True
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@app.route('/logout', methods=['POST'])
@doc(description="Logout the user and clear session.", tags=["Authentication"])
def logout():
    session.pop('user_logged_in', None)
    return jsonify({"message": "Logged out successfully"}), 200


@app.route('/person', methods=['GET'])
@doc(description="Fetch LinkedIn person details.", tags=["LinkedIn Data"])
def get_person():
    if 'user_logged_in' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    profile_url = request.args.get('url')
    if not profile_url:
        return jsonify({"message": "Profile URL is required"}), 400

    try:
        person = Person(profile_url, driver=driver, close_on_complete=False)
        return jsonify({
            "name": person.name,
            "job_title": person.job_title,
            "company": person.company,
            "education": person.education
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Register routes with Flask-APISpec
docs.register(login)
docs.register(logout)
docs.register(get_person)

# Serve the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
