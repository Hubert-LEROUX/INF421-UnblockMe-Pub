"""
This document contains the implementation of a hash table and a set to store visited states.
"""



class My_hash_table:
    """
    Hash table implementation to store the visited states
    
    keys and values are game_states (dict with attributes "cars")
    """
    @staticmethod
    def fast_exp_mod(base, exp, mod):
        """
        Compute (base^exp) % mod using fast exponentiation
        :param base: the base
        :param exp: the exponent
        :param mod: the modulus
        :return: (base^exp) % mod
        """
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:  # If exp is odd, multiply base with result
                result = (result * base) % mod
            exp = exp >> 1  # Divide exp by 2
            base = (base * base) % mod  # Square the base
        return result



    @staticmethod
    def generate_primes(n):
        """
        Generate the first n prime numbers.
        
        :param n: int, the number of prime numbers to generate
        :return: list, the first n prime numbers
        """
        primes = []
        i = 2
        while len(primes) < n:
            is_prime = True
            for p in primes:
                if i % p == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(i)
            i += 1
        return primes
    
    def __init__(self, nb_cars=10, size=1000003):
        """
        Initialize the hash table.
        
        :param nb_cars: int, the number of cars in the game
        :param size: int, the size of the hash table
        """
        self.size = size
        self.nb_items = 0
        self.max_items_in_one_bucket = 0
        self.primes = My_hash_table.generate_primes(nb_cars)
        self.table = [None for _ in range(size)]

    def __len__(self):
        """
        Get the number of items in the hash table.
        
        :return: int, the number of items in the hash table
        """
        return self.nb_items
    
    def hash(self, key):
        """
        Compute the hash value for a given key.
        
        :param key: dict, the game state
        :return: int, the hash value
        """
        from tools import distance_top_left
        h = 1
        for car in key["cars"]:
            d = distance_top_left(car)
            h = (h * My_hash_table.fast_exp_mod(self.primes[car["id_car"]-1], d+1, self.size)) % self.size
        return h
    
    def get(self, key):
        """
        Get the value associated with a given key.
        
        :param key: dict, the game state
        :return: dict or None, the value associated with the key or None if the key is not found
        """
        h = self.hash(key)
        if self.table[h] is None:
            return None
        for k, v in self.table[h]:
            if key == k:
                return v
        return None
    
    def add(self, key, value):
        """
        Add a key-value pair to the hash table.
        
        :param key: dict, the game state
        :param value: dict, the value to associate with the key
        """
        h = self.hash(key)
        if self.table[h] is None:
            self.table[h] = [(key, value)]
        else:
            self.table[h].append((key, value))
        self.max_items_in_one_bucket = max(self.max_items_in_one_bucket, len(self.table[h]))
        self.nb_items += 1
    
    def contains(self, key):
        """
        Check if a key is in the hash table.
        
        :param key: dict, the game state
        :return: bool, True if the key is in the hash table, False otherwise
        """
        h = self.hash(key)
        if self.table[h] is None:
            return False
        for k, _ in self.table[h]:
            if key["cars"] == k["cars"]:
                return True
        return False
    
    def show_table(self):
        """
        Display the contents of the hash table.
        """
        for data in self.table:
            if data is not None:
                print(data)

class My_set(My_hash_table):
    """
    A set implementation based on My_hash_table to store unique game states.
    Inherits from My_hash_table and overrides the add method to store only keys.
    """
    def add(self, key):
        """
        Add a key to the set.
         
        :param key: dict, the game state to add
        """
        super().add(key, None)


