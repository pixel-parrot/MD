'''
This module defines various methods for formatting text.
'''
from __future__ import division
import math

class FormatLine:
    '''
    This class contains methods for formatting text.    
    '''

    LINE_WIDTH = 80

    BUFFER_WIDTH = 8


    def breakLine(self, input_text_list, *center_title):
        '''
        Creates line breaks at or before the value of self.LINE_WIDTH.

        If the optional argument center_title is given, the room title
            will be centered. It can be any non-zero, non-None, or non-empty
            argument. The suggested form should be 'title'.
        '''

        # remove any blank line entries that come from the input
        for line in [line for line in input_text_list if line == '']:
            input_text_list.remove(line)

        # this will just be used to determine if the optional argument is present
        args = [self, input_text_list, center_title]

        # if the optional arguement to center a title is selected, it removes this line
        #  from the input_text_list and stores it in title_list so we can work with it
        #  separately
        title_list = []
        title = ''
        if args[2]:
            title_list.append(input_text_list[0])
            input_text_list.remove(input_text_list[0])
            title = self.centerText(title_list)

        # this removes any possible double or triple spaces that might be in the lines
        input_text_list_enum = list(enumerate(input_text_list))
        for i, line in input_text_list_enum:
            input_text_list.remove(input_text_list_enum[i][1])
            input_text_list.insert(i, line.strip().replace('  ',' ').replace('   ',' '))

        # set up a sublist of words for each line of text in input_text_list
        #  this will be the list where we actually apply the line breaks, later
        #  we join these lists of lists back into single lists
        input_text_words = []
        for line in input_text_list:
            input_text_words.append(line.split())

        # here we go through each line of text, then each column of the line
        #  once we reach the desired column width, we prepend the word that
        #  hit the width with a line break
        for i, line in list(enumerate(input_text_list)):
            word_count = 0
            column_count = 1
            columns_since_space = 1
            for column in line:
                if column.isspace():
                    word_count += 1
                    columns_since_space = 0
                if (column_count / self.LINE_WIDTH).is_integer(): 
                    input_text_words[i][word_count] = '\n' + input_text_words[i][word_count]
                    column_count = columns_since_space
                column_count += 1
                columns_since_space += 1

        # here we create our output text by joining the outer_list's inner elements with
        #  spaces and put a line break at the front. We do that because each 'line' from
        #  our input text serves separate purposes, like 'room/character title',
        #  'description', 'objects in room', 'exits in room', and so forth.
        output_text = []
        for outer_list in input_text_words:
            output_text.append('\n' + ' '.join(outer_list))

        # the centering method adds an extra space to a title, so we remove that if
        #   title centering is desired. In either case we add a final line break for
        #   aesthetics.
        if args[2]:
            output_text[0] = output_text[0].lstrip('\n')
            return title + ''.join(output_text) + '\n'
        else:
            return ''.join(output_text) + '\n'

    
    def blockText(self, input_text_list):
        '''
        Formats text into a block-style.
        '''

        input_text_list_enum = list(enumerate(input_text_list))
        for i, line in input_text_list_enum:
            input_text_list.remove(input_text_list_enum[i][1])
            input_text_list.insert(i, line.strip().replace('  ',' ').replace('   ',' '))

        original_LINE_WIDTH = self.LINE_WIDTH
        self.LINE_WIDTH = self.LINE_WIDTH - (self.BUFFER_WIDTH * 2)
        output_text = self.breakLine(input_text_list)
        output_text = output_text.replace('\n','\n' + ' ' * self.BUFFER_WIDTH)
        self.LINE_WIDTH = original_LINE_WIDTH
        
        return output_text

    
    def centerText(self, input_text_list, *block):
        '''
        Centers text on the screen.             

        When calling the method, if given only the input_text_list argument, it    
            will center text normally, using self.LINE_WIDTH.

        A second, optional argument is also valid. This will center the
            text but will do so in a block-text style, using self.LINE_WIDTH
            and self.BUFFER_WIDTH to define the line length.
        This optional argument can be any non-zero value, non-None value, or
            a non-empty string. For clarity purposes it is recommended that
            the string 'block' be used as the optional argument.
        '''
            
        input_text_list_enum = list(enumerate(input_text_list))
        for i, line in input_text_list_enum:
            input_text_list.remove(input_text_list_enum[i][1])
            input_text_list.insert(i, line.strip().replace('  ',' ').replace('   ',' '))

        args = [self,input_text_list,block]

        screen_center = int(math.modf(self.LINE_WIDTH / 2)[1])

        original_LINE_WIDTH = self.LINE_WIDTH
        if args[2]:
            self.LINE_WIDTH = self.LINE_WIDTH - (self.BUFFER_WIDTH * 2)
        output_text = self.breakLine(input_text_list)
        output_text_list = output_text.split('\n')
        for i, line in enumerate(output_text_list):
            line_center = int(math.modf(len(line) / 2)[1]) + 1
            front_buffer = screen_center - line_center
            line = ' ' * front_buffer + line
            output_text_list[i] = line
        output_text_list[len(output_text_list)-1] = output_text_list[len(output_text_list)-1].strip()
        output_text = '\n'.join(output_text_list)
        self.LINE_WIDTH = original_LINE_WIDTH

        return output_text
