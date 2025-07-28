from datetime import datetime, timedelta
import json

# Authentication data
user_credentials = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'sai': {'password': 'sai123', 'role': 'consultant'},
    'nandhini': {'password': 'nandhini123', 'role': 'consultant'},
    'priya': {'password': 'priya123', 'role': 'consultant'},
    'rajesh': {'password': 'rajesh123', 'role': 'consultant'},
    'kavya': {'password': 'kavya123', 'role': 'consultant'},
    'arjun': {'password': 'arjun123', 'role': 'consultant'},
    'divya': {'password': 'divya123', 'role': 'consultant'},
    'kiran': {'password': 'kiran123', 'role': 'consultant'}
}

# Enhanced in-memory data structures with synthetic data
consultants = {
    'sai': {
        'name': 'Sai Ram',
        'email': 'sai.ram@company.com',
        'phone': '+91-9876543210',
        'resume': {
            'updated': False,
            'personal_info': {
                'address': 'Chennai, Tamil Nadu',
                'linkedin': 'linkedin.com/in/sairam',
                'github': 'github.com/sairam'
            },
            'experience': '2 years in Python development',
            'education': 'B.Tech Computer Science',
            'certifications': ['AWS Cloud Practitioner'],
            'projects': ['E-commerce API', 'Data Analytics Dashboard']
        },
        'attendance': [
            {'date': '2025-07-22', 'check_in': '09:00', 'check_out': '18:00', 'hours': 9.0},
            {'date': '2025-07-23', 'check_in': '09:15', 'check_out': '17:45', 'hours': 8.5}
        ],
        'training': ['Python Fundamentals', 'SQL Basics'],
        'opportunities_applied': ['AI Tool Development'],
        'skillset': ['Python', 'SQL', 'Django', 'PostgreSQL'],
        'current_session': None
    },
    'nandhini': {
        'name': 'Nandhini R',
        'email': 'nandhini.r@company.com',
        'phone': '+91-9876543211',
        'resume': {
            'updated': True,
            'personal_info': {
                'address': 'Bangalore, Karnataka',
                'linkedin': 'linkedin.com/in/nandhini',
                'github': 'github.com/nandhini'
            },
            'experience': '3 years in Java Spring development',
            'education': 'M.Tech Software Engineering',
            'certifications': ['Oracle Java SE 11', 'Spring Professional'],
            'projects': ['Microservices Architecture', 'Banking Application']
        },
        'attendance': [
            {'date': '2025-07-22', 'check_in': '08:45', 'check_out': '17:30', 'hours': 8.75},
            {'date': '2025-07-23', 'check_in': '09:00', 'check_out': '18:15', 'hours': 9.25},
            {'date': '2025-07-24', 'check_in': '08:30', 'check_out': '17:00', 'hours': 8.5}
        ],
        'training': ['Agile Fundamentals', 'Spring Boot Advanced', 'Microservices'],
        'opportunities_applied': ['Backend API Development'],
        'skillset': ['Java', 'Spring', 'Spring Boot', 'Hibernate', 'MySQL'],
        'current_session': None
    },
    'priya': {
        'name': 'Priya Kumar',
        'email': 'priya.kumar@company.com',
        'phone': '+91-9876543212',
        'resume': {
            'updated': False,
            'personal_info': {
                'address': 'Hyderabad, Telangana',
                'linkedin': 'linkedin.com/in/priyakumar',
                'github': 'github.com/priyakumar'
            },
            'experience': '1.5 years in Frontend development',
            'education': 'B.E Electronics and Communication',
            'certifications': ['React Developer'],
            'projects': ['E-learning Platform', 'Portfolio Website']
        },
        'attendance': [
            {'date': '2025-07-21', 'check_in': '09:30', 'check_out': '18:30', 'hours': 9.0},
            {'date': '2025-07-22', 'check_in': '09:00', 'check_out': '17:45', 'hours': 8.75}
        ],
        'training': ['React for Beginners', 'JavaScript ES6'],
        'opportunities_applied': ['Frontend Dashboard'],
        'skillset': ['React', 'JavaScript', 'HTML', 'CSS', 'Node.js'],
        'current_session': None
    },
    'rajesh': {
        'name': 'Rajesh Kumar',
        'email': 'rajesh.kumar@company.com',
        'phone': '+91-9876543213',
        'resume': {
            'updated': True,
            'personal_info': {
                'address': 'Mumbai, Maharashtra',
                'linkedin': 'linkedin.com/in/rajeshkumar',
                'github': 'github.com/rajeshkumar'
            },
            'experience': '4 years in Full Stack development',
            'education': 'M.Sc Computer Science',
            'certifications': ['AWS Solutions Architect', 'Docker Certified'],
            'projects': ['Cloud Migration', 'DevOps Pipeline', 'Mobile App Backend']
        },
        'attendance': [
            {'date': '2025-07-20', 'check_in': '08:30', 'check_out': '17:00', 'hours': 8.5},
            {'date': '2025-07-21', 'check_in': '09:00', 'check_out': '18:00', 'hours': 9.0},
            {'date': '2025-07-22', 'check_in': '08:45', 'check_out': '17:30', 'hours': 8.75},
            {'date': '2025-07-23', 'check_in': '09:15', 'check_out': '18:15', 'hours': 9.0}
        ],
        'training': ['AWS Fundamentals', 'Docker & Kubernetes', 'Agile Fundamentals'],
        'opportunities_applied': ['Cloud Infrastructure'],
        'skillset': ['Python', 'JavaScript', 'AWS', 'Docker', 'Kubernetes', 'MongoDB'],
        'current_session': None
    },
    'kavya': {
        'name': 'Kavya Sharma',
        'email': 'kavya.sharma@company.com',
        'phone': '+91-9876543214',
        'resume': {
            'updated': True,
            'personal_info': {
                'address': 'Pune, Maharashtra',
                'linkedin': 'linkedin.com/in/kavyasharma',
                'github': 'github.com/kavyasharma'
            },
            'experience': '2.5 years in Data Science',
            'education': 'M.Tech Data Science',
            'certifications': ['Google Data Analytics', 'Tableau Desktop'],
            'projects': ['Sales Prediction Model', 'Customer Segmentation', 'Business Intelligence Dashboard']
        },
        'attendance': [
            {'date': '2025-07-21', 'check_in': '09:00', 'check_out': '17:30', 'hours': 8.5},
            {'date': '2025-07-22', 'check_in': '08:45', 'check_out': '18:00', 'hours': 9.25},
            {'date': '2025-07-23', 'check_in': '09:30', 'check_out': '17:45', 'hours': 8.25}
        ],
        'training': ['Data Analytics with Python', 'Machine Learning Basics', 'Tableau Advanced'],
        'opportunities_applied': ['Data Science Project'],
        'skillset': ['Python', 'R', 'SQL', 'Tableau', 'Machine Learning', 'Statistics'],
        'current_session': None
    },
    'arjun': {
        'name': 'Arjun Patel',
        'email': 'arjun.patel@company.com',
        'phone': '+91-9876543215',
        'resume': {
            'updated': False,
            'personal_info': {
                'address': 'Ahmedabad, Gujarat',
                'linkedin': 'linkedin.com/in/arjunpatel',
                'github': 'github.com/arjunpatel'
            },
            'experience': '1 year in Mobile development',
            'education': 'B.Tech Information Technology',
            'certifications': ['Android Developer'],
            'projects': ['Food Delivery App', 'Fitness Tracker']
        },
        'attendance': [
            {'date': '2025-07-22', 'check_in': '09:30', 'check_out': '18:30', 'hours': 9.0},
            {'date': '2025-07-23', 'check_in': '09:00', 'check_out': '17:00', 'hours': 8.0}
        ],
        'training': ['Android Fundamentals'],
        'opportunities_applied': [],
        'skillset': ['Java', 'Kotlin', 'Android', 'Firebase', 'SQLite'],
        'current_session': None
    },
    'divya': {
        'name': 'Divya Reddy',
        'email': 'divya.reddy@company.com',
        'phone': '+91-9876543216',
        'resume': {
            'updated': True,
            'personal_info': {
                'address': 'Vizag, Andhra Pradesh',
                'linkedin': 'linkedin.com/in/divyareddy',
                'github': 'github.com/divyareddy'
            },
            'experience': '3.5 years in QA Testing',
            'education': 'B.E Computer Science',
            'certifications': ['ISTQB Foundation', 'Selenium WebDriver'],
            'projects': ['Test Automation Framework', 'API Testing Suite', 'Performance Testing']
        },
        'attendance': [
            {'date': '2025-07-20', 'check_in': '09:00', 'check_out': '18:00', 'hours': 9.0},
            {'date': '2025-07-21', 'check_in': '08:45', 'check_out': '17:30', 'hours': 8.75},
            {'date': '2025-07-22', 'check_in': '09:15', 'check_out': '18:15', 'hours': 9.0},
            {'date': '2025-07-23', 'check_in': '09:00', 'check_out': '17:45', 'hours': 8.75}
        ],
        'training': ['Selenium Automation', 'API Testing', 'Performance Testing'],
        'opportunities_applied': ['QA Automation'],
        'skillset': ['Java', 'Selenium', 'TestNG', 'REST Assured', 'JMeter', 'SQL'],
        'current_session': None
    },
    'kiran': {
        'name': 'Kiran Singh',
        'email': 'kiran.singh@company.com',
        'phone': '+91-9876543217',
        'resume': {
            'updated': False,
            'personal_info': {
                'address': 'Delhi, India',
                'linkedin': 'linkedin.com/in/kiransingh',
                'github': 'github.com/kiransingh'
            },
            'experience': '2 years in UI/UX Design',
            'education': 'B.Des Visual Communication',
            'certifications': ['Google UX Design', 'Adobe Certified'],
            'projects': ['Mobile App UI', 'Website Redesign', 'Design System']
        },
        'attendance': [
            {'date': '2025-07-22', 'check_in': '10:00', 'check_out': '18:00', 'hours': 8.0},
            {'date': '2025-07-23', 'check_in': '09:30', 'check_out': '17:30', 'hours': 8.0}
        ],
        'training': ['Design Thinking', 'Figma Advanced'],
        'opportunities_applied': ['UI/UX Design'],
        'skillset': ['Figma', 'Adobe XD', 'Sketch', 'HTML', 'CSS', 'Prototyping'],
        'current_session': None
    }
}

