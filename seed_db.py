import pymongo
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import random
import sys

MONGO_CONNECTION_STRING = "mongodb+srv://user:12345@cluster1.qjxgsoy.mongodb.net/"

print("Connecting to MongoDB...")
try:
    client = pymongo.MongoClient(MONGO_CONNECTION_STRING, serverSelectionTimeoutMS=5000)
    client.admin.command('ismaster')
    db = client.pool_management_system
    print("Connection successful.")
except pymongo.errors.ServerSelectionTimeoutError as err:
    print("\n--- MONGODB CONNECTION FAILED ---")
    print("Error details:", err)
    sys.exit(1)

print("Clearing any old data...")
db.users.drop()
db.employees.drop()
db.opportunities.drop()
db.applications.drop()
db.resumes.drop()
db.user_certifications.drop()
db.user_trainings.drop()
db.attendance_records.drop()
db.system_logs.drop()
print("Old data cleared.")

# --- MERGED EMPLOYEE & USER DATA SECTION ---

# This is the primary list from your newer file
users_data = [
    {'username': 'admin', 'password': 'admin123', 'role': 'admin', 'name': 'Admin User'},
    {'username': 'surendar', 'password': 'pass', 'role': 'consultant', 'name': 'Surendar'},
    {'username': 'mirudhula', 'password': 'pass', 'role': 'consultant', 'name': 'Mirudhula'},
    {'username': 'roshan', 'password': 'pass', 'role': 'consultant', 'name': 'Roshan'},
    {'username': 'sheela', 'password': 'pass', 'role': 'consultant', 'name': 'Sheela Maggi'},
    {'username': 'saikiran', 'password': 'pass', 'role': 'consultant', 'name': 'Sai Kiran'},
    {'username': 'gokul', 'password': 'pass', 'role': 'consultant', 'name': 'Gokul'},
    {'username': 'ananya', 'password': 'pass', 'role': 'consultant', 'name': 'Ananya'},
    {'username': 'tamilselvi', 'password': 'pass', 'role': 'consultant', 'name': 'Tamil Selvi'},
    {'username': 'arjun', 'password': 'pass', 'role': 'consultant', 'name': 'Arjun'},
    {'username': 'priya', 'password': 'pass', 'role': 'consultant', 'name': 'Priya'},
    {'username': 'karthik', 'password': 'pass', 'role': 'consultant', 'name': 'Karthik'},
    {'username': 'neha', 'password': 'pass', 'role': 'consultant', 'name': 'Neha'},
    {'username': 'vijay', 'password': 'pass', 'role': 'consultant', 'name': 'Vijay'},
    {'username': 'saranya', 'password': 'pass', 'role': 'consultant', 'name': 'Saranya Krishnan'}
]

