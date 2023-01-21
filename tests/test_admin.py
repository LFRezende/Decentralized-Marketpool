from brownie import accounts, network, Market
from scripts.deploy import signToConsume, buyProduct, submitGood, deployMarket
from scripts.utils import getAccount, getAddress


def test_admin_first():
    # arrange
    account = getAccount()
    account1 = getAccount(id=1)
    account2 = getAccount(id=2)
    # act
    market = deployMarket(id=0)
    market1 = deployMarket(id=1)
    market2 = deployMarket(id=2)
    # assert
    assert account == market.getConsumers()[0]
    assert account1 == market1.getConsumers()[0]
    assert account2 == market2.getConsumers()[0]


def test_correct_trade():
    # arrange
    market = deployMarket()
    seller = getAccount(id=1)
    buyer = getAccount(id=2)
    signToConsume(AccountId=1)
    signToConsume(AccountId=2)
    # act
    seller_wallet_i = seller.balance()
    buyer_wallet_i = buyer.balance()
    submitGood(10, "Joanne", AccountId=1)
    price = market.getProductETHPrice("Joanne")
    owner_i = market.getOwner("Joanne")
    buyProduct("Joanne", AccountId=2)
    owner_f = market.getOwner("Joanne")
    seller_wallet_f = seller.balance()
    buyer_wallet_f = buyer.balance()
    assert owner_i == getAccount(id=1)
    assert owner_f == getAccount(id=2)
    assert seller_wallet_f - seller_wallet_i == price
    assert buyer_wallet_i - buyer_wallet_f == price
    assert market.getOwner("Joanne") == owner_f


def test_resetting():
    # arrange
    account = getAccount()
    
