"""
Forbidden Error example for Spectacular
"""
forbidden = {
                "type": "object",
                "properties": {"detail": {"type": "string"}},
                "example": {"detail": "You do not have permission to perform this action."},
            }