employees_data = [
    {'username': 'surendar', 'name': 'Surendar', 'initials': 'S', 'role': 'Senior React Developer', 'status': 'Active', 'grade': 'A', 'email': 'surendar@company.com', 'domain': 'Frontend Development', 'experience': '4 years', 'phone': '+91 9876543210', 'joined': '2022-08-15', 'location': 'Chennai', 'project': 'E-commerce Platform', 'skills': ['React', 'TypeScript', 'Node.js', 'Redux'], 'attendance_score': 92, 'training_score': 85},
    {'username': 'mirudhula', 'name': 'Mirudhula', 'initials': 'M', 'role': 'Cloud Solutions Architect', 'status': 'Active', 'grade': 'A', 'email': 'mirudhula@company.com', 'domain': 'Cloud Computing', 'experience': '6 years', 'phone': '+91 9876543211', 'joined': '2020-01-20', 'location': 'Bangalore', 'project': 'Cloud Migration Project', 'skills': ['AWS', 'Azure', 'Kubernetes', 'Docker'], 'attendance_score': 96, 'training_score': 92},
    {'username': 'roshan', 'name': 'Roshan', 'initials': 'R', 'role': 'Mobile App Developer', 'status': 'Bench', 'grade': 'B', 'email': 'roshan@company.com', 'domain': 'Mobile Development', 'experience': '3 years', 'phone': '+91 9876543215', 'joined': '2023-04-18', 'location': 'Pune', 'project': 'Not Assigned', 'skills': ['React Native', 'Flutter', 'JavaScript', 'Firebase'], 'attendance_score': 85, 'training_score': 75},
    {'username': 'sheela', 'name': 'Sheela Maggi', 'initials': 'SM', 'role': 'DevOps Engineer', 'status': 'Active', 'grade': 'B+', 'email': 'sheela.maggi@company.com', 'domain': 'DevOps', 'experience': '3 years', 'phone': '+91 9876543212', 'joined': '2022-01-10', 'location': 'Hyderabad', 'project': 'Infrastructure Automation', 'skills': ['Jenkins', 'Docker', 'Kubernetes', 'Python'], 'attendance_score': 88, 'training_score': 78},
    {'username': 'saikiran', 'name': 'Sai Kiran', 'initials': 'SK', 'role': 'Full Stack Developer', 'status': 'Active', 'grade': 'B+', 'email': 'sai.kiran@company.com', 'domain': 'Full Stack Development', 'experience': '2.5 years', 'phone': '+91 9876543213', 'joined': '2023-09-05', 'location': 'Chennai', 'project': 'Customer Portal', 'skills': ['React', 'Node.js', 'MongoDB', 'Express'], 'attendance_score': 90, 'training_score': 82},
    {'username': 'gokul', 'name': 'Gokul', 'initials': 'G', 'role': 'Data Analyst', 'status': 'Active', 'grade': 'A-', 'email': 'gokul@company.com', 'domain': 'Data Science', 'experience': '3 years', 'phone': '+91 9876543220', 'joined': '2022-06-20', 'location': 'Mumbai', 'project': 'Analytics Dashboard', 'skills': ['SQL', 'Tableau', 'Python', 'Pandas'], 'attendance_score': 95, 'training_score': 88},
    {'username': 'ananya', 'name': 'Ananya', 'initials': 'A', 'role': 'UI/UX Designer', 'status': 'Active', 'grade': 'A', 'email': 'ananya@company.com', 'domain': 'Design', 'experience': '4 years', 'phone': '+91 9876543221', 'joined': '2021-11-15', 'location': 'Bangalore', 'project': 'Mobile App Redesign', 'skills': ['Figma', 'Adobe XD', 'User Research', 'Prototyping'], 'attendance_score': 94, 'training_score': 91},
    {'username': 'tamilselvi', 'name': 'Tamil Selvi', 'initials': 'TS', 'role': 'QA Engineer', 'status': 'Bench', 'grade': 'B', 'email': 'tamil.selvi@company.com', 'domain': 'Quality Assurance', 'experience': '2 years', 'phone': '+91 9876543222', 'joined': '2023-02-01', 'location': 'Chennai', 'project': 'Not Assigned', 'skills': ['Selenium', 'Jira', 'API Testing', 'SQL'], 'attendance_score': 89, 'training_score': 80},
    {'username': 'arjun', 'name': 'Arjun', 'initials': 'A', 'role': 'AI/ML Engineer', 'status': 'Active', 'grade': 'A', 'email': 'arjun@company.com', 'domain': 'Artificial Intelligence', 'experience': '5 years', 'phone': '+91 9876543223', 'joined': '2021-03-10', 'location': 'Bangalore', 'project': 'Predictive Analytics Engine', 'skills': ['Python', 'TensorFlow', 'PyTorch', 'Scikit-learn'], 'attendance_score': 96, 'training_score': 94},
    {'username': 'priya', 'name': 'Priya', 'initials': 'P', 'role': 'Product Manager', 'status': 'Active', 'grade': 'A-', 'email': 'priya@company.com', 'domain': 'Product Management', 'experience': '6 years', 'phone': '+91 9876543224', 'joined': '2020-09-01', 'location': 'Pune', 'project': 'SaaS Platform Development', 'skills': ['Agile', 'Roadmapping', 'Jira', 'User Stories'], 'attendance_score': 98, 'training_score': 90},
    {'username': 'karthik', 'name': 'Karthik', 'initials': 'K', 'role': 'Cybersecurity Specialist', 'status': 'Active', 'grade': 'B+', 'email': 'karthik@company.com', 'domain': 'Security', 'experience': '4 years', 'phone': '+91 9876543225', 'joined': '2022-01-20', 'location': 'Hyderabad', 'project': 'Threat Intelligence', 'skills': ['Penetration Testing', 'SIEM', 'Cryptography', 'CISSP'], 'attendance_score': 93, 'training_score': 85},
    {'username': 'neha', 'name': 'Neha', 'initials': 'N', 'role': 'Business Analyst', 'status': 'Active', 'grade': 'B+', 'email': 'neha@company.com', 'domain': 'Business Analysis', 'experience': '3.5 years', 'phone': '+91 9876543226', 'joined': '2022-07-11', 'location': 'Mumbai', 'project': 'Client Requirement Analysis', 'skills': ['BRD', 'FRD', 'UML', 'SQL'], 'attendance_score': 91, 'training_score': 84},
    {'username': 'vijay', 'name': 'Vijay', 'initials': 'V', 'role': 'Backend Developer (Java)', 'status': 'Bench', 'grade': 'B', 'email': 'vijay@company.com', 'domain': 'Backend Development', 'experience': '2 years', 'phone': '+91 9876543227', 'joined': '2023-05-19', 'location': 'Chennai', 'project': 'Not Assigned', 'skills': ['Java', 'Spring Boot', 'Microservices', 'PostgreSQL'], 'attendance_score': 87, 'training_score': 78},
    {'username': 'saranya', 'name': 'Saranya Krishnan', 'initials': 'SK', 'role': 'Full Stack Developer', 'status': 'Active', 'grade': 'B+', 'email': 'saranya.k@company.com', 'domain': 'Full Stack Development', 'experience': '3 years', 'phone': '+91 9876543230', 'joined': '2022-10-01', 'location': 'Chennai', 'project': 'Inventory Management System', 'skills': ['Angular', 'Node.js', 'Express', 'MongoDB'], 'attendance_score': 93, 'training_score': 88}
]

