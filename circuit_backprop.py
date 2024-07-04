import numpy as np 

class CompGraphExpr:
    def __init__(self):
        return NotImplementedError

    def get_value(self):
        if self.value is None:
            self.value = self.calc_value()
        return self.value
    
    def calc_value(self):
        return NotImplementedError

    def get_adjoint(self):
        if self.adjoint is None:
            self.adjoint = self.calc_adjoint()
        return self.value

    def calc_adjoint(self):
        return NotImplementedError
    
    def __add__(self,other):
        if type(other) is CompGraphExpr:
            return AddCompGraphExpr(self,other)

    def __sub__(self,other):
        return SubCompGraphExpr(self,other)

    def __mul__(self,other):
        return MulCompGraphExpr(self,other)

    def __div__(self,other):
        return DivCompGraphExpr(self,other)
    
class ConstCompGraphExpr(CompGraphExpr):
    def __init__(self,value):
        self.value = value

    def get_value(self):
        return self.value

    def get_adjoint(self):
        return 0

class InputCompGraphExpr(CompGraphExpr):
    def __init__(self,value):
        self.value = value

    def get_value(self):
        return self.value

    def get_adjoint(self):
        return 1

class SingleFuncCompGraphExpr(CompGraphExpr):
    def __init__(self, f, df, input):
        self.value = None
        self.adjoint = None
        self.func = f
        self.df = df
        self.input = input

    def calc_value(self):
        return self.f(self.input.get_value())
    
    def get_adjoint(self):
        return self.input.get_adjoint()*self.df(self.input.get_value())
    
    def clear(self):
        self.value = None
        self.input.clear()

class TwoInputCompGraphExpr(CompGraphExpr):
    def __init__(self,a,b):
        self.a = a
        self.b = b
    
    def clear(self):
        self.a.clear()
        self.b.clear()

class MulCompGraphExpr(TwoInputCompGraphExpr):
    def calc_value(self): 
        return self.a.get_value()*self.b.get_value()

    def calc_adjoint(self): 
        return self.a.get_value()*self.b.get_adjoint() + self.a.get_adjoint()*self.b.get_value()

class DivCompGraphExpr(TwoInputCompGraphExpr):
    def calc_value(self): 
        return self.a.get_value()/self.b.get_value()

    def calc_adjoint(self): 
        return (self.b.get_value()*self.a.get_adjoint() - self.b.get_adjoint()*self.a.get_value())/(self.b.get_value()^2)

class AddCompGraphExpr(TwoInputCompGraphExpr):
    def calc_value(self): 
        return self.a.get_value() + self.b.get_value()

    def calc_adjoint(self): 
        return self.a.get_adjoint() + self.b.get_adjoint()

class SubCompGraphExpr(TwoInputCompGraphExpr):
    def calc_value(self): 
        return self.a.get_value() - self.b.get_value()

    def calc_adjoint(self): 
        return self.a.get_adjoint() - self.b.get_adjoint()
        

    