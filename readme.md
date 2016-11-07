# BitCoin Trading
## Strategy
### Strategy Class
#### Class Variables
__bitcoin__ - BitCoin class object for holding and analyzing the data. 
__short_flag__ - this will tell us if we are looking to short or buy bitcoin
__open_price__ - this is the price at which we bought or shorted
__close_price__ - this is the price that we are looking to close the transaction. 
#### Class Functions
##### init
1. Initialize the bitcoin object and the current_interval object.
2. Call __run__ method
#### run
1. Check if __current_interval__ is more than a minute past:
    * _True_ - sleep until minute past.
    * _False_ - run __update_interval__ 
2. If __update_interval__ returns a transaction value:
    * _True_ - set the buy/short price and the correponding sell/buy price. 
    * _False_ - sleep for another minute
    
