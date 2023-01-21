# Decentralized Consumer Pool.

The concept of the project is to be an open marketplace where users can submit goods and their respective prices in both ETH and USD for a consumer to avail and purchase.

The actions of the project envelop the following:

- Buyer/Seller:
1. Sign to Consume: The member needs to be enrolled with the pool in order to sell or buy from the market pool
2. Submit Good: An enrolled member may submit a product to the pool, setting up its price and name. The good is pushed into a list of products whose structure registers the ownership, the price in USD, the price in ETH and the name of it.
3. Buy Product: An enrolled member may purchase a product in the pool, as long as it has been added by some other member. The purchase allows only precise payments, to avoid fund losts.
4. Reset Price: A member who submitted its product into the pool may reconsider its price - therefore, there is a function that allows so. It is valid to remember that this function will inherit a modifier, to check whether the call has been made by the owner of the product or not.

- Project Attributes

This project has been developed via Brownie, in order to automize testing and debugging in a forked environment in Ganache, provided by an Alchemy URL, as well as in development chains native to Ganache. 
Therefore, this GitHub repo will contain the MockV3Aggregator for the AggregatorV3Interface for local chains, as well as a Price Feed Address for the Mainnet Fork. 
The testing utilizing testnets such as Goerli has been mostly done in interactive testing via Remix IDE, so files for brownie testing are still under development. Not to mention, some scaling for this project is still required for working with Testnets.


