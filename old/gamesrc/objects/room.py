"""
Template module for Rooms

Copy this module up one level and name it as you like, then
use it as a template to create your own Objects.

To make the default commands (such as @dig) default to creating rooms
of your new type, change settings.BASE_ROOM_TYPECLASS to point to
your new class, e.g.

settings.BASE_ROOM_TYPECLASS = "game.gamesrc.objects.myroom.MyRoom"

Note that objects already created in the database will not notice
this change, you have to convert them manually e.g. with the
@typeclass command.

"""

from ev import Room as DefaultRoom
from src.utils import search

class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    def at_object_creation(self):
        # This is the database entry for a room, called 'description'. We can set the description using the @py command within the game on the fly like: @py <roomname>.db.description = 'text'
        # Alternatively we can also set the description in a batch fileautomatically by adding after the creation command: <roomname>.db.descrption = 'text'
        # setting up the room title database entry
        self.db.title = ''
        # These will typically begin and end a room description text, with other stuff
        #   that may appear between them.
        self.db.description_start = ''
        self.db.description_end = ''
        # setting up optional directional description strings. Where applicable these will
        #   contain object descriptions in those areas and characters near them, right
        #   between the room's main description_start and description_end strings. I think
        #   all we will need are the four cardinal directions, since for the most part these
        #   are just general indicators of where we'll be placing the string in relation to
        #   other room details. These will likely end up being dynamically set, based on what
        #   objects are in the room at the time and what they are doing, etc.
        self.db.description_north = ''
        self.db.description_south = ''
        self.db.description_east = ''
        self.db.description_west = ''
        # setting coordinates entry
        self.db.coordinates = ()

    # this method is called by the 'look' command 
    def return_appearance(self,looker):
        # tag_character holds all OBJECTS with the tag 'character'
        tag_character = search.search_object_tag('character')
        tag_exit = search.search_object_tag('exit')
        tag_thing = search.search_object_tag('thing')
        tag_container = search.search_object_tag('container')
        tag_stationary = search.search_object_tag('stationary')
        tag_contained = []
        for things in [container.contents for container in tag_container if container in self.contents]:
            tag_contained.extend(things)
    
        # examples of setting a tag can be seen in the test_batch.py file in the directory /md/game/gamesrc/world. It can also be set in a similar way in the game on the fly with @py <syntax>
        characters_in_room = []
        for thing in self.contents:
            if thing in tag_character:
                characters_in_room.append(thing.key)
        non_characters_in_room = []
        for thing in self.contents:
            if thing not in tag_character and thing not in tag_exit and thing not in tag_thing:
                non_characters_in_room.append(thing.key)

        things_in_room = []
        for thing in self.contents:
            if thing in tag_container:
                if 'stack' in thing.aliases.all():
                    container_string = 'a stack of ' + thing.db.stack_size + ' ' + thing.db.container_key
                else:
                    container_string = 'a pile of ' + thing.db.stack_size + ' ' + thing.db.container_key
                things_in_room.append(container_string)
            elif thing in tag_thing:
                things_in_room.append(thing.key)

        # exits
        exits_in_room = []
        for thing in self.contents:
            if thing in tag_exit:
                exits_in_room.append(thing.key)

        # objects near other objects in_room_descriptions
        #### first find stationary landmarks that have in_room_description_default strings, these would be the
        ####    dominant landmarks. During room creation and item creation, stationary landmarks that do not
        ####    have a string for this property would be ones that are near other stationary landmarks.
        dominant_landmarks = []
        dominant_landmarks.extend([obj for obj in self.contents if 'stationary' in obj.tags.all() and len(obj.db.in_room_description_default)])
        #looker.msg('dominant_landmarks: ' + str([obj.dbref for obj in dominant_landmarks]))
        for landmark in dominant_landmarks:
            landmark.db.in_room_description = landmark.db.in_room_description_default
            # removing any None objects from the list leftover from object deletion
            for obj in landmark.db.objects_nearby:
                if None in landmark.db.objects_nearby:
                    landmark.db.objects_nearby.remove(None)
            # creating the additional string added to the in_room_description for
            #   any objects near the landmark
            if landmark.db.objects_nearby:
                landmark.db.in_room_description = landmark.db.in_room_description + ' Near this ' + landmark.key + ' '
                # getting nearby objects that are not the looker
                nearby_objects = [obj for obj in landmark.db.objects_nearby if obj not in tag_contained and obj <> looker]
                for i,obj in enumerate(nearby_objects):
                    object_string = obj.db.object_title
                    # setting up character string for if name is known
                    if 'character' in obj.tags.all() and looker.db.characters_met[obj] == False:
                        object_string = ' a ' + obj.db.object_title
                    elif 'character' in obj.tags.all():
                        object_string = looker.db.characters_met[obj]
                    if i == 0 and i+1 == len(nearby_objects):
                        if 'stack' in obj.aliases.all() or 'pile' in obj.aliases.all():
                            landmark.db.in_room_description = landmark.db.in_room_description + ' is ' + container_string + '.'
                        else:
                            landmark.db.in_room_description = landmark.db.in_room_description + ' is ' + object_string + '.'
                    if i == 0 and len(nearby_objects) == 2:
                        if 'stack' in obj.aliases.all() or 'pile' in obj.aliases.all():
                            landmark.db.in_room_description = landmark.db.in_room_description + ' is ' + container_string + ' and '
                        else:
                            landmark.db.in_room_description = landmark.db.in_room_description + ' is ' + object_string + ' and '
                    elif i == 0 and i+1 <> len(nearby_objects):
                        if 'stack' in obj.aliases.all() or 'pile' in obj.aliases.all():
                            landmark.db.in_room_description = landmark.db.in_room_description + ' is ' + container_string + ', '
                        else:
                            landmark.db.in_room_description = landmark.db.in_room_description + ' is ' + object_string + ', '
                    elif i+1 <> len(nearby_objects):
                        if 'stack' in obj.aliases.all() or 'pile' in obj.aliases.all():
                            landmark.db.in_room_description = landmark.db.in_room_description +  container_string + ' and '
                        else:
                            landmark.db.in_room_description = landmark.db.in_room_description + object_string + ' and '
                    elif i <> 0 and i+1 == len(nearby_objects):
                        if 'stack' in obj.aliases.all() or 'pile' in obj.aliases.all():
                            landmark.db.in_room_description = landmark.db.in_room_description +  container_string + '.'
                        else:
                            landmark.db.in_room_description = landmark.db.in_room_description + object_string + '.'


        # stationary objects in room descriptions
        self.db.description_north = ''
        self.db.description_south = ''
        self.db.description_east = ''
        self.db.description_west = ''
        for thing in self.contents:
            if thing in tag_stationary:
                if thing.db.in_room_location == 'north':
                    self.db.description_north = self.db.description_north + ' ' + thing.db.in_room_description
                if thing.db.in_room_location == 'south':
                    self.db.description_south = self.db.description_south + ' ' + thing.db.in_room_description
                if thing.db.in_room_location == 'east':
                    self.db.description_east = self.db.description_east + ' ' + thing.db.in_room_description
                if thing.db.in_room_location == 'west':
                    self.db.description_west = self.db.description_west + ' ' + thing.db.in_room_description

        # converting the lists into strings and cleaning them up by removing the brackets, apostrophes, and the unicode marker (u). 
        char_text = ''
        if characters_in_room: char_text = 'Characters in room: ' + str(characters_in_room).strip('[').strip(']').replace("u'",'').replace("'",'')
        non_char_text = ''
        if non_characters_in_room: non_char_text = 'Weirdos in room: ' + str(non_characters_in_room).strip('[').strip(']').replace("u'",'').replace("'",'')
        thing_text = ''
        if things_in_room: thing_text = 'Things in room: ' + str(things_in_room).strip('[').strip(']').replace("u'",'').replace("'",'')
        exit_text = ''
        if exits_in_room: exit_text = 'Exits in room: ' + str(exits_in_room).strip('[').strip(']').replace("u'",'').replace("'",'')

        directional_room_text = self.db.description_north + ' ' + self.db.description_east + ' ' + self.db.description_west + ' ' + self.db.description_south 
        combined_room_text = self.db.description_start + ' ' + directional_room_text + ' ' + self.db.description_end
        combined_room_text = combined_room_text.replace('     ',' ').replace('    ',' ').replace('   ',' ').replace('  ',' ')
        
        text = [self.db.title, combined_room_text, char_text, thing_text, non_char_text, exit_text]

        return text


    def at_object_receive(self, obj, source_location):
        if 'character' in obj.tags.all():
            for char in [thing for thing in self.contents if 'character' in thing.tags.all() and thing <> obj]:
                if char not in obj.db.characters_met:
                    obj.db.characters_met[char] = False
                if obj not in char.db.characters_met:
                    char.db.characters_met[obj] = False




