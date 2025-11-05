"""Unit tests for port scanner."""

import unittest
from unittest.mock import patch, MagicMock
from modules.port_scanner import scan_port, scan_http_ports


class TestPortScanner(unittest.TestCase):
    """Test cases for port scanning functions."""

    @patch('modules.port_scanner.socket.socket')
    def test_scan_port_open(self, mock_socket):
        """Test scanning an open port."""
        # Mock successful connection
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.connect_ex.return_value = 0

        open_ports = []
        scan_port("192.168.1.1", 80, open_ports)

        # Should add port to list
        self.assertEqual(len(open_ports), 1)
        self.assertEqual(open_ports[0], 80)

    @patch('modules.port_scanner.socket.socket')
    def test_scan_port_closed(self, mock_socket):
        """Test scanning a closed port."""
        # Mock failed connection
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.connect_ex.return_value = 1

        open_ports = []
        scan_port("192.168.1.1", 9999, open_ports)

        # Should not add port to list
        self.assertEqual(len(open_ports), 0)

    @patch('modules.port_scanner.scan_port')
    def test_scan_http_ports(self, mock_scan_port):
        """Test scanning multiple HTTP ports."""
        # Mock scan_port to simulate finding some open ports
        def mock_scan_side_effect(ip, port, open_ports):
            if port in [80, 443]:
                open_ports.append(port)

        mock_scan_port.side_effect = mock_scan_side_effect

        open_ports = scan_http_ports("192.168.1.1", ports=[80, 443, 8080, 8443])

        # Should return list of open ports
        self.assertIsInstance(open_ports, list)
        self.assertEqual(len(open_ports), 2)
        self.assertIn(80, open_ports)
        self.assertIn(443, open_ports)


if __name__ == '__main__':
    unittest.main()
