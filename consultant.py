from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request, current_app
from functools import wraps
from bson import json_util, ObjectId
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os
import google.generativeai as genai

# --- Gemini API Configuration ---
# This uses the same GOOGLE_API_KEY environment variable as the admin section
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
except KeyError:
    gemini_model = None
    print("\n--- WARNING: GOOGLE_API_KEY environment variable not set. ---")
    print("--- Chatbot functionality will be disabled. ---\n")


consultant_bp = Blueprint('consultant', __name__, url_prefix='/consultant')

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
@consultant_bp.route('/home')
@login_required
@role_required('consultant')
def consultant_home(): return render_template('consultant/consultant_home.html')

@consultant_bp.route('/training')
@login_required
@role_required('consultant')
def consultant_training(): return render_template('consultant/consultant_training.html')

@consultant_bp.route('/attendance')
@login_required
@role_required('consultant')
def consultant_attendance(): return render_template('consultant/consultant_attendance.html')

@consultant_bp.route('/certifications')
@login_required
@role_required('consultant')
def consultant_certifications(): return render_template('consultant/consultant_certifications.html')

@consultant_bp.route('/opportunities')
@login_required
@role_required('consultant')
def consultant_opportunities(): return render_template('consultant/consultant_opportunities.html')

@consultant_bp.route('/resume-builder')
@login_required
@role_required('consultant')
def consultant_resume_builder(): return render_template('consultant/consultant_resume builder.html')

@consultant_bp.route('/chatbot')
@login_required
@role_required('consultant')
def consultant_chatbot(): return render_template('consultant/consultant_chatbot.html')

# --- API Endpoints ---
@consultant_bp.route('/api/dashboard')
@login_required
@role_required('consultant')
def api_consultant_dashboard():
    username = session.get('username')
    db = current_app.db
    emp = db.employees.find_one({"username": username})
    if not emp: return jsonify({"error": "Employee not found"}), 404
    
    certs_count = db.user_certifications.count_documents({"consultant_username": username, "status": "Active"})
    trainings = list(db.user_trainings.find({"consultant_username": username}))
    training_summary = {'completed': sum(1 for t in trainings if t['status'] == 'Completed'), 'inProgress': sum(1 for t in trainings if t['status'] == 'In Progress'), 'notAttended': sum(1 for t in trainings if t['status'] == 'Not Started')}
    
    now = datetime.now()
    thirty_days_ago = (now - timedelta(days=30)).strftime("%Y-%m-%d")
    attendance_recs = list(db.attendance_records.find({'consultant_username': username, 'date': {'$gte': thirty_days_ago}}))
    working_recs = [r for r in attendance_recs if datetime.strptime(r['date'], "%Y-%m-%d").weekday() < 5]
    present_count = sum(1 for a in working_recs if a['status'] in ['Present', 'WFH'])
    total_working_days = len(working_recs)
    attendance_rate = min(100, int((present_count / total_working_days) * 100)) if total_working_days else 100
    
    training_score = emp.get('training_score', 0)
    
    attendance_breakdown = {
        'present': sum(1 for r in working_recs if r['status'] == 'Present'),
        'absent': sum(1 for r in working_recs if r['status'] in ['Absent', 'Leave']),
        'workFromHome': sum(1 for r in working_recs if r['status'] == 'WFH')
    }

    performance_progress = {'labels': [], 'scores': []}
    for i in range(3, -1, -1):
        month_date = now - relativedelta(months=i)
        start_of_month = month_date.replace(day=1).strftime("%Y-%m-%d")
        end_of_month = (month_date + relativedelta(months=1) - timedelta(days=1)).strftime("%Y-%m-%d")
        month_records = list(db.attendance_records.find({'consultant_username': username, 'date': {'$gte': start_of_month, '$lte': end_of_month}}))
        working_days = sum(1 for r in month_records if datetime.strptime(r['date'], "%Y-%m-%d").weekday() < 5)
        month_present = sum(1 for a in month_records if a['status'] in ['Present', 'WFH'])
        base_rate = (month_present / working_days) * 100 if working_days else 0
        variability_factor = 1 - (i * 0.05)
        month_attendance_rate = max(40, int(base_rate * variability_factor))
        monthly_score = int(month_attendance_rate * 0.6 + training_score * 0.4)
        performance_progress['labels'].append(month_date.strftime("%b"))
        performance_progress['scores'].append(monthly_score)
    
    current_performance_score = performance_progress['scores'][-1] if performance_progress['scores'] else 0
    recent_certs = list(db.user_certifications.find({"consultant_username": username, "status": "Active"}).sort("issueDate", -1).limit(3))
    
    dashboard_data = {
        'name': emp['name'],
        'stats': {'attendanceRate': attendance_rate, 'trainingProgress': training_score, 'activeCertifications': certs_count, 'performanceScore': current_performance_score},
        'attendanceBreakdown': attendance_breakdown, 'trainingSummary': training_summary, 'performanceProgress': performance_progress,
        'recentCertifications': [{'name': c['title'], 'completed': c['issueDate'], 'status': c['status']} for c in recent_certs]
    }
    return jsonify(dashboard_data)

