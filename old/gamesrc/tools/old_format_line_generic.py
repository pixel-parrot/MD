'''
This module defines various methods for formatting text.
'''
from __future__ import division
import math

class FormatLine:
    '''
    This class contains methods for formatting text.    
    '''

    # this sets where you want to break a line, default is 80 columns
    # to change the default, reset it before calling breakLine()
    # note that if there are words in the text longer than LINE_WIDTH,
    #    it won't work properly. If this is determined to be an issue at
    #    some point, I'll fix it.
    # This value should represent the width we want standard room
    #    descriptions to have.
    LINE_WIDTH = 80

    # this is used in the blockText and centerText methods to define how 
    #    large the space buffers on each side should be
    BUFFER_WIDTH = 8


    def breakLine(self, input_text):
        '''
        Creates line breaks at or before the value of self.LINE_WIDTH.
        '''

        # remove any starting and ending spaces as well as any triple and 
        #    double spaces (if there are any larger spacing errors, we'll have to 
        #    fix that by hand
        input_text = input_text.strip().replace('   ',' ').replace('  ',' ')
        # split the input text into a list
        input_text_list = input_text.split()
        # this will be used as an index for input_text_list,
        #    first word is at index zero
        word_count = 0
        # marks the column we are looking at in the current line
        column_count = 1
        # this will hold the value we use to reinitialize the column_count
        columns_since_space = 1

        for column in input_text:
            if column.isspace():
                # if we encounter a space, we are at the start of a new word
                word_count += 1
                # since we are on a space character, this resets to zero
                columns_since_space = 0
            if (column_count / self.LINE_WIDTH).is_integer(): 
                # when we reach the point where we want a line to not go further
                #    we prepend a line break to the appropriate word. If this happens
                #    to be exactly on a space character, word_count will reference
                #    the word after the space to get prepended with a line break.
                #    If we happen to be somwhere inside of a word, word_count will
                #    referece that word to be prepended.
                input_text_list[word_count] = '\n' + input_text_list[word_count]
                # once we break to a new line, we have to reinitialize column_count
                #    to start over. We have to use columns_since_space for this since
                #    we might have reached the "end of line" in the middle of a word,
                #    so we have to know from where to restart the count for the next
                #    line.
                column_count = columns_since_space
            # here we just increment these two variables in preparation for the next
            #    iteration
            column_count += 1
            columns_since_space += 1

        # this just adds a line break to the very start and end of any text. This is so we
        #    don't have to do it ourselves, and it is useful for making block text
        input_text_list[0] = '\n' + input_text_list[0]
        input_text_list[len(input_text_list)-1] = input_text_list[len(input_text_list)-1] + '\n'
        
        # finally we return the input_text_list elements as text joined together
        #    with spaces.
        return ' '.join(input_text_list)

    
    def blockText(self, input_text):
        '''
        Formats text into a block-style.
        '''

        # remove any starting and ending spaces as well as any triple and 
        #    double spaces (if there are any larger spacing errors, we'll have to 
        #    fix that by hand
        input_text = input_text.strip().replace('   ',' ').replace('  ',' ')
        # temporarily store the original value of self.LINE_WIDTH so that we
        #    can restore it later
        original_LINE_WIDTH = self.LINE_WIDTH
        # temporarily change the value of self.LINE_WIDTH so that line
        #    breaks will be added at or before the number of columns we
        #    want as an end-buffer
        self.LINE_WIDTH = self.LINE_WIDTH - (self.BUFFER_WIDTH * 2)
        # call the breakLine() method to add line breaks at the new LINE_WIDTH value
        output_text = self.breakLine(input_text)
        # create the beginning-buffer by replacing any line breaks with a line
        #    break plus the correct number of spaces
        output_text = output_text.replace('\n','\n' + ' ' * self.BUFFER_WIDTH)

        # restore self.LINE_WIDTH to original value (so that subsequent calls to
        #    breakLine() or blockText() work correctly)
        self.LINE_WIDTH = original_LINE_WIDTH
        
        return output_text

    
    def centerText(self, input_text, *block):
        '''
        Centers text on the screen.             

        When calling the method, if given only the input_text argument, it    
            will center text normally, using self.LINE_WIDTH.

        A second, optional argument is also valid. This will center the
            text but will do so in a block-text style, using self.LINE_WIDTH
            and self.BUFFER_WIDTH to define the line length.
        This optional argument can be any non-zero value, non-None value, or
            a non-empty string. For clarity purposes it is recommended that
            the string 'block' be used as the optional argument.
        '''
            
        # remove any starting and ending spaces as well as any triple and 
        #    double spaces (if there are any larger spacing errors, we'll have to 
        #    fix that by hand
        input_text = input_text.strip().replace('   ',' ').replace('  ',' ')
        # we use this to check if the optional argument is used
        args = [self,input_text,block]
        # defines the center of the screen
        screen_center = int(math.modf(self.LINE_WIDTH / 2)[1])

        original_LINE_WIDTH = self.LINE_WIDTH
        # checks if there is an optional argument, if there is it centers the text
        #    in a block-text format
        if args[2]:
            self.LINE_WIDTH = self.LINE_WIDTH - (self.BUFFER_WIDTH * 2)
        output_text = self.breakLine(input_text)
        output_text_list = output_text.split('\n')
        # find the center of each line and add an appropriate front-buffer
        for i, line in enumerate(output_text_list):
            line_center = int(math.modf(len(line) / 2)[1]) + 1
            front_buffer = screen_center - line_center
            line = ' ' * front_buffer + line
            output_text_list[i] = line
        # join the list elements again using line breaks as the delimiter
        output_text = '\n'.join(output_text_list)

        self.LINE_WIDTH = original_LINE_WIDTH

        return output_text
