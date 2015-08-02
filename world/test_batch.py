
#There must be at least one blank or commented line at the top, beforethe header.
#

'''
IMPORTANT NOTE!!!!!!!!!!!!!
This sets Nexus as the location and Home location for some created objects.
First you will have to uncomment the Nexus creation code below, then run
@batchcode test_batch
within the game so that everything is set up correctly.
Next you can delete the 'limbo' area if you want to.
Finally you'll have to edit your /md/server/conf/settings.py file to change the
default home locations to whatever the dbref for Nexus is on your instance
of the game.
DEFAULT_HOME = '#<dbref>'
START_LOCATION = '#<dbref>'
You can get the dbref of Nexus from using @objects in the game.
You should only have to do this once, since I have set my settings file to
not be tracked for changes. Once you pull the settings file from my
MistDude.git branch, you can change those locations to whatever number
they get. As long as you make sure settings.py isn't tracked for changes in
git, any changes I make or you make to it won't be shared. --For now we'll
do it that way.
'''

#HEADER

from evennia import create_object, search_object
from evennia import DefaultObject
from typeclasses import characters
from typeclasses import rooms
from typeclasses import exits
from typeclasses import object_template
from typeclasses import stackable_object
from typeclasses import stationary_object
import commands.default_cmdsets 


#CODE (create testing rooms) arena

