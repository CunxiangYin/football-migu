"""Common schemas."""

from typing import Generic, TypeVar, List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )


class PaginationParams(BaseModel):
    """Pagination parameters."""
    
    page: int = Field(default=1, ge=1, description="Page number")
    per_page: int = Field(default=20, ge=1, le=100, description="Items per page")
    
    @property
    def offset(self) -> int:
        """Calculate offset for database query."""
        return (self.page - 1) * self.per_page


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""
    
    status: str = "success"
    data: List[T]
    pagination: dict
    metadata: Optional[dict] = None
    
    @classmethod
    def create(
        cls,
        data: List[T],
        page: int,
        per_page: int,
        total: int,
        **kwargs
    ) -> "PaginatedResponse[T]":
        """Create paginated response."""
        total_pages = (total + per_page - 1) // per_page
        
        return cls(
            data=data,
            pagination={
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            },
            metadata=kwargs.get("metadata", {
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0.0"
            })
        )


class SuccessResponse(BaseModel):
    """Standard success response."""
    
    status: str = "success"
    message: Optional[str] = None
    data: Optional[Any] = None
    metadata: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Standard error response."""
    
    status: str = "error"
    error: dict
    metadata: Optional[dict] = None
    
    @classmethod
    def create(
        cls,
        code: str,
        message: str,
        details: Optional[Any] = None,
        **kwargs
    ) -> "ErrorResponse":
        """Create error response."""
        return cls(
            error={
                "code": code,
                "message": message,
                "details": details
            },
            metadata=kwargs.get("metadata", {
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": kwargs.get("request_id")
            })
        )