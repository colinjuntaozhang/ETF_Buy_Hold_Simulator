# ETF_Buy_Hold_Simulator



# Issues found===
1. rebalance mechanism has some significant flaws 
  1.1 like: we calculate portfolio on 2005-09-01, get $X amount. then rebalance on the next day 2005-09-02 end price
            which means we lost 1 day growth/loss. these is a gap, the gap is 1 day. 
  


