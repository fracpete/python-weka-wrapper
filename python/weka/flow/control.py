# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# control.py
# Copyright (C) 2015 Fracpete (pythonwekawrapper at gmail dot com)


from weka.flow.base import Actor, InputConsumer, OutputProducer, Stoppable


class ActorHandler(Actor):
    """
    The ancestor for all actors that handle other actors.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the actor handler.
        :param name: the name of the actor handler
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(Actor, self).__init__(name=name, options=options)

    def default_actors(self):
        """
        Returns the default actors to use.
        :return: the default actors, if any
        :rtype: list
        """
        return []

    def check_actors(self, actors):
        """
        Performs checks on the actors that are to be used. Raises an exception if invalid setup.
        :param actors: the actors to check
        :type actors: list
        """
        pass

    def fix_options(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(Actor, self).fix_options(options)
        if "actors" not in options:
            options["actors"] = self.default_actors()
        if "actors" not in self.help:
            self.help["actors"] = "The list of sub-actors that this actor manages."
        self.check_actors(self.options["actors"])
        return options

    @property
    def actors(self):
        """
        Obtains the currently set sub-actors.
        :return: the sub-actors
        :rtype: list
        """
        result = self.options["actors"]
        if result is None:
            result = []
        return result

    @actors.setter
    def actors(self, actors):
        """
        Sets the sub-actors of the actor.
        :param actors: the sub-actors
        :type actors: list
        """
        if actors is None:
            actors = self.default_actors()
        self.check_actors(actors)
        self.options["actors"] = actors

    @property
    def active(self):
        """
        Returns the count of non-skipped actors.
        :return: the count
        :rtype: int
        """
        result = 0
        for actor in self.actors:
            if not actor.options["skip"]:
                result += 1
        return result

    @property
    def first_active(self):
        """
        Returns the first non-skipped actor.
        :return: the first active actor, None if not available
        :rtype: Actor
        """
        result = None
        for actor in self.actors:
            if not actor.options["skip"]:
                result = actor
                break
        return result

    @property
    def last_active(self):
        """
        Returns the last non-skipped actor.
        :return: the last active actor, None if not available
        :rtype: Actor
        """
        result = None
        for actor in reversed(self.actors):
            if not actor.options["skip"]:
                result = actor
                break
        return result

    def index_of(self, name):
        """
        Returns the index of the actor with the given name.
        :param name: the name of the Actor to find
        :type name: str
        :return: the index, -1 if not found
        :rtype: int
        """
        result = -1
        for index, actor in enumerate(self.actors):
            if actor.name == name:
                result = index
                break
        return result

    def update_parent(self):
        """
        Updates the parent in its sub-actors.
        """
        for actor in self.actors:
            actor.parent = self

    def setup(self):
        """
        Configures the actor before execution.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super(Actor, self).setup()
        if result is None:
            self.update_parent()
            try:
                self.check_actors(self.actors)
            except Exception, e:
                result = str(e)
        return result


class Director(object):
    """
    Ancestor for classes that "direct" the flow of tokens.
    """

    def __init__(self, owner):
        """
        Initializes the director
        :param owner: the owning actor
        :type owner: Actor
        """
        self.check_owner(owner)
        self._owner = owner

    def __str__(self):
        """
        Returns a short description about the director.
        :return: the description
        :rtype: str
        """
        result = self.__name__
        if self.owner is not None:
            result = result + ", owner=" + self.owner.name
        return result

    @property
    def owner(self):
        """
        Obtains the currently set owner.
        :return: the owner
        :rtype: Actor
        """
        return self._owner

    def check_owner(self, owner):
        """
        Checks the owner. Raises an exception if invalid.
        :param owner: the owner to check
        :type owner: Actor
        """
        pass

    def do_execute(self):
        """
        Actual execution of the director.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        raise Exception("Not implemented!")

    def execute(self):
        """
        Executes the director.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        if self.owner is None:
            return "No actor set as owner!"
        if self.owner.options["skip"]:
            return None
        return self.do_execute()


class SequentialDirectory(Director, Stoppable):
    """
    Director for sequenial execution of actors.
    """

    def __init__(self, owner):
        """
        Initializes the director
        :param owner: the owning actor
        :type owner: Actor
        """
        super(Director, self).__init__(owner)
        super(Stoppable, self).__init__()
        self._stopping = False
        self._stopped = False
        self._record_final_output = True
        self._final_output = []

    def stop_execution(self):
        """
        Triggers the stopping of the object.
        """
        if not (self._stopping or self._stopped):
            self._stopping = True

    def is_stopping(self):
        """
        Returns whether the director is in the process of stopping
        :return:
        """
        return self._stopping

    def is_stopped(self):
        """
        Returns whether the object has been stopped.
        :return: whether stopped
        :rtype: bool
        """
        return self._stopped

    def check_owner(self, owner):
        """
        Checks the owner. Raises an exception if invalid.
        :param owner: the owner to check
        :type owner: Actor
        """
        if not isinstance(owner, ActorHandler):
            raise Exception("Owner is not an ActorHandler: " + owner.__name__)

    def do_execute(self):
        """
        Actual execution of the director.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        self._stopped = False
        self._stopping = False
        not_finished_actor = self.owner.first_active
        pending_actors = []
        finished = False
        actor_result = None

        while not (self.is_stopping() or self.is_stopped()) and not finished:
            # determing starting point of next iteration
            if len(pending_actors) > 0:
                start_index = self.owner.index_of(pending_actors[-1].name)
            else:
                start_index = self.owner.index_of(not_finished_actor.name)
                not_finished_actor = None

            # iterate over actors
            curr = None
            token = None
            last_active = -1
            if self.owner.active > 0:
                last_active = self.owner.last_active.index
            for i in xrange(start_index, last_active + 1):
                # do we have to stop the execution?
                if self.is_stopped() or self.is_stopping():
                    break

                curr = self.owner.actors[i]
                if curr.options["skip"]:
                    continue

                # no token? get pending one or produce new one
                if token is None:
                    if isinstance(curr, OutputProducer) and curr.has_output():
                        pending_actors.pop()
                    else:
                        actor_result = curr.execute()
                        if actor_result is not None:
                            self.owner.logger.error(curr.full_name + " generated following error output:\n" + actor_result)
                            break

                    if isinstance(curr, OutputProducer) and curr.has_output():
                        token = curr.output()
                    else:
                        token = None

                    # still more to come?
                    if isinstance(curr, OutputProducer) and curr.has_output():
                        pending_actors.append(curr)

                else:
                    # process token
                    curr.input(token)
                    actor_result = curr.execute()
                    if actor_result is not None:
                        self.owner.logger.error(curr.full_name + " generated following error output:\n" + actor_result)
                        break

                    # was a new token produced?
                    if isinstance(curr, OutputProducer):
                        if curr.has_output():
                            token = curr.output()
                        else:
                            token = None

                        # still more to come?
                        if curr.has_output():
                            pending_actors.append(curr)
                    else:
                        token = None

                # token from last actor generated? -> store
                if (i == self.owner.last_active().index) and (token is not None):
                    if self._record_final_output:
                        self._final_output.append(token)

                # no token produced, ignore rest of actors
                if isinstance(curr, OutputProducer) and (token is None):
                    break

            # all actors finished?
            finished = (not_finished_actor is None) and (len(pending_actors) == 0)

        return actor_result
