class cursed_list(list):
    def __getitem__(self, key):
        if isinstance(key,slice):
            start, stop, step = key.start, key.stop, key.step
            if start is None:
                start = 0
            if stop is None:
                stop = len(self)-1
            if step is None:
                step = 1
            
            # case: standard slice
            if type(start) == type(stop) == type(step) == int:
                return super(cursed_list, self).__getitem__(key)
            
            # handle looping around
            if start<0:
                start = len(self) + start
            if stop<0:
                stop = len(self) + stop
            
            # case: floating point slice, -ve step
            if step<0:
                return cursed_list(reversed(self))[-start-1:-stop-1:-step]

            else:
                sliced_list = cursed_list()
                for i in range(int(((stop-start)/step)//1)):
                    sliced_list.append(self.__getitem__(start +i*step))
                return sliced_list
        elif type(key) in (int,float):
            if -len(self)<=key<=len(self)-1:
                # handle standard
                if isinstance(key,int):
                    return super(cursed_list, self).__getitem__(key)

                # handle floats
                elif isinstance(key,float):
                    lower = int(key//1)
                    upper = int(key//1 + 1)
                    lower_val = super(cursed_list, self).__getitem__(lower)
                    upper_val = super(cursed_list, self).__getitem__(upper)
                    if not {type(lower_val),type(upper_val)}.issubset({int,float,complex}):
                        raise TypeError("cursed_list only supports non-integer indices for numeric elements")
                    weight_upper = key - lower
                    weight_lower = upper - key
                    lower_contrib = weight_lower * lower_val
                    upper_contrib = weight_upper * upper_val
                    return lower_contrib + upper_contrib
                    
                else:
                    raise TypeError(f"cursed_list indices must be integers or floats, received {type(key)}")

            else:
                raise IndexError("cursed_list index out of range")
        
        else:
            raise TypeError(f"cursed list only accepts int or float indices, or slices, received {type(key)}")

    def __setitem__(self, key, val):
        if type(key) not in (int,slice):
            raise TypeError("""
            cursed_list only supports assignment to 
            integer indices and integer slices""")
        if type(key) is slice:
            start, stop, step = key.start, key.stop, key.step
            if start is None:
                start = 0
            if stop is None:
                stop = len(self)-1
            if step is None:
                step = 1
            if not (type(start) == type(start) == type(step) == int):
                raise TypeError("cursed_list only supports assignment to integer\nindices and integer slices")
        return super(cursed_list, self).__setitem__(key,val)