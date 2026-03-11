from django.shortcuts import render
import mlflow
import yaml
import os

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '../../config.yaml')
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def experiment_list(request):
    config = load_config()
    mlflow.set_tracking_uri(config['mlflow']['tracking_uri'])
    
    # Get all runs in the experiment
    experiment = mlflow.get_experiment_by_name(config['mlflow']['experiment_name'])
    runs = []
    if experiment:
        # Search runs
        all_runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id], order_by=["start_time DESC"])
        
        # Manually parse runs to handle the nested structure correctly for the template
        for _, run in all_runs.iterrows():
            # Extract tags/params/metrics safely
            # Note: mlflow.search_runs returns a DataFrame where metrics/params are prefixed
            runs.append({
                "start_time": str(run.get("start_time", "Unknown")),
                "run_name": run.get("tags.mlflow.runName", "N/A"),
                "model_type": run.get("params.model_type", "N/A"),
                "rmse": run.get("metrics.rmse", 0.0),
                "accuracy": run.get("metrics.direction_accuracy", 0.0) * 100,
                "status": run.get("status", "FINISHED")
            })
        
    # Load comparison results from JSON
    import json
    perf_path = os.path.join(os.path.dirname(__file__), '../../monitoring/model_performance.json')
    performance = {}
    if os.path.exists(perf_path):
        with open(perf_path, "r") as f:
            raw_perf = json.load(f)
            # Normalize keys to snake_case for Django template compatibility
            # Also multiply directional_accuracy by 100 for display
            for model, metrics in raw_perf.items():
                performance[model] = {}
                for k, v in metrics.items():
                    norm_key = k.lower().replace(" ", "_")
                    if norm_key == "directional_accuracy":
                        performance[model][norm_key] = v * 100
                    else:
                        performance[model][norm_key] = v
            
    return render(request, 'experiments/list.html', {
        'runs': runs,
        'performance': performance
    })
