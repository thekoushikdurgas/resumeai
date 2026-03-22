"""Custom exceptions for Resume AI API."""


class ResumeAIException(Exception):
    """Base exception."""

    pass


class ResumeNotFoundError(ResumeAIException):
    """Resume document not found."""

    pass


class InvalidResumeIDError(ResumeAIException):
    """Invalid resume id format."""

    pass


class AIServiceError(ResumeAIException):
    """Upstream AI provider failure."""

    pass


class ValidationError(ResumeAIException):
    """Request validation failed."""

    pass


class AuthenticationError(ResumeAIException):
    """API key or auth failure."""

    pass


class DatabaseError(ResumeAIException):
    """Database operation failed."""

    pass


class ResumeStorageError(ResumeAIException):
    """s3storage / resume object persistence failed."""

    pass
