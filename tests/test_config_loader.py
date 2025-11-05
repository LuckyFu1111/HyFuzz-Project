"""Unit tests for configuration loader."""

import unittest
import os
import tempfile
import json
import yaml
from utils.config_loader import ConfigLoader


class TestConfigLoader(unittest.TestCase):
    """Test cases for ConfigLoader class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_default_config_loaded(self):
        """Test that default configuration is loaded when no file is provided."""
        config = ConfigLoader()
        self.assertIsNotNone(config.config)
        self.assertEqual(config.get('fuzzing.engine'), 'hypothesis')

    def test_load_yaml_config(self):
        """Test loading configuration from YAML file."""
        yaml_config = {
            'fuzzing': {
                'engine': 'boofuzz',
                'max_depth': 5
            }
        }

        yaml_path = os.path.join(self.temp_dir, 'test_config.yaml')
        with open(yaml_path, 'w') as f:
            yaml.safe_dump(yaml_config, f)

        config = ConfigLoader(yaml_path)
        self.assertEqual(config.get('fuzzing.engine'), 'boofuzz')
        self.assertEqual(config.get('fuzzing.max_depth'), 5)

    def test_load_json_config(self):
        """Test loading configuration from JSON file."""
        json_config = {
            'fuzzing': {
                'engine': 'boofuzz',
                'max_depth': 7
            }
        }

        json_path = os.path.join(self.temp_dir, 'test_config.json')
        with open(json_path, 'w') as f:
            json.dump(json_config, f)

        config = ConfigLoader(json_path)
        self.assertEqual(config.get('fuzzing.engine'), 'boofuzz')
        self.assertEqual(config.get('fuzzing.max_depth'), 7)

    def test_get_nested_value(self):
        """Test getting nested configuration values."""
        config = ConfigLoader()
        value = config.get('fuzzing.max_depth')
        self.assertEqual(value, 3)

    def test_get_nonexistent_key(self):
        """Test getting a nonexistent key returns default."""
        config = ConfigLoader()
        value = config.get('nonexistent.key', 'default')
        self.assertEqual(value, 'default')

    def test_set_value(self):
        """Test setting configuration values."""
        config = ConfigLoader()
        config.set('fuzzing.max_depth', 10)
        self.assertEqual(config.get('fuzzing.max_depth'), 10)

    def test_validate_valid_config(self):
        """Test validation of valid configuration."""
        config = ConfigLoader()
        self.assertTrue(config.validate())

    def test_validate_invalid_engine(self):
        """Test validation fails for invalid fuzzing engine."""
        config = ConfigLoader()
        config.set('fuzzing.engine', 'invalid_engine')
        self.assertFalse(config.validate())

    def test_save_yaml_config(self):
        """Test saving configuration to YAML file."""
        config = ConfigLoader()
        config.set('fuzzing.max_depth', 15)

        output_path = os.path.join(self.temp_dir, 'saved_config.yaml')
        config.save(output_path)

        self.assertTrue(os.path.exists(output_path))

        # Verify saved content
        with open(output_path, 'r') as f:
            saved_config = yaml.safe_load(f)
        self.assertEqual(saved_config['fuzzing']['max_depth'], 15)

    def test_save_json_config(self):
        """Test saving configuration to JSON file."""
        config = ConfigLoader()
        config.set('fuzzing.max_depth', 20)

        output_path = os.path.join(self.temp_dir, 'saved_config.json')
        config.save(output_path)

        self.assertTrue(os.path.exists(output_path))

        # Verify saved content
        with open(output_path, 'r') as f:
            saved_config = json.load(f)
        self.assertEqual(saved_config['fuzzing']['max_depth'], 20)


if __name__ == '__main__':
    unittest.main()
