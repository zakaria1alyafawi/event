import logging
from passlib.context import CryptContext

logger = logging.getLogger("api.utils.encryption")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordHasher:
    """
    Secure password hashing using bcrypt.
    """
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plaintext password.
        
        Args:
            password (str): Plaintext password.
            
        Returns:
            str: Hashed password.
            
        Raises:
            ValueError: If password is empty.
        """
        if not isinstance(password, str) or not password:
            logger.error("Invalid or empty password")
            raise ValueError("Password must be a non-empty string")
        
        hashed = pwd_context.hash(password)
        logger.debug("Password hashed successfully")
        return hashed
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify plaintext against hashed password.
        
        Args:
            plain_password (str): Plaintext password.
            hashed_password (str): Stored hash.
            
        Returns:
            bool: True if match.
        """
        return pwd_context.verify(plain_password, hashed_password)