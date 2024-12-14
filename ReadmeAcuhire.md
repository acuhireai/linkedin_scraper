### AcuHire AI


# Step 1: Create a Virtual Environment  using venv:

python3 -m venv venv
source venv/bin/activate
(Windows:)
venv\Scripts\activate


# Step 2: Install Dependencies


pip install -r requirements.txt


# Step 3: Set Environment Variables
.env


## Build the Docker Image:
docker build -t flask-linkedin-app .
docker run -p 8080:8080 flask-linkedin-app

bash
Copy code
docker build --build-arg OS_TYPE=mac -t linkedin-scraper .
Replace mac with linux if you are deploying on a Linux host.

Run the Container:

bash
Copy code
docker run -d -p 8080:8080 --env OS_TYPE=mac linkedin-scraper
Test the API: Use curl or any API testing tool like Postman:

bash
Copy code
curl -X POST http://localhost:8080/scrape -H "Content-Type: application/json" -d '{"linkedin_profile_url": "https://www.linkedin.com/in/some-profile"}'