# 定义缓冲区大小
BUFFER_SIZE = 5

# 模拟磁盘上的元组数据
disk_data = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10]

# 用于存储结果的缓冲区
buffer = []

# 读取数据块的函数
def read_data_block(start_index, end_index):
    return disk_data[start_index:end_index]

# 写入数据块的函数
def write_data_block(data):
    buffer.extend(data)

# 进行交集运算的函数
def intersection():
    # 对磁盘数据进行分块处理
    num_blocks = len(disk_data) // BUFFER_SIZE
    if len(disk_data) % BUFFER_SIZE != 0:
        num_blocks += 1

    # 逐个处理每个数据块
    for i in range(num_blocks):
        start_index = i * BUFFER_SIZE
        end_index = (i + 1) * BUFFER_SIZE

        # 读取数据块到缓冲区
        block_data = read_data_block(start_index, end_index)
        buffer.extend(block_data)

        # 对缓冲区中的数据进行交集运算
        result = [num for num in buffer if num in block_data]

        # 清空缓冲区
        buffer.clear()

        # 将结果写回磁盘
        write_data_block(result)

# 进行并集运算的函数
def union():
    # 对磁盘数据进行分块处理
    num_blocks = len(disk_data) // BUFFER_SIZE
    if len(disk_data) % BUFFER_SIZE != 0:
        num_blocks += 1

    # 逐个处理每个数据块
    for i in range(num_blocks):
        start_index = i * BUFFER_SIZE
        end_index = (i + 1) * BUFFER_SIZE

        # 读取数据块到缓冲区
        block_data = read_data_block(start_index, end_index)
        buffer.extend(block_data)

        # 对缓冲区中的数据进行并集运算
        result = list(set(buffer).union(block_data))

        # 清空缓冲区
        buffer.clear()

        # 将结果写回磁盘
        write_data_block(result)

# 执行交集运算
intersection()

# 执行并集运算
union_result = buffer.copy()
union()

# 输出结果
print("交集结果：", buffer)
print("并集结果：", union_result)
