'''
Task Coach - Your friendly task manager
Copyright (C) 2004-2008 Frank Niessink <frank@niessink.com>

Task Coach is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Task Coach is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import datetime

class TimeDelta(datetime.timedelta):
    def hoursMinutesSeconds(self):
        ''' Return a tuple (hours, minutes, seconds). Note that the caller
            is responsible for checking whether the TimeDelta instance is
            positive or negative. '''
        if self < TimeDelta():
            seconds = 3600*24 - self.seconds
            days = abs(self.days) - 1
        else:
            seconds = self.seconds
            days = self.days
        hours, seconds = seconds/3600, seconds%3600
        minutes, seconds = seconds/60, seconds%60
        hours += days*24
        return hours, minutes, seconds
    
    def hours(self):
        ''' Return hours as float. '''
        hours, minutes, seconds = self.hoursMinutesSeconds()
        return hours + (minutes / 60.) + (seconds / 3600.)
        
    def __add__(self, other):
        ''' Make sure we return a TimeDelta instance and not a 
            datetime.timedelta instance '''
        sum = super(TimeDelta, self).__add__(other)
        return self.__class__(sum.days, sum.seconds, sum.microseconds)
    
    def __sub__(self, other):
        result = super(TimeDelta, self).__sub__(other)
        return self.__class__(result.days, result.seconds, result.microseconds)
        
oneDay = TimeDelta(days=1)
oneYear = TimeDelta(days=365)

def parseTimeDelta(string):
    try:
        hours, minutes, seconds = [int(x) for x in string.split(':')]
    except ValueError:
        hours, minutes, seconds = 0, 0, 0 
    return TimeDelta(hours=hours, minutes=minutes, seconds=seconds)

