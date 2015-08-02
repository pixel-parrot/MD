"""

Template for Characters

Copy this module up one level and name it as you like, then
use it as a template to create your own Character class.

To make new logins default to creating characters
of your new type, change settings.BASE_CHARACTER_TYPECLASS to point to
your new class, e.g.

settings.BASE_CHARACTER_TYPECLASS = "game.gamesrc.objects.mychar.MyChar"

Note that objects already created in the database will not notice
this change, you have to convert them manually e.g. with the
@typeclass command.

"""
from evennia import DefaultCharacter

import random as r


class Character(DefaultCharacter):
    """
    The Character is like any normal Object (see example/object.py for
    a list of properties and methods), except it actually implements
    some of its hook methods to do some work:

    at_basetype_setup - always assigns the default_cmdset to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead)
    at_after_move - launches the "look" command
    at_post_puppet(player) -  when Player disconnects from the Character, we
                    store the current location, so the "unconnected" character
                    object does not need to stay on grid but can be given a
                    None-location while offline.
    at_pre_puppet - just before Player re-connects, retrieves the character's
                    old location and puts it back on the grid with a "charname
                    has connected" message echoed to the room

    """
    def at_object_creation(self):
        #delete this later
        self.db.strength = 5
        self.db.agility = 4
        self.db.constitution = 2
        self.db.pilot = 2
        self.db.honorific_prefix = ''
        self.db.first_name = ''
        self.db.middle_name = ''
        self.db.last_name = ''
        self.db.honorific_suffix = ''
        self.db.namestring = self.db.first_name
        # this holds all characters encountered. the key is the object's dbref,
        #   their value is False if no name is known, given, or set until
        #   it is known, given, or set
        self.db.characters_met = {}
        self.db.description = ''
        self.db.object_title = ''
        self.db.deface_string = ''
        self.db.valid_prepositions = []
        self.db.objects_interacting_with = []
        self.db.objects_nearby = []
        self.db.location_objects_nearby = []
        # add property for which body parts are on the person. Some may be near inexhaustible like hair or nail shavings
        #   and will need separate object_creation procedures to get them...
        # body-parts properties could be dictionaries that contain lists and dictionaries, or could be separate flat-properties.

    # make char creation system method and use it below to set traits etc.
    def rollStats(self):
        'Placeholder for stat-generation system'

        if self.db.menuvar == 1:
            self.msg('peasant chosen')
        if self.db.menuvar == 2:
            self.msg('farmer chosen')
        if self.db.menuvar == 3:
            self.msg('pilot chosen')
        self.db.strength = r.randint(1,100)
        self.db.agility = r.randint(1,100)
        self.db.constitution = r.randint(1,100)
        self.db.pilot = r.randint(1,100)

    def get_abilities(self):
        "simple hook to return ability scores as a tuple"
        #delete this later
        return self.db.strength, self.db.agility, self.db.constitution, self.db.pilot

    # this method is called by the 'look' command (see /md/src/commands/default/general.py)
    def return_appearance(self,looker):
        text = [self.db.object_title, self.db.description]        

        return text

    def at_before_move(self, destination):
        """
        Called just before starting to move
        this object to destination.

        destination - the object we are moving to

        If this method returns False/None, the move
        is cancelled before it is even started.
        """
        # uncomment that later and add support for has_perm to use this for restricted areas?
        #return has_perm(self, destination, "can_move")
        return True


    def announce_move_from(self, destination):
        """
        Called if the move is to be announced. This is
        called while we are still standing in the old
        location.

        destination - the place we are going to.
        """
        if not self.location:
            return
        name = self.name
        loc_name = ""
        loc_name = self.location.name
        dest_name = destination.name

        # MistDude added this to customize our movement descriptions
        #  Basically this detects if the exits moved from and to have articles or not
        #  already, then either uses the one that it has, or adds one in.
        loc_dest_list = [loc_name,dest_name]
        loc_dest_articles = ['the','the']
        article_list = ['a','an','the','some']
        for article in [part.lower().split()[0] for i, part in list(enumerate(loc_dest_list)) if part.lower().split()[0] in article_list]:
            loc_dest_articles[i] = article
            if loc_name.lower().startswith(article):
                loc_name = (loc_name.split()[0].lower() + ' ' + ' '.join(loc_name.split()[1:len(loc_name)])).lstrip(article).strip()
            if dest_name.lower().startswith(article):
                dest_name = (dest_name.split()[0].lower() + ' ' + ' '.join(dest_name.split()[1:len(dest_name)])).lstrip(article).strip()

        watcher_string = name + ' leaves toward ' + loc_dest_articles[0] + ' ' + dest_name + '.'
        self.location.msg_contents(watcher_string, exclude = self)

        mover_string = 'You leave heading toward ' + loc_dest_articles[0] + ' ' + dest_name + ' from ' + loc_dest_articles[1] + ' ' + loc_name + '.'
        self.msg(mover_string)

    def announce_move_to(self, source_location):
        """
        Called after the move if the move was not quiet. At this
        point we are standing in the new location.

        source_location - the place we came from
        """

        name = self.name
        if not source_location and self.location.has_player:
            # This was created from nowhere and added to a player's
            # inventory; it's probably the result of a create command.
            string = "You now have %s in your possession." % name
            self.location.msg(string)
            return

        src_name = "nowhere"
        loc_name = self.location.name
        if source_location:
            src_name = source_location.name

        # same deal as above in announce_move_from, detecting exit articles and doing
        #  what needs to be done to use/add it to the announcement
        loc_src_list = [loc_name,src_name]
        loc_src_articles = ['the','the']
        article_list = ['a','an','the','some']
        for article in [part.lower().split()[0] for i, part in list(enumerate(loc_src_list)) if part.lower().split()[0] in article_list]:
            loc_src_articles[i] = article
            if loc_name.lower().startswith(article):
                loc_name = (loc_name.split()[0].lower() + ' ' + ' '.join(loc_name.split()[1:len(loc_name)])).lstrip(article).strip()
            if src_name.lower().startswith(article):
                src_name = (src_name.split()[0].lower() + ' ' + ' '.join(src_name.split()[1:len(src_name)])).lstrip(article).strip()

        watcher_string = name + ' approaches from ' + loc_src_articles[0] + ' ' + src_name + '.'
        self.location.msg_contents(watcher_string, exclude = self)

#        string = "%s arrives to %s from %s."
#        self.location.msg_contents(string % (name, loc_name, src_name), exclude=self)

    def at_after_move(self, source_location):
        """
        Called after move has completed, regardless of quiet mode or not.
        Allows changes to the object due to the location it is now in.

        source_location - where we came from. This may be None.
        """
        self.execute_cmd('look')