# create nexus
#nexus = create_object(rooms.Room, key = 'The Nexus', aliases = ['Nexus','nexus','The nexus','the Nexus','the nexus'], location = None)
#nexus.db.description = 'A dark, menacing vibration fills this place. The repeated creation, destruction, and manipulation of Realities has taken its toll on the fabric of space-time. Everything about this place feels as if it is only half-phased into the physical world and could easily return to the inifity of obilivion from which some cruel god imagined it.'
#nexus.db.title = '--An otherwordly plane--'
#nexus.tags.add('room')
##
### announce room creations
##caller.msg('Rooms created: %s' % nexus.key)
#
# this fetches the room-object 'Nexus', so that we can use it to assign locations and destinations
nexus = search_object('Nexus')[0]
#
#arena = create_object(rooms.Room, key = 'The Arena', aliases = ['Arena'], location = None)
#arena.db.title = '--An oval tile-and-stone venue--'
#arena.db.description = 'A massive stadium of beige stone blocks assembles around an ornately tiled elliptical field, each accomodative to a generous number of spectators or participants. The stone ledges that act as seating create an unusual contrast in their tidy and sterile appearance against the mosaic of dry, dark seas that stain the tiled playing-field floor. Lacking the activity and hubbub of festivities, the air hangs heavily with a stale quality.' 
#arena.tags.add('room')
### create exits back and forth and add the 'exit' tag to them
#arena_to_nexus = create_object(exits.Exit, key = 'Nexus', aliases = ['the nexus'], location = arena, destination = nexus)
#arena_to_nexus.tags.add('exit')
#nexus_to_arena = create_object(exits.Exit, key = 'Arena', aliases = ['the arena'], location = nexus, destination = arena)
#nexus_to_arena.tags.add('exit')
##caller.msg('Rooms created: %s' % arena.key)
##caller.msg('Exits created: %s, %s' % (arena_to_nexus.key, nexus_to_arena.key))
#
#void = create_object(rooms.Room, key = 'The Void', aliases = ['void'], location = None)
#void.db.title = "--Nothing to see here!--"
#void.tags.add('room')
#void.tags.add('void')
#
#
## updating existing rooms with newly added properties
#arena = search_object('arena')[0]
#arena.db.description_start = arena.db.description
#arena.db.description_end = ''
#arena.db.description_north = ''
#arena.db.description_south = ''
#arena.db.description_east = ''
#arena.db.description_west = ''
#nexus = search_object('nexus')[0]
#nexus.db.description_start = nexus.db.description
#nexus.db.description_end = ''
#nexus.db.description_north = ''
#nexus.db.description_south = ''
#nexus.db.description_east = ''
#nexus.db.description_west = ''
#void = search_object('void')[0]
#void.db.description_start = void.db.description
#void.db.description_end = ''
#void.db.description_north = ''
#void.db.description_south = ''
#void.db.description_east = ''
#void.db.description_west = ''
#
#
#market1 = create_object(rooms.Room, key = 'The Market', aliases = ['market'], location = None)
#market1 = search_object('market')[0]
#market1.db.title = "--A dingy market plaza--"
#market1.db.description_start = "The dirt roads running through the market are heavily rutted and have fallen into disrepair. Despite this, the plaza is obviously heavily used on the days that merchants and those peddling comestables visit; the somewhat permanent stands, tents, and booths all appear sturdy and in relative good-repair."
#market1.db.description_north = "Makeshift dwellings populate the northern edges of the plaza, with a few very narrow, filthy alleys occasionally breaking the wall of mud, stones, and planks."
#market1.db.description_end = "The main thoroughfare leaves the plaza center to the east and west, toward other districts of the city."
#market1.db.description_south = ''
#market1.db.description_east = ''
#market1.db.description_west = ''
#
#arena = search_object('arena')[0]
#arena_to_market = create_object(exits.Exit, key = 'east', aliases = ['the market', 'market'], location = arena, destination = market1)
#arena_to_market.tags.add('exit')
#
#market_to_arena = create_object(exits.Exit, key = 'west', aliases = ['the arena', 'arena'], location = market1, destination = arena)
#market_to_arena.tags.add('exit')
#
#
#
#
##CODE (create characters) frito, camacho, aragorn, gandalf
#
#nexus = search_object('Nexus')[0]
#arena = search_object('Arena')[0]
#
#frito = create_object(characters.Character, key = "Frito", location = nexus, home = nexus)
##make it so anyone can pick up the char
#frito.locks.add('get:all()') #default for char typeclass is get:false()
#frito.tags.add('character')
#frito.db.description = 'This male human has short, dark hair parted to one side. He is wearing a long-sleeved polyester shirt that displays the words "Attourney at Law" in large letters vertically down both arms. There is a meaningful twinkle in his eyes at the mention of sex or money.'
#frito.db.honorific_prefix = 'Senyor'
#frito.db.first_name = 'Frito'
#frito.db.middle_name = 'Lay'
#frito.db.last_name = 'Pendejo'
#frito.db.honorific_suffix = 'Esquire'
#frito.db.object_title = ' '.join([frito.db.honorific_prefix, frito.db.first_name, frito.db.middle_name, frito.db.last_name, frito.db.honorific_suffix])
#
#camacho = create_object(characters.Character, key = "Camacho", location = nexus, home = nexus)
#camacho.tags.add('character')
#camacho.db.description = 'Huge knotted muscles, long, braided black hair, a strongly-set jaw, and a booming voice give this imposing figure an air of presidential authority. You don''t want to fuck with him. Often wearing sleeveless polyester formalwear, he is usually seen carrying his favourite automatic rifle.'
#camacho.db.honorific_prefix = 'President'
#camacho.db.first_name = 'Dwayne'
#camacho.db.middle_name = 'Elizondo Mountain-Dew Herbert'
#camacho.db.last_name = 'Camacho'
#camacho.db.honorific_suffix = 'Actor and Porn-Star'
#camacho.db.object_title = ' '.join([camacho.db.honorific_prefix, camacho.db.first_name, camacho.db.middle_name, camacho.db.last_name, camacho.db.honorific_suffix])
#
#aragorn = create_object(characters.Character, key = 'Aragorn', location = nexus, home = nexus)
#aragorn.tags.add('character')
#aragorn.db.description = 'Such king. So return. Wow.'
#aragorn.db.first_name = 'Aragorn'
#aragorn.db.middle_name = 'Sonof'
#aragorn.db.last_name = 'Arathorn'
#aragorn.db.object_title = ' '.join([aragorn.db.honorific_prefix, aragorn.db.first_name, aragorn.db.middle_name, aragorn.db.last_name, aragorn.db.honorific_suffix])
#
#gandalf = create_object(characters.Character, key = 'Gandalf', location = nexus, home = nexus)
#gandalf.tags.add('character')
#gandalf.db.description = 'Always showing up when he''s most needed and least expected. Witty little cunt, m8.'
#gandalf.db.first_name = 'Gandalf'
#gandalf.db.last_name = 'Stormcrow'
#gandalf.db.honorific_suffix = 'The White'
#gandalf.db.object_title = ' '.join([gandalf.db.honorific_prefix, gandalf.db.first_name, gandalf.db.middle_name, gandalf.db.last_name, gandalf.db.honorific_suffix])
#
## announce character creations
#caller.msg("Characters created: %s, %s, %s, %s" % (frito.key, camacho.key, aragorn.key, gandalf.key))
##
#caller.msg("Dbrefs created: %s - %s" % (arena.dbref,gandalf.dbref))