@consultant_bp.route('/api/training')
@login_required
@role_required('consultant')
def api_consultant_training():
    username = session.get('username')
    courses = list(current_app.db.user_trainings.find({'consultant_username': username}))
    stats = {'completed': 0, 'inProgress': 0, 'notStarted': 0}
    total_progress = 0
    for course in courses:
        if course['status'] == 'Completed': stats['completed'] += 1
        elif course['status'] == 'In Progress': stats['inProgress'] += 1
        else: stats['notStarted'] += 1
        total_progress += course.get('progress', 0)
    stats['avgProgress'] = int(total_progress / len(courses)) if courses else 0
    return jsonify({"stats": stats, "courses": parse_json(courses)})

@consultant_bp.route('/api/attendance')
@login_required
@role_required('consultant')
def api_consultant_attendance():
    username = session.get('username')
    db = current_app.db
    one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    records = list(db.attendance_records.find({'consultant_username': username, 'date': {'$gte': one_year_ago}}))
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_records = [r for r in records if datetime.strptime(r['date'], "%Y-%m-%d") >= thirty_days_ago]
    present = sum(1 for r in recent_records if r['status'] == 'Present')
    wfh = sum(1 for r in recent_records if r['status'] == 'WFH')
    absent = sum(1 for r in recent_records if r['status'] in ['Absent', 'Leave'])
    stats = {
        'monthlyAttendance': int(((present + wfh) / len(recent_records)) * 100) if recent_records else 100,
        'presentDays': present,
        'absentDays': absent,
        'wfhDays': wfh
    }
    breakdown = {"present": present, "absent": absent, "wfh": wfh}
    trends = {"labels": [], "present": [], "absent": [], "wfh": []}
    for i in range(2, -1, -1):
        month_date = datetime.now() - relativedelta(months=i)
        month_str, month_name = month_date.strftime("%Y-%m"), month_date.strftime("%b")
        month_records = [r for r in records if r['date'].startswith(month_str)]
        trends['labels'].append(month_name)
        trends['present'].append(sum(1 for r in month_records if r['status'] == 'Present'))
        trends['absent'].append(sum(1 for r in month_records if r['status'] in ['Absent', 'Leave']))
        trends['wfh'].append(sum(1 for r in month_records if r['status'] == 'WFH'))
    return jsonify({"stats": stats, "breakdown": breakdown, "trends": trends, "all_records": parse_json(records)})

@consultant_bp.route('/api/certifications', methods=['GET', 'POST', 'DELETE'])
@login_required
@role_required('consultant')
def api_consultant_certifications():
    username = session.get('username')
    db = current_app.db
    if request.method == 'POST':
        cert_data = request.json
        cert_id_str = cert_data.pop('_id', {}).get('$oid')
        if cert_id_str:
            db.user_certifications.update_one({'_id': ObjectId(cert_id_str), 'consultant_username': username}, {'$set': cert_data})
        else:
            cert_data['consultant_username'] = username
            db.user_certifications.insert_one(cert_data)
        return jsonify({'success': True})
    if request.method == 'DELETE':
        db.user_certifications.delete_one({'_id': ObjectId(request.json.get('id')), 'consultant_username': username})
        return jsonify({'success': True})
    certs = list(db.user_certifications.find({'consultant_username': username}))
    stats = {'total': len(certs), 'active': sum(1 for c in certs if c['status'] == 'Active'), 'expired': sum(1 for c in certs if c['status'] != 'Active'), 'categories': len(set(c['category'] for c in certs))}
    return jsonify({'stats': stats, 'list': parse_json(certs)})

@consultant_bp.route('/api/resume', methods=['GET', 'POST'])
@login_required
@role_required('consultant')
def api_consultant_resume():
    username = session.get('username')
    db = current_app.db
    if request.method == 'POST':
        db.resumes.update_one({'consultant_username': username}, {'$set': {'resume_data': request.json}}, upsert=True)
        return jsonify({'success': True})
    resume_doc = db.resumes.find_one({'consultant_username': username})
    return jsonify(parse_json(resume_doc['resume_data']) if resume_doc else None)

@consultant_bp.route('/api/resume/generate-summary', methods=['POST'])
@login_required
@role_required('consultant')
def api_generate_resume_summary():
    if not gemini_model:
        return jsonify({'error': "AI model is not configured. Please contact an administrator."}), 503
    username = session.get('username')
    db = current_app.db
    employee_profile = db.employees.find_one({'username': username}, {'_id': 0})
    if not employee_profile:
        return jsonify({'error': 'Could not find employee profile.'}), 404
    prompt = f"""
    You are an expert technical resume writer...
    **Consultant's Profile:**
    {json.dumps(employee_profile, indent=2)}
    """
    try:
        ai_response = gemini_model.generate_content(prompt)
        summary_text = ai_response.text
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        summary_text = "I'm sorry, I encountered an error while generating the summary."
    return jsonify({'summary': summary_text})

