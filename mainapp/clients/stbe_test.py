# s = {'r':'1','r1':'2'}
# s1 = s.keys()
# print(s1)
# print(s)
# for s2 in s1:
#      print(s2)

class S1():
     s2='s2'
     s3='s3'
     s4='s4'
     s5='s5'
     @staticmethod
     def stMethod(t=4):
          print('S1.stMethod  '  + str(t))

     def __init__(self,s4='s4p',s5='s5p'):
          print('S1 __init__')
          self.s4 = s4
          self.s5 = s5

class S2(S1):
     s6='s6'
     s7='s7'

     def __init__(self, s6='s6p'):
          S1.__init__(self)
          print('S2 __init__')
          self.s6 = s6
s2cl = S2('s6sss')

 # print(s2cl.s6)
# print(s2cl.s4)
globals()['S1'].stMethod(t=';')