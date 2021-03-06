from bjHand import Hand

def ofType(item, type):
    return item.__class__.__name__ == type


class Player:
    """
    This class defines a blackjack player. Each blackjack player can have one or more hands.
    """

    def __init__(self, money, strategy=None,name=None):
        """
        Initialize the player. No hands initially.
        Class attributes are:
          - money -- float value of money the player has
          - strategy -- strategy the player wants to use based on file
                if no strategy selected, assume this is a human
          - hands -- Initially a blank list that will eventually contain Hand objects
          - bets -- List of integer bet values that corresponds to the same index in hands list
          - name -- Ascii name used for drawing user interface.
        """

        # How much money does this player have
        self.money = float(money)

        # If no strategy file selected, assume human
        if strategy == None:
            self.isInteractive = True
        
        else:
            # Import this person's strategy
            self.strategy = __import__(strategy).strategy
            self.isInteractive = False
        
        # Save our name
        self.name = name

        # Start up our hands spots
        self.hands = []
        
        # Start up bets list
        self.bets = []
    
    def getMoney(self):
        """
        Input:
            Nothing
        Action:
            Get amount of money this player has
        Returns:
            Amount of money this player has as a float value (i.e.:10.5)
        """
        
        # For now just return the variable
        return self.money
    
    def addMoney(self,amount):
        """
        Input:
            amount = Amount to add (note, just use negative values to subtract)
        Action:
            Adds $amount to the player's money
        Returns:
            Nothing
        """
        
        self.money += amount
        
    def isHuman(self):
        """
        Input:
            Nothing
        Action:
            Checks if this player is human.
        Returns:
            True if this player is interactive, False otherwise.
        """
        # Keeping this as a method in case I change how I do things later.
        return self.isInteractive
    
    def addHand(self, hand=None):
        """
        Input:
            (optional) hand = Hand object to give to the user. If none given, a blank hand will be added.
        Action:
            Adds given hand to the user's hand list
        Returns:
            Nothing
        """
        
        # If we're adding a blank one
        if hand == None:
            hand = Hand()
        
        # Make this really is a hand object
        assert ofType(hand, "Hand")

        # Append the hand
        self.hands.append(hand)

    def getHand(self, index=0):
        """
        Input:
            (optional) index = index of the hand to look at if more than one (i.e.: player split hand)
        Action:
            Returns a pointer to the hand at index (default of index 0)
        Returns:
            Pointer to hand
        """
        return self.hands[index]
    
    def getHands(self):
        """
        Input:
            None
        Action:
            Get list of hands for player
        Returns:
            List of hands for player
        """
        return self.hands

    def clearBets(self):
        """
        Input:
            None
        Action:
            Clears out the bets for this player.
        Returns:
            Nothing
        """
        # Easy.
        self.bets = []
    
    def clearHands(self):
        """
        Input:
            Nothing
        Action:
            Clears out all hands associated with player
        Returns:
            Nothing
        """
        # Easy
        self.hands = []
    
    def placeBet(self,amount=None):
        """
        Input:
            (optional) amount = amount of money to bet for this hand
        Action:
            If amount isn't specified:
                If player is human prompt for amount
                If player is not human, call betting method in strategy
            If amount is specified simply use that value as the bet
            Note: The bet amount will be subtracted from the player's current money amount
        Returns:
            Nothing
        """
        
        # If we're not being given an amount
        if amount == None:
            # If we need to figure it out ourself
            
            # If the player is human
            if self.isHuman():
                amount = ""
                # Keep asking for amount until we get a valid integer
                while not amount.isdigit():
                    amount = input("What's your wager: ")
                amount = int(amount,10)
            
            # Only other option is a machine
            else:
                raise Exception("I haven't added automatic betting yet. :-(")
        
        # Sanity check here to ensure player can over bet
        if self.getMoney() < amount:
            raise Exception("You're trying to bet more than you have! I really need to handle this case better.")
        
        # Are we doing silly tricks?
        if amount < 0:
            raise Exception("Please don't bet negative values :-)")
        
        # Add it to the bet 
        self.bets.append(amount)
        
        # Remove it from our holdings
        self.addMoney(amount*-1)
    
    def getBets(self):
        """
        Input:
            None
        Action:
            Gets the list of bets active for this player
        Returns:
            List of bets active for this player
        """

        return self.bets
    
    def selectHandAction(self,hand,validActions):
        """
        Input:
            hand == Hand index to ask for an action
            validActions == Set of valid actions for this hand.
                This is created through Dealer.allowedHandActions method
        Action:
            If this is a human user, ask for action
            If this is a machine, use the appropriate method to get action
        Returns:
            Selected action
        """
        
        # If we're a human, ask for action
        if self.isHuman():
            # Dictionary of things we can do
            # TODO: This is hackish
            lookup = {"hit":"","stand":"","double":", [d]ouble","split":", s[p]lit","surrender":", su[r]render"}
            print("Actions: [h]it, [s]tand" + ''.join([lookup[action] for action in validActions]))
            action = ""
            # Loop until valid input
            while action.lower() not in ["h","s","d","p","r"]:
                action = input("What do you want to do?: ")
        else:
            raise Exception("Sorry, haven't implemented logic for automatic action")
        
        actionLookup = {"h":"hit","s":"stand","d":"double","p":"split","r":"surrender"}
        
        # Validate our action
        action = actionLookup[action[0].lower()]
        
        if action not in validActions:
            raise Exception("You selected an action that isn't allowed!")
        
        # Ok, we're good.
        return action