#CODE (create objects) rock, rock

nexus = search_object('Nexus')[0]

market = search_object('The Market')[0]
market.tags.add('room')
pillory1 = create_object(stationary_object.StationaryObject, key = 'pillory', aliases = ['stocks'], location = market, home = market)
pillory1.db.object_title = 'a rough wooden restraint'
pillory1.db.description = "Two broad oaken boards hinged horizontally and fastened to a thick, waist-high center post stand here. Each board has three mirrored semicurcular cuts, one large in the center and one smaller on each side which, when closed and locked, form the holes that secure an unfortunate offender's neck and wrists in a considerably unaccomodaing fashion."
pillory1.db.adjective_list.extend(['rough'])
pillory1.db.in_room_location = 'north'
pillory1.db.in_room_description_default = 'A rough-hewn, sturdy oak pillory stands near the center of this part of the plaza, inviting scowls, snickers, and the occasional volley of vegetables from visitors venerable and vulgar alike.'
pillory1.db.valid_prepositions = ['on', 'under', 'near', 'next to', 'on top of', 'beside', 'by']

menhir = create_object(stationary_object.StationaryObject, key = 'menhir', aliases = ['statue', 'monolith'], location = market, home = market)
menhir.db.object_title = 'a huge stone statue'
menhir.db.description = "Beginning at its bottom a substantial slab of rough, unworked stone, this imposing monolith gradually tapers, gaining shape as it looms ever higher over the plaza. Crowning the monument in impossibly detailed sculpture sits the ubiquitous icon of the theocracy: bare collarbone and muscle-ridged neck support a stern, sinewy jaw that regards the market below mouth-open and teeth faintly bared in an expression suspended mid-judgement. At the cheekbones the sculpture ends flat. An abrupt half-head deliberately returns to raw, unpolished rock. Those divinely chosen to bear the burdens and duties of Service are gifted with voices informed by Truth; those deserving punishment shall find it whether or not there were eyes to witness."
menhir.db.in_room_location = 'south'
menhir.db.in_room_description_default = 'Facing the north and overlooking the entire market towers a severely sculpted menhir. The top appears to be decorated by a huge, unfinished half-bust of a man.'
menhir.db.valid_prepositions = ['near', 'next to', 'beside', 'by']

menhir = search_object('menhir')[0]
pillory2 = create_object(stationary_object.StationaryObject, key = 'pillory', aliases = ['stocks'], location = market, home = market)
pillory2.db.object_title = 'a crude wooden restraint'
pillory2.db.description = "Two broad oaken boards hinged horizontally and fastened to a thick, waist-high center post stand here. Each board has three mirrored semicurcular cuts, one large in the center and one smaller on each side which, when closed and locked, form the holes that secure an unfortunate offender's neck and wrists in a considerably unaccomodaing fashion."
pillory2.db.adjective_list.extend([crude, wooden])
pillory2.db.in_room_location = 'south'
pillory2.db.in_room_description_default = ''
pillory2.db.valid_prepositions = ['on', 'under', 'near', 'next to', 'on top of', 'beside', 'by']

