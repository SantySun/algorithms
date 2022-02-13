class Knapsack:

  @staticmethod
  def solution(profits, weights, capacity):
    assert len(weights) == len(profits)
    assert capacity >= 0
    assert all([w > 0 for w in weights])
    assert all([p > 0 for p in weights])

    dp = [[ 0 for _ in range(capacity + 1) ] for _ in range(len(weights) + 1) ]
    for i in range(1, len(weights) + 1):
      for j in range(1, capacity + 1):
        # not taking current object, with increased capacity for previous objects
        profit_1 = dp[i - 1][j]

        # taking current object, with decreased capacity for previous objects
        profit_2 = 0
        if weights[i - 1] <= j:
          profit_2 = dp[i - 1][j - weights[i - 1]] + profits[i - 1]
        dp[i][j] = max(profit_1, profit_2)

    return dp[-1][-1]
  
# Knapsack.solution([1, 6, 10, 16], [1, 2, 3, 5], 5)
# Knapsack.solution([1, 6, 10, 16], [1, 2, 3, 5], 6)
Knapsack.solution([1, 6, 10, 16], [1, 2, 3, 5], 7)