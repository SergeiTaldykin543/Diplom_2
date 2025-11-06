class ExpectedResponses:
    # Сообщения об ошибках
    USER_ALREADY_EXISTS = "User already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"
    INCORRECT_CREDENTIALS = "email or password are incorrect"
    NOT_AUTHORIZED = "You should be authorised"
    INGREDIENTS_REQUIRED = "Ingredient ids must be provided"
    
    # Успешные сообщения
    SUCCESSFUL_LOGOUT = "Successful logout"
    RESET_EMAIL_SENT = "Reset email sent"
    PASSWORD_RESET = "Password successfully reset"