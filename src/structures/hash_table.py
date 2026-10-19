class HashTable:
    def __init__(self, cap=1000):
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

    def get(self, key, default=None):
        id = self._hash(key)
        bucket = self.buckets[id]
        
        for kv in bucket:
            if kv[0] == key:
                return kv[1]
        return default

    def __len__(self):
        return self.size

    def __contains__(self, key):
        return self.contains(key)

    def __getitem__(self, key):
        val = self.get(key)
        if val is None and not self.contains(key):
            raise KeyError(f"Không tìm thấy key: {key}")
        return val

    def __setitem__(self, key, value):
        self.put(key, value)

    def contains(self, key):
        idx = self._hash(key)
        for kv in self.buckets[idx]:
            if kv[0] == key:
                return True
        return False    

    def remove(self, key):
        id = self._hash(key)
        bucket = self.buckets[id]

        for i, kv in enumerate(bucket):
            if kv[0] == key:
                bucket.pop(i)
                self.size -= 1
                return True
            
    def clear(self):
        self.buckets = [[] for _ in range(self.cap)]
        self.size = 0

    def __del__(self):
        self.clear()
        self.buckets = None
        self.size = 0

    def __str__(self):
        elements = []
        for bucket in self.buckets:
            for kv in bucket:
                elements.append(f"{repr(kv[0])}: {repr(kv[1])}")
        return "{" + ", ".join(elements) + "}"
