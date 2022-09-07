# ETF_Buy_Hold_Simulator



# Issues found===
1. rebalance mechanism has some significant flaws 
  1.1 like: we calculate portfolio on 2005-09-01, get $X amount. then rebalance on the next day 2005-09-02 end price
            which means we lost 1 day growth/loss. these is a gap, the gap is 1 day. 
  1.2 so, the solutuion is rebalance the ETFs using the same day price as we calculate the portfolio value 
  
2. affecting parameters:
  2.1 rebalance strategy. eg: top 3 performing sector ETFs 
  2.2 rebalance frequency eg: every 3 months 
  2.3 SPY distribution for conservativeness  eg: 60% in SPY, and stick with this ratio 
  2.4 Alpha ETF distribution  eg: evenly distributed among top 3 ETFs
