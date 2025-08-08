# project/admin.py
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request, current_app
from functools import wraps
from bson import json_util, ObjectId
import json
from datetime import datetime
import os
import google.generativeai as genai

# --- Gemini API Configuration ---
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
except KeyError:
    gemini_model = None
    print("\n--- WARNING: GOOGLE_API_KEY environment variable not set. ---")
    print("--- Chatbot and AI Insights functionality will be disabled. ---\n")


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('auth.main_login_page'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('role') != role:
                return redirect(url_for('auth.main_login_page'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def parse_json(data):
    return json.loads(json_util.dumps(data))

# --- HTML Page Routes ---
@admin_bp.route('/home')
@login_required
@role_required('admin')
def admin_home(): return render_template('admin/admin_home.html')

@admin_bp.route('/employees')
@login_required
@role_required('admin')
def admin_employees(): return render_template('admin/admin_employees.html')

@admin_bp.route('/opportunities')
@login_required
@role_required('admin')
def admin_opportunities(): return render_template('admin/admin_opportunities.html')

@admin_bp.route('/reports')
@login_required
@role_required('admin')
def admin_reports(): return render_template('admin/admin_reports.html')

@admin_bp.route('/monitor')
@login_required
@role_required('admin')
def admin_monitor():
    return render_template('admin/admin_monitor.html')

@admin_bp.route('/chatbot')
@login_required
@role_required('admin')
def admin_chatbot(): return render_template('admin/admin_chatbot.html')

# --- API Endpoints ---

@admin_bp.route('/api/leaderboard')
@login_required
def api_leaderboard():
    db = current_app.db
    try:
        employees = list(db.employees.find({}, {"_id": 1, "name": 1, "username": 1}))
        leaderboard = []
        for emp in employees:
            username = emp.get('username')
            if not username: continue
            accepted_apps_count = db.applications.count_documents({"consultant_username": username, "status": "Accepted"})
            active_certs_count = db.user_certifications.count_documents({"consultant_username": username, "status": "Active"})
            score = (accepted_apps_count * 10) + (active_certs_count * 5)
            leaderboard.append({"name": emp.get('name', 'Unknown'), "score": score})
        sorted_leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
        return jsonify(sorted_leaderboard[:10])
    except Exception as e:
        print(f"Error fetching leaderboard data: {e}")
        return jsonify({"error": "Could not fetch leaderboard data"}), 500

@admin_bp.route('/api/dashboard-stats')
@login_required
@role_required('admin')
def api_admin_dashboard_stats():
    db = current_app.db
    total_employees = db.employees.count_documents({})
    active_employees = db.employees.count_documents({"status": "Active"})
    open_opportunities = db.opportunities.count_documents({"status": "Open"})
    total_applications = db.applications.count_documents({})
    bench_employees = total_employees - active_employees
    
    completed_trainings = db.user_trainings.count_documents({"status": "Completed"})
    in_progress_trainings = db.user_trainings.count_documents({"status": "In Progress"})
    not_started_trainings = db.user_trainings.count_documents({"status": "Not Started"})
    
    stats = {'totalEmployees': total_employees, 'activeProjects': active_employees, 'openOpportunities': open_opportunities, 'totalApplications': total_applications}
    charts = {
        'employeeDistribution': {'active': active_employees, 'bench': bench_employees},
        'trainingStatus': {'completed': completed_trainings, 'inProgress': in_progress_trainings, 'notStarted': not_started_trainings}
    }
    return jsonify({'homeStats': stats, 'charts': charts})


@admin_bp.route('/api/employees')
@login_required
@role_required('admin')
def api_admin_employees():
    employees = list(current_app.db.employees.find({}))
    stats = {
        'totalEmployees': len(employees),
        'activeProjects': sum(1 for e in employees if e['status'] == 'Active'),
        'benchResources': sum(1 for e in employees if e['status'] == 'Bench'),
        'avgAttendance': f"{int(sum(e.get('attendance_score', 0) for e in employees) / len(employees)) if employees else 0}%"
    }
    return jsonify({'employeePageStats': stats, 'employees': parse_json(employees)})

@admin_bp.route('/api/opportunities', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def api_admin_opportunities():
    db = current_app.db
    if request.method == 'POST':
        new_opp = request.json
        new_opp['posted'] = datetime.now().strftime("%Y-%m-%d")
        db.opportunities.insert_one(new_opp)
        return jsonify({'success': True}), 201

    opportunities = list(db.opportunities.find().sort("posted", -1))
    for opp in opportunities:
        opp['application_count'] = db.applications.count_documents({'opportunity_id': opp['_id']})
    
    total_apps = db.applications.count_documents({})
    stats = {
        'total': len(opportunities),
        'totalApplications': total_apps,
        'accepted': db.applications.count_documents({"status": "Accepted"}),
        'underReview': db.applications.count_documents({"status": "Under Consideration"})
    }
    return jsonify({'stats': stats, 'jobs': parse_json(opportunities)})

@admin_bp.route('/api/opportunities/<job_id>/applications')
@login_required
@role_required('admin')
def get_job_applications(job_id):
    db = current_app.db
    applications = list(db.applications.find({'opportunity_id': ObjectId(job_id)}))
    
    for app in applications:
        consultant = db.employees.find_one({'username': app['consultant_username']})
        app['consultant_name'] = consultant.get('name', 'N/A') if consultant else 'N/A'
        app['consultant_role'] = consultant.get('role', 'N/A') if consultant else 'N/A'

    return jsonify(parse_json(applications))

@admin_bp.route('/api/applications/update', methods=['POST'])
@login_required
@role_required('admin')
def update_application_status():
    db = current_app.db
    data = request.json
    application_id = data.get('applicationId')
    new_status = data.get('status')

    if not application_id or not new_status:
        return jsonify({'success': False, 'error': 'Missing data'}), 400

    db.applications.update_one(
        {'_id': ObjectId(application_id)},
        {'$set': {'status': new_status}}
    )
    return jsonify({'success': True})


@admin_bp.route('/api/reports')
@login_required
@role_required('admin')
def api_admin_reports():
    employees = list(current_app.db.employees.find({}))
    return jsonify({'employees': parse_json(employees)})

@admin_bp.route('/api/monitor-stats')
@login_required
@role_required('admin')
def api_monitor_stats():
    db = current_app.db
    all_projects = list(db.opportunities.find({}))
    projects_in_queue = sum(1 for p in all_projects if p.get('status') == 'Open')
    active_projects_count = sum(1 for p in all_projects if p.get('status') == 'In Progress')
    failed_projects = sum(1 for p in all_projects if p.get('status') == 'Cancelled')
    total_duration_days, valid_completed_projects = 0, 0
    completed_projects_list = [p for p in all_projects if p.get('status') == 'Completed']
    for p in completed_projects_list:
        try:
            start_date_str, end_date_str = p.get('startDate'), p.get('endDate')
            if start_date_str and end_date_str:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                total_duration_days += (end_date - start_date).days
                valid_completed_projects += 1
        except (ValueError, TypeError) as e:
            print(f"Warning: Could not parse dates for project {p.get('_id')}. Error: {e}")
            continue
    avg_duration = (total_duration_days / valid_completed_projects) if valid_completed_projects > 0 else 0
    total_closed_projects = valid_completed_projects + failed_projects
    failure_rate = (failed_projects / total_closed_projects) * 100 if total_closed_projects > 0 else 0
    stats = {
        "projectsInQueue": projects_in_queue,
        "avgProjectDuration": f"{avg_duration:.1f} days",
        "projectFailureRate": f"{failure_rate:.2f}%",
        "activeProjects": active_projects_count,
        "completedProjects": valid_completed_projects,
        "failedProjects": failed_projects
    }
    return jsonify(stats)

@admin_bp.route('/api/project-activity')
@login_required
@role_required('admin')
def api_project_activity():
    db = current_app.db
    activity = list(db.opportunities.find({}, {'_id': 1, 'title': 1, 'company': 1, 'status': 1, 'lastUpdate': 1}).sort("lastUpdate", -1).limit(10))
    return jsonify(parse_json(activity))

# +++ CHATBOT ENDPOINT UPDATED FOR FULL DATA ACCESS +++
@admin_bp.route('/api/chatbot', methods=['POST'])
@login_required
@role_required('admin')
def api_admin_chatbot():
    if not gemini_model: 
        return jsonify({'response': "AI model is not configured."}), 503
    
    user_query = request.json.get('query')
    if not user_query: 
        return jsonify({'response': "No query provided."}), 400
    
    db = current_app.db
    
    # Fetch all relevant data from the database, excluding sensitive fields
    context_data = {
        "employees": list(db.employees.find({}, {'_id': 0})),
        "opportunities": list(db.opportunities.find({}, {'_id': 0})),
        "applications": list(db.applications.find({}, {'_id': 0})),
        "consultant_certifications": list(db.user_certifications.find({}, {'_id': 0})),
        "consultant_trainings": list(db.user_trainings.find({}, {'_id': 0}))
    }
    
    # Convert the data to a JSON string for the prompt
    # Using json_util to handle MongoDB specific types like ObjectId
    context_json = json.loads(json_util.dumps(context_data))

    prompt = f"""
    You are an expert HR and data analyst for a technology consulting firm.
    Your role is to provide insights by analyzing the complete dataset of the company provided below in JSON format.
    Answer the user's query based ONLY on this data. Do not invent information.
    Format your answers clearly using Markdown (e.g., headings, lists, bold text).

    **Complete Company Data:**
    {json.dumps(context_json, indent=2)}

    **User Query:** "{user_query}"
    """
    
    try:
        ai_response = gemini_model.generate_content(prompt)
        response_text = ai_response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        response_text = "Sorry, an error occurred while processing your request with the AI model."
    
    return jsonify({'response': response_text})

@admin_bp.route('/api/genai-summary', methods=['POST'])
@login_required
@role_required('admin')
def genai_summary():
    if not gemini_model: return jsonify({'summary': "AI model is not configured."}), 503
    report_data_str = request.json.get('report_data')
    if not report_data_str: return jsonify({'summary': "No report data provided."}), 400
    report_data = json.loads(report_data_str)
    prompt = f"""
    You are an expert HR and performance analyst...
    **Report Data:**
    {json.dumps(report_data, indent=2)}
    """
    try:
        ai_response = gemini_model.generate_content(prompt)
        summary_text = ai_response.parts[0].text
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        summary_text = "I'm sorry, I encountered an error."
    return jsonify({'summary': summary_text})
