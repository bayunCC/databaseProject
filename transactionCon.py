# 定义事务类
class Transaction:
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def execute(self):
        # 模拟事务执行
        print("执行事务，时间戳：", self.timestamp)

# 初始化事务列表的时间戳
timestamps = [10, 5, 8, 3]
transactions = []

# 创建事务对象并按时间戳顺序排序
for timestamp in timestamps:
    transactions.append(Transaction(timestamp))
transactions.sort(key=lambda x: x.timestamp)

# 执行事务并输出时间戳变化
current_timestamp = 0
for transaction in transactions:
    if transaction.timestamp > current_timestamp:
        current_timestamp = transaction.timestamp
    else:
        current_timestamp += 1
    transaction.execute()
    print("时间戳变化：", current_timestamp)
