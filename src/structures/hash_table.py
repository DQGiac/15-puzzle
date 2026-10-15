class HashTable:
    def __init__(self, cap=100):
        self.cap = cap 
        self.size = 0            
        self.buckets = [[] for _ in range(cap)]

    def _hash(self, key):
        return hash(key) % self.cap

    def put(self, key, value):
        id = self._hash(key)
        bucket = self.buckets[id]
        
        for i, kv in enumerate(bucket):
            if kv[0] == key:
                bucket[i] = (key, value)
                return
                
        bucket.append((key, value))
        self.size += 1

    def get(self, key):
        id = self._hash(key)
        bucket = self.buckets[id]
        
        for kv in bucket:
            if kv[0] == key:
                return kv[1]
                
        raise KeyError(f"Không tìm thấy key: {key}")

    def remove(self, key):
        id = self._hash(key)
        bucket = self.buckets[id]

        for i, kv in enumerate(bucket):
            if kv[0] == key:
                bucket.pop(i)
                self.size -= 1
                return True
                
        raise KeyError(f"Không tìm thấy key để xóa: {key}")

    def __str__(self):
        elements = []
        for bucket in self.buckets:
            for kv in bucket:
                elements.append(f"{repr(kv[0])}: {repr(kv[1])}")
        return "{" + ", ".join(elements) + "}"
