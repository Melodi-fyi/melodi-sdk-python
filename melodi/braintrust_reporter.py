# melodi/melodi/braintrust_reporter.py
import os
import re
import json
import requests
from typing import Optional
from braintrust import Reporter

def create_melodi_experiment(name: Optional[str] = None, 
                             instructions: Optional[str] = None, 
                             project: Optional[str] = None, 
                             template: Optional[str] = None) -> Optional[int]:
    api_key = os.environ.get("MELODI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Set the MELODI_API_KEY environment variable.")
    
    base_url = "https://app.melodi.fyi/api/external/experiments"
    if template:
        base_url += f"/templates/{template}"
    url = f"{base_url}?apiKey={api_key}"
    
    headers = {"Content-Type": "application/json"}
    data = {"experiment": {"name": name, "instructions": instructions, "project": project}}
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        print(f"Error creating Melodi experiment: {response.status_code}")
        return None

    feedback_url = response.json().get("feedbackUrl")
    match = re.search(r"(\d+)$", feedback_url)
    return int(match.group(1)) if match else None

def log_to_melodi_comparison_json(expected: str, output: str, experiment_id: int) -> int:
    api_key = os.environ.get("MELODI_API_KEY")
    url = f"https://app.melodi.fyi/api/external/experiments/{experiment_id}/comparisons/templates/json?apiKey={api_key}"
    headers = {"Content-Type": "application/json"}
    
    samples = [{"response": output, "version": "output"},
               {"response": expected, "version": "expected"}]
    
    response = requests.post(url, headers=headers, json={"samples": samples})
    return 1 if response.status_code == 200 else 0

def make_shareable(experiment_id: int) -> Optional[str]:
    api_key = os.environ.get("MELODI_API_KEY")
    url = f"https://app.melodi.fyi/api/external/experiments/{experiment_id}/shareable-link?apiKey={api_key}"
    response = requests.post(url)
    
    return response.json().get("shareableLink") if response.status_code == 200 else None

def report_evaluator_result(evaluator, result, verbose: bool, jsonl: bool):
    experiment_id = create_melodi_experiment(
        name=result.summary.experiment_name, 
        project=result.summary.project_name, 
        template='json'
    )
    
    if experiment_id is None:
        print("Failed to create experiment.")
        return
    
    for res in result.results:
        log_to_melodi_comparison_json(expected=res.expected, output=res.output, experiment_id=experiment_id)
    
    share_link = make_shareable(experiment_id)
    if share_link:
        print("---------------------------")
        print(f"Shareable Melodi Link: {share_link}")

melodi_reporter = Reporter(
    name="melodi_report",
    report_eval=report_evaluator_result,
    report_run=lambda results, verbose, jsonl: all(x.error is None for x in results),
)