opportunities = [
    {'id': 1, 'title': 'AI Tool Development', 'skills': ['Python', 'Machine Learning'], 'assigned_to': ['sai']},
    {'id': 2, 'title': 'Frontend Dashboard', 'skills': ['React', 'JavaScript'], 'assigned_to': ['priya']},
    {'id': 3, 'title': 'Backend API Development', 'skills': ['Java', 'Spring'], 'assigned_to': ['nandhini']},
    {'id': 4, 'title': 'Cloud Infrastructure', 'skills': ['AWS', 'Docker'], 'assigned_to': ['rajesh']},
    {'id': 5, 'title': 'Data Science Project', 'skills': ['Python', 'Machine Learning'], 'assigned_to': ['kavya']},
    {'id': 6, 'title': 'Mobile App Development', 'skills': ['Android', 'Kotlin'], 'assigned_to': []},
    {'id': 7, 'title': 'QA Automation', 'skills': ['Selenium', 'Java'], 'assigned_to': ['divya']},
    {'id': 8, 'title': 'UI/UX Design', 'skills': ['Figma', 'Design'], 'assigned_to': ['kiran']},
    {'id': 9, 'title': 'DevOps Pipeline', 'skills': ['Docker', 'Kubernetes'], 'assigned_to': []},
    {'id': 10, 'title': 'Database Optimization', 'skills': ['SQL', 'PostgreSQL'], 'assigned_to': []}
]

