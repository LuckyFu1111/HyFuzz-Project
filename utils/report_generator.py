import json
from datetime import datetime


def generate_html_report(target_ip, open_ports, service, cve_list, fuzz_results):
    """Generate an HTML vulnerability detection report.

    Args:
        target_ip (str): Target IP address
        open_ports (list): List of open ports detected
        service (str): Detected service and version
        cve_list (list): List of CVEs associated with the service
        fuzz_results (dict): Results from fuzz testing

    Returns:
        str: Path to the generated HTML report
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Count vulnerabilities
    vuln_count = len(cve_list) if cve_list else 0
    fuzz_count = len(fuzz_results.get('fuzz_cases', [])) if fuzz_results else 0

    # Determine risk level
    if vuln_count >= 3 or fuzz_count >= 5:
        risk_level = "High"
        risk_class = "risk-high"
    elif vuln_count >= 1 or fuzz_count >= 2:
        risk_level = "Medium"
        risk_class = "risk-medium"
    else:
        risk_level = "Low"
        risk_class = "risk-low"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyFuzz Vulnerability Report - {target_ip}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; }}
        h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .timestamp {{ opacity: 0.9; font-size: 14px; }}
        .content {{ padding: 30px; }}
        .section {{ margin-bottom: 30px; }}
        .section-title {{ font-size: 20px; color: #333; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #667eea; }}
        .info-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .info-card {{ background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #667eea; }}
        .info-label {{ font-weight: bold; color: #555; font-size: 12px; text-transform: uppercase; }}
        .info-value {{ color: #333; font-size: 16px; margin-top: 5px; }}
        .risk-high {{ border-left-color: #dc3545 !important; }}
        .risk-high .info-value {{ color: #dc3545; font-weight: bold; }}
        .risk-medium {{ border-left-color: #ffc107 !important; }}
        .risk-medium .info-value {{ color: #f57c00; font-weight: bold; }}
        .risk-low {{ border-left-color: #28a745 !important; }}
        .risk-low .info-value {{ color: #28a745; font-weight: bold; }}
        .cve-list {{ list-style: none; }}
        .cve-item {{ background: #fff3cd; padding: 12px; margin-bottom: 10px; border-radius: 5px; border-left: 4px solid #ffc107; }}
        .cve-id {{ font-weight: bold; color: #856404; }}
        .port-list {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .port-badge {{ background: #667eea; color: white; padding: 8px 15px; border-radius: 20px; font-weight: 500; }}
        .no-data {{ color: #999; font-style: italic; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #667eea; color: white; font-weight: 600; }}
        tr:hover {{ background: #f8f9fa; }}
        footer {{ background: #f8f9fa; padding: 20px 30px; border-radius: 0 0 8px 8px; text-align: center; color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔒 HyFuzz Vulnerability Assessment Report</h1>
            <div class="timestamp">Generated: {timestamp}</div>
        </header>

        <div class="content">
            <div class="section">
                <h2 class="section-title">Target Information</h2>
                <div class="info-grid">
                    <div class="info-card">
                        <div class="info-label">Target IP</div>
                        <div class="info-value">{target_ip}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">Detected Service</div>
                        <div class="info-value">{service if service else 'Unknown'}</div>
                    </div>
                    <div class="info-card {risk_class}">
                        <div class="info-label">Risk Level</div>
                        <div class="info-value">{risk_level}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">Vulnerabilities Found</div>
                        <div class="info-value">{vuln_count + fuzz_count}</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Open Ports</h2>
                <div class="port-list">
"""

    if open_ports:
        for port in open_ports:
            html_content += f'                    <span class="port-badge">Port {port}</span>\n'
    else:
        html_content += '                    <span class="no-data">No open ports detected</span>\n'

    html_content += """                </div>
            </div>

            <div class="section">
                <h2 class="section-title">CVE Vulnerabilities</h2>
"""

    if cve_list:
        html_content += '                <ul class="cve-list">\n'
        for cve in cve_list:
            if isinstance(cve, dict):
                cve_id = cve.get('id', 'Unknown')
                cve_desc = cve.get('description', 'No description available')
            else:
                cve_id = str(cve)
                cve_desc = 'No description available'
            html_content += f'                    <li class="cve-item"><span class="cve-id">{cve_id}</span><br>{cve_desc}</li>\n'
        html_content += '                </ul>\n'
    else:
        html_content += '                <p class="no-data">No CVE vulnerabilities detected</p>\n'

    html_content += """            </div>

            <div class="section">
                <h2 class="section-title">Fuzzing Results</h2>
"""

    if fuzz_results and fuzz_results.get('fuzz_cases'):
        html_content += """                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Test Case</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for idx, case in enumerate(fuzz_results['fuzz_cases'], 1):
            case_info = str(case)[:100] + '...' if len(str(case)) > 100 else str(case)
            html_content += f"""                        <tr>
                            <td>{idx}</td>
                            <td>{case_info}</td>
                            <td>Tested</td>
                        </tr>
"""
        html_content += """                    </tbody>
                </table>
"""
    else:
        html_content += '                <p class="no-data">No fuzzing tests performed</p>\n'

    html_content += """            </div>
        </div>

        <footer>
            <p>Generated by HyFuzz - A Hybrid AI-Enhanced Vulnerability Detection Framework</p>
            <p>© 2025 CS7 Lab, Friedrich-Alexander University Erlangen-Nürnberg</p>
        </footer>
    </div>
</body>
</html>
"""

    report_file = f"{target_ip}_report.html"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    return report_file


def generate_report(target_ip, open_ports, service, cve_list, fuzz_results):
    """Generate vulnerability detection reports in both JSON and HTML formats.

    Args:
        target_ip (str): Target IP address
        open_ports (list): List of open ports detected
        service (str): Detected service and version
        cve_list (list): List of CVEs associated with the service
        fuzz_results (dict): Results from fuzz testing

    Returns:
        tuple: Paths to the generated JSON and HTML reports
    """
    report = {
        "target_ip": target_ip,
        "open_ports": open_ports,
        "service": service,
        "cve_list": cve_list,
        "fuzz_results": fuzz_results,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Generate JSON report
    json_report_file = f"{target_ip}_report.json"
    with open(json_report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
    print(f"JSON Report generated: {json_report_file}")

    # Generate HTML report
    html_report_file = generate_html_report(target_ip, open_ports, service, cve_list, fuzz_results)
    print(f"HTML Report generated: {html_report_file}")

    return json_report_file, html_report_file