LOGIN_SCENARIOUS = [
    # --- Positive Scenarios ---
    ({"email": "user1@test.com", "password": "123456"}, 200, {'role': 'user'}, "1 - user 1 login "),
    ({"email": "user2@test.com", "password": 123456}, 200, {'role': 'user'}, "2 - user 2 login "), # בדיקת ה"גם וגם"
    ({"email": "admin@test.com", "password": "admin123"}, 200, {'role': 'admin'}, "3 - admin login"),

    # --- Negative Scenarios: ---
    ({"email": "locked@test.com", "password": 123456}, 403, {'message': 'is locked'}, "4 - locked login"),
    ({"email": "user1@test.com"}, 400, {'message': 'required'}, "5 - missing password field"),
    ({"email": "", "password": "123456"}, 400, {'message': 'empty'}, "6 - empty email"),
    ({"email": "user1@test.com", "password": 12345}, 400, {'message': 'must be '}, "7 - password too short (5 chars)"), # Boundary Test!
    ({"email": "user1@test.com", "password": "a" * 51}, 400, {'message': 'less than or equal to 50'}, "8 - password too long (51 chars)"),

    ({"email": "user1@test.com", "password": "wrongpassword"}, 401, {'message': 'Invalid email or password.'}, "9 - wrong password"),
    ({"email": "nonexistent@test.com", "password": "123456"}, 401, {'message': 'Invalid email or password.'}, "10 - user not found"),
]