training_catalog = [
    {'id': 1, 'title': 'Data Analytics with Python'},
    {'id': 2, 'title': 'Agile Fundamentals'},
    {'id': 3, 'title': 'React for Beginners'},
    {'id': 4, 'title': 'Machine Learning Basics'},
    {'id': 5, 'title': 'Spring Boot Advanced'},
    {'id': 6, 'title': 'AWS Fundamentals'},
    {'id': 7, 'title': 'Docker & Kubernetes'},
    {'id': 8, 'title': 'Selenium Automation'},
    {'id': 9, 'title': 'API Testing'},
    {'id': 10, 'title': 'Performance Testing'},
    {'id': 11, 'title': 'Design Thinking'},
    {'id': 12, 'title': 'Figma Advanced'},
    {'id': 13, 'title': 'JavaScript ES6'},
    {'id': 14, 'title': 'Python Fundamentals'},
    {'id': 15, 'title': 'SQL Basics'},
    {'id': 16, 'title': 'Android Fundamentals'},
    {'id': 17, 'title': 'Microservices'},
    {'id': 18, 'title': 'Tableau Advanced'}
]


def authenticate_user():
    """🔐 User Authentication"""
    print("\n🔐 Login Required")
    username = input("Username: ").lower().strip()
    password = input("Password: ").strip()

    if username in user_credentials and user_credentials[username]['password'] == password:
        role = user_credentials[username]['role']
        if role == 'consultant' and username in consultants:
            return username, role
        elif role == 'admin':
            return username, role
        else:
            print("❌ User data not found.")
            return None, None
    else:
        print("❌ Invalid credentials.")
        return None, None


def calculate_hours(check_in, check_out):
    """Calculate hours between check-in and check-out times"""
    try:
        check_in_time = datetime.strptime(check_in, '%H:%M')
        check_out_time = datetime.strptime(check_out, '%H:%M')

        if check_out_time < check_in_time:
            check_out_time += timedelta(days=1)

        duration = check_out_time - check_in_time
        return round(duration.total_seconds() / 3600, 2)
    except:
        return 0.0


def display_resume(username):
    """Display formatted resume"""
    resume = consultants[username]['resume']
    consultant = consultants[username]

    print(f"\n{'=' * 50}")
    print(f"📄 RESUME: {consultant['name']}")
    print(f"{'=' * 50}")
    print(f"📧 Email: {consultant['email']}")
    print(f"📱 Phone: {consultant['phone']}")
    print(f"🏠 Address: {resume['personal_info']['address']}")
    print(f"💼 LinkedIn: {resume['personal_info']['linkedin']}")
    print(f"🔗 GitHub: {resume['personal_info']['github']}")
    print(f"\n🎓 Education: {resume['education']}")
    print(f"💼 Experience: {resume['experience']}")
    print(f"🏆 Certifications: {', '.join(resume['certifications'])}")
    print(f"🚀 Projects: {', '.join(resume['projects'])}")
    print(f"🛠️ Skills: {', '.join(consultant['skillset'])}")
    print(f"{'=' * 50}")


