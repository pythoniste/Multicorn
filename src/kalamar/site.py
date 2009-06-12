# -*- coding: utf-8 -*-
# This file is part of Dyko
# Copyright © 2008-2009 Kozea
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Kalamar library.  If not, see <http://www.gnu.org/licenses/>.

"""
TODO : Change this docstring
Create one for each
independent site with its own configuration.
"""

class Site(object):
    """Create a kalamar site from a configuration file."""
    
    class NotOneObjectReturned(Exception): pass
    class MultipleObjectsReturned(NotOneObjectReturned): pass
    class ObjectDoesNotExist(NotOneObjectReturned): pass
    
    def __init__(self, config_filename=None):
        pass
    
    def search(self, access_point, request):
        """List every item in access_point that match request"""
        raise NotImplementedError # TODO
    
    def open(self, access_point, request):
        """Return the item in access_point that match request
        
        If there is no result, raise Site.ObjectDoesNotExist
        If there is more than one result, raise Site.MultipleObjectsReturned
        
        """
        it = iter(self.search(access_point, request))
        try:
            obj = it.next()
        except StopIteration:
            raise self.ObjectDoesNotExist
        
        try:
            it.next()
        except StopIteration:
            return obj
        else:
            raise self.MultipleObjectsReturned
    
    def save(self, item):
        """Update or add the item"""
        raise NotImplementedError # TODO

    def remove(self, item):
        """
        Remove/delete the item from the backend storage
        """
        raise NotImplementedError # TODO
