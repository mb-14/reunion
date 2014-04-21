import ffield
import genericmatrix
import math

def div_ceil(n, d):
    """
    The smallest integer k such that k*d >= n.
    """
    return (n/d) + (n%d != 0)

class FEC:
    def __init__(self, n, k):
        self.field = ffield.FField(7)
        self.n = n
        self.k = k
        self.CreateVandermondeMatrix()
        self.CreateVandermondeMatrixInv()

               
    def CreateVandermondeMatrix(self):
        """
        Create a Vandermonde Matrix
        """
        self.vMatrix = genericmatrix.GenericMatrix((self.n,self.k),0,1,self.field.Add,self.field.Subtract,self.field.Multiply,self.field.Divide)
        self.vMatrix[0,0] = 1
        for i in range(0,self.n):
            term = 1
            for j in range(0, self.k):
                self.vMatrix[i,j] = term
                term = self.field.Multiply(term,i+1)

    def CreateVandermondeMatrixInv(self):
        """
        Create a inverse Vandermonde Matrix
        """
        self.vInvMatrix = genericmatrix.GenericMatrix((self.k,self.k),0,1,self.field.Add,self.field.Subtract,self.field.Multiply,self.field.Divide)
        for i in range(self.k):
            self.vInvMatrix.SetRow(i,self.vMatrix.GetRow(i))
        self.vInvMatrix = self.vInvMatrix.Inverse()
    
    def CreateDataMatrix(self,data):
        """
        Create Matrix from the data
        """
        self.chunk = div_ceil(len(data),self.k) 
        data = [ord(char) for char in list(data)]
        data.extend([0]*(self.chunk*self.k-len(data)))
        chunks=[data[x:x+self.chunk] for x in xrange(0, len(data), self.chunk)]
        self.dMatrix = genericmatrix.GenericMatrix((self.k,self.chunk),0,1,self.field.Add,self.field.Subtract,self.field.Multiply,self.field.Divide)
        for i in range(self.k):
            self.dMatrix.SetRow(i,chunks[i])

    def Encode(self, data):
        """
        Function:       Encode(data)
        Purpose:        Split data into n parts k of which are sufficient to
                        recover the original data. Returns a list of chunks
        """
        self.CreateDataMatrix(data)
        result =  self.vMatrix*self.dMatrix
        result_chunks = []
        for i in range(self.n):
            result_chunks.append(''.join([chr(x) for x in result.GetRow(i)]))  
        return result_chunks

    def Decode(self, chunks):
        """
        Function:       Decode(chunks)
        Purpose:        Recover original data using given list of chunks.
        """
        self.CreateDecodeMatrix(chunks)
        result =  self.vInvMatrix*self.decMatrix
        result_list = []
        for i in range(self.k):
            result_list.append(''.join([chr(x) for x in result.GetRow(i)]))
        result_string = ''.join(result_list)   
        return result_string

    def CreateDecodeMatrix(self, chunks):
        """
        Create a matrix from the given list of chunks.
        """
        self.decMatrix = genericmatrix.GenericMatrix((self.k,len(chunks[0])),0,1,self.field.Add,self.field.Subtract,self.field.Multiply,self.field.Divide)
        for i in range(self.k):
             self.decMatrix.SetRow(i,[ord(x) for x in chunks[i]])