def edit_resume(username):
    """Edit resume fields"""
    while True:
        print(f"\n📝 Edit Resume Fields:")
        print("1. Personal Info (Address, LinkedIn, GitHub)")
        print("2. Education")
        print("3. Experience")
        print("4. Add Certification")
        print("5. Add Project")
        print("6. Mark Resume as Updated")
        print("7. Back to Main Menu")

        choice = input("Choose option: ")
        resume = consultants[username]['resume']

        if choice == '1':
            print("\n🏠 Current Personal Info:")
            print(f"Address: {resume['personal_info']['address']}")
            print(f"LinkedIn: {resume['personal_info']['linkedin']}")
            print(f"GitHub: {resume['personal_info']['github']}")

            field = input("Edit (a)address, (l)linkedin, (g)github, or (s)skip: ").lower()
            if field == 'a':
                new_address = input("New Address: ").strip()
                if new_address:
                    resume['personal_info']['address'] = new_address
                    print("✅ Address updated.")
            elif field == 'l':
                new_linkedin = input("New LinkedIn: ").strip()
                if new_linkedin:
                    resume['personal_info']['linkedin'] = new_linkedin
                    print("✅ LinkedIn updated.")
            elif field == 'g':
                new_github = input("New GitHub: ").strip()
                if new_github:
                    resume['personal_info']['github'] = new_github
                    print("✅ GitHub updated.")

        elif choice == '2':
            print(f"Current Education: {resume['education']}")
            new_education = input("New Education: ").strip()
            if new_education:
                resume['education'] = new_education
                print("✅ Education updated.")

        elif choice == '3':
            print(f"Current Experience: {resume['experience']}")
            new_experience = input("New Experience: ").strip()
            if new_experience:
                resume['experience'] = new_experience
                print("✅ Experience updated.")

        elif choice == '4':
            print(f"Current Certifications: {', '.join(resume['certifications'])}")
            new_cert = input("Add Certification: ").strip()
            if new_cert and new_cert not in resume['certifications']:
                resume['certifications'].append(new_cert)
                print("✅ Certification added.")

        elif choice == '5':
            print(f"Current Projects: {', '.join(resume['projects'])}")
            new_project = input("Add Project: ").strip()
            if new_project and new_project not in resume['projects']:
                resume['projects'].append(new_project)
                print("✅ Project added.")

        elif choice == '6':
            resume['updated'] = True
            print("✅ Resume marked as updated.")

        elif choice == '7':
            break

        else:
            print("❌ Invalid choice.")


