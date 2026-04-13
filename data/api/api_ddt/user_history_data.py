
USER_ORDER_HISTORY = [
    # POSITIVE :
    (1, 1, 200, "1 - Matching IDs: Success"),
    # NEGATIVE :
    (1, 2, 403, "2 - Different IDs: blocked"),
    (0, 1, 403, "3 - Different IDs: blocked by priority"),
    (0, 0, 200, "4 - Matching IDs - Empty History")
]