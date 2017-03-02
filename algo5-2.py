#!/usr/bin python
import math
import random
 
 
x = "the road not taken by robert frost two roads diverged in a yellow wood, and sorry i could not travel both and be one traveler, long i stood and looked down one as far as i could to where it bent in the undergrowth; then took the other, as just as fair, and having perhaps the better claim, because it was grassy and wanted wear; though as for that the passing there had worn them really about the same, and both that morning equally lay in leaves no step had trodden black. oh, i kept the first for another day! yet knowing how way leads on to way, i doubted if i should ever come back. i shall be telling this with a sigh somewhere ages and ages hence: two roads diverged in a wood, and i- i took the one less traveled by, and that has made all the difference."
 
 
class MinHeap:
    heap = []
 
    def __init__(self, freq_symbol_list):
        for i in range(0, len(freq_symbol_list)):
            self.insert_element(freq_symbol_list[i])
 
    def get_children_index(self, index):
        if (2*index) + 1 >= len(self.heap):
            left_index = -1
            right_index = -1
        elif (2*index) + 2 >= len(self.heap):
            left_index = 2*index + 1
            right_index = -1
        else:
            left_index = 2*index + 1
            right_index = 2*index + 2
        return left_index, right_index
 
 
    def get_parent(self, index):
        return self.heap[(index - 1)/2]
 
    def get_parent_index(self, index):
        return int((index - 1)/2)
 
    def insert_element(self, freq_symbol):
        new_index = len(self.heap)
        self.heap.append(freq_symbol)
        parent_index = self.get_parent_index(new_index)
 
        while self.heap[parent_index][0] >= freq_symbol[0] and parent_index >= 0:
            if self.heap[parent_index][0] == freq_symbol[0] and random.random() > .5:
                break
 
            else:
                temp = self.heap[parent_index]
                self.heap[parent_index] = self.heap[new_index]
                self.heap[new_index] = temp
 
                new_index = parent_index
                parent_index = self.get_parent_index(new_index)
 
    def pop_min(self):
        minimum = self.heap[0]
 
        self.heap[0] = self.heap[len(self.heap) - 1]
        del self.heap[len(self.heap) - 1]
        current_index = 0
 
        left_index, right_index = self.get_children_index(current_index)
 
        if left_index != -1:
            left_child = self.heap[left_index]
        else:
            left_child = [float("inf")]
 
        if right_index != -1:
            right_child = self.heap[right_index]
        else:
            right_child = [float("inf")]
 
        while len(self.heap) == 1 or (self.heap[current_index][0] >= left_child[0] or self.heap[current_index][0] >= right_child[0]):
            if len(self.heap) == 1:
                del self.heap[0]
                break

            if left_child[0] < right_child[0]:
                small_index = left_index
            else:
                small_index = right_index
 
            if self.heap[small_index][0] == self.heap[current_index][0] and random.random() > .5:
                break
 
            else:
                temp = self.heap[current_index]
                self.heap[current_index] = self.heap[small_index]
                self.heap[small_index] = temp
 
                current_index = small_index
 
                left_index, right_index = self.get_children_index(current_index)
 
                if left_index != -1:
                    left_child = self.heap[left_index]
                else:
                    left_child = [float("inf")]
 
                if right_index != -1:
                    right_child = self.heap[right_index]
                else:
                    right_child = [float("inf")]
 
        return minimum, len(self.heap)
 
    def print_heap(self):
        print(self.heap)


class Node(object):
    right_child = None
    left_child = None
    total_weight = None

    def __init__(self, left=None, right=None):
        self.right_child = right
        self.left_child = left
        print left[0], left[1]
        print right[0], right[1]
        self.total_weight = [left[0] + right[0]]

    def right(self):
        return self.right_child

    def left(self):
        return self.left_child

    def create_right(self, right):
        self.right_child = right

    def create_left(self, left):
        self.left_child = left


def createTree(array, parent):
    left_parent = array[parent.left()]
    right_parent = array[parent.right()]
    parent.create_left = left_parent
    parent.create_right = right_parent

    if type(parent.right()) is Node:
        createTree(array, right_parent)

    if type(parent.left()) is Node:
        createTree(array, left_parent)

    return parent


def createDict(S, parent, encode_string, T):
    left = parent.left
    right = parent.right

    if type(right) is Node:
        T = createDict(S, right, (encode_string + "1"), T)

    if type(left) is Node:
        T = createDict(S, right, (encode_string + "0"), T) 

    return T

 
def string2freq(x):
    total_freq = [0 for _ in range(90)]
    freq = []
    symbols = []
 
    for c in x:
        total_freq[ord(c) - ord(' ')] += 1
 
    for n in range(0, len(total_freq)):
        if total_freq[n] != 0:
            freq.append(total_freq[n])
            symbols.append(chr(ord(' ') + n))
    return [symbols, freq]


def huffmanEncode(S, f):
    length = len(f)
    H = MinHeap([list(x) for x in zip(S, f)])
    

    for k in range((length+1), (2*length - 1)):
        i = H.pop_min()
        j = H.pop_min()
        newNode = Node(i, j) #create a node numbered k with children i,j

        f.append([(i[0] + j[0]), [i[1], j[1]]])
        S.append(newNode)
        
        H.insert_element(f[k])


    root_length = S[len(S) - 1]
    tree = createTree(S, root_length)

    encode_string = ""
    T = createDict(S, tree, encode_string, T)

    return T


def encodeString(x, T): #takes an input ASCII string x and a codebook T, and returns a string y, which is the binary encoding of x using T:
    y = ""
    for i in range(0, len(x)):
        y = y + T[x[i]]
    
    return y

 
def main():
    y = encodeString(x, huffmanEncode(string2freq(x))),
    print y

main()


# https://www.youtube.com/watch?v=fJORlbOGm9Y
# http://stackoverflow.com/questions/31217116/pairwise-appending-in-python-without-zip
# Maxine Hartnett answered questions about the heap & node implementations

