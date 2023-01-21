// SPDX-License-Identifier: MIT
pragma experimental ABIEncoderV2;
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

// Add SafeMath not necessary --> version 0.8.0
contract Market {
    //  -------- Initial Settings   --------
    struct good {
        address owner;
        uint256 EthPrice;
        uint256 USDPrice;
        string goodname;
    }
    AggregatorV3Interface priceFeed;
    good[] public listedgoods;
    address payable[] public consumers;
    enum STATUS {
        OFF,
        ON
    }

    //      --------    Mappings    ---------
    mapping(address => STATUS) internal isConsumer;
    mapping(address => uint256) internal OwnerIndex;
    mapping(string => uint256) internal ProductIndex;
    mapping(string => address) public ProductOwner;

    //      -------     Constructor --------
    constructor(address priceFeedAddress) {
        address payable admin;
        admin = payable(msg.sender);
        // Admin is the first consumers
        consumers.push(admin);
        // Already able to consume - no need to sign Up
        isConsumer[admin] = STATUS.ON;
        priceFeed = AggregatorV3Interface(priceFeedAddress);
        // Dummy product - for mapping purposes.
        good memory Dummy;
        Dummy.owner = admin;
        Dummy.EthPrice = 0;
        Dummy.USDPrice = 0;
        Dummy.goodname = "Dummy";
        listedgoods.push(Dummy); // This will have index 0 in the list.
    }

    //                      ------ Modifiers -------
    // Checks the consumer status. If not a member, orders to sign up.
    modifier notMember() {
        require(
            isConsumer[msg.sender] == STATUS.ON,
            "You need to sign up first!"
        );
        _;
    }
    // Checks if buyer is purchasing the product with the accorded price.
    modifier accordedPrice(string memory name) {
        require(
            ProductIndex[name] > 0,
            "This product doesn't exist in the market."
        );
        require(msg.sender != ProductOwner[name], "You already bought it!");
        require(
            msg.value >= listedgoods[ProductIndex[name]].EthPrice,
            "Not Enough ETH!"
        );
        require(
            msg.value <= listedgoods[ProductIndex[name]].EthPrice + 10**9,
            "Too much ETH!"
        );
        _;
    }
    // Checks if the sender is the owner of the contract.
    modifier isOwner(string memory name) {
        require(
            msg.sender == ProductOwner[name],
            "You can't do this - you don't own it."
        );
        _;
    }

    // Functions
    function signToConsume() public {
        require(
            isConsumer[msg.sender] == STATUS.OFF,
            "You are signed up already!"
        );
        isConsumer[msg.sender] = STATUS.ON;
        OwnerIndex[msg.sender] = consumers.length;
        consumers.push(payable(msg.sender));
    }

    // Amount of Dollars required to purchase One ETH
    function getETHPrice() public view returns (uint256) {
        (, int256 ethPrice, , , ) = priceFeed.latestRoundData();
        uint256 EthPrice = uint256(ethPrice) * 10**10;
        return EthPrice;
    }

    // Amount of ETHs purchasable with one dollar
    function getUSDETH() public view returns (uint256) {
        uint256 ethusd = getETHPrice();
        uint256 usdeth = ((10**18) * 10**18) / ethusd;
        return usdeth;
    }

    // Submitting a good to be sold
    function submitGood(uint256 _USDPrice, string memory _goodname)
        public
        notMember
        returns (good memory)
    {
        good memory product;
        product.goodname = _goodname;
        product.USDPrice = _USDPrice;
        product.EthPrice = _USDPrice * getUSDETH();
        product.owner = msg.sender;
        ProductOwner[_goodname] = product.owner;
        ProductIndex[_goodname] = listedgoods.length;
        listedgoods.push(product);
        return product;
    }

    // The buyProduct function stores the value in the contract, and then sends it to the seller.
    function buyProduct(string memory name)
        public
        payable
        notMember
        accordedPrice(name)
    {
        // After accorded Price check, the contract transfer the money to the seller.
        address payable seller = payable(ProductOwner[name]);
        seller.transfer(listedgoods[ProductIndex[name]].EthPrice);
        // Then, it transfers the ownership.
        listedgoods[ProductIndex[name]].owner = msg.sender;
        ProductOwner[name] = msg.sender;
    }

    function resetPrice(string memory name, uint256 newUSDprice)
        public
        isOwner(name)
    {
        listedgoods[ProductIndex[name]].USDPrice = newUSDprice;
        listedgoods[ProductIndex[name]].EthPrice = newUSDprice * getUSDETH();
    }

    function getProductUSDPrice(string memory name)
        public
        view
        returns (uint256)
    {
        require(
            ProductIndex[name] > 0,
            "This product doesn't exist in the market."
        );
        return listedgoods[ProductIndex[name]].USDPrice;
    }

    function getProductETHPrice(string memory name)
        public
        view
        returns (uint256)
    {
        require(
            ProductIndex[name] > 0,
            "This product doesn't exist in the market."
        );
        uint256 ProductETHPrice = getProductUSDPrice(name) * getUSDETH();
        return ProductETHPrice;
    }

    function getOwner(string memory name) public view returns (address) {
        return ProductOwner[name];
    }

    function getConsumers() public view returns (address payable[] memory) {
        return consumers;
    }
    // After all of this:
    // Reentrancy Attack
    // SafeMath attack
}
