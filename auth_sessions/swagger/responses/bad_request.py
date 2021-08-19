bad_request = {
    "type": "object",
    "properties": {"detail": {"type": "string"}},
    "example": {
        "password": ["This field is required."],
        "password_confirm": ["This field is required."],
        "email": ["This field must be unique."],
    },
}
