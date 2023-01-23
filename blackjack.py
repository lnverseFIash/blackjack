from random import sample

DECKS = 6

CARDS = [
    'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'
] * DECKS

SUITS = [
    'S', 'H', 'D', 'C'
] * DECKS

class player:
    def __init__(self):
        self.hand = []

    def draw(self, numOfCards):
        newCards = sample(CARDS, numOfCards)
        newSuits = sample(SUITS, numOfCards)
        newCardsSuits = []

        for i, j in zip(newCards, newSuits):
            newCardsSuits.append(i + j)
            CARDS.remove(i)
            SUITS.remove(j)

        self.hand.extend(newCardsSuits)

    def showHand(self):
        return ' '.join(self.hand)

    def value(self):
        v = 0
        
        for i in self.hand: 
            if i[0] == 'A' and v <= 10:
                v += 11
            elif i[0] == 'A':
                v += 1
            elif i[0] == 'J' or i[0] == 'Q' or i[0] == 'K':
                v += 10
            else:
                v += int(i[:-1])

        return v

class bj:
    def __init__(self):
        self.player = player()
        self.dealer = player()
        self.didSplit = False
        self.running = True
        self.endReason = None
        self.canDoubleDown = True

    def startHands(self):
        self.player.draw(2)
        self.dealer.draw(2)

        while self.dealer.value() < 17:
            self.dealer.draw(1)

    def display(self, message=None):
        #  one hand + hide dealer's hand
        if self.running:
            playerHand = self.player.showHand()
            dealerHand = self.dealer.hand[0]
            print(
                '\n'*100 + 
                f'DEALER:  {dealerHand} ?  \n' + 
                f'(value:  ?) \n \n \n' + 
                f'YOUR HAND:  {playerHand} \n' + 
                f'(value:  {self.player.value()}) \n \n'
                )
        
        #  show dealer's hand and reason for game end
        else:
            playerHand = self.player.showHand()
            dealerHand = self.dealer.showHand()
            print(
                '\n'*100 + 
                f'DEALER:  {dealerHand}  \n' + 
                f'(value:  {self.dealer.value()}) \n \n \n' + 
                f'YOUR HAND:  {playerHand} \n' + 
                f'(value:  {self.player.value()}) \n \n' + 
                f'{message} \n'
                )

    def canSplit(self):
        if len(self.player.hand) == 2:
            return self.player.hand[0][0] == self.player.hand[1][0]
        else:
            return False

    def displayOrEndReason(self, message):
        if self.didSplit:
            self.endReason = message
        else:
            self.display(message)

    def getInput(self, didntSplitYet=True):
        if not self.didSplit and self.canSplit() and didntSplitYet:
            userInput = input('HIT    STAND    DOUBLE DOWN    SPLIT:  ').lower()
        elif self.canDoubleDown:
            userInput = input('HIT    STAND    DOUBLE DOWN:  ').lower()
        else:
            userInput = input('HIT    STAND:  ').lower()
        return userInput

    def hit(self):
        self.player.draw(1)
        self.canDoubleDown = False  #  can't double down with more than 2 cards

    def fiveCardCharlie(self):
        if len(self.player.hand) == 5 and self.running:
            self.running = False
            self.displayOrEndReason('WIN')

    def checkTie(self, onlyCheck21=False):
        if self.player.value() == 21 and self.dealer.value() == 21 and self.running and onlyCheck21:
            self.running = False
            self.displayOrEndReason('TIE')
        elif self.player.value() == self.dealer.value() and self.running and not onlyCheck21:
            self.running = False
            self.displayOrEndReason('TIE')

    def check21Player(self):
        if self.player.value() == 21 and self.running:
            self.running = False
            self.displayOrEndReason('WIN')
    
    def check21Dealer(self):
        if self.dealer.value() == 21 and self.running:
            self.running = False
            self.displayOrEndReason('LOST')
        
    def ifBusted(self):
        if self.player.value() > 21 and self.running:
            self.running = False
            self.displayOrEndReason('BUST')

    def stand(self):
        if self.running:
            self.running = False

            if self.dealer.value() > 21:
                self.displayOrEndReason('WIN')
            
            elif self.player.value() > self.dealer.value():
                self.displayOrEndReason('WIN')
            
            elif self.player.value() < self.dealer.value():
                self.displayOrEndReason('LOSE')

    def insideSplit(self):
        self.didSplit = True

bj1 = bj()
bj2 = bj()

def outsideSplit():
    bj2.player.hand.append(bj1.player.hand[1])
    del bj1.player.hand[1]
    bj2.dealer.hand = bj1.dealer.hand
    bj2.didSplit = True

