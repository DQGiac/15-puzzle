class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        if self.is_empty():
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        min_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        
        return min_item

    def is_empty(self):
        return len(self.heap) == 0

    def _sift_up(self, id):
        pId = (id - 1) // 2

        while id > 0 and self.heap[id] < self.heap[pId]:
            self.heap[id], self.heap[pId] = self.heap[pId], self.heap[id]
            id = pId
            pId = (id - 1) // 2

    def _sift_down(self, id):
        n = len(self.heap)
        while True:
            l = 2 * id + 1
            r = 2 * id + 2
            smallest = id

            if l < n and self.heap[l] < self.heap[smallest]:
                smallest = l
            if r < n and self.heap[r] < self.heap[smallest]:
                smallest = r

            if smallest != id:
                self.heap[id], self.heap[smallest] = self.heap[smallest], self.heap[id]
                id = smallest
            else:
                break