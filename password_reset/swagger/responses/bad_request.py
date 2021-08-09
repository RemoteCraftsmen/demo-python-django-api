bad_request = {
                "type": "object",
                "properties": {"detail": {"type": "string"}},
                "example": {"errors": {"name": ["This field is required."]}},
            }
