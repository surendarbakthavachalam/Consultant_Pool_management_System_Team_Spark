<p align="center">
  <img src="https://readme-templates.com/banner-example.png" alt="Pool Consultant Management System" width="100%" />
</p>

<h1 align="center">💼 Pool Consultant Management System (CLI Edition)</h1>

<p align="center">
  📊 A CLI-driven solution developed for <b>Hexaware's Hackathon</b> to streamline the lifecycle of bench consultants by automating key workflows like resume tracking, attendance, skill mapping, training progress, and opportunity documentation.
</p>

---

## 🧩 Problem Statement Overview

Hexaware manages a pool of consultants who are periodically on the bench. Managing this workforce presents challenges:

- ❌ Outdated resumes and skill sets
- ⏳ Inefficient attendance reporting for bench meetings
- 🎯 Poor visibility into opportunities and training completion
- 🧠 Limited insight into consultant readiness

This project **simulates an intelligent AI-agentic consultant management system**, aligning with Hexaware's expectations using a simplified **Command Line Interface (CLI)** for the **first round demo**.

---

## ✅ Core Modules Implemented

| Agent Role        | CLI Functionality                                                                 |
|-------------------|-----------------------------------------------------------------------------------|
| 🧠 Resume Agent    | View/edit resumes, track update status, generate resume summaries                 |
| 🕒 Attendance Agent | Check-in/out tracking with hours calculation, history viewer, and summary reports|
| 💼 Opportunity Agent| Apply/view opportunities, simulate engagement tracking                           |
| 🎓 Training Agent   | Track training progress, mark completed trainings, show progress                 |
| 🛠️ Skillset Tracker | Manage and view consultant technical skillsets                                    |

---

## 🧪 Key CLI Screens (Round 1 Deliverables)

- 🔐 **Role-based login** (admin or consultant)
- 🧑‍💼 **Consultant Panel**: Resume manager, training tracker, attendance log, opportunity viewer
- 🛠️ **Admin Panel**: View & filter consultants, assign trainings, post opportunities, generate reports
- 📊 **Filtered Reports**: Based on resume status, skillset, training, attendance hours, opportunities
- 📈 **Status Summary**: For both consultants and admins, CLI reports give clear visibility

---

## 💻 Technology Stack

<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="50" height="50" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/json/json-original.svg" width="50" height="50" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="50" height="50" />
</p>

- Language: **Python 3.10+**
- Data: **In-memory JSON structures with synthetic data**
- UI: **Command Line Interface (for Phase 1 Hackathon)**
- Next Phase: UI Integration (Web-based agentic interaction with dashboards)

---



# 🧪 Proposed CLI Output Solution

The following command-line interface (CLI) output simulates the core functionality of our **Pool Consultant Management System**, aligned with Hexaware’s problem statement. This demo showcases role-based access and consultant lifecycle management using synthetic data.

---

### 🔐 Authentication

```
🏢 ENHANCED POOL CONSULTANT CLI SYSTEM
========================================
🔒 Secure Authentication Required
👥 Available Roles: Admin | Consultant
🎯 Enhanced Features: Resume Management, Check-in/out, Filtered Reports
========================================

🔐 Authentication Required
Available usernames: admin, sai, nandhini, priya, rajesh, kavya, arjun, divya, kiran

Username: sai
Password: sai123
✅ Login successful! Welcome sai
🧑 Accessing Consultant Panel for Sai Ram...
```

---

### 🧑 Consultant Dashboard

```
===== 🧑 Consultant Panel: Sai Ram =====
1. 📄 View/Edit Resume
2. 🕒 Attendance Management
3. 🎓 Training Progress
4. 💼 Opportunities
5. 🛠️ Manage Skillset
6. 📊 My Status Summary
7. 🚪 Logout
Choose an option: 1
```

---

### 📄 Resume Management

```
📄 Resume Status: ❌ Needs Update
1. View Resume
2. Edit Resume
3. Back
Choose option: 1

==================================================
📄 RESUME: Sai Ram
==================================================
📧 Email: sai.ram@company.com
📱 Phone: +91-9876543210
🏠 Address: Chennai, Tamil Nadu
💼 LinkedIn: linkedin.com/in/sairam
🔗 GitHub: github.com/sairam

🎓 Education: B.Tech Computer Science
💼 Experience: 2 years in Python development
🏆 Certifications: AWS Cloud Practitioner
🚀 Projects: E-commerce API, Data Analytics Dashboard
🛠️ Skills: Python, SQL, Django, PostgreSQL
==================================================
```

---

### 🕒 Attendance Management

```
🕒 Attendance Management
✅ Ready to check in
1. Check In
2. View Attendance History
3. Back
Choose option: 1
✅ Checked in at 10:05
```

```
🕒 Attendance Management
⏰ Currently checked in since: 10:05
1. Check Out
2. View Attendance History
3. Back
Choose option: 1
✅ Checked out at 18:10. Hours worked: 8.08
```

---

### 🎓 Training Progress

```
📚 Your Completed Trainings:
  🎓 Python Fundamentals
  🎓 SQL Basics

📖 Available Trainings:
  4. Machine Learning Basics
  18. Tableau Advanced

Enter training ID to mark as completed (0 to skip): 4
🎓 Training 'Machine Learning Basics' marked as completed.
```

---

### 💼 Opportunities

```
💼 Available Opportunities:
  9. DevOps Pipeline (Skills: Docker, Kubernetes)
  10. Database Optimization (Skills: SQL, PostgreSQL)

📋 Your Applied Opportunities:
  ✅ AI Tool Development

Enter opportunity ID to apply (0 to skip): 10
💼 Successfully applied to 'Database Optimization'.
```

---

### 📊 My Status Summary

```
===== 📊 Status Summary: Sai Ram =====
📝 Resume Updated: ❌ No
🕒 Attendance Sessions: 3 (Total: 25.58 hours)
    Recent: 2025-07-22, 2025-07-23, 2025-07-27
🎓 Trainings Completed: 3
    List: Python Fundamentals, SQL Basics, Machine Learning Basics
💼 Opportunities Applied: 2
    List: AI Tool Development, Database Optimization
🛠️ Skills: Python, SQL, Django, PostgreSQL
```

---

### 🧑‍💼 Admin Panel (Sample)

```
===== 👩‍💼 Admin Panel =====
1. ✅ View All Consultants
2. ✅ Check Resume Status
3. ✅ Track Attendance Report
4. ✅ Assign/View Training
5. ✅ Post/View Opportunities
6. ✅ Generate Complete Report
7. 🔍 Generate Filtered Report
8. 🚪 Logout
```

---

📌 **Note**: This CLI simulation demonstrates all agentic roles defined in the Hexaware challenge:
- **Resume Agent**
- **Attendance Agent**
- **Opportunity Agent**
- **Training Agent**




