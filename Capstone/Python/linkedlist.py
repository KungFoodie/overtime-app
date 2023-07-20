#   Name: William Sung
#   Description: CS493 Capstone
#                Linked List Code
from Capstone.Python import employee


class LinkedList:
    def __init__(self: employee.Employee):
        self.head = None
        self.tail = None
        self.node_count = 0

    def get_node_count(self):
        return self.node_count

    def insert(self, node: employee.Employee):
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

    def insert_order(self: employee.Employee, node: employee.Employee):
        if self.head is None:
            self.head = node
            self.tail = node
        elif self.head.get_hours() >= node.get_hours():
            node.next = self.head
            node.prev = None
            self.head.prev = node
            self.head = node
        else:
            curr: employee.Employee = self.head
            while curr.next is not None and curr.get_hours() < node.get_hours():
                curr = curr.next

            if curr.get_hours() < node.get_hours():
                self.tail = node
                curr.next = node
                node.prev = curr
            else:
                before = curr.prev
                before.next = node
                node.prev = before
                node.next = curr
                curr.prev = node
        self.node_count = self.node_count + 1

    def merge(self, a: employee.Employee, b: employee.Employee):
        merged = None

        if a is None:
            return b
        if b is None:
            return a

        if a.get_hours() <= b.get_hours():
            merged = a
            merged.next = self.merge(a.next, b)
        else:
            merged = b
            b.next = self.merge(a, b.next)
        return merged

    def merge_sort(self, first_half: employee.Employee):
        if first_half is None or first_half.next is None:
            return first_half

        middle = self.middle(first_half)
        second_half = middle.next

        middle.next = None

        left = self.merge_sort(first_half)
        right = self.merge_sort(second_half)

        sorted_list = self.merge(left, right)
        return sorted_list

    def sort(self):
        self.head = self.merge_sort(self.head)
        node = self.head
        while node is not None and node.next is not None:
            node.next.prev = node
            node = node.next
        self.tail = node

    def middle(self, head):
        if head is None:
            return head

        slow = head
        fast = head

        while fast.next is not None and fast.next.next is not None:
            slow = slow.next
            fast = fast.next.next

        return slow

    def print(self):
        node = self.head
        while node is not None:
            print(node)
            node = node.next

    def search(self, empid):
        node: employee.Employee = self.head
        while node is not None:
            if node.get_empid() == empid:
                return node
            node = node.next

        return None

    def delete(self, empid):
        node: employee.Employee = self.head
        while node is not None:
            if node.get_empid() == empid:
                temp = node.next
                node.prev.next = temp
                temp.prev = node.prev
                return True
            node = node.next
        return None
