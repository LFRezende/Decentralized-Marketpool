from brownie import accounts, network, config, MockV3Aggregator

LOCAL_BLOCKCHAINS = ["development"]
FORKED_CHAINS = ["mainnet-fork"]

DECIMALS = 8
INITIAL_VALUE = 2000 * 10**10


def getAccount(id=None):
    if id:
        return accounts[id]
    if (
        network.show_active() in LOCAL_BLOCKCHAINS
        or network.show_active() in FORKED_CHAINS
    ):
        account = accounts[0]
    else:
        account = accounts.add(config["wallets"]["from_key"])
    return account


def getAddress():
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        return config["networks"][network.show_active()]["priceFeedAddress"]
    else:
        if len(MockV3Aggregator) <= 0:
            deploy_mocks()
        mock = MockV3Aggregator[-1]
        return mock.address


def deploy_mocks():
    account = getAccount()
    mock = MockV3Aggregator.deploy(DECIMALS, INITIAL_VALUE, {"from": account})
    print("\n\n --- MockV3Aggregator deployed! ---\n\n")
    return mock


def checkName():
    while True:
            _name = (
                str(
                    input(
                        "Type the name of the product you wish to submit into the Marketpool."
                    )
                )
                .strip()
                .upper()
            )
            option = (
                str(input(f"Is the name {_name} correct? [Y/N]")).strip().upper()[0]
            )
            if option in "YN":
                if option == "Y":
                    break
            else:
                print(f"Invalid option. Please, try again!")
    return _name


def checkPrice(_name):
    while True:
            _USDprice = int(input(f"Type the price of the product {_name}, in USD."))
            if _USDprice > 0:
                break
            else:
                print("The price in USD must be greater than 0. Please, try again.")
    return _USDprice