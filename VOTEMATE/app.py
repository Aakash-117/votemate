from flask import flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import os

app = flask(__name__)
CORS(app)
EXCEL_FILE = 'reported_issues.xlsx'
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['Issue Title', 'Reported By', 'Description', 'Status', 'Scheme Name', 'Department', 'Reported At'])
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/report-issue', methods=['POST'])
def report_issue():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        description = data.get('description')
        scheme_name = data.get('scheme_name', 'General')  
        department = data.get('department', 'General') 
        if not name or not email or not description:
            return jsonify({"message": "Name, email, and description are required!"}), 400

        new_row = {
            'Issue Title': f"Issue reported by {name}",
            'Reported By': email,
            'Description': description,
            'Status': 'Null',
            'Scheme Name': scheme_name,
            'Department': department,
            'Reported At': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        df = pd.read_excel(EXCEL_FILE)
        df = df.append(new_row, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)

        return jsonify({"message": "Issue reported successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to report issue. Please try again later."}), 500

if __name__ == "__main__":
    app.run(debug=True)