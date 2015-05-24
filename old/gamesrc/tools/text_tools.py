# A module to hold any general text related tools that we might come up with.
#  format_line.py will be kept separate, because we'll have that used more or
#  less on its own, built-in to objects that use it naturally. These tools are
#  more used on-the-fly.

class TextTools:

    # A method to pluralize words properly. We'll add more rules and exceptions
    #  as we go and as we need.
    def pluralKey(self, key):
        for letter in 'a e i o u'.split():
            if key.endswith('y') and key.rstrip('y').endswith(letter):
                plural_key = key + 's' 
            elif key.endswith('y') and not key.rstrip('y').endswith(letter):
                plural_key = key + 'ies' 
            elif key.endswith('o') or key.endswith('sh') or key.endswith('ch'):
                plural_key = key + 'es'
            else:
                plural_key = key + 's'

        return plural_key

    
    def prepositionList(self):
        # returns a list of prepositions used in commands
        preps = 'above around atop before behind below beneath beside beyond by from in inside near onto outside over past toward towards under underneath unto upon with within without'.split(' ')
        preps.append('next to')
        preps.append('on top of')
        preps.append('inside of')
        preps.append('outside of')
        preps.append('opposite of')
        preps.append('next')
        preps.append('to')
        preps.append('of')
        preps.append('on')
        preps.append('top')
        preps.append('inside')
        preps.append('outside')

        return preps


    def articleList(self):
        # returns a list of articles used in player input
        return 'a an the some'.split(' ')
