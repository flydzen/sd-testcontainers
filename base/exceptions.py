from fastapi import HTTPException


class CompanyNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="CompanyNotFoundError")


class NotEnoughSharesError(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="NotEnoughSharesError")


class NegativeSharesError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="NegativeSharesError")


class NotEnoughMoneyError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="NotEnoughMoneyError")


class InteractionError(HTTPException):
    def __init__(self, status, method, detail):
        super().__init__(status_code=status, detail=f"InteractionError in {method}: {detail}")