def outsideDisplay(firstHand=True):
    #  show dealer's hand and reason for game end
    if not (bj1.running or bj2.running):
        playerHand = bj1.player.showHand()
        playerHand2 = bj2.player.showHand()
        dealerHand = bj1.dealer.showHand()
        print(
            '\n'*100 + 
            f'DEALER:  {dealerHand}  \n' + 
            f'(value:  {bj1.dealer.value()}) \n \n \n' + 
            f'FIRST HAND:  {playerHand} \n' + 
            f'(value:  {bj1.player.value()}) \n' + 
            f'{bj1.endReason} \n \n' + 
            f'SECOND HAND:  {playerHand2} \n' + 
            f'(value:  {bj2.player.value()}) \n' + 
            f'{bj2.endReason} \n \n'
            )
            
    #  current hand is first hand + hide dealer's hand
    elif firstHand:
        playerHand = bj1.player.showHand()
        playerHand2 = bj2.player.showHand()
        dealerHand = bj1.dealer.hand[0]
        print(
            '\n'*100 + 
            f'DEALER:  {dealerHand} ?  \n' + 
            f'(value:  ?) \n \n \n' + 
            f'▶  CURRENT HAND:  {playerHand} \n' + 
            f'▶  (value:  {bj1.player.value()}) \n \n'
            f'other hand:  {playerHand2} \n' + 
            f'(value:  {bj2.player.value()}) \n \n'
            )
    
    #  current hand is second hand + hide dealer's hand
    else:
        playerHand = bj1.player.showHand()
        playerHand2 = bj2.player.showHand()
        dealerHand = bj1.dealer.hand[0]
        print(
            '\n'*100 + 
            f'DEALER:  {dealerHand} ?  \n' + 
            f'(value:  ?) \n \n \n' + 
            f'other hand:  {playerHand} \n' + 
            f'(value:  {bj1.player.value()}) \n \n' + 
            f'▶  CURRENT HAND:  {playerHand2} \n' + 
            f'▶  (value:  {bj2.player.value()}) \n \n'
            )
        
def play():
    bj1.startHands()
    bj1.checkTie(True)
    bj1.check21Player()
    bj1.check21Dealer()

    while bj1.running and not bj1.didSplit:
        bj1.display()
        userInput = bj1.getInput()

        #  hit
        if userInput == 'h':
            bj1.hit()

            bj1.ifBusted()
            bj1.check21Player()
            bj1.fiveCardCharlie()

        #  stand
        elif userInput == 's':
            bj1.checkTie()
            bj1.check21Player()

            bj1.check21Dealer()
            bj1.stand()
        
        #  double down
        elif userInput == 'd' and bj1.canDoubleDown:
            bj1.hit()

            bj1.ifBusted()
            bj1.check21Player()
            bj1.fiveCardCharlie()

            bj1.checkTie()
            bj1.check21Dealer()
            bj1.stand()
        
        #  split
        elif userInput == 'p' and bj1.canSplit():
            bj1.insideSplit()
            outsideSplit()

    #  SPLIT LOOP

    #  split aces
    if bj1.running and bj1.player.hand[0][0] == 'A':
        bj1.hit()
        
        bj1.ifBusted()
        bj1.check21Player()
        bj1.fiveCardCharlie()

        bj1.checkTie()
        bj1.check21Dealer()
        bj1.stand()
        
        bj2.hit()

        bj2.ifBusted()
        bj2.check21Player()
        bj2.fiveCardCharlie()

        bj2.checkTie()
        bj2.check21Dealer()
        bj2.stand()

    #  second hand
    while bj2.running and bj1.running:
        outsideDisplay(False)
        bj2Input = bj2.getInput()

        if bj2Input == 'h':
            bj2.hit()

            bj2.ifBusted()
            bj2.check21Player()
            bj2.fiveCardCharlie()

        elif bj2Input == 's':
            bj2.checkTie()
            bj2.check21Player()

            bj2.check21Dealer()
            bj2.stand()
        
        elif bj2Input == 'd' and bj1.canDoubleDown:
            bj2.hit()
            
            bj2.ifBusted()
            bj2.check21Player()
            bj2.fiveCardCharlie()

            bj2.checkTie()
            bj2.check21Dealer()
            bj2.stand()

    #  first hand
    while bj1.running and not bj2.running:
        outsideDisplay()
        bj1Input = bj1.getInput()

        if bj1Input == 'h':
            bj1.hit()

            bj1.ifBusted()
            bj1.check21Player()
            bj1.fiveCardCharlie()

        elif bj1Input == 's':
            bj1.checkTie()
            bj1.check21Player()

            bj1.check21Dealer()
            bj1.stand()
        
        elif bj1Input == 'd' and bj1.canDoubleDown:
            bj1.hit()
            
            bj1.ifBusted()
            bj1.check21Player()
            bj1.fiveCardCharlie()

            bj1.checkTie()
            bj1.check21Dealer()
            bj1.stand()

    if not bj1.running and not bj2.running:
        outsideDisplay()



play()

'''
cards = [
    'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 
    'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 
    'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 
    'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC'
    ]
'''
# https://app.driversed.com/courseflow/page/983HHTlih1DoLKlU
# https://app.driversed.com/courseflow/page/983HHTlih1DoLKlU


