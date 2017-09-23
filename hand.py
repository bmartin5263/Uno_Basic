class Hand():

    ''''deck' (Deck) : Card's Color (rgby)
       'numberOfCards' (int) : Card's Value (0-9, R, X, W, +2, +4)'''

    def __init__(self, deck=None, numberOfCards=0):
        self.hand = []

    def __iter__(self):
        return iter(self.hand)

    def __len__(self):
        return len(self.hand)

    def __getitem__(self, item):
        try:
            return self.hand[item]
        except:
            return ''

    def addCard(self, card):
        self.hand.append(card)

    def removeCard(self, index):
        index = int(index)
        if (0 <= index < len(self)):
            return self.hand.pop(index)

    def discard(self):
        self.hand = []

    def show(self, scrollNum=0, hide=False):
        if scrollNum == -1:
            scrollNum = 0
        output = ''
        num = 0
        header, footer, upper, lower = '', '', '', ''
        header += ('\033[97m\u2666--\u2666\033[0m ')
        upper += ('\033[97m|<-|\033[0m ')
        lower += ('\033[97m|<-|\033[0m ')
        footer += ('\033[97m\u2666--\u2666\033[0m ')
        for i in range(10):
            indexNum = i + (10 * scrollNum)
            if indexNum < len(self):
                header += (self[indexNum].getRow(0, hide) + ' ')
                upper += (self[indexNum].getRow(1, hide) + ' ')
                lower += (self[indexNum].getRow(2, hide) + ' ')
                footer += (self[indexNum].getRow(3, hide) + ' ')
                num += 1
        for j in range(10 - num):
            j  # unused
            header += ('     ')
            footer += ('     ')
            upper += ('     ')
            lower += ('     ')
        header += ('\033[97m\u2666--\u2666\033[0m ')
        upper += ('\033[97m|->|\033[0m ')
        lower += ('\033[97m|->|\033[0m ')
        footer += ('\033[97m\u2666--\u2666\033[0m ')
        output += ('  ' + header + '\n  ' + upper + '\n  ' + lower + '\n  ' + footer + '\n\033[97m|-(<)--')
        for k in range(num):
            output += '({})'.format(k)
            output += '--'
        for l in range(10 - num):
            l  # unused
            output += '-----'
        output += '(>)--|\033[0m\n'
        return output

    def getCard(self, index):
        return self.hand[index]

    def indexCard(self, card):
        return self.hand.index(card)