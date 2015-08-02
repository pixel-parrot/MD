# Stackable object related stuff. 

#from game.gamesrc.objects.object import * 
from typeclasses.object_template import * 
from tools.text_tools import TextTools
from tools.list_tools import ListTools as LT
#from evennia import Object as DefaultObject
from evennia import DefaultObject
from evennia.utils import search
import commands.default_cmdsets
import evennia.commands.cmdset
from evennia import create_object
import random as r

class StackableObject(DefaultObject):
    '''
    at_before_move(destination)             - called just before moving object
                    to the destination. If returns False, move is cancelled.
    announce_move_from(destination)         - called in old location, just
                    before move, if obj.move_to() has quiet=False
    announce_move_to(source_location)       - called in new location, just
                    after move, if obj.move_to() has quiet=False
    at_after_move(source_location)          - always called after a move has
                    been successfully performed.
    at_object_leave(obj, target_location)   - called when an object leaves
                    this object in any fashion
    at_object_receive(obj, source_location) - called when this object receives
                    another object
    at_drop(dropper)          - called when this object has been dropped.
    at_get(getter)            - called after object has been picked up.
    contents (list of Objects, read-only) - returns all objects inside this
    move_to(destination, quiet=False, emit_to_obj=None, use_destination=True)
    '''
   
    def stackSize(self):
        # measure size of pile, and set stack_size attribute string
        if len(self.contents) < 2: 
            self.db.stack_size = 'should_be_deleted'
        if len(self.contents) == 2: 
            self.db.stack_size = 'two'
        if len(self.contents) >= 3 and len(self.contents) <= 4: 
            self.db.stack_size = 'a few'
        if len(self.contents) >= 5 and len(self.contents) <= 7:
            self.db.stack_size = 'several'
        if len(self.contents) >= 8 and len(self.contents) <= 20:
            self.db.stack_size = 'some'
        if len(self.contents) >= 21:
            self.db.stack_size = "numerous"


    def at_object_creation(self):
        if self.key.endswith('_stack'):
            key = self.key.rstrip('stack').rstrip('_')
            alias_string = TextTools.pluralKey(TextTools(),key)
            self.aliases.add(alias_string)
            ''' IN PROGRESS : delete this note below later'''
            # testing out having a generic alias of 'pile' that should 
            #   end up being auto validated by the rest of the CmdGet system
            self.aliases.add('pile')
            self.db.stack_size = ''
            self.stackSize()
            self.db.container_key = alias_string
            self.tags.add('thing')
            self.tags.add('container')
            self.tags.add(self.key)
            self.db.object_title = alias_string
            self.db.description = ''
            self.db.deface_string = ''
            self.db.valid_prepositions = ['on', 'in', 'from', 'inside']
            self.db.objects_nearby = []
            self.db.location_objects_nearby = []
            self.db.objects_interacting_with = []
            # when a new stack-object is created, at this point we'll give it
            #   the same location_objects_nearby and objects_nearby as its location
            if 'room' not in self.location.tags.all():
                self.db.location_objects_nearby.append(self.location.db.location_objects_nearby[0])
            else:
                self.db.location_objects_nearby.append(self.location)
            self.db.objects_nearby.append(self.location)
            if 'room' not in self.location.tags.all():
                self.db.objects_nearby.append(self.location.location)
            self.db.objects_interacting_with.append(self.location)
            # collect any valid objects that can be stacked into this new stack
            for thing in [thing for thing in self.location.contents if thing <> self and thing.key in self.key and self.db.objects_interacting_with[0] == thing.db.objects_nearby[0] and self.db.location_objects_nearby[0] == thing.db.location_objects_nearby[0]]:
                thing.move_to(self,quiet=True)
        else:
            self.tags.add('thing')
            self.tags.add('stackable')
            self.db.object_title = ''
            self.db.description = ''
            self.db.deface_string = ''
            self.db.adjective_list = []
            self.db.adjective_string = ''
            self.db.object_owners = []
            self.db.object_possession_history = []
            self.db.location_objects_nearby = []
            self.db.objects_nearby = []
            self.db.objects_interacting_with = []


    def at_before_move(self, destination):
        # we only want to do the next operations if the object is not a stack,
        #  if the destination of the object is not a stack, and if there
        #  are no stack-objects of the same kind in the object's destination 
        if not self.key.endswith('_stack') and not destination.key.endswith('_stack') and not [stack for stack in destination.contents if stack.key.endswith('_stack') and self.key in stack.key]:
            # do the next lines if there are matching stackable objects in the destination
            if [thing for thing in destination.contents if thing.key == self.key and 'stackable' in thing.tags.all() and self.db.objects_interacting_with[0].db.location_objects_nearby[0] == thing.db.location_objects_nearby[0]]:
                if search.search_object_tag('void')[0].contents:
                    if not [old for old in search.search_object_tag(self.key + '_stack') if old in search.search_object_tag('void')[0].contents]:
                        # creating stack-object
                        create_object(self.typeclass, key = self.key + '_stack', location = destination, home = destination)
                    else:
                        old_container = [old for old in search.search_object_tag(self.key + '_stack') if old in search.search_object_tag('void')[0].contents][0]
                        old_container.db.location_objects_nearby = []
                        if not 'room' in self.location.tags.all():
                            old_container.db.location_objects_nearby.append(self.location.db.location_objects_nearby[0])
                        else:
                            old_container.db.location_objects_nearby.append(self.location)
                        old_container.db.objects_nearby = []
                        if 'room' not in self.location.tags.all():
                            old_container.db.objects_nearby.append(self.location.location)
                        old_container.db.objects_nearby.append(self.location)
                        old_container.db.objects_interacting_with = []
                        if 'container' in self.location.tags.all() and 'room' not in self.location.location.tags.all():
                            old_container.db.objects_interacting_with.append(self.location.location)
                        if 'container' in self.location.tags.all() and 'room' in self.location.location.tags.all():
                            old_container.db.objects_interacting_with.append(self.location.db.objects_nearby[1])
                        if 'room' in self.location.tags.all():
                            old_container.db.objects_interacting_with.append(destination)
                        if 'character' in self.location.tags.all():
                            old_container.db.objects_interacting_with.append(self.location)
                        old_container.move_to(destination,quiet=True)
                else:
                    # creating stack-object
                    create_object(self.typeclass, key = self.key + '_stack', location = destination, home = destination)

        return True


    def at_after_move(self,source_location):
        # when an object is moved, the objects_nearby and location_objects_nearby are
        #   updated depending on what the source_location and destination are:
        #### object moved from character to non-container location:
        ######## condition to stop new stack-objects from going through this part
        if source_location:
            if 'character' in source_location.tags.all() and 'container' not in self.location.tags.all():
                self.db.location_objects_nearby = []
                self.db.objects_nearby = []
                # make the character and object's location_objects_nearby match
                if source_location.db.location_objects_nearby:
                    self.db.location_objects_nearby.append(source_location.db.location_objects_nearby[0])
                # first objects_nearby is the room it is in
                self.db.objects_nearby.append(self.location)
                # second objects_nearby is the character it came from
                self.db.objects_nearby.append(source_location)
                # additional objects_nearby are those that are also near the charcacter
                nearby_objects_not_contained = []
                nearby_objects_not_contained = [obj for obj in source_location.db.objects_nearby if obj not in source_location.contents]
                for obj in [obj for obj in nearby_objects_not_contained if obj <> self]:
                    self.db.objects_nearby.append(obj)
                # update character's objects_nearby to include the dropped item
                source_location.db.objects_nearby.insert(1,self)
                source_location.db.objects_nearby = LT.dedupeList(LT(), source_location.db.objects_nearby)

                

        #### object moved to character
        ######## condition to stop new stack-objects from going through this part
        if source_location:
            if 'character' in self.location.tags.all():
                self.db.location_objects_nearby = []
                self.db.objects_nearby = []
                if self.location.db.location_objects_nearby:
                    self.db.location_objects_nearby.append(self.location.db.location_objects_nearby[0])
                if self.location.db.objects_nearby:
                    self.db.objects_nearby.append(self.location)
                    self.db.objects_nearby.append(self.location.location)
                self.location.db.objects_nearby.insert(1,self)
                self.location.db.objects_nearby = LT.dedupeList(LT(), self.location.db.objects_nearby)



        '''NEED TO IMPLEMENT'''
        #### object moved from character to container location directly (like a 'put')

        #### object moved to container location indirectly (when it merges into a container via a simple 'drop', or 'get', etc)
        if 'container' in self.location.tags.all():
            self.db.objects_nearby.insert(0, self.location)

        # update the container's contents to include the new destination object as
        #   an element in their own objects_nearby properties
        for obj in self.contents:
            obj.db.objects_nearby = []
            # update objs in container with container's, then insert the container as the first obj
            obj.db.objects_nearby = self.db.objects_nearby
            obj.db.objects_nearby.insert(0,self)

        self.db.objects_nearby = LT.dedupeList(LT(), self.db.objects_nearby)

        # this condition added since an object created newly won't have a source_location
        if source_location:
            if self.key + '_stack' in source_location.tags.all():
                source_location.stackSize()
                length = len(source_location.contents)
                if length == 1:
                    previous_location = source_location.location
                    source_location.move_to(self.search('the void', global_search = True),quiet=True)
                    source_location.contents[0].db.objects_nearby.remove(source_location)
                    source_location.contents[0].db.objects_nearby.insert(1,source_location.db.objects_nearby[1])
                    source_location.contents[0].move_to(previous_location,quiet=True)
                    # removing any references in other objects to this one, as of now it leaves
                    #   a "None" type object behind, which is deleted from the list in room.py
                    #   in return_appearance.
                    '''might not need this'''
                    if source_location.db.objects_nearby:
                        for obj in [obj for obj in source_location.db.objects_nearby if 'room' not in obj.tags.all()]:
                            print 'source_location: ' + source_location.key
                            print 'objects_nearby after del: ' + obj.key
                            print 'objects_nearby after del all: ' + str([obj.key for obj in source_location.db.objects_nearby])
                            obj.db.objects_nearby.remove(source_location)
                '''commented out for now since we might just delete stacks during maintenance'''
                #if length == 0:
                #    source_location.delete()

        # if a stack-object enters the same location as a matching stack-object we
        #  will merge them, so we have to handle the things inside of them
        if self.location.contents:
            for thing in [thing for thing in self.location.contents if thing.dbref <> self.dbref and 'container' in self.tags.all() and 'container' in thing.tags.all() and thing.key == self.key and self.db.location_objects_nearby[0] == thing.db.location_objects_nearby[0] and source_location in self.db.objects_nearby and source_location in thing.db.objects_nearby]:
            # move all objects from old container to new
                for contained in thing.contents:
                    contained.move_to(self, quiet = True)

        # if a stack-object enters a location with a compatible stackable object
        # this condition added since an object created newly won't have a source_location
        if source_location:
            if not 'void' in source_location.tags.all():
                for thing in [thing for thing in self.location.contents if 'stackable' in thing.tags.all() and thing.key + '_stack' in self.tags.all() and self.db.location_objects_nearby[0] == thing.db.location_objects_nearby[0] and source_location in self.db.objects_nearby and source_location in thing.db.objects_nearby]:
                    thing.move_to(self, quiet = True, emit_to_obj = None, use_destination = True)
            else:
                for thing in [thing for thing in self.location.contents if 'stackable' in thing.tags.all() and thing.key + '_stack' in self.tags.all() and self.db.location_objects_nearby[0] == thing.db.location_objects_nearby[0] and self.db.objects_interacting_with[0] in thing.db.objects_nearby]:
                    thing.move_to(self, quiet = True, emit_to_obj = None, use_destination = True)
                

        # if a stackable object enters a location with a compatible stack-object
        # this condition added since an object created newly won't have a source_location
        if source_location and self.db.objects_interacting_with:
            for thing in [thing for thing in self.location.contents if self.key + '_stack' in thing.tags.all() and 'stackable' in self.tags.all() and thing.db.location_objects_nearby[0] in self.db.location_objects_nearby and self.db.objects_interacting_with[0] in thing.db.objects_nearby]:
                self.move_to(thing, quiet = True)

        # clearing out the objects_interacting_with property
        # this condition added since an object created newly won't have a source_location
        if source_location:
            self.db.objects_interacting_with = []
            self.location.db.objects_interacting_with = []


    def return_appearance(self, looker):
        if 'container' in self.tags.all():
            self.stackSize()
            item_glanced = r.choice(self.contents).db.description
            text = [self.db.stack_size + ' ' + self.db.object_title, 'In this pile you happen to glance at one of the ' + self.db.object_title + ': ', item_glanced]
        else:
            text = [self.db.object_title, self.db.description]

        return text


    def at_object_receive(self, obj, source_location):
        tag_stack = search.search_object_tag(obj.key + '_stack')
        if self in tag_stack:
            self.stackSize()

        # updating the stack object to have it's nearest location_objects_nearby be the same
        #   as the source_location's nearest location_objects_nearby
        #self.db.location_objects_nearby.insert(0,source_location.db.location_objects_nearby[0])

        # here below need to add on 'true stack' functionality. Once a stack recieves an object that has the
        #   'true stack' property, then the appropriate tags will also be added to that stack. This will be used
        #   for determining how the 'true stack' will return appearances and how items will be put into it and out
        #   from it, as well as how it can be picked up and moved around, etc.
        #   It will also remove the 'pile' alias and replace it with a 'stack' alias. This
        #   distinction will be used, for example, in room.py's return_appearance method.


    def at_object_leave(self, obj, target_location):
        pass


    def at_object_delete(self):
        return True





