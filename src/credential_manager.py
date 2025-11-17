"""
Secure credential management using OS keyring.

This module provides secure storage and retrieval of sensitive credentials
using the operating system's native keyring/credential storage:
- Windows: Windows Credential Manager
- macOS: Keychain
- Linux: Secret Service API (freedesktop.org)
"""

import keyring
import logging
from typing import Optional
from enum import Enum

logger = logging.getLogger(__name__)

# Service name for all Kinic credentials in the keyring
SERVICE_NAME = "kinic-backend"


class CredentialKey(Enum):
    """Enumeration of all credential keys used by Kinic."""
    MONAD_PRIVATE_KEY = "monad_private_key"
    ANTHROPIC_API_KEY = "anthropic_api_key"
    IC_IDENTITY_NAME = "ic_identity_name"
    KINIC_MEMORY_ID = "kinic_memory_id"
    MONAD_RPC_URL = "monad_rpc_url"


class CredentialManager:
    """Manages secure storage and retrieval of credentials using OS keyring."""

    def __init__(self, service_name: str = SERVICE_NAME):
        """
        Initialize the credential manager.

        Args:
            service_name: The service name to use in the keyring (default: "kinic-backend")
        """
        self.service_name = service_name
        logger.info(f"Initialized CredentialManager with service: {service_name}")

    def set_credential(self, key: CredentialKey, value: str) -> bool:
        """
        Store a credential securely in the OS keyring.

        Args:
            key: The credential key (from CredentialKey enum)
            value: The credential value to store

        Returns:
            True if successful, False otherwise
        """
        try:
            keyring.set_password(self.service_name, key.value, value)
            logger.info(f"Successfully stored credential: {key.value}")
            return True
        except Exception as e:
            logger.error(f"Failed to store credential {key.value}: {e}")
            return False

    def get_credential(self, key: CredentialKey, fallback_env_var: Optional[str] = None) -> Optional[str]:
        """
        Retrieve a credential from the OS keyring.

        Args:
            key: The credential key (from CredentialKey enum)
            fallback_env_var: Optional environment variable name to check if keyring fails

        Returns:
            The credential value if found, None otherwise
        """
        try:
            value = keyring.get_password(self.service_name, key.value)

            if value:
                logger.debug(f"Retrieved credential from keyring: {key.value}")
                return value

            # If not found in keyring and fallback is provided, try environment variable
            if fallback_env_var:
                import os
                env_value = os.getenv(fallback_env_var)
                if env_value:
                    logger.warning(
                        f"Credential {key.value} not in keyring, using environment variable {fallback_env_var}. "
                        f"Consider migrating to keyring for better security."
                    )
                    return env_value

            logger.warning(f"Credential not found: {key.value}")
            return None

        except Exception as e:
            logger.error(f"Failed to retrieve credential {key.value}: {e}")

            # Try fallback to environment variable on error
            if fallback_env_var:
                import os
                env_value = os.getenv(fallback_env_var)
                if env_value:
                    logger.warning(
                        f"Keyring error for {key.value}, falling back to environment variable {fallback_env_var}"
                    )
                    return env_value

            return None

    def delete_credential(self, key: CredentialKey) -> bool:
        """
        Delete a credential from the OS keyring.

        Args:
            key: The credential key (from CredentialKey enum)

        Returns:
            True if successful, False otherwise
        """
        try:
            keyring.delete_password(self.service_name, key.value)
            logger.info(f"Successfully deleted credential: {key.value}")
            return True
        except keyring.errors.PasswordDeleteError:
            logger.warning(f"Credential not found for deletion: {key.value}")
            return False
        except Exception as e:
            logger.error(f"Failed to delete credential {key.value}: {e}")
            return False

    def has_credential(self, key: CredentialKey) -> bool:
        """
        Check if a credential exists in the keyring.

        Args:
            key: The credential key (from CredentialKey enum)

        Returns:
            True if the credential exists, False otherwise
        """
        return self.get_credential(key) is not None

    def get_all_credentials(self) -> dict[str, Optional[str]]:
        """
        Retrieve all Kinic credentials from the keyring.

        Returns:
            Dictionary mapping credential keys to their values (None if not found)
        """
        credentials = {}
        for key in CredentialKey:
            credentials[key.value] = self.get_credential(key)
        return credentials

    def validate_required_credentials(self) -> tuple[bool, list[str]]:
        """
        Validate that all required credentials are present.

        Returns:
            Tuple of (all_present: bool, missing_keys: list[str])
        """
        required_keys = [
            CredentialKey.MONAD_PRIVATE_KEY,
            CredentialKey.ANTHROPIC_API_KEY,
            CredentialKey.IC_IDENTITY_NAME,
            CredentialKey.KINIC_MEMORY_ID,
            CredentialKey.MONAD_RPC_URL,
        ]

        missing = []
        for key in required_keys:
            if not self.has_credential(key):
                missing.append(key.value)

        all_present = len(missing) == 0
        return all_present, missing


# Global instance for easy access
_credential_manager = None


def get_credential_manager() -> CredentialManager:
    """
    Get the global credential manager instance.

    Returns:
        The global CredentialManager instance
    """
    global _credential_manager
    if _credential_manager is None:
        _credential_manager = CredentialManager()
    return _credential_manager