pillory2.db.location_objects_nearby = [menhir]
menhir.db.location_objects_nearby = [pillory2]
menhir.db.objects_nearby = [pillory2]

pogostick = create_object(stackable_object.StackableObject, key = 'pogo stick', location = nexus, home = nexus)
pogostick.db.object_title = 'a fucking pogo stick, m8'
pogostick.db.description = "wtf do you expect, it's a goddamn pogo stick you witty little cunt"

pogostick2 = create_object(stackable_object.StackableObject, key = 'pogo stick', location = nexus, home = nexus)
pogostick2.db.object_title = 'just another pogo stick, surprised?'
pogostick2.db.description = "we're all lookin' for answers, bud. ain't finding none here either."

pogostick3 = create_object(stackable_object.StackableObject, key = 'pogo stick', location = nexus, home = nexus)
pogostick3.db.object_title = 'pogo stickier than ever'
pogostick3.db.description = "pogo stick you like a hurricane"

pogostick4 = create_object(stackable_object.StackableObject, key = 'pogo stick', location = nexus, home = nexus)
pogostick4.db.object_title = 'such pogo stick'
pogostick4.db.description = "wow"

pogostick5 = create_object(stackable_object.StackableObject, key = 'pogo stick', location = nexus, home = nexus)
pogostick5.db.object_title = 'this pogo stick is special'
pogostick5.db.description = "a unique pogo stick with a soul of its own"


rock = create_object(stackable_object.StackableObject, key = 'rock', location = market, home = nexus)
rock.db.object_title = 'a fucking rock, m8'
rock.db.description = "wtf do you expect, it's a goddamn rock you witty little cunt"
rock.db.location_objects_nearby.extend([rock.location, pillory2])

rock2 = create_object(stackable_object.StackableObject, key = 'rock', location = market, home = nexus)
rock2.db.object_title = 'just another rock, surprised?'
rock2.db.description = "we're all lookin' for answers, bud. ain't finding none here either."
rock2.db.location_objects_nearby.extend([rock2.location, pillory2])

rock3 = create_object(stackable_object.StackableObject, key = 'rock', location = market, home = nexus)
rock3.db.object_title = 'rockier than ever'
rock3.db.description = "rock you like a hurricane"
rock3.db.location_objects_nearby.extend([rock3.location, pillory2])

rock4 = create_object(stackable_object.StackableObject, key = 'rock', location = market, home = nexus)
rock4.db.object_title = 'such rock'
rock4.db.description = "wow"
rock4.db.location_objects_nearby.extend([rock4.location, pillory2])

rock5 = create_object(stackable_object.StackableObject, key = 'rock', location = market, home = nexus)
rock5.db.object_title = 'this rock is special'
rock5.db.description = "a unique rock with a soul of its own"
rock5.db.location_objects_nearby.extend([rock5.location, pillory2])

pillory2.db.objects_nearby.extend([rock, rock2, rock3, rock4, rock5])

caller.msg("Objects created: %s, %s, %s, %s, %s, " % (rock.key, rock2.key, rock3.key, rock4.key, rock5.key))

#caller.msg("Dbrefs created: %s, %s" % (pogostick.dbref, rock5.dbref))

# change this manually when you add any new objects to the beginning or end of the batch file,
#   this lets you use the 'dbat' command in the game to quickly delete the last objects you
#   created in this file. Keep this block at the very end of the file. fbat is the first
#   object created in the batch file and lbat is the last object created in the batch file.
#caller.db.fbat = pogostick.dbref
#caller.db.lbat = rock5.dbref
caller.cmdset.add('default_cmdsets.PlayerCmdSet')