def consultant_menu(username):
    """🧑 Consultant Features Panel"""
    while True:
        consultant_data = consultants[username]
        print(f"\n===== 🧑 Consultant Panel: {consultant_data['name']} =====")
        print("1. 📄 View/Edit Resume")
        print("2. 🕒 Attendance Management")
        print("3. 🎓 Training Progress")
        print("4. 💼 Opportunities")
        print("5. 🛠️ Manage Skillset")
        print("6. 📊 My Status Summary")
        print("7. 🚪 Logout")

        choice = input("Choose an option: ")

        if choice == '1':
            # Resume Management
            while True:
                resume_status = "✅ Updated" if consultant_data['resume']['updated'] else "❌ Needs Update"
                print(f"\n📄 Resume Status: {resume_status}")
                print("1. View Resume")
                print("2. Edit Resume")
                print("3. Back")

                resume_choice = input("Choose option: ")
                if resume_choice == '1':
                    display_resume(username)
                elif resume_choice == '2':
                    edit_resume(username)
                elif resume_choice == '3':
                    break

        elif choice == '2':
            # Attendance Management
            while True:
                print(f"\n🕒 Attendance Management")
                if consultant_data['current_session']:
                    print(f"⏰ Currently checked in since: {consultant_data['current_session']}")
                    print("1. Check Out")
                else:
                    print("✅ Ready to check in")
                    print("1. Check In")

                print("2. View Attendance History")
                print("3. Back")

                att_choice = input("Choose option: ")
                current_time = datetime.now()
                today = str(current_time.date())

                if att_choice == '1':
                    if consultant_data['current_session']:
                        # Check Out
                        check_out_time = current_time.strftime('%H:%M')
                        check_in_time = consultant_data['current_session']
                        hours_worked = calculate_hours(check_in_time, check_out_time)

                        # Update or add today's attendance
                        today_attendance = None
                        for att in consultant_data['attendance']:
                            if att['date'] == today:
                                today_attendance = att
                                break

                        if today_attendance:
                            today_attendance['check_out'] = check_out_time
                            today_attendance['hours'] = hours_worked
                        else:
                            consultant_data['attendance'].append({
                                'date': today,
                                'check_in': check_in_time,
                                'check_out': check_out_time,
                                'hours': hours_worked
                            })

                        consultant_data['current_session'] = None
                        print(f"✅ Checked out at {check_out_time}. Hours worked: {hours_worked}")

                    else:
                        # Check In
                        check_in_time = current_time.strftime('%H:%M')
                        consultant_data['current_session'] = check_in_time
                        print(f"✅ Checked in at {check_in_time}")

                elif att_choice == '2':
                    # View Attendance History
                    print(f"\n📅 Attendance History:")
                    total_hours = 0
                    for att in consultant_data['attendance']:
                        print(
                            f"  📅 {att['date']}: {att['check_in']} - {att.get('check_out', 'Not checked out')} ({att.get('hours', 0)} hours)")
                        total_hours += att.get('hours', 0)
                    print(f"\n⏱️ Total Hours Worked: {total_hours} hours")

                elif att_choice == '3':
                    break

        elif choice == '3':
            # Training Progress (existing code with minor improvements)
            print("\n📚 Your Completed Trainings:")
            for training in consultant_data['training']:
                print(f"  🎓 {training}")

            print("\n📖 Available Trainings:")
            available_trainings = [t for t in training_catalog if t['title'] not in consultant_data['training']]

            if not available_trainings:
                print("  🎉 All trainings completed!")
            else:
                for t in available_trainings:
                    print(f"  {t['id']}. {t['title']}")

                try:
                    tid = int(input("Enter training ID to mark as completed (0 to skip): "))
                    if tid == 0:
                        continue
                    for t in training_catalog:
                        if t['id'] == tid and t['title'] not in consultant_data['training']:
                            consultants[username]['training'].append(t['title'])
                            print(f"🎓 Training '{t['title']}' marked as completed.")
                            break
                    else:
                        print("❌ Invalid training ID or already completed.")
                except ValueError:
                    print("❌ Please enter a valid number.")

        elif choice == '4':
            # Opportunities (existing code)
            print("\n💼 Available Opportunities:")
            available_opps = [opp for opp in opportunities if username not in opp['assigned_to']]

            if not available_opps:
                print("  📋 No new opportunities available.")
            else:
                for opp in available_opps:
                    print(f"  {opp['id']}. {opp['title']} (Skills: {', '.join(opp['skills'])})")

            print("\n📋 Your Applied Opportunities:")
            for opp_title in consultant_data['opportunities_applied']:
                print(f"  ✅ {opp_title}")

            if available_opps:
                try:
                    oid = int(input("Enter opportunity ID to apply (0 to skip): "))
                    if oid == 0:
                        continue
                    for opp in opportunities:
                        if opp['id'] == oid and username not in opp['assigned_to']:
                            opp['assigned_to'].append(username)
                            consultants[username]['opportunities_applied'].append(opp['title'])
                            print(f"💼 Successfully applied to '{opp['title']}'.")
                            break
                    else:
                        print("❌ Invalid opportunity ID or already applied.")
                except ValueError:
                    print("❌ Please enter a valid number.")

        elif choice == '5':
            # Skillset Management (existing code)
            print(f"\n🛠️ Your current skills: {', '.join(consultant_data['skillset'])}")
            action = input("(a)add skill, (r)remove skill, or (s)skip: ").lower()

            if action == 'a':
                new_skill = input("Enter skill to add: ").strip()
                if new_skill and new_skill not in consultant_data['skillset']:
                    consultants[username]['skillset'].append(new_skill)
                    print(f"✅ Skill '{new_skill}' added.")
                elif new_skill in consultant_data['skillset']:
                    print("🔁 Skill already exists.")
            elif action == 'r':
                if consultant_data['skillset']:
                    print("Current skills:")
                    for i, skill in enumerate(consultant_data['skillset'], 1):
                        print(f"  {i}. {skill}")
                    try:
                        idx = int(input("Enter skill number to remove: ")) - 1
                        if 0 <= idx < len(consultant_data['skillset']):
                            removed_skill = consultants[username]['skillset'].pop(idx)
                            print(f"❌ Skill '{removed_skill}' removed.")
                        else:
                            print("❌ Invalid skill number.")
                    except ValueError:
                        print("❌ Please enter a valid number.")
                else:
                    print("📝 No skills to remove.")

        elif choice == '6':
            # Status Summary
            data = consultant_data
            print(f"\n===== 📊 Status Summary: {data['name']} =====")
            print(f"📝 Resume Updated: {'✅ Yes' if data['resume']['updated'] else '❌ No'}")

            total_hours = sum(att.get('hours', 0) for att in data['attendance'])
            print(f"🕒 Attendance Sessions: {len(data['attendance'])} (Total: {total_hours} hours)")
            if data['attendance']:
                recent_dates = [att['date'] for att in data['attendance'][-3:]]
                print(f"    Recent: {', '.join(recent_dates)}")

            print(f"🎓 Trainings Completed: {len(data['training'])}")
            if data['training']:
                print(f"    List: {', '.join(data['training'])}")
            print(f"💼 Opportunities Applied: {len(data['opportunities_applied'])}")
            if data['opportunities_applied']:
                print(f"    List: {', '.join(data['opportunities_applied'])}")
            print(f"🛠️ Skills: {', '.join(data['skillset'])}")

        elif choice == '7':
            print("👋 Logging out...")
            break
        else:
            print("❌ Invalid choice. Please try again.")


