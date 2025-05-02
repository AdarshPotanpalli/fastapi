import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

# to avoid initalizing a variable multiple number of times
@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

#for multiple tests on a testing function
@pytest.mark.parametrize("num1, num2, expected", [
    (4,6,10),
    (5,7,12),
    (8,9,17)
])
def test_add(num1, num2, expected):
    print("Lets do some testing")
    assert add(3,5) == 8
    
def test_subtract():
    assert subtract(7,5) == 2
    
def test_multiply():
    assert multiply(7,5) == 35
    
# the functions should be descriptive    
def test_set_initial_amount(bank_account):
    assert bank_account.balance == 50
    
def test_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0
    
def test_withdraw_amount(bank_account):
    bank_account.withdraw(40)
    assert bank_account.balance == 10
    
def test_deposit_amount(bank_account):
    bank_account.deposit(50)
    assert bank_account.balance == 100

def test_interest_collected(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,6) == 55


@pytest.mark.parametrize("deposited, withdrawl, expected", [
    (100,30,70),
    (1200,90,1110),
    (80, 5, 75)
])    
def test_bank_transaction(zero_bank_account, deposited, withdrawl, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawl)
    assert zero_bank_account.balance == expected
    
# testing if exception is being raised properly
def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)