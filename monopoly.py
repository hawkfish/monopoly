import random
import sys

#
#   Constants
#

#   Board Squares
Go = 0
Reading = 5
Jail = 10
StCharlesPlace = 11
ElectricCompany = 12
PennsylvaniaRR = 15
FreeParking = 20
Illinois = 24
BandO = 25
WaterWorks = 28
MarvinGardens = 29
GoToJail = 30
ShortLine = 35
Boardwalk = 39
InJail = 40

#   Cards
Chance = [7, 22, 36,]
CommunityChest = [2, 17, 33,]

DontMove = -1
GoBackThree = -3
AdvanceToUtility = -2
AdvanceToRailroad = -5

chanceCards = [
    DontMove,
    DontMove,
    DontMove,
    DontMove,
    DontMove,
    Jail,
    AdvanceToUtility,
    Boardwalk,
    Reading,
    Go,
    AdvanceToRailroad,
    AdvanceToRailroad,
    StCharlesPlace,
    Illinois,
    GoBackThree,
    ]
random.shuffle( chanceCards )

communityChestCards = [
    Jail,
    Go,
    DontMove,
    DontMove,
    DontMove,
    DontMove,
    DontMove,
    DontMove,
    DontMove,
    DontMove,
    DontMove,
    DontMove,
    DontMove,
    DontMove,
    DontMove,
    DontMove,
]
random.shuffle( communityChestCards )

def moveToken(token, distance):
    token += distance
    if token < 0: token += 40
    token %= 40
    
    return token

def drawCard(cards):
    n = len(cards)
    card = cards[0]
    cards[:n-1] = cards[1:]
    cards[n-1] = card
    return card
    
class Player:
    def __init__(self, _turns = 0, _token = Go, _doubles = 0, _jail = 3, _trips = 0):
        self.counts = []
        for c in range(0,41):
            self.counts.append(0)
        
        self.token = _token
        self.doubles = _doubles
        self.jail = _jail
        self.trips = _trips
        self.turns = _turns
        
        self.jailCard = 0
        self.jailDoubles = 0
        self.jailCop = 0

    def move(self, d1, d2):
        #   Where did we start out?
        previous = self.token
        
        #   Are we in jail?
        if self.token == Jail and self.jail < 2:
            self.jail += 1
            if d1 != d2:
                self.counts[InJail] += 1
                self.turns += 1
                return
                
        #   Count the doubles
        if d1 == d2 and self.jail == 3:
            self.doubles += 1
        else:
            self.doubles = 0
            self.jail = 3
        
        #   Did we roll three doubles in a row?
        if self.doubles == 3:
            self.token = Jail
            self.jail = 0
            self.counts[InJail] += 1
            self.doubles = 0
            self.turns += 1
            self.jailDoubles += 1
            return
            
        #   Move the self.token
        self.token = moveToken(self.token, d1 + d2)
        
        #   Count where we wound up
        self.counts[self.token] += 1
        
        # Did we land on Go To Jail?
        if self.token == GoToJail:
            self.token = Jail
            self.jail = 0
            self.counts[InJail] += 1
            self.doubles = 0
            self.turns += 1
            self.jailCop += 1
            return
            
        while ( 1 ):
            #   Did we land on Chance?
            if self.token in Chance:
                card = drawCard(chanceCards)
            
            #   Did we land on Community Chest?
            elif self.token in CommunityChest:
                card = drawCard(communityChestCards)
            
            else:
                card = DontMove
            
            if card == DontMove:
                break
            
            #   Advance to utility
            elif card == AdvanceToUtility:    
                if self.token > GoToJail or self.token < Jail:
                    self.token = ElectricCompany
                else:
                    self.token = WaterWorks
                
            #   Back three spaces
            elif card == GoBackThree:  
                self.token = moveToken( self.token, card )
            
            #   Advance to railroad
            elif card == AdvanceToRailroad:    
                if self.token < PennsylvaniaRR:
                    self.token = PennsylvaniaRR
                
                elif self.token < BandO:
                    self.token = BandO
                
                elif self.token < ShortLine:
                    self.token = ShortLine
                
                else:
                    self.token = Reading
            
            else:
                self.token = card
            
            #   Did  we move to Jail?
            if self.token == Jail:
                self.jail = 0
                self.counts[InJail] += 1
                self.doubles = 0
                self.jailCard += 1
            else:
                self.counts[self.token] += 1
    
        #   Count trips
        if self.token < previous and self.jail == 3:
            self.trips += 1
        
        #   Count turns
        if self.jail < 3 or self.doubles == 0:
            self.turns += 1

    def report(self):
        print "Trips: %d, Turns: %d, Turns per Trip: %3.1f" % (self.trips, self.turns, float(self.turns)/self.trips)
        percents = [c * 100.0 / self.trips for c in self.counts]
        for p in range(0,11):
            print "%4.1f" % percents[p],
        print "%4.1f" % percents[InJail]
        
        for p in range(1,10):
            print "%4.1f" % percents[40-p],
            for s in range(1,10):
                print "    ",
            print "%4.1f" % percents[20+p]
        
        for p in range(30,19,-1):
            print "%4.1f" % percents[p],
        print
        print "Jail: Card: %d, Cop: %d, Doubles: %d" % (self.jailCard, self.jailCop, self.jailDoubles,)

    def dump(self):
        print "Square,Row,Col,Percent"
        format = "%d,%d,%d,%f"
        percents = [c * 100.0 / self.trips for c in self.counts]
        for p in range(0,InJail):
            col = 10 - p % 10
            row = 10
            if p >= GoToJail:
                row = 10 - col
                col = 10
            elif p >= FreeParking:
                col = 10 - col
                row = 0
            elif p >= Jail:
                row = col
                col = 0
                
            print "%d,%d,%d,%f" % (p, row, col+1, percents[p],)
        
        print "%d,%d,%d,%f" % (InJail, 10, 0, percents[InJail],)
            
if __name__ == '__main__':
    rolls = 1000
    if len(sys.argv) > 1:
        rolls = int (sys.argv[1])
        
    player = Player()
    for roll in range(0,rolls):
        #   Roll the dice
        d1 = random.randint(1,6)
        d2 = random.randint(1,6)
        
        #   Move the player
        player.move(d1, d2)
    
    player.report()
    