# This is the list from your older file, to be merged
old_users_data = [
    {'username': 'isha', 'password': 'pass', 'role': 'consultant', 'name': 'Isha Singh'},
    {'username': 'rohan', 'password': 'pass', 'role': 'consultant', 'name': 'Rohan Gupta'},
    {'username': 'aditi', 'password': 'pass', 'role': 'consultant', 'name': 'Aditi Rao'},
    {'username': 'vikram', 'password': 'pass', 'role': 'consultant', 'name': 'Vikram Kumar'},
    {'username': 'pooja', 'password': 'pass', 'role': 'consultant', 'name': 'Pooja Desai'},
    {'username': 'rahul', 'password': 'pass', 'role': 'consultant', 'name': 'Rahul Nair'},
    {'username': 'sneha', 'password': 'pass', 'role': 'consultant', 'name': 'Sneha Reddy'},
    {'username': 'amit', 'password': 'pass', 'role': 'consultant', 'name': 'Amit Patel'},
    {'username': 'divya', 'password': 'pass', 'role': 'consultant', 'name': 'Divya Iyer'},
    {'username': 'manish', 'password': 'pass', 'role': 'consultant', 'name': 'Manish Joshi'},
    {'username': 'sunita', 'password': 'pass', 'role': 'consultant', 'name': 'Sunita Menon'},
    {'username': 'sanjay', 'password': 'pass', 'role': 'consultant', 'name': 'Sanjay Verma'},
]

old_employees_data = [
    {'username': 'isha', 'name': 'Isha Singh', 'initials': 'IS', 'role': 'Frontend Developer', 'status': 'Active', 'grade': 'B', 'email': 'isha.singh@company.com', 'domain': 'Frontend Development', 'experience': '2 years', 'phone': '+91 9876543240', 'joined': '2023-03-12', 'location': 'Pune', 'project': 'Retail Analytics Dashboard', 'skills': ['Vue.js', 'JavaScript', 'HTML5', 'CSS3'], 'attendance_score': 94, 'training_score': 80, 'gender': 'Female'},
    {'username': 'rohan', 'name': 'Rohan Gupta', 'initials': 'RG', 'role': 'AWS Cloud Engineer', 'status': 'Bench', 'grade': 'B+', 'email': 'rohan.gupta@company.com', 'domain': 'Cloud Computing', 'experience': '3 years', 'phone': '+91 9876543241', 'joined': '2022-11-20', 'location': 'Bangalore', 'project': 'Not Assigned', 'skills': ['AWS EC2', 'S3', 'Lambda', 'Terraform'], 'attendance_score': 88, 'training_score': 85, 'gender': 'Male'},
    {'username': 'aditi', 'name': 'Aditi Rao', 'initials': 'AR', 'role': 'iOS Developer', 'status': 'Active', 'grade': 'A-', 'email': 'aditi.rao@company.com', 'domain': 'Mobile Development', 'experience': '4 years', 'phone': '+91 9876543242', 'joined': '2021-08-01', 'location': 'Hyderabad', 'project': 'Banking App', 'skills': ['Swift', 'UIKit', 'CoreData', 'Objective-C'], 'attendance_score': 97, 'training_score': 90, 'gender': 'Female'},
    {'username': 'vikram', 'name': 'Vikram Kumar', 'initials': 'VK', 'role': 'Site Reliability Engineer', 'status': 'Active', 'grade': 'A', 'email': 'vikram.kumar@company.com', 'domain': 'DevOps', 'experience': '5 years', 'phone': '+91 9876543243', 'joined': '2020-05-18', 'location': 'Pune', 'project': 'High-Traffic API Gateway', 'skills': ['Go', 'Prometheus', 'Grafana', 'Kubernetes'], 'attendance_score': 95, 'training_score': 93, 'gender': 'Male'},
    {'username': 'pooja', 'name': 'Pooja Desai', 'initials': 'PD', 'role': 'Python Developer', 'status': 'Bench', 'grade': 'B', 'email': 'pooja.desai@company.com', 'domain': 'Backend Development', 'experience': '2.5 years', 'phone': '+91 9876543244', 'joined': '2023-01-25', 'location': 'Mumbai', 'project': 'Not Assigned', 'skills': ['Python', 'Django', 'Flask', 'PostgreSQL'], 'attendance_score': 90, 'training_score': 79, 'gender': 'Female'},
    {'username': 'rahul', 'name': 'Rahul Nair', 'initials': 'RN', 'role': 'Data Scientist', 'status': 'Active', 'grade': 'A', 'email': 'rahul.nair@company.com', 'domain': 'Data Science', 'experience': '4 years', 'phone': '+91 9876543245', 'joined': '2021-09-01', 'location': 'Bangalore', 'project': 'Fraud Detection System', 'skills': ['Python', 'Scikit-learn', 'Pandas', 'SQL'], 'attendance_score': 96, 'training_score': 95, 'gender': 'Male'},
    {'username': 'sneha', 'name': 'Sneha Reddy', 'initials': 'SR', 'role': 'Product Designer', 'status': 'Active', 'grade': 'B+', 'email': 'sneha.reddy@company.com', 'domain': 'Design', 'experience': '3 years', 'phone': '+91 9876543246', 'joined': '2022-02-14', 'location': 'Hyderabad', 'project': 'Healthcare Management App', 'skills': ['UX Research', 'Wireframing', 'Figma', 'Prototyping'], 'attendance_score': 93, 'training_score': 88, 'gender': 'Female'},
    {'username': 'amit', 'name': 'Amit Patel', 'initials': 'AP', 'role': 'Automation Tester', 'status': 'Active', 'grade': 'A-', 'email': 'amit.patel@company.com', 'domain': 'Quality Assurance', 'experience': '5 years', 'phone': '+91 9876543247', 'joined': '2020-10-30', 'location': 'Chennai', 'project': 'Insurance Platform Testing', 'skills': ['Cypress', 'Playwright', 'JavaScript', 'CI/CD'], 'attendance_score': 95, 'training_score': 89, 'gender': 'Male'},
    {'username': 'divya', 'name': 'Divya Iyer', 'initials': 'DI', 'role': 'Machine Learning Engineer', 'status': 'Bench', 'grade': 'A', 'email': 'divya.iyer@company.com', 'domain': 'Artificial Intelligence', 'experience': '4 years', 'phone': '+91 9876543248', 'joined': '2021-07-22', 'location': 'Bangalore', 'project': 'Not Assigned', 'skills': ['PyTorch', 'NLP', 'Computer Vision', 'Python'], 'attendance_score': 92, 'training_score': 94, 'gender': 'Female'},
    {'username': 'manish', 'name': 'Manish Joshi', 'initials': 'MJ', 'role': 'Technical Product Manager', 'status': 'Active', 'grade': 'A', 'email': 'manish.joshi@company.com', 'domain': 'Product Management', 'experience': '7 years', 'phone': '+91 9876543249', 'joined': '2019-04-15', 'location': 'Mumbai', 'project': 'Developer API Platform', 'skills': ['Product Strategy', 'API Design', 'Agile', 'Jira'], 'attendance_score': 98, 'training_score': 91, 'gender': 'Male'},
    {'username': 'sunita', 'name': 'Sunita Menon', 'initials': 'SM', 'role': 'Security Consultant', 'status': 'Active', 'grade': 'A-', 'email': 'sunita.menon@company.com', 'domain': 'Security', 'experience': '6 years', 'phone': '+91 9876543250', 'joined': '2020-02-01', 'location': 'Pune', 'project': 'Cloud Security Audit', 'skills': ['Ethical Hacking', 'ISO 27001', 'Cloud Security', 'CISSP'], 'attendance_score': 97, 'training_score': 92, 'gender': 'Female'},
    {'username': 'sanjay', 'name': 'Sanjay Verma', 'initials': 'SV', 'role': 'Senior Business Analyst', 'status': 'Active', 'grade': 'A', 'email': 'sanjay.verma@company.com', 'domain': 'Business Analysis', 'experience': '8 years', 'phone': '+91 9876543251', 'joined': '2018-11-11', 'location': 'Hyderabad', 'project': 'Logistics Optimization', 'skills': ['Agile', 'SQL', 'Requirement Gathering', 'BRD'], 'attendance_score': 99, 'training_score': 90, 'gender': 'Male'}
]

