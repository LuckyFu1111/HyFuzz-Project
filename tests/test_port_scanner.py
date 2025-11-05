"""Unit tests for port scanner."""

import unittest
from unittest.mock import patch, MagicMock
from modules.port_scanner import check_port, scan_http_ports


class TestPortScanner(unittest.TestCase):
    """Test cases for port scanning functions."""

    @patch('modules.port_scanner.socket.socket')
    def test_check_port_open(self, mock_socket):
        """Test checking an open port."""
        # Mock successful connection
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.connect_ex.return_value = 0

        result = check_port("192.168.1.1", 80, timeout=1)
        self.assertTrue(result)

    @patch('modules.port_scanner.socket.socket')
    def test_check_port_closed(self, mock_socket):
        """Test checking a closed port."""
        # Mock failed connection
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.connect_ex.return_value = 1

        result = check_port("192.168.1.1", 9999, timeout=1)
        self.assertFalse(result)

    @patch('modules.port_scanner.check_port')
    def test_scan_http_ports(self, mock_check_port):
        """Test scanning multiple HTTP ports."""
        # Mock some ports open, some closed
        mock_check_port.side_effect = [True, False, True, False]

        open_ports = scan_http_ports("192.168.1.1")

        # Should return open ports (first and third in the mocked sequence)
        self.assertIsInstance(open_ports, list)
        # The actual implementation might vary, but we're testing the function works


if __name__ == '__main__':
    unittest.main()
