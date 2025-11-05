"""Unit tests for report generator."""

import unittest
import os
import tempfile
import json
from utils.report_generator import generate_report, generate_html_report


class TestReportGenerator(unittest.TestCase):
    """Test cases for report generation functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)

        self.target_ip = "192.168.1.100"
        self.open_ports = [80, 443]
        self.service = "Nginx 1.18"
        self.cve_list = [
            {"id": "CVE-2021-23017", "description": "Test vulnerability 1"},
            {"id": "CVE-2021-3618", "description": "Test vulnerability 2"}
        ]
        self.fuzz_results = {
            "fuzz_cases": ["case1", "case2", "case3"]
        }

    def tearDown(self):
        """Clean up test files."""
        os.chdir(self.original_dir)
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_generate_json_report(self):
        """Test JSON report generation."""
        json_file, html_file = generate_report(
            self.target_ip,
            self.open_ports,
            self.service,
            self.cve_list,
            self.fuzz_results
        )

        # Check JSON file exists
        self.assertTrue(os.path.exists(json_file))

        # Verify JSON content
        with open(json_file, 'r') as f:
            report = json.load(f)

        self.assertEqual(report['target_ip'], self.target_ip)
        self.assertEqual(report['open_ports'], self.open_ports)
        self.assertEqual(report['service'], self.service)
        self.assertEqual(len(report['cve_list']), 2)

    def test_generate_html_report(self):
        """Test HTML report generation."""
        html_file = generate_html_report(
            self.target_ip,
            self.open_ports,
            self.service,
            self.cve_list,
            self.fuzz_results
        )

        # Check HTML file exists
        self.assertTrue(os.path.exists(html_file))

        # Verify HTML content
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn(self.target_ip, content)
        self.assertIn(self.service, content)
        self.assertIn("CVE-2021-23017", content)
        self.assertIn("<!DOCTYPE html>", content)

    def test_html_report_with_no_vulnerabilities(self):
        """Test HTML report generation with no vulnerabilities."""
        html_file = generate_html_report(
            self.target_ip,
            self.open_ports,
            self.service,
            [],
            {"fuzz_cases": []}
        )

        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("No CVE vulnerabilities detected", content)
        self.assertIn("No fuzzing tests performed", content)

    def test_html_report_risk_levels(self):
        """Test risk level calculation in HTML reports."""
        # High risk (3+ CVEs)
        high_risk_cves = [{"id": f"CVE-2021-{i}", "description": "Test"} for i in range(5)]
        html_file = generate_html_report(
            self.target_ip, [80], "Test Service", high_risk_cves, {"fuzz_cases": []}
        )

        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("High", content)

        # Low risk (no vulnerabilities)
        html_file = generate_html_report(
            self.target_ip, [80], "Test Service", [], {"fuzz_cases": []}
        )

        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("Low", content)


if __name__ == '__main__':
    unittest.main()
