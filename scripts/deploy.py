from brownie import Market, network
from scripts.utils import (
    getAccount,
    getAddress,
    checkName,
    checkPrice,
    LOCAL_BLOCKCHAINS,
    FORKED_CHAINS,
)


def deployMarket(id=None):
    """
    deployMarket grabs an account and an address for a Price Feed to the deployment of a Smart Contract
    """
    if id:
        account = getAccount(id)
    else:
        account = getAccount()
    priceFeedAddress = getAddress()
    market = Market.deploy(priceFeedAddress, {"from": account})
    print("\n\n>>>>>>   Market Contract Deployed!  <<<<<<<")
    return market


def signToConsume(AccountId=None):
    """
    All participants must sign before consuming/selling
    """
    account = getAccount(AccountId)
    market = Market[-1]
    tx = market.signToConsume({"from": account})
    tx.wait(1)
    return tx


def buyProduct(name, AccountId):
    """
    After signed, the member is permitted to purchase whatever is available in the market pool.
    It checks the 
    """
    if AccountId:
        account = getAccount(AccountId)
    else:
        account = getAccount()
    market = Market[-1]

    if name:
        _name = name
    else:
        _name = (
            str(input("Type the name of the product you wish to purchase:"))
            .strip()
            .upper()
        )
    old_owner = market.getOwner(_name)
    tx = market.buyProduct(
        _name, {"from": account, "value": market.getProductETHPrice(_name)}
    )
    tx.wait(1)
    print(
        f'\n>>>>>>> "{_name}" bought for U$ {market.getProductUSDPrice(_name):.2f}.\n>>> Buyer: {account}.\n>>> Seller: {old_owner}.\n'
    )
    return tx


def submitGood(USDprice=None, name=None, AccountId=None):
    if AccountId:
        account = getAccount(AccountId)
    else:
        account = getAccount()
    market = Market[-1]
    if name:
        _name = name
    else:
        _name = checkName()
    if USDprice:
        _USDprice = USDprice
    else:
        checkPrice(_name)
    print(
        f"\n>>> Submitting {_name} for the price of U$ {_USDprice:.2f}.\nOwner:{account}.<<<"
    )
    tx = market.submitGood(_USDprice, _name, {"from": account})
    tx.wait(1)
    return tx


def getOwner(name):
    market = Market[-1]
    print(f">>>    Owner of {name} is {market.getOwner(name)}. <<<")
    return market.getOwner(name)


def main():
    deployMarket()
    submitGood(5, "TestCoin")
    signToConsume(AccountId=1)
    submitGood(10, "MarWag", AccountId=1)
    signToConsume(AccountId=2)
    submitGood(20, "Joanne", AccountId=2)
    submitGood(15, "SecondCoin")
    getOwner("Joanne")
    buyProduct("Joanne", AccountId=1)
    getOwner("Joanne")
