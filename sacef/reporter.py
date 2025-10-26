import json
from typing import List, Dict, Any

def generate_report(results: List[Dict[str, Any]], vulnerabilities: List[Any]) -> Dict[str, Any]:
    """
    Generates a structured report from the analysis results and vulnerabilities.
    """
    report = {
        'summary': {
            'total_functions_analyzed': len(results),
            'total_vulnerabilities_found': len(vulnerabilities),
            'total_duration': sum(r.get('duration', 0) for r in results)
        },
        'vulnerabilities': [vuln.to_dict() for vuln in vulnerabilities],
        'details': results
    }
    return report

def save_report_to_json(report: Dict[str, Any], file_path: str):
    """
    Saves the generated report to a JSON file.
    """
    with open(file_path, 'w') as f:
        json.dump(report, f, indent=4)
