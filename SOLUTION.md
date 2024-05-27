## Design Approach:
I started with loading the json files. next I iterated over them and in a batch of 32 or less, started adding them to my blocks

## Implementation Details:
I created a class block which will be used to create all the required blocks.
I used few lists to keep track of transaction data and txid's
I then used for loops to iterate over these txid's and form my merkel root.
then I use this and other required info to create a block
Here I also print all the necessary things.

## Results and Performance: 
I was able to get my block header in the required format

Also able to print the txid's in the way it was asked to.
I didn't format my coin based transactions in the required way since the given files had none of them.

## Conclusion: 
It was a great experience in developing this simplistic blockchain. Did face a lot of issue but overcame them with time.

If I would understand what to do with the info in these json files, those things could be implemented in it.

Reference:
https://www.geeksforgeeks.org/implementing-the-proof-of-work-algorithm-in-python-for-blockchain-mining/