def filter_consultants():
    """Filter consultants based on various criteria"""
    print("\n🔍 Filter Consultants By:")
    print("1. Resume Status")
    print("2. Skills")
    print("3. Training Completed")
    print("4. Opportunities Applied")
    print("5. Attendance Hours")
    print("6. Return All Consultants")

    choice = input("Choose filter option: ")
    filtered_consultants = {}

    if choice == '1':
        # Filter by Resume Status
        status = input("Filter by resume status (u)pdated or (n)ot updated: ").lower()
        for username, data in consultants.items():
            if status == 'u' and data['resume']['updated']:
                filtered_consultants[username] = data
            elif status == 'n' and not data['resume']['updated']:
                filtered_consultants[username] = data

    elif choice == '2':
        # Filter by Skills
        skill = input("Enter skill to filter by: ").strip()
        for username, data in consultants.items():
            if any(skill.lower() in s.lower() for s in data['skillset']):
                filtered_consultants[username] = data

    elif choice == '3':
        # Filter by Training
        training = input("Enter training name to filter by: ").strip()
        for username, data in consultants.items():
            if any(training.lower() in t.lower() for t in data['training']):
                filtered_consultants[username] = data

    elif choice == '4':
        # Filter by Opportunities Applied
        min_opps = input("Minimum opportunities applied (enter number): ").strip()
        try:
            min_count = int(min_opps)
            for username, data in consultants.items():
                if len(data['opportunities_applied']) >= min_count:
                    filtered_consultants[username] = data
        except ValueError:
            print("❌ Invalid number.")
            return {}

    elif choice == '5':
        # Filter by Attendance Hours
        min_hours = input("Minimum total hours worked (enter number): ").strip()
        try:
            min_hrs = float(min_hours)
            for username, data in consultants.items():
                total_hours = sum(att.get('hours', 0) for att in data['attendance'])
                if total_hours >= min_hrs:
                    filtered_consultants[username] = data
        except ValueError:
            print("❌ Invalid number.")
            return {}

    elif choice == '6':
        # Return all consultants
        filtered_consultants = consultants.copy()

    else:
        print("❌ Invalid choice.")
        return {}

    return filtered_consultants


def generate_filtered_report(filtered_data):
    """Generate report for filtered consultants"""
    if not filtered_data:
        print("📋 No consultants match the filter criteria.")
        return

    print("\n" + "=" * 80)
    print("📊 FILTERED CONSULTANT REPORT")
    print("=" * 80)
    print(f"📈 Showing {len(filtered_data)} consultant(s)")

    for username, data in filtered_data.items():
        total_hours = sum(att.get('hours', 0) for att in data['attendance'])
        print(f"\n🧑 CONSULTANT: {data['name']} (@{username})")
        print("-" * 50)
        print(f"📧 Contact: {data['email']} | {data['phone']}")
        print(f"📝 Resume Status: {'✅ Updated' if data['resume']['updated'] else '❌ Needs Update'}")
        print(f"🕒 Total Hours Worked: {total_hours} hours ({len(data['attendance'])} sessions)")
        if data['attendance']:
            recent_sessions = data['attendance'][-3:]
            print(f"    Recent Sessions:")
            for session in recent_sessions:
                print(
                    f"      📅 {session['date']}: {session['check_in']}-{session.get('check_out', 'N/A')} ({session.get('hours', 0)}h)")

        print(f"🎓 Training Progress: {len(data['training'])} completed")
        if data['training']:
            print(f"    Completed: {', '.join(data['training'][:3])}{'...' if len(data['training']) > 3 else ''}")

        print(f"💼 Opportunities: {len(data['opportunities_applied'])} applied")
        if data['opportunities_applied']:
            print(f"    Applied to: {', '.join(data['opportunities_applied'])}")

        print(f"🛠️ Skills ({len(data['skillset'])}): {', '.join(data['skillset'])}")

        # Resume details if updated
        if data['resume']['updated']:
            print(f"🎓 Education: {data['resume']['education']}")
            print(f"💼 Experience: {data['resume']['experience']}")
            print(
                f"🏆 Certifications: {', '.join(data['resume']['certifications'][:2])}{'...' if len(data['resume']['certifications']) > 2 else ''}")

    # Summary statistics for filtered data
    print(f"\n📈 FILTERED STATISTICS")
    print("-" * 50)
    updated_resumes = sum(1 for data in filtered_data.values() if data['resume']['updated'])
    total_hours_all = sum(sum(att.get('hours', 0) for att in data['attendance']) for data in filtered_data.values())
    total_trainings = sum(len(data['training']) for data in filtered_data.values())
    total_applications = sum(len(data['opportunities_applied']) for data in filtered_data.values())

    print(f"👥 Filtered Consultants: {len(filtered_data)}")
    print(
        f"📝 Resumes Updated: {updated_resumes}/{len(filtered_data)} ({updated_resumes / len(filtered_data) * 100:.1f}%)")
    print(f"🕒 Total Hours Worked: {total_hours_all} hours")
    print(f"🎓 Total Training Completions: {total_trainings}")
    print(f"💼 Total Opportunity Applications: {total_applications}")
    print("=" * 80)


