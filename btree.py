class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.child = []


class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)  # 创建一个叶节点作为根节点
        self.t = t  # B树的阶数

    def insert(self, k):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            # 根节点已满，需要进行分裂操作
            temp = BTreeNode()
            self.root = temp
            temp.child.insert(0, root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)

    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            # 如果当前节点是叶节点，直接插入键值
            x.keys.append(k)
            x.keys.sort()  # 每次插入后需要对键值进行排序
        else:
            # 找到合适的子节点进行递归插入
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                # 子节点已满，进行分裂操作
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self.insert_non_full(x.child[i], k)

    def split_child(self, x, i):
        t = self.t
        y = x.child[i]
        z = BTreeNode(y.leaf)
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.child = y.child[t: 2 * t]
            y.child = y.child[0: t - 1]

    def delete(self, k):
        root = self.root
        self.delete_key(root, k)
        if len(root.keys) == 0:
            self.root = root.child[0]

    def delete_key(self, x, k):
        t = self.t
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
        if x.leaf:
            if i < len(x.keys) and x.keys[i] == k:
                # 键值在叶节点中，直接删除
                x.keys.pop(i)
                return
            return
        if i < len(x.keys) and x.keys[i] == k:
            # 键值在内部节点中，继续递归删除
            return self.delete_internal_node(x, k, i)
        elif len(x.child[i].keys) >= t:
            # 子节点包含足够的键值，递归删除
            self.delete_key(x.child[i], k)
        else:
            if i != 0 and i + 2 < len(x.child):
                # 从前一个子节点借一个键值
                if len(x.child[i - 1].keys) >= t:
                    self.borrow_from_prev(x, i)
                # 从后一个子节点借一个键值
                elif len(x.child[i + 1].keys) >= t:
                    self.borrow_from_next(x, i)
                else:
                    # 前后子节点均无法借键值，合并子节点
                    self.merge(x, i)
            elif i == 0:
                # 从后一个子节点借一个键值
                if len(x.child[i + 1].keys) >= t:
                    self.borrow_from_next(x, i)
                else:
                    # 合并子节点
                    self.merge(x, i)
            elif i + 1 == len(x.child):
                # 从前一个子节点借一个键值
                if len(x.child[i - 1].keys) >= t:
                    self.borrow_from_prev(x, i)
                else:
                    # 合并子节点
                    self.merge(x, i - 1)
            self.delete_key(x.child[i], k)

    def delete_internal_node(self, x, k, i):
        t = self.t
        if x.leaf:
            if x.keys[i] == k:
                x.keys.pop(i)
                return
            return
        if len(x.child[i].keys) >= t:
            # 用前驱键值替代要删除的键值，并递归删除前驱键值
            x.keys[i] = self.find_predecessor(x.child[i])
            self.delete_key(x.child[i], x.keys[i])
        elif len(x.child[i + 1].keys) >= t:
            # 用后继键值替代要删除的键值，并递归删除后继键值
            x.keys[i] = self.find_successor(x.child[i + 1])
            self.delete_key(x.child[i + 1], x.keys[i])
        else:
            # 前驱和后继子节点均无法借键值，合并子节点
            self.merge(x, i)
            self.delete_key(x.child[i], k)

    def find_predecessor(self, x):
        if x.leaf:
            return x.keys[-1]
        return self.find_predecessor(x.child[-1])

    def find_successor(self, x):
        if x.leaf:
            return x.keys[0]
        return self.find_successor(x.child[0])

    def borrow_from_prev(self, x, i):
        child = x.child
        child[i].keys.insert(0, x.keys[i - 1])
        x.keys[i - 1] = child[i - 1].keys[-1]
        if not child[i].leaf:
            child[i].child.insert(0, child[i - 1].child[-1])
            child[i - 1].child.pop()
        child[i - 1].keys.pop()

    def borrow_from_next(self, x, i):
        child = x.child
        child[i].keys.append(x.keys[i])
        x.keys[i] = child[i + 1].keys[0]
        if not child[i].leaf:
            child[i].child.append(child[i + 1].child[0])
            child[i + 1].child.pop(0)
        child[i + 1].keys.pop(0)

    def merge(self, x, i):
        child = x.child
        c1 = child[i]
        c2 = child[i + 1]
        c1.keys.append(x.keys[i])
        c1.keys.extend(c2.keys)
        if not c1.leaf:
            c1.child.extend(c2.child)
        x.keys.pop(i)
        x.child.remove(c2)

    def search(self, k, x=None):
        if x is not None:
            i = 0
            while i < len(x.keys) and k > x.keys[i]:
                i += 1
            if i < len(x.keys) and x.keys[i] == k:
                return True
            elif x.leaf:
                return False
            else:
                return self.search(k, x.child[i])
        else:
            return self.search(k, self.root)

    def print_btree(self):
        self.print_recursive(self.root, "")

    def print_recursive(self, x, prefix):
        print(prefix + str(x.keys))
        if not x.leaf:
            for i in range(len(x.child)):
                self.print_recursive(x.child[i], prefix + "  ")


# 测试代码
btree = BTree(3)  # 创建一个t=3的B树

# 插入操作
btree.insert(8)
btree.insert(12)
btree.insert(18)
btree.insert(6)
btree.insert(9)
btree.insert(15)
btree.insert(21)
btree.insert(17)

# 打印B树结构
print("B树结构:")
btree.print_btree()

# 搜索操作
print("搜索键值 6:", btree.search(6))  # 输出: True
print("搜索键值 10:", btree.search(10))  # 输出: False

# 删除操作
btree.delete(15)
print("删除键值 15")
print("搜索键值 15:", btree.search(15))  # 输出: False

# 打印B树结构
print("删除后的B树结构:")
btree.print_btree()
