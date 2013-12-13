# This file is part of Pebble.

# Pebble is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# Pebble is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with Pebble.  If not, see <http://www.gnu.org/licenses/>.


from .pebble import HighlanderKilledException


def synchronized(lock, highlander=False):
    """ Synchronization decorator.

    Locks the execution on given 'lock', or kill the execution if 'highlander'
    is True and the 'lock' is held by someone else.

    Works with both threading and multiprocessing Lock s
    """

    if highlander:
        def wrap(f):
            def new_function(*args, **kw):
                can_run = lock.acquire(False)
                if can_run:
                    try:
                        return f(*args, **kw)
                    finally:
                        lock.release()
                else:
                    raise IsNotTheOneException()
            return new_function
    else:
        def wrap(f):
            def new_function(*args, **kw):
                lock.acquire()
                try:
                    return f(*args, **kw)
                finally:
                    lock.release()
            return new_function

    return wrap