# Get a set of existing usernames for quick lookup
existing_usernames = {user['username'] for user in users_data}

# Add new users and employees only if they don't already exist
for user in old_users_data:
    if user['username'] not in existing_usernames:
        users_data.append(user)
        # Find the corresponding employee and add them too
        employee_to_add = next((emp for emp in old_employees_data if emp['username'] == user['username']), None)
        if employee_to_add:
            employees_data.append(employee_to_add)

# --- REVISED OPPORTUNITIES DATA FOR REALISTIC MONITORING ---
opportunities_data = [
    # --- Live/Recent Activity ---
    {'title': 'AI/ML Engineer', 'company': 'FutureAI Corp', 'description': 'Work on cutting-edge machine learning models.', 'location': 'Bangalore', 'salary': '₹18L - ₹28L', 'experience': '4+ years', 'domain': 'AI/ML', 'skills': ['TensorFlow', 'Python', 'NLP'], 'posted': '2025-07-28', 'status': 'In Progress', 'startDate': '2025-05-20', 'endDate': None, 'lastUpdate': datetime.now() - timedelta(minutes=5)},
    {'title': 'Java Backend Developer', 'company': 'Enterprise Systems', 'description': 'Build high-performance, server-side applications.', 'location': 'Chennai', 'salary': '₹9L - ₹15L', 'experience': '2-4 years', 'domain': 'Backend', 'skills': ['Java', 'Spring Boot', 'Microservices'], 'posted': '2025-07-21', 'status': 'Open', 'startDate': None, 'endDate': None, 'lastUpdate': datetime.now() - timedelta(minutes=35)},
    {'title': 'Data Analyst', 'company': 'Data Insights Inc.', 'description': 'Analyze large datasets to identify trends.', 'location': 'Mumbai', 'salary': '₹8L - ₹14L', 'experience': '2-4 years', 'domain': 'Data Science', 'skills': ['SQL', 'Tableau', 'Python'], 'posted': '2025-07-25', 'status': 'In Progress', 'startDate': '2025-07-01', 'endDate': None, 'lastUpdate': datetime.now() - timedelta(hours=1, minutes=15)},
    {'title': 'UI/UX Designer', 'company': 'Creative Solutions', 'description': 'Create compelling user interfaces.', 'location': 'Bangalore', 'salary': '₹10L - ₹16L', 'experience': '3+ years', 'domain': 'Design', 'skills': ['Figma', 'Sketch', 'Prototyping'], 'posted': '2025-07-22', 'status': 'Open', 'startDate': None, 'endDate': None, 'lastUpdate': datetime.now() - timedelta(hours=3, minutes=45)},
    {'title': 'Senior React Developer', 'company': 'TechCorp Solutions', 'description': 'Build next-gen web applications with React.', 'location': 'Chennai', 'salary': '₹12L - ₹18L', 'experience': '3-5 years', 'domain': 'Frontend', 'skills': ['React.js', 'Redux', 'TypeScript'], 'posted': '2025-07-20', 'status': 'In Progress', 'startDate': '2025-06-01', 'endDate': None, 'lastUpdate': datetime.now() - timedelta(hours=8)},
    {'title': 'Scrum Master', 'company': 'AgileFlow', 'description': 'Facilitate agile ceremonies and remove impediments.', 'location': 'Bangalore', 'salary': '₹14L - ₹20L', 'experience': '4+ years', 'domain': 'Management', 'skills': ['Scrum', 'Jira', 'Agile Coaching'], 'posted': '2025-07-19', 'status': 'In Progress', 'startDate': '2025-07-10', 'endDate': None, 'lastUpdate': datetime.now() - timedelta(days=1, hours=4)},
    {'title': 'Site Reliability Engineer', 'company': 'Reliable Systems', 'description': 'Focus on reliability, scalability, and performance.', 'location': 'Hyderabad', 'salary': '₹16L - ₹24L', 'experience': '4+ years', 'domain': 'DevOps', 'skills': ['Kubernetes', 'Terraform', 'Prometheus'], 'posted': '2025-07-17', 'status': 'Completed', 'startDate': '2025-04-20', 'endDate': '2025-07-28', 'lastUpdate': datetime.now() - timedelta(days=2, hours=10)},
    
    # --- Completed Projects (for a healthier failure rate) ---
    {'title': 'Cloud Solutions Architect', 'company': 'CloudTech Innovations', 'description': 'Design and implement scalable cloud solutions.', 'location': 'Bangalore', 'salary': '₹20L - ₹30L', 'experience': '5-8 years', 'domain': 'Cloud', 'skills': ['AWS', 'Azure', 'Kubernetes'], 'posted': '2025-07-18', 'status': 'Completed', 'startDate': '2025-02-10', 'endDate': '2025-07-15', 'lastUpdate': datetime.now() - timedelta(days=22)},
    {'title': 'QA Automation Engineer', 'company': 'BugFinders Ltd.', 'description': 'Develop automated test scripts.', 'location': 'Chennai', 'salary': '₹7L - ₹11L', 'experience': '2+ years', 'domain': 'QA', 'skills': ['Selenium', 'Java', 'API Testing'], 'posted': '2025-07-20', 'status': 'Completed', 'startDate': '2025-03-15', 'endDate': '2025-06-30', 'lastUpdate': datetime.now() - timedelta(days=36)},
    {'title': 'Product Manager', 'company': 'Innovate Inc.', 'description': 'Define product vision and roadmap.', 'location': 'Pune', 'salary': '₹25L - ₹40L', 'experience': '5+ years', 'domain': 'Management', 'skills': ['Agile', 'Roadmapping', 'Market Research'], 'posted': '2025-07-24', 'status': 'Completed', 'startDate': '2025-01-05', 'endDate': '2025-07-25', 'lastUpdate': datetime.now() - timedelta(days=12)},
    {'title': 'UX Researcher', 'company': 'UserFirst', 'description': 'Conduct user research to inform product design.', 'location': 'Pune', 'salary': '₹9L - ₹13L', 'experience': '2+ years', 'domain': 'Design', 'skills': ['User Interviews', 'Usability Testing', 'Survey Design'], 'posted': '2025-07-15', 'status': 'Completed', 'startDate': '2025-06-05', 'endDate': '2025-07-10', 'lastUpdate': datetime.now() - timedelta(days=25)}, # Changed from Cancelled to Completed
    
    # --- Add more completed projects to make the data more robust ---
    {'title': 'Mobile Banking App', 'company': 'SecureBank', 'status': 'Completed', 'startDate': '2024-11-01', 'endDate': '2025-04-15', 'lastUpdate': datetime.now() - timedelta(days=110), 'description': 'Phase 1 of mobile banking app.', 'location': 'Mumbai', 'salary': 'N/A', 'experience': 'N/A', 'domain': 'Mobile', 'skills': ['React Native', 'Firebase']},
    {'title': 'E-commerce Platform Migration', 'company': 'Shopify Experts', 'status': 'Completed', 'startDate': '2025-01-15', 'endDate': '2025-05-20', 'lastUpdate': datetime.now() - timedelta(days=75), 'description': 'Migrated from Magento to Shopify Plus.', 'location': 'Remote', 'salary': 'N/A', 'experience': 'N/A', 'domain': 'Frontend', 'skills': ['Shopify', 'Liquid', 'React']},
    {'title': 'CRM Integration', 'company': 'ConnectAll', 'status': 'Completed', 'startDate': '2025-03-01', 'endDate': '2025-06-01', 'lastUpdate': datetime.now() - timedelta(days=65), 'description': 'Integrated Salesforce with internal tools.', 'location': 'Bangalore', 'salary': 'N/A', 'experience': 'N/A', 'domain': 'Backend', 'skills': ['Salesforce API', 'Python', 'MuleSoft']},
    {'title': 'Data Warehouse Setup', 'company': 'DataCorp', 'status': 'Completed', 'startDate': '2024-10-01', 'endDate': '2025-03-30', 'lastUpdate': datetime.now() - timedelta(days=125), 'description': 'Built a new data warehouse using BigQuery.', 'location': 'Hyderabad', 'salary': 'N/A', 'experience': 'N/A', 'domain': 'Data Science', 'skills': ['GCP', 'BigQuery', 'SQL', 'ETL']},
    {'title': 'Internal Helpdesk Portal', 'company': 'InnoTech', 'status': 'Completed', 'startDate': '2025-02-01', 'endDate': '2025-05-01', 'lastUpdate': datetime.now() - timedelta(days=95), 'description': 'A new portal for IT support tickets.', 'location': 'Chennai', 'salary': 'N/A', 'experience': 'N/A', 'domain': 'Full Stack', 'skills': ['React', 'Node.js', 'MongoDB']},
    {'title': 'Compliance Reporting Tool', 'company': 'FinReg Solutions', 'status': 'Completed', 'startDate': '2025-04-01', 'endDate': '2025-07-05', 'lastUpdate': datetime.now() - timedelta(days=30), 'description': 'Automated quarterly compliance reports.', 'location': 'Mumbai', 'salary': 'N/A', 'experience': 'N/A', 'domain': 'Backend', 'skills': ['Python', 'Pandas', 'PostgreSQL']},
    {'title': 'Marketing Automation', 'company': 'GrowthHackers', 'status': 'Completed', 'startDate': '2025-05-10', 'endDate': '2025-07-20', 'lastUpdate': datetime.now() - timedelta(days=16), 'description': 'Setup of HubSpot marketing funnels.', 'location': 'Remote', 'salary': 'N/A', 'experience': 'N/A', 'domain': 'Management', 'skills': ['HubSpot', 'Marketing API']},

    # --- One cancelled project for a low failure rate ---
    {'title': 'Cybersecurity Analyst', 'company': 'SecureNet', 'description': 'Monitor security infrastructure.', 'location': 'Hyderabad', 'salary': '₹11L - ₹17L', 'experience': '3-5 years', 'domain': 'Security', 'skills': ['SIEM', 'Penetration Testing', 'CISSP'], 'posted': '2025-07-26', 'status': 'Cancelled', 'startDate': '2025-04-01', 'endDate': '2025-05-10', 'lastUpdate': datetime.now() - timedelta(days=88)},
]