@consultant_bp.route('/api/opportunities')
@login_required
@role_required('consultant')
def api_consultant_opportunities():
    username = session.get('username')
    db = current_app.db
    opportunities = list(db.opportunities.find({"status": {"$in": ["Open", "In Progress"]}}).sort("posted", -1))
    applications = list(db.applications.find({'consultant_username': username}))
    user_app_map = {str(app['opportunity_id']): app['status'] for app in applications}
    for opp in opportunities:
        if str(opp['_id']) in user_app_map:
            opp['applicationStatus'] = user_app_map[str(opp['_id'])]
    stats = {'total': len(opportunities), 'sent': len(applications), 'review': sum(1 for app in applications if app['status'] == 'Under Consideration'), 'accepted': sum(1 for app in applications if app['status'] == 'Accepted')}
    return jsonify({'stats': stats, 'list': parse_json(opportunities)})

@consultant_bp.route('/api/apply', methods=['POST'])
@login_required
@role_required('consultant')
def api_apply():
    username = session.get('username')
    job_id = request.json.get('jobId')
    db = current_app.db
    if not db.applications.find_one({'consultant_username': username, 'opportunity_id': ObjectId(job_id)}):
        db.applications.insert_one({'consultant_username': username, 'opportunity_id': ObjectId(job_id), 'status': 'Under Consideration'})
        db.opportunities.update_one({'_id': ObjectId(job_id)}, {'$inc': {'applications': 1}})
    return jsonify({'success': True})

# +++ CHATBOT ENDPOINT UPDATED FOR EFFICIENCY AND BETTER ADVICE +++
@consultant_bp.route('/api/chatbot', methods=['POST'])
@login_required
@role_required('consultant')
def api_consultant_chatbot():
    if not gemini_model:
        return jsonify({'response': "AI model is not configured. Please contact an administrator."}), 503

    user_query = request.json.get('query')
    username = session.get('username')
    if not user_query or not username:
        return jsonify({'response': "I'm sorry, there was an issue with your request."}), 400

    db = current_app.db
    
    # Fetch the consultant's personal data
    employee_data = db.employees.find_one({'username': username}, {'_id': 0})
    certifications = list(db.user_certifications.find({'consultant_username': username}, {'_id': 0, 'consultant_username': 0}))
    trainings = list(db.user_trainings.find({'consultant_username': username}, {'_id': 0, 'consultant_username': 0}))

    # --- INTELLIGENT CONTEXT ADDITION ---
    # Only add the list of opportunities if the query is about jobs, to keep the prompt fast and efficient.
    job_keywords = ['job', 'opportunity', 'opportunities', 'career', 'apply', 'role', 'skills for']
    include_opportunities = any(keyword in user_query.lower() for keyword in job_keywords)
    
    opportunities_context = ""
    if include_opportunities:
        open_opportunities = list(db.opportunities.find({"status": {"$in": ["Open", "In Progress"]}}, {'_id': 0}))
        opportunities_context = f"""
        **4. Available Job Opportunities:**
        {json.dumps(open_opportunities, indent=2)}
        """

    # Construct the new, more powerful prompt
    prompt = f"""
    You are a helpful, encouraging, and proactive AI career coach for a technology consultant.
    Your role is to provide actionable advice and insights based on the user's personal data and available opportunities.
    
    **Your Persona & Rules:**
    - **Be Proactive:** Don't just answer the question. Analyze the user's data to find opportunities for growth.
    - **Give Actionable Advice:** Provide specific, concrete suggestions. For example, instead of "improve your skills," say "The 'Senior React Developer' role requires TypeScript. I see you have a training for it that is not started. Completing that would be a great next step."
    - **Skill Gap Analysis:** If the user asks about a job AND job opportunities are provided in the context, compare their skills with the job requirements and clearly identify any gaps. Suggest specific trainings or certifications from their list to fill those gaps.
    - **Performance Improvement:** If the user asks about their performance or attendance, analyze their scores and provide positive, encouraging advice on how to improve.
    - **Use Only Provided Data:** Do not invent information. If the answer isn't in the data, state that you don't have that information.
    - **Format clearly:** Use Markdown (headings, bold text, and lists) to make your response easy to read.

    **Here is the complete data for your analysis:**

    **1. Consultant's Profile:**
    {json.dumps(employee_data, indent=2)}

    **2. Consultant's Certifications:**
    {json.dumps(certifications, indent=2)}

    **3. Consultant's Trainings:**
    {json.dumps(trainings, indent=2)}
    {opportunities_context}
    ---
    
    Now, based on all the data above, please answer the following question from the consultant in a helpful and proactive way:
    
    **Consultant's Question:** "{user_query}"
    """

    try:
        ai_response = gemini_model.generate_content(prompt)
        response_text = ai_response.text
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        response_text = "I'm sorry, I encountered an error while processing your request."

    return jsonify({'response': response_text})
