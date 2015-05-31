# This module holds commands for the character creation system.

from commands.commands import *
import random as r

class CharacterCreationSystem(Command):
    '''
    Basic set up and testing for character creation system.

    Usage:
      grow char
    '''

    key = 'grow char'
    aliases = ['grow']
    locks = 'cmd:all()'
    help_category = 'character creation'
    

    def preRoll(self, player):
        player.db.next_node = 'jobNode'


    def classRoll(self, player):
        player.db.social_class = player.db.menuvar
        player.db.next_node = 'incomeNode'


    def jobRoll(self, player):
        player.db.job = player.db.menuvar
        player.db.next_node = 'exitNode'
        
    
    def finalRoll(self, player):
        player.db.income = player.db.menuvar
        player.db.next_node = 'DONE'

    def makeNode1(self):
        node = MenuNode('START', 
                         text = 'Choose one of the following classes.',
                         links = ['END', 'END', 'END'], 
                         keywords = ['Slave', 'Peasant', 'Craftsman'], 
                         callback = lambda self: CharacterCreationSystem.preRoll(CharacterCreationSystem(), self.caller))
        return node

    def makeNode2(self, next_node, choice):
        if next_node == 'jobNode':
            key = 'START'
        else:
            key = 'INACTIVE'
        text = ''

        slave_text = "You are a slave, your jobs are decided for you."
        peasant_text = "Be happy you have some choice in life. Choose your job."
        craftsman_text = "The world is your oyster. Make your choice."
        links = ['END', 'END', 'END', 'END']
        linktexts = [' ',' ',' ','Your only choice']
        keywords = ['Farmer', 'Shopminder', 'Dongsmith', 'Slave']

        set_links = []
        set_linktexts = []
        set_keywords = []

        if choice == 'Slave':
            text = slave_text
            set_links.extend(links[3:4])
            set_linktexts.extend(linktexts[3:4])
            set_keywords.extend(keywords[3:4])
        if choice == 'Peasant':
            text = peasant_text
            set_links.extend(links[0:2])
            set_keywords.extend(keywords[0:2])
        if choice == 'Craftsman':
            text = craftsman_text
            set_links.extend(links[0:3])
            set_keywords.extend(keywords[0:3])

        node = MenuNode(key, 
                         text = text,
                         links = set_links, 
                         linktexts = set_linktexts,
                         keywords = set_keywords,
                         callback = lambda self: CharacterCreationSystem.classRoll(CharacterCreationSystem(), self.caller))
        return node

    def makeNode3(self, next_node, chosen_class):
        if next_node == 'incomeNode':
            key = 'START'
        else:
            key = 'INACTIVE'
        text = ''

        slave_text = "You are a slave, income doesn't exist for you."
        peasant_text = "Be happy you have some food to eat, at least. Choose your income level."
        craftsman_text = "Your skills are such that you may set your price. Choose your income."
        links = ['END', 'END', 'END', 'END']
        linktexts = [' ',' ',' ','Your only choice']
        keywords = ['Low', 'Medium', 'High', 'Slave']

        set_links = []
        set_linktexts = []
        set_keywords = []

        if chosen_class == 'Slave':
            text = slave_text
            set_links.extend(links[3:4])
            set_linktexts.extend(linktexts[3:4])
            set_keywords.extend(keywords[3:4])
        if chosen_class == 'Peasant':
            text = peasant_text
            set_links.extend(links[0:2])
            set_keywords.extend(keywords[0:2])
        if chosen_class == 'Craftsman':
            text = craftsman_text
            set_links.extend(links[0:3])
            set_keywords.extend(keywords[0:3])

        node = MenuNode(key, 
                         text = text,
                         links = set_links, 
                         linktexts = set_linktexts,
                         keywords = set_keywords,
                         callback = lambda self: CharacterCreationSystem.jobRoll(CharacterCreationSystem(), self.caller))
        return node

    def makeExitNode(self, next_node, choice):
        if next_node == 'exitNode':
            key = 'START'
        else:
            key = 'INACTIVE'
        node = MenuNode(key, text = "All done!", links = ['END'], keywords = ['Exit'],
                         callback = lambda self: CharacterCreationSystem.finalRoll(CharacterCreationSystem(), self.caller))
            

        return node


    def func(self):
        'Character creation system'

        if not self.args:
            startNode = self.makeNode1()
            jobNode = self.makeNode2(self.caller.db.next_node, self.caller.db.menuvar)
            incomeNode = self.makeNode3(self.caller.db.next_node, self.caller.db.social_class)
            exitNode = self.makeExitNode(self.caller.db.next_node, self.caller.db.menuvar)

            if self.caller.db.next_node <> 'exitNode':
                menu = MenuTree(self.caller, nodes = (startNode, jobNode, incomeNode, exitNode), exec_end = "grow")
            else:
                menu = MenuTree(self.caller, nodes = (startNode, jobNode, incomeNode, exitNode))

            menu.start()

