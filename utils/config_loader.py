"""Configuration loader for HyFuzz.

This module provides functionality to load and validate configuration
from YAML/JSON files with fallback to defaults.
"""

import os
import json
import yaml
import copy
from typing import Dict, Any, Optional


class ConfigLoader:
    """Load and manage HyFuzz configuration."""

    DEFAULT_CONFIG = {
        "targets": {
            "default_ip": "192.168.25.133",
            "cidr_range": None
        },
        "port_scanning": {
            "ports": [80, 443, 8080, 8443, 8000, 8888, 9090],
            "timeout": 2,
            "threads": 10
        },
        "service_detection": {
            "timeout": 3,
            "user_agent": "HyFuzz/1.0"
        },
        "fuzzing": {
            "engine": "hypothesis",
            "max_depth": 3,
            "num_examples": 50,
            "timeout": 5
        },
        "ai_generation": {
            "mode": "none",
            "gan": {
                "epochs": 500,
                "batch_size": 32,
                "learning_rate": 0.0002
            },
            "deepseek": {
                "model": "deepseek-r1:8b",
                "temperature": 0.7
            }
        },
        "cve_database": {
            "path": "data/cve_database.json",
            "update_interval": 86400
        },
        "vulnerability_testing": {
            "timeout": 5,
            "max_retries": 2,
            "retry_delay": 1
        },
        "reporting": {
            "output_dir": "reports",
            "formats": ["json", "html"],
            "include_screenshots": False,
            "verbose": True
        },
        "logging": {
            "level": "INFO",
            "file": "hyfuzz.log",
            "max_size": 10485760,
            "backup_count": 5,
            "console_output": True,
            "colored_output": True
        },
        "performance": {
            "max_concurrent_scans": 5,
            "memory_limit_mb": 2048,
            "cache_results": True
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the configuration loader.

        Args:
            config_path: Path to configuration file (YAML or JSON)
        """
        self.config_path = config_path
        # Use deep copy to prevent shared state between instances
        self.config = copy.deepcopy(self.DEFAULT_CONFIG)

        if config_path and os.path.exists(config_path):
            self.load_config(config_path)

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from a file.

        Args:
            config_path: Path to the configuration file

        Returns:
            Dict containing the loaded configuration

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file format is invalid
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                    loaded_config = yaml.safe_load(f)
                elif config_path.endswith('.json'):
                    loaded_config = json.load(f)
                else:
                    raise ValueError(f"Unsupported config file format: {config_path}")

            # Deep merge with defaults
            self.config = self._deep_merge(self.DEFAULT_CONFIG, loaded_config)
            print(f"[INFO] Configuration loaded from: {config_path}")

        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")

        return self.config

    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Recursively merge two dictionaries.

        Args:
            base: Base dictionary (defaults)
            override: Override dictionary (user config)

        Returns:
            Merged dictionary
        """
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.

        Args:
            key_path: Configuration key path (e.g., 'fuzzing.max_depth')
            default: Default value if key not found

        Returns:
            Configuration value or default

        Examples:
            >>> config.get('fuzzing.max_depth')
            3
            >>> config.get('nonexistent.key', 'default')
            'default'
        """
        keys = key_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path: str, value: Any) -> None:
        """Set configuration value using dot notation.

        Args:
            key_path: Configuration key path (e.g., 'fuzzing.max_depth')
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config

        for key in keys[:-1]:
            if key not in config or not isinstance(config[key], dict):
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value

    def save(self, output_path: str) -> None:
        """Save current configuration to a file.

        Args:
            output_path: Path to save the configuration
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            if output_path.endswith('.yaml') or output_path.endswith('.yml'):
                yaml.safe_dump(self.config, f, default_flow_style=False)
            elif output_path.endswith('.json'):
                json.dump(self.config, f, indent=4)
            else:
                raise ValueError(f"Unsupported output format: {output_path}")

        print(f"[INFO] Configuration saved to: {output_path}")

    def validate(self) -> bool:
        """Validate the configuration.

        Returns:
            True if configuration is valid, False otherwise
        """
        required_keys = [
            'port_scanning.ports',
            'fuzzing.engine',
            'cve_database.path'
        ]

        for key in required_keys:
            if self.get(key) is None:
                print(f"[ERROR] Missing required configuration: {key}")
                return False

        # Validate fuzzing engine
        if self.get('fuzzing.engine') not in ['boofuzz', 'hypothesis']:
            print("[ERROR] Invalid fuzzing engine. Must be 'boofuzz' or 'hypothesis'")
            return False

        # Validate AI mode
        if self.get('ai_generation.mode') not in ['none', 'gan', 'deepseek']:
            print("[ERROR] Invalid AI mode. Must be 'none', 'gan', or 'deepseek'")
            return False

        return True

    def __repr__(self) -> str:
        """String representation of the configuration."""
        return f"ConfigLoader(config_path={self.config_path})"


# Singleton instance
_config_instance: Optional[ConfigLoader] = None


def get_config(config_path: Optional[str] = None) -> ConfigLoader:
    """Get or create the global configuration instance.

    Args:
        config_path: Path to configuration file

    Returns:
        ConfigLoader instance
    """
    global _config_instance

    if _config_instance is None:
        # Try to find config file if not specified
        if config_path is None:
            search_paths = [
                'configs/config.yaml',
                'configs/config.yml',
                'configs/config.json',
                'config.yaml',
                'config.yml'
            ]
            for path in search_paths:
                if os.path.exists(path):
                    config_path = path
                    break

        _config_instance = ConfigLoader(config_path)

    return _config_instance


def reload_config(config_path: str) -> ConfigLoader:
    """Reload configuration from a new file.

    Args:
        config_path: Path to new configuration file

    Returns:
        Updated ConfigLoader instance
    """
    global _config_instance
    _config_instance = ConfigLoader(config_path)
    return _config_instance
