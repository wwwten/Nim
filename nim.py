
import random
import time

class CantMove( Exception ) :

   def __init__( self, reason ) : 
      self. __reason = reason

   def __repr__( self ) :
      return "unable to find a move: {}". format( self.__reason )


class Nim :
   def __init__( self, startstate ) :
      self. state = startstate


   # Goal is to be unambiguous : 

   def __repr__( self ) :
      s=""
      for i in range(len(self.state)) :
         j=0
         s+=str(i+1) + " : "
         while j < self.state[i]:
            s += " 1 " 
            j = j+1
         s+="\n"
      return s      
      #print (range(len(self.state)))

   # Return sum of all rows:

   def sum( self ) :
      s = 0
      for i in range(len(self.state)):
      	 j=0
      	 while j < self.state[i]:
      	 	s = s + 1
      	 	j = j+1
      return s


   # Return nimber (xor of all rows): 

   def nimber( self ) :
      s = 0
      for i in range(len(self.state)):
      	 s = s^self.state[i]
      return s

   # Make a random move, raise a CantMove if
   # there is nothing left to remove. 

   def randommove( self ) :
      if self.sum() == 0:
         raise CantMove("no sticks left")
      else:
         i = random.randrange(len(self.state))
         j = random.randrange( self.state[i])+1
         if(j== self.state[i]):
            self.state.remove(self.state[i])
         else:
            self.state[i] = self.state[i] - j


   # Try to force a win with misere strategy.
   # This functions make a move, if there is exactly
   # one row that contains more than one stick.
   # In that case, it makes a move that will leave
   # an odd number of rows containing 1 stick.
   # This will eventually force the opponent to take the
   # last stick.
   # If it cannot obtain this state, it should raise
   # CantMove( "more than one row has more than one stick" )

   def removelastmorethantwo( self ) :
      s = 0
      num = len(self.state)
      for i in range(len(self.state)):
      	 if self.state[i] > 1:
      	    s=s+1
      	    index = i
      if s != 1 :
         raise CantMove( "more than one row has more than one stick" )
      else:
         if num%2 == 0:
            self.state.remove(self.state[index])
         else:
         	self.state[index] = self.state[index] - (self.state[index] - 1)


   # Try to find a move that makes the nimber zero.
   # Raise CantMove( "nimber is already zero" ), if the
   # nimber is zero already.

   def makenimberzero( self ) :
      cur_nim = self.nimber()
      # j=0
      # while j < 10:
      if cur_nim == 0:
         raise CantMove("nimber is already zero")
      else:
         i=0
         while i < 10:
               value = random.randint(0, len(self.state)-1)     
               if(self.state[value]^cur_nim) < self.state[value]:
                   if cur_nim == self.state[value]:
               	      self.state.remove(self.state[value])
               	      break
                   else:
                      self.state[value] = self.state[value]^cur_nim
                      break

  
 
   def optimalmove( self ) :
      try:
         self.removelastmorethantwo()
      except CantMove:
         try:
            self.makenimberzero()
         except CantMove:
            try:
               self.randommove()
            except CantMove:
               print("There is no Optimal move")           
               


   # Let the user make a move. Make sure that the move
   # is correct. This function never crashes, not
   # even with the dumbest user in the world. 
   def rowdata (self) :
      i=0
      while i < 10 :
         row = input("Enter the number of a row : ")
         try:
            row=int(row)
         except ValueError:
       	    print ("u have to enter integer")
       	    continue
         else:
            row=int(row)
            if row > len(self.state) or row <= 0:
               print("Enter the number in this range : (1," + str(len(self.state)) + ")")
               continue 
            else: 
               return row
               break

   def stickdata (self, row) :
      i=0
      while i<10 :	
         number = input("Enter the number of a sticks : ")
         try:
            number=int(number)
         except ValueError:
            print("You have to enter the integer!")
            continue
         else:
            number=int(number)
            if number > (self.state[row - 1]) or number <= 0 :
               print("Enter the number in this range : (1," + str((self.state[row-1])) + ")")
               continue   
            else:
               return number
               break
           
   def usermove( self ) : 
      row = int(self.rowdata())
      number = self.stickdata(row)
      if number == (self.state[row-1]):
         self.state.remove(self.state[row-1])
      else:
         self.state[row-1] = self.state[row-1] - number


   def play( ) :
      st = Nim( [1, 2, 4] )
      turn = 'user'
      while st.sum( ) > 1 :

         if turn == 'user' :
            print( "\n" )
            print( st )
            print( "hello, user, please make a move" )
            st. usermove( )
            turn = 'computer'
         else :
            print( "\n" )
            print( st )
            print( "now i will make a move\n" )
            print( "thinking" )
            for r in range( 15 ) :
               print( ".", end = "", flush = True )
               time. sleep( 0.1 )
            print( "\n" )

            st. optimalmove( )
            turn = 'user'
      print( "\n" )

      if turn == 'user' :
         print( "you lost\n" )
      else :
         print( "you won\n" )
