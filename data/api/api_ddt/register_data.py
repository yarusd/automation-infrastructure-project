
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
    ({**VALID_REGISTER, "password": 1225454, "password_confirmation": 1225454}, 
    201, {"message": "User registered successfully"}, "3 - only numbers in password"), 
    # negative: Name
    ({**VALID_REGISTER, "name": "n"}, 400, {"message": "at least 2"}, "4 - name too short"),
    ({**VALID_REGISTER, "name": "n" * 51}, 400, {"message": "less than or equal to 50"}, "5 - name too long"),
    ({**VALID_REGISTER, "name": 123}, 400, {"message": "must be a string"}, "6 - numbers in name"),
    ({**VALID_REGISTER, "name": "!@#$%"}, 400, {"message": "required"}, "7 - special chars in name"),

    # negative: Email
    ({**VALID_REGISTER, "email": "neomi.test.com"}, 400, {"message": "valid email"}, "8 - missing @"),
    ({**VALID_REGISTER, "email": "neomi.test.il"}, 400, {"message": "valid email"}, "9 - invalid TLD (.il)"),
    # Bug: Hebrew Email (xfail)
    pytest.param({**VALID_REGISTER, "email": "נעומי@test.com"}, 400, {"message": "valid email"}, "10 - heb creds in email",
                 marks=pytest.mark.xfail(reason="Bug: API accepts Hebrew in email")),

    # negative: Password
    ({**VALID_REGISTER, "password": "abc" * 20, "password_confirmation": "abc" * 20}, 
    400, {"message": "less than or equal to 50"}, "11 - password too long"),
    
    #  Bug: API accepts Only spaces
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