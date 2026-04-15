
import pytest

VALID_REGISTER = {
    "name": "Neomi Levi",
    "email": "neomi@test.com",
    "password": "securepass123",
    "password_confirmation": "securepass123"
}

REGISTER_SCENARIOUS = [
    # positive
    ({**VALID_REGISTER}, 201, {"message": "User registered successfully"}, "1 - valid register"),
    ({**VALID_REGISTER, "password": "helloooo", "password_confirmation": "helloooo"}, 
    201, {"message": "User registered successfully"}, "2 - alpha only password"),

    # negative: Name
    ({**VALID_REGISTER, "name": "n"}, 400, {"message": "at least 2"}, "3 - name too short"),
    ({**VALID_REGISTER, "name": "n" * 41}, 400, {"message": "less than or equal to 40"}, "4 - name too long"),
    ({**VALID_REGISTER, "name": 123}, 400, {"message": "must be a string"}, "5 - numbers in name"),
    ({**VALID_REGISTER, "name": "!@#$%"}, 400, {"message": "required"}, "6 - special chars in name"),

    # negative: Email
    ({**VALID_REGISTER, "email": "neomi.test.com"}, 400, {"message": "valid email"}, "7 - missing @"),
    ({**VALID_REGISTER, "email": "neomi.test.il"}, 400, {"message": "valid email"}, "8 - invalid TLD (.il)"),
    # Bug: Hebrew Email (xfail)
    pytest.param({**VALID_REGISTER, "email": "נעומי@test.com"}, 400, {"message": "valid email"}, "9 - heb creds in email",
                 marks=pytest.mark.xfail(reason="Bug: API accepts Hebrew in email")),

    # negative: Password
    ({**VALID_REGISTER, "password": 1225454, "password_confirmation": 1225454}, 
    400, {"message": "must be a string"}, "10 - only numbers in password"), 
    ({**VALID_REGISTER, "password": "abc" * 20, "password_confirmation": "abc" * 20}, 
    400, {"message": "less than or equal to 50"}, "11 - password too long"),
    
    #  Bug: Only spaces
    pytest.param({**VALID_REGISTER, "password": " " * 8, "password_confirmation": " " * 8}, 
                400, {'error': 'Validation Failed'}, "12 - password with spaces",
                marks=pytest.mark.xfail(reason="Bug: API accepts Spaces instead of chars")),

    # negative: Mismatch & Missing
    ({**VALID_REGISTER, "password_confirmation": "different123"}, 400, {'error': 'Validation Failed'}, "13 - password mismatch"),
    ({**VALID_REGISTER, "password_confirmation": ""}, 400, {'error': 'Validation Failed'}, "14 - empty confirmation pass"),
    ({ "name": "Neomi Levi",
    "password": "securepass123","password_confirmation": "securepass123"},
    400, {"message": "is required"}, "15 - missing email field")

]