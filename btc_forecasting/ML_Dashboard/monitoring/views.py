from django.shortcuts import render
import pandas as pd
import os
import json

def dashboard_overview(request):
    log_path = os.path.join(os.path.dirname(__file__), '../../logs/predictions.parquet')
    drift_report_path = os.path.join(os.path.dirname(__file__), '../../reports/drift/data_drift_report.json')
    model_drift_path = os.path.join(os.path.dirname(__file__), '../../reports/drift/model_drift_report.json')
    
    logs = []
    chart_logs = "[]"
    if os.path.exists(log_path):
        df = pd.read_parquet(log_path)
        
        # Handle NaN values for JSON safety
        df = df.where(pd.notnull(df), None)
        
        # 1. Prepare Chart Logs (Latest 50, ascending)
        # to_json handles Timestamps and NaNs perfectly for Chart.js
        chart_df = df.tail(50).copy()
        chart_logs = chart_df.to_json(orient='records', date_format='iso')
        
        # 2. Prepare Table Logs (Latest 100, descending)
        # For the table, we'll format the timestamp string here
        table_df = df.tail(100).copy()
        if 'timestamp' in table_df.columns:
            table_df['timestamp'] = pd.to_datetime(table_df['timestamp']).dt.strftime('%d %b %Y, %I:%M %p')
        logs = table_df.sort_index(ascending=False).to_dict('records')
    
    data_drift = {}
    if os.path.exists(drift_report_path):
        with open(drift_report_path, "r") as f:
            data_drift = json.load(f)
            
    model_drift = {}
    if os.path.exists(model_drift_path):
        with open(model_drift_path, "r") as f:
            model_drift = json.load(f)
    
    return render(request, 'monitoring/dashboard.html', {
        'logs': logs,
        'chart_logs': chart_logs,
        'data_drift': data_drift,
        'model_drift': model_drift
    })

def drift_monitoring(request):
    import json
    drift_report_path = os.path.join(os.path.dirname(__file__), '../../reports/drift/data_drift_report.json')
    alerts_log_path = os.path.join(os.path.dirname(__file__), '../../logs/alerts.log')
    
    data_drift = {}
    if os.path.exists(drift_report_path):
        with open(drift_report_path, "r") as f:
            data_drift = json.load(f)
            
    alerts = []
    if os.path.exists(alerts_log_path):
        with open(alerts_log_path, "r") as f:
            alerts = f.readlines()
            alerts.reverse()
            alerts = [a.strip() for a in alerts[:20]]

    return render(request, 'monitoring/drift.html', {
        'data_drift': data_drift,
        'alerts': alerts
    })

def prediction_ui(request):
    log_path = os.path.join(os.path.dirname(__file__), '../../logs/predictions.parquet')
    
    history = []
    if os.path.exists(log_path):
        df = pd.read_parquet(log_path)
        # Handle NaN values for JSON safety
        df = df.where(pd.notnull(df), None)
        
        # Convert ALL datetime columns for JSON
        for col in df.select_dtypes(include=['datetime', 'datetimetz']).columns:
            df[col] = df[col].astype(str)
        
        # Sort by timestamp descending
        if 'timestamp' in df.columns:
            df = df.sort_values('timestamp', ascending=False)
        history = df.head(20).to_dict('records')
        
    return render(request, 'monitoring/prediction.html', {
        'history': history,
        'api_url': 'http://127.0.0.1:8000/trigger' # Correct port and endpoint
    })