def admin_menu():
    """👩‍💼 Admin Features Panel"""
    while True:
        print("\n===== 👩‍💼 Admin Panel =====")
        print("1. ✅ View All Consultants")
        print("2. ✅ Check Resume Status")
        print("3. ✅ Track Attendance Report")
        print("4. ✅ Assign/View Training")
        print("5. ✅ Post/View Opportunities")
        print("6. ✅ Generate Complete Report")
        print("7. 🔍 Generate Filtered Report")
        print("8. 🚪 Logout")

        choice = input("Choose an option: ")

        if choice == '1':
            # View All Consultants
            print("\n👥 All Consultants:")
            for uname, data in consultants.items():
                total_hours = sum(att.get('hours', 0) for att in data['attendance'])
                resume_status = '✅ Updated' if data['resume']['updated'] else '⚠️ Needs Update'
                print(f"  🧑 {data['name']} (@{uname})")
                print(f"      📧 {data['email']} | 📱 {data['phone']}")
                print(f"      🛠️ Skills: {', '.join(data['skillset'][:3])}{'...' if len(data['skillset']) > 3 else ''}")
                print(f"      📝 Resume: {resume_status} | 🕒 Hours: {total_hours}h")

        elif choice == '2':
            # Resume Status Report
            print("\n📝 Resume Status Report:")
            updated_count = 0
            for uname, data in consultants.items():
                status = '✅ Updated' if data['resume']['updated'] else '❌ Needs Update'
                print(f"  {data['name']}: {status}")
                if data['resume']['updated']:
                    updated_count += 1
                    # Show resume summary for updated resumes
                    print(f"    🎓 {data['resume']['education']} | 💼 {data['resume']['experience']}")
                    print(f"    🏆 Certifications: {len(data['resume']['certifications'])}")
            print(f"\n📊 Summary: {updated_count}/{len(consultants)} consultants have updated resumes")

        elif choice == '3':
            # Attendance Report
            print("\n🕒 Detailed Attendance Report:")
            total_hours_all = 0
            for uname, data in consultants.items():
                total_hours = sum(att.get('hours', 0) for att in data['attendance'])
                total_hours_all += total_hours
                print(f"  🧑 {data['name']}: {len(data['attendance'])} sessions, {total_hours} hours")

                if data['attendance']:
                    print(f"    Recent sessions:")
                    for session in data['attendance'][-3:]:
                        status = f"{session['check_in']}-{session.get('check_out', 'Active')}"
                        print(f"      📅 {session['date']}: {status} ({session.get('hours', 0)}h)")

                if data['current_session']:
                    print(f"    ⏰ Currently checked in since: {data['current_session']}")

            print(f"\n📊 Total hours worked by all consultants: {total_hours_all} hours")
            avg_hours = total_hours_all / len(consultants) if consultants else 0
            print(f"📊 Average hours per consultant: {avg_hours:.2f} hours")

        elif choice == '4':
            # Training Management
            print("\n🎓 Training Management:")
            print("Current Training Catalog:")
            for t in training_catalog:
                completed_by = [consultants[uname]['name'] for uname in consultants
                                if t['title'] in consultants[uname]['training']]
                print(f"  {t['id']}. {t['title']}")
                if completed_by:
                    print(
                        f"      ✅ Completed by ({len(completed_by)}): {', '.join(completed_by[:3])}{'...' if len(completed_by) > 3 else ''}")
                else:
                    print("      ❌ No completions yet")

            action = input("\n(a)dd new training or (s)kip: ").lower()
            if action == 'a':
                title = input("Enter new training title: ").strip()
                if title:
                    new_id = max([t['id'] for t in training_catalog]) + 1
                    training_catalog.append({'id': new_id, 'title': title})
                    print(f"🎓 Training '{title}' added with ID {new_id}.")

        elif choice == '5':
            # Opportunities Management
            print("\n💼 Opportunities Management:")
            for opp in opportunities:
                applicant_names = [consultants[uname]['name'] for uname in opp['assigned_to'] if uname in consultants]
                print(f"  {opp['id']}. {opp['title']}")
                print(f"      🛠️ Required Skills: {', '.join(opp['skills'])}")
                print(
                    f"      👥 Applicants ({len(applicant_names)}): {', '.join(applicant_names) if applicant_names else 'None'}")

            action = input("\n(p)ost new opportunity or (s)kip: ").lower()
            if action == 'p':
                title = input("Opportunity Title: ").strip()
                skills_input = input("Required Skills (comma-separated): ").strip()
                if title and skills_input:
                    skills = [s.strip() for s in skills_input.split(',')]
                    new_id = max([opp['id'] for opp in opportunities]) + 1
                    opportunities.append({
                        'id': new_id,
                        'title': title,
                        'skills': skills,
                        'assigned_to': []
                    })
                    print(f"💼 Opportunity '{title}' posted with ID {new_id}.")

        elif choice == '6':
            # Complete Report
            print("\n" + "=" * 80)
            print("📊 COMPLETE CONSULTANT SUMMARY REPORT")
            print("=" * 80)

            for uname, data in consultants.items():
                total_hours = sum(att.get('hours', 0) for att in data['attendance'])
                print(f"\n🧑 CONSULTANT: {data['name']} (@{uname})")
                print("-" * 50)
                print(f"📧 Contact: {data['email']} | {data['phone']}")
                print(f"📝 Resume Status: {'✅ Updated' if data['resume']['updated'] else '❌ Needs Update'}")

                if data['resume']['updated']:
                    print(f"    🎓 Education: {data['resume']['education']}")
                    print(f"    💼 Experience: {data['resume']['experience']}")
                    print(f"    🏆 Certifications: {', '.join(data['resume']['certifications'])}")

                print(f"🕒 Attendance: {len(data['attendance'])} sessions, {total_hours} total hours")
                if data['attendance']:
                    recent = data['attendance'][-2:]
                    for session in recent:
                        print(
                            f"    📅 {session['date']}: {session['check_in']}-{session.get('check_out', 'N/A')} ({session.get('hours', 0)}h)")

                print(f"🎓 Training Progress: {len(data['training'])} completed")
                if data['training']:
                    print(f"    Completed: {', '.join(data['training'])}")

                print(f"💼 Opportunities: {len(data['opportunities_applied'])} applied")
                if data['opportunities_applied']:
                    print(f"    Applied to: {', '.join(data['opportunities_applied'])}")

                print(f"🛠️ Skills ({len(data['skillset'])}): {', '.join(data['skillset'])}")

            # Overall statistics
            print(f"\n📈 OVERALL STATISTICS")
            print("-" * 50)
            total_consultants = len(consultants)
            updated_resumes = sum(1 for data in consultants.values() if data['resume']['updated'])
            total_attendance = sum(len(data['attendance']) for data in consultants.values())
            total_hours_all = sum(
                sum(att.get('hours', 0) for att in data['attendance']) for data in consultants.values())
            total_trainings = sum(len(data['training']) for data in consultants.values())
            total_applications = sum(len(data['opportunities_applied']) for data in consultants.values())

            print(f"👥 Total Consultants: {total_consultants}")
            print(
                f"📝 Resumes Updated: {updated_resumes}/{total_consultants} ({updated_resumes / total_consultants * 100:.1f}%)")
            print(f"🕒 Total Attendance Sessions: {total_attendance}")
            print(f"⏱️ Total Hours Worked: {total_hours_all} hours")
            print(f"📊 Average Hours per Consultant: {total_hours_all / total_consultants:.2f} hours")
            print(f"🎓 Total Training Completions: {total_trainings}")
            print(f"💼 Total Opportunity Applications: {total_applications}")
            print("=" * 80)

        elif choice == '7':
            # Filtered Report
            filtered_data = filter_consultants()
            if filtered_data:
                generate_filtered_report(filtered_data)

        elif choice == '8':
            print("👋 Logging out...")
            break
        else:
            print("❌ Invalid choice. Please try again.")


def run_cli_system():
    """🔐 Enhanced Login System & Entry Point"""
    print("=" * 80)
    print("🏢 ENHANCED POOL CONSULTANT CLI SYSTEM")
    print("=" * 80)
    print("🔒 Secure Authentication Required")
    print("👥 Available Roles: Admin | Consultant")
    print("🎯 Enhanced Features: Resume Management, Check-in/out, Filtered Reports")
    print("=" * 80)

    while True:
        print(f"\n🔐 Authentication Required")
        print("Available usernames: admin, sai, nandhini, priya, rajesh, kavya, arjun, divya, kiran")
        print("=" * 80)
        print("For consultant Access username with Password")
        print("username : admin , Password : admin123  ")
        print("=" * 80)
        print("For consultant Access username with Password ")
        print("{username : sai ,  Password : sai123} \n {username : nandhini , Password : nandhini123 }  \n {username : priya , Password : priya123 } \n {username : rajesh , Password : rajesh123} \n {username : kavya , Password : kavya123 } \n {username : arjun , Password : arjun123 }  \n {username : divya , Password : divya123 } \n {username : kiran Password : kiran123}  ")
        print("=" * 80)
        username, role = authenticate_user()

        if username and role:
            print(f"✅ Login successful! Welcome {username}")

            if role == 'consultant':
                print(f"🧑 Accessing Consultant Panel for {consultants[username]['name']}...")
                consultant_menu(username)
            elif role == 'admin':
                print(f"👩‍💼 Accessing Admin Panel...")
                admin_menu()
        else:
            retry = input("❌ Authentication failed. Try again? (y/n): ").lower()
            if retry != 'y':
                break

    print("👋 Thank you for using Enhanced Pool Consultant CLI System!")


# Entry point
if __name__ == "__main__":
    run_cli_system()