print("Seeding base data into MongoDB...")
db.users.insert_many(users_data)
db.employees.insert_many(employees_data)
result = db.opportunities.insert_many(opportunities_data)
opp_ids = result.inserted_ids
opp_map = {opp['title']: str(opp_id) for opp, opp_id in zip(opportunities_data, opp_ids)}

print("\nGenerating detailed profiles for each consultant...")
total_employees = len(employees_data)

for index, emp in enumerate(employees_data):
    progress = (index + 1) / total_employees * 100
    sys.stdout.write(f"\rProcessing consultant {index + 1}/{total_employees} ({progress:.0f}%)")
    sys.stdout.flush()

    username = emp['username']
    
    # --- Attendance ---
    attendance_records = []
    today = datetime.now()
    for day_offset in range(365):
        current_date = today - timedelta(days=day_offset)
        if current_date.weekday() < 5:  # Monday to Friday
            attendance_prob = emp.get('attendance_score', 90) / 100.0 # Use .get for safety
            status = random.choices(
                ['Present', 'WFH', 'Leave', 'Absent'],
                weights=[attendance_prob * 0.8, attendance_prob * 0.2, (1 - attendance_prob) * 0.5, (1 - attendance_prob) * 0.5],
                k=1
            )[0]
            attendance_records.append({
                'consultant_username': username,
                'date': current_date.strftime("%Y-%m-%d"),
                'status': status
            })

    if attendance_records:
        db.attendance_records.insert_many(attendance_records)

    # --- Certifications and Trainings (RESTORED FULL VERSION) ---
    certs, trainings = [], []

    if emp.get('domain') == 'Frontend Development':
        certs.extend([
            {'title': 'Meta Certified React Developer', 'issuer': 'Meta', 'status': 'Active', 'category': 'Frontend', 'issueDate': '2024-03-20', 'expiryDate': '2026-03-20', 'description': 'Official certification for advanced React skills.'},
            {'title': 'Advanced TypeScript', 'issuer': 'Udemy', 'status': 'Active', 'category': 'Frontend', 'issueDate': '2023-11-15', 'expiryDate': 'N/A', 'description': 'Mastery of TypeScript for large-scale applications.'}
        ])
        trainings.extend([
            {'title': 'Advanced React Patterns', 'type': 'Technical', 'status': 'In Progress', 'progress': 60, 'modulesCompleted': 6, 'modulesTotal': 10, 'duration': 25, 'deadline': '2025-09-01', 'instructor': 'Jane Doe'},
            {'title': 'Web Accessibility (WCAG)', 'type': 'Technical', 'status': 'Not Started', 'progress': 0, 'modulesCompleted': 0, 'modulesTotal': 7, 'duration': 15, 'deadline': '2025-09-15', 'instructor': 'John Smith'}
        ])
    elif emp.get('domain') == 'Full Stack Development':
        certs.extend([
            {'title': 'MERN Stack Certification', 'issuer': 'Coursera', 'status': 'Active', 'category': 'Full Stack', 'issueDate': '2024-04-10', 'expiryDate': 'N/A', 'description': 'Proficiency in MongoDB, Express, React, and Node.js.'},
        ])
        trainings.extend([
            {'title': 'Advanced Node.js', 'type': 'Technical', 'status': 'Completed', 'progress': 100, 'modulesCompleted': 12, 'modulesTotal': 12, 'duration': 30, 'deadline': '2025-01-15', 'instructor': 'Tech Academy'},
            {'title': 'GraphQL for Developers', 'type': 'Technical', 'status': 'In Progress', 'progress': 50, 'modulesCompleted': 5, 'modulesTotal': 10, 'duration': 20, 'deadline': '2025-10-01', 'instructor': 'API Masters'}
        ])
    elif emp.get('domain') == 'Cloud Computing':
        certs.extend([
            {'title': 'AWS Certified Solutions Architect', 'issuer': 'Amazon', 'status': 'Active', 'category': 'Cloud', 'issueDate': '2024-01-10', 'expiryDate': '2027-01-10', 'description': 'Expertise in AWS cloud architecture.'},
            {'title': 'Azure Fundamentals', 'issuer': 'Microsoft', 'status': 'Active', 'category': 'Cloud', 'issueDate': '2023-09-20', 'expiryDate': 'N/A', 'description': 'Foundational knowledge of Azure services.'}
        ])
        trainings.extend([
            {'title': 'Kubernetes for Cloud Engineers', 'type': 'Technical', 'status': 'Completed', 'progress': 100, 'modulesCompleted': 8, 'modulesTotal': 8, 'duration': 20, 'deadline': '2024-12-01', 'instructor': 'Cloud Academy'},
            {'title': 'Cloud Security Essentials', 'type': 'Technical', 'status': 'In Progress', 'progress': 40, 'modulesCompleted': 4, 'modulesTotal': 10, 'duration': 30, 'deadline': '2025-10-01', 'instructor': 'Security Co.'}
        ])
    elif emp.get('domain') == 'Mobile Development':
        certs.extend([
            {'title': 'React Native Certified Developer', 'issuer': 'Udemy', 'status': 'Active', 'category': 'Mobile', 'issueDate': '2023-12-01', 'expiryDate': 'N/A', 'description': 'Proficiency in React Native development.'}
        ])
        trainings.extend([
            {'title': 'Flutter App Development', 'type': 'Technical', 'status': 'In Progress', 'progress': 50, 'modulesCompleted': 5, 'modulesTotal': 10, 'duration': 25, 'deadline': '2025-09-10', 'instructor': 'Mobile Academy'}
        ])
    elif emp.get('domain') == 'DevOps':
        certs.extend([
            {'title': 'Certified Kubernetes Administrator', 'issuer': 'CNCF', 'status': 'Active', 'category': 'DevOps', 'issueDate': '2024-02-15', 'expiryDate': '2026-02-15', 'description': 'Expertise in Kubernetes administration.'}
        ])
        trainings.extend([
            {'title': 'Advanced DevOps Practices', 'type': 'Technical', 'status': 'Not Started', 'progress': 0, 'modulesCompleted': 0, 'modulesTotal': 12, 'duration': 30, 'deadline': '2025-11-01', 'instructor': 'DevOps Institute'}
        ])
    elif emp.get('domain') == 'Data Science':
        certs.extend([
            {'title': 'Tableau Desktop Specialist', 'issuer': 'Tableau', 'status': 'Active', 'category': 'Data Science', 'issueDate': '2024-04-01', 'expiryDate': '2026-04-01', 'description': 'Proficiency in data visualization with Tableau.'}
        ])
        trainings.extend([
            {'title': 'Python for Data Analysis', 'type': 'Technical', 'status': 'Completed', 'progress': 100, 'modulesCompleted': 10, 'modulesTotal': 10, 'duration': 20, 'deadline': '2024-11-15', 'instructor': 'DataCamp'}
        ])
    elif emp.get('domain') == 'Design':
        certs.extend([
            {'title': 'Figma Certified Professional', 'issuer': 'Figma', 'status': 'Active', 'category': 'Design', 'issueDate': '2024-03-10', 'expiryDate': 'N/A', 'description': 'Expertise in UI/UX design with Figma.'}
        ])
        trainings.extend([
            {'title': 'Advanced UI/UX Design', 'type': 'Technical', 'status': 'In Progress', 'progress': 70, 'modulesCompleted': 7, 'modulesTotal': 10, 'duration': 25, 'deadline': '2025-09-20', 'instructor': 'Design Academy'}
        ])
    elif emp.get('domain') == 'Quality Assurance':
        certs.extend([
            {'title': 'ISTQB Certified Tester', 'issuer': 'ISTQB', 'status': 'Active', 'category': 'QA', 'issueDate': '2023-10-20', 'expiryDate': 'N/A', 'description': 'Foundational testing certification.'}
        ])
        trainings.extend([
            {'title': 'API Testing with Postman', 'type': 'Technical', 'status': 'Not Started', 'progress': 0, 'modulesCompleted': 0, 'modulesTotal': 8, 'duration': 15, 'deadline': '2025-10-15', 'instructor': 'QA Academy'}
        ])
    elif emp.get('domain') == 'Artificial Intelligence':
        certs.extend([
            {'title': 'TensorFlow Developer Certificate', 'issuer': 'Google', 'status': 'Active', 'category': 'AI/ML', 'issueDate': '2024-05-01', 'expiryDate': 'N/A', 'description': 'Proficiency in TensorFlow for ML models.'}
        ])
        trainings.extend([
            {'title': 'Deep Learning with PyTorch', 'type': 'Technical', 'status': 'In Progress', 'progress': 80, 'modulesCompleted': 8, 'modulesTotal': 10, 'duration': 30, 'deadline': '2025-09-30', 'instructor': 'AI Academy'}
        ])
    elif emp.get('domain') == 'Product Management':
        certs.extend([
            {'title': 'Certified Scrum Product Owner', 'issuer': 'Scrum Alliance', 'status': 'Active', 'category': 'Management', 'issueDate': '2023-11-01', 'expiryDate': '2025-11-01', 'description': 'Expertise in Scrum product ownership.'}
        ])
        trainings.extend([
            {'title': 'Advanced Product Management', 'type': 'Technical', 'status': 'Completed', 'progress': 100, 'modulesCompleted': 10, 'modulesTotal': 10, 'duration': 20, 'deadline': '2024-12-10', 'instructor': 'Product School'}
        ])
    elif emp.get('domain') == 'Security':
        certs.extend([
            {'title': 'CISSP Certification', 'issuer': 'ISC2', 'status': 'Active', 'category': 'Security', 'issueDate': '2024-01-15', 'expiryDate': '2027-01-15', 'description': 'Certified Information Systems Security Professional.'}
        ])
        trainings.extend([
            {'title': 'Ethical Hacking Fundamentals', 'type': 'Technical', 'status': 'In Progress', 'progress': 50, 'modulesCompleted': 5, 'modulesTotal': 10, 'duration': 25, 'deadline': '2025-10-20', 'instructor': 'Security Academy'}
        ])
    elif emp.get('domain') == 'Business Analysis':
        certs.extend([
            {'title': 'CBAP Certification', 'issuer': 'IIBA', 'status': 'Active', 'category': 'Business Analysis', 'issueDate': '2023-12-10', 'expiryDate': 'N/A', 'description': 'Certified Business Analysis Professional.'}
        ])
        trainings.extend([
            {'title': 'Advanced UML Modeling', 'type': 'Technical', 'status': 'Not Started', 'progress': 0, 'modulesCompleted': 0, 'modulesTotal': 8, 'duration': 15, 'deadline': '2025-11-10', 'instructor': 'BA Academy'}
        ])
    elif emp.get('domain') == 'Backend Development':
        certs.extend([
            {'title': 'Oracle Certified Professional Java SE', 'issuer': 'Oracle', 'status': 'Active', 'category': 'Backend', 'issueDate': '2024-02-20', 'expiryDate': 'N/A', 'description': 'Expertise in Java development.'}
        ])
        trainings.extend([
            {'title': 'Microservices with Spring Boot', 'type': 'Technical', 'status': 'In Progress', 'progress': 60, 'modulesCompleted': 6, 'modulesTotal': 10, 'duration': 20, 'deadline': '2025-09-15', 'instructor': 'Backend Academy'}
        ])

    base_trainings = [
        {'title': 'Effective Communication', 'type': 'Soft Skills', 'status': 'Completed', 'progress': 100, 'modulesCompleted': 5, 'modulesTotal': 5, 'duration': 10, 'deadline': '2024-10-01', 'instructor': 'Communicate Co.'},
        {'title': 'Agile & Scrum Fundamentals', 'type': 'Methodology', 'status': 'In Progress', 'progress': 75, 'modulesCompleted': 6, 'modulesTotal': 8, 'duration': 15, 'deadline': '2025-08-15', 'instructor': 'Agile Academy'}
    ]

    for cert in certs:
        cert['consultant_username'] = username
        db.user_certifications.insert_one(cert)

    for training in trainings + base_trainings:
        training['consultant_username'] = username
        db.user_trainings.insert_one(training)

    # --- Resume ---
    resume = {
        'personal': {
            'name': emp['name'], 'email': emp.get('email', ''), 'phone': emp.get('phone', ''),
            'linkedin': f'https://linkedin.com/in/{username}'
        },
        'summary': f"Experienced {emp.get('role', 'Consultant')} with {emp.get('experience', 'N/A')} in the IT industry. Skilled in {', '.join(emp.get('skills', []))}.",
        'experience': [{
            'role': emp.get('role', 'Consultant'), 'company': 'Tech Solutions Inc.',
            'startDate': '2022-01', 'endDate': 'Present',
            'description': '- Led development on key projects.\n- Mentored junior team members.'
        }],
        'education': [{
            'institution': 'State University', 'degree': 'B.Tech in Computer Science', 'year': '2020'
        }],
        'skills': emp.get('skills', [])
    }
    db.resumes.insert_one({'consultant_username': username, 'resume_data': resume})

    # --- Applications ---
    role_to_opp = {
        'Senior React Developer': 'Senior React Developer',
        'Cloud Solutions Architect': 'Cloud Solutions Architect',
        'Data Analyst': 'Data Analyst',
        'UI/UX Designer': 'UI/UX Designer',
        'QA Engineer': 'QA Automation Engineer',
        'AI/ML Engineer': 'AI/ML Engineer',
        'Cybersecurity Specialist': 'Cybersecurity Analyst',
        'Product Manager': 'Product Manager',
        'Backend Developer (Java)': 'Java Backend Developer'
    }
    if emp.get('role') in role_to_opp and role_to_opp[emp.get('role')] in opp_map:
        status = random.choice(['Under Consideration', 'Accepted', 'Rejected'])
        db.applications.insert_one({
            'consultant_username': username,
            'opportunity_id': ObjectId(opp_map[role_to_opp[emp.get('role')]]),
            'status': status
        })

print("\n\nDatabase seeding complete!")
client.close()
