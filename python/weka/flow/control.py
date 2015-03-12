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


import weka.flow.base as base
from weka.flow.base import Actor, InputConsumer, OutputProducer, Stoppable, StorageHandler
from weka.flow.transformer import Transformer
import weka.core.utils as utils


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
        super(ActorHandler, self).__init__(name=name, options=options)
        self._director = self.new_director()

    def new_director(self):
        """
        Creates the director to use for handling the sub-actors.
        :return: the director instance
        :rtype: Director
        """
        raise Exception("Not implemented!")

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
        options = super(ActorHandler, self).fix_options(options)

        opt = "actors"
        if opt not in options:
            options[opt] = self.default_actors()
        if opt not in self.help:
            self.help[opt] = "The list of sub-actors that this actor manages."

        return options

    def to_options_dict(self):
        """
        Returns a dictionary of its options.
        :return: the options as dictionary
        :rtype: dict
        """
        result = super(ActorHandler, self).to_options_dict()
        result["options"].pop("actors", None)
        actors = {}
        for index, actor in enumerate(self.actors):
            actors[index] = actor.to_options_dict()
        result["actors"] = actors
        return result

    def from_options_dict(self, d):
        """
        Restores the object from the given options dictionary.
        :param d: the dictionary to use for restoring the options
        :type d: dict
        """
        actors = d["actors"]
        num = len(actors)
        for i in xrange(num):
            item = actors[str(i)]
            cls = utils.get_class(item["class"])
            actor = cls(name=item["name"])
            actor.parent = self
            actor.from_options_dict(item["options"])
            self.actors.append(actor)
        d.pop("actors", None)
        super(ActorHandler, self).from_options_dict(d)

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
            if not actor.skip:
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
            if not actor.skip:
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
            if not actor.skip:
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
        result = super(ActorHandler, self).setup()
        if result is None:
            self.update_parent()
            try:
                self.check_actors(self.actors)
            except Exception, e:
                result = str(e)
        if result is None:
            for actor in self.actors:
                name = actor.name
                newname = actor.unique_name(actor.name)
                if name != newname:
                    actor.name = newname
        if result is None:
            for actor in self.actors:
                if actor.skip:
                    continue
                result = actor.setup()
                if result is not None:
                    break
        if result is None:
            result = self._director.setup()
        return result

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        return self._director.execute()

    def wrapup(self):
        """
        Finishes up after execution finishes, does not remove any graphical output.
        """
        for actor in self.actors:
            if actor.skip:
                continue
            actor.wrapup()
        super(ActorHandler, self).wrapup()

    def cleanup(self):
        """
        Destructive finishing up after execution stopped.
        """
        for actor in self.actors:
            if actor.skip:
                continue
            actor.cleanup()
        super(ActorHandler, self).cleanup()


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

    def setup(self):
        """
        Performs some checks.
        :return: None if successful, otherwise error message.
        :rtype: str
        """
        return None

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
        if self.owner.skip:
            return None
        return self.do_execute()


class SequentialDirector(Director, Stoppable):
    """
    Director for sequential execution of actors.
    """

    def __init__(self, owner):
        """
        Initializes the director
        :param owner: the owning actor
        :type owner: Actor
        """
        super(SequentialDirector, self).__init__(owner)
        self._stopping = False
        self._stopped = False
        self._allow_source = False
        self._record_output = True
        self._recorded_output = []

    @property
    def allow_source(self):
        """
        Obtains whether to allow a source actor.
        :return: true if to allow
        :rtype: bool
        """
        return self._allow_source

    @allow_source.setter
    def allow_source(self, allow):
        """
        Sets whether to allow a source actor.
        :param allow: true if to allow
        :type allow: bool
        """
        self._allow_source = allow

    @property
    def record_output(self):
        """
        Obtains whether to record the output of the last actor.
        :return: true if to record
        :rtype: bool
        """
        return self._record_output

    @record_output.setter
    def record_output(self, record):
        """
        Sets whether to record the output of the last actor.
        :param record: true if to record
        :type record: bool
        """
        self._record_output = record

    @property
    def recorded_output(self):
        """
        Obtains the recorded output.
        :return: the output
        :rtype: list
        """
        return self._recorded_output

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

    def check_actors(self):
        """
        Checks the actors of the owner. Raises an exception if invalid.
        """
        actors = []
        for actor in self.owner.actors:
            if actor.skip:
                continue
            actors.append(actor)
        if len(actors) == 0:
            return
        if not self.allow_source and base.is_source(actors[0]):
            raise Exception("Actor '" + actors[0].full_name + "' is a source, but no sources allowed!")
        for i in xrange(1, len(actors)):
            if not isinstance(actors[i], InputConsumer):
                raise Exception("Actor does not accept any input: " + actors[i].full_name)

    def setup(self):
        """
        Performs some checks.
        :return: None if successful, otherwise error message.
        :rtype: str
        """
        result = super(SequentialDirector, self).setup()
        if result is None:
            try:
                self.check_actors()
            except Exception, e:
                result = str(e)
        return result

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
            token = None
            last_active = -1
            if self.owner.active > 0:
                last_active = self.owner.last_active.index
            for i in xrange(start_index, last_active + 1):
                # do we have to stop the execution?
                if self.is_stopped() or self.is_stopping():
                    break

                curr = self.owner.actors[i]
                if curr.skip:
                    continue

                # no token? get pending one or produce new one
                if token is None:
                    if isinstance(curr, OutputProducer) and curr.has_output():
                        pending_actors.pop()
                    else:
                        actor_result = curr.execute()
                        if actor_result is not None:
                            self.owner.logger.error(
                                curr.full_name + " generated following error output:\n" + actor_result)
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
                    curr.input = token
                    actor_result = curr.execute()
                    if actor_result is not None:
                        self.owner.logger.error(
                            curr.full_name + " generated following error output:\n" + actor_result)
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
                if (i == self.owner.last_active.index) and (token is not None):
                    if self._record_output:
                        self._recorded_output.append(token)

                # no token produced, ignore rest of actors
                if isinstance(curr, OutputProducer) and (token is None):
                    break

            # all actors finished?
            finished = (not_finished_actor is None) and (len(pending_actors) == 0)

        return actor_result


class Flow(ActorHandler, StorageHandler):
    """
    Root actor for defining and executing flows.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the sequence.
        :param name: the name of the sequence
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(Flow, self).__init__(name=name, options=options)
        self._storage = {}

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Root actor for defining and executing flows."

    def new_director(self):
        """
        Creates the director to use for handling the sub-actors.
        :return: the director instance
        :rtype: Director
        """
        result = SequentialDirector(self)
        result.record_output = False
        result.allow_source = True
        return result

    def check_actors(self, actors):
        """
        Performs checks on the actors that are to be used. Raises an exception if invalid setup.
        :param actors: the actors to check
        :type actors: list
        """
        super(Flow, self).check_actors(actors)
        actor = self.first_active
        if not base.is_source(actor):
            raise Exception("First active actor is not a source: " + actor.full_name)

    @property
    def storage(self):
        """
        Returns the internal storage.
        :return: the internal storage
        :rtype: dict
        """
        return self._storage

    @classmethod
    def load(cls, fname):
        """
        Loads the flow from a JSON file.
        :param fname: the file to load
        :type fname: str
        :return: the flow
        :rtype: Flow
        """
        with open(fname) as f:
            content = f.readlines()
        result = Flow()
        result.from_json(''.join(content))
        return result

    @classmethod
    def save(cls, flow, fname):
        """
        Saves the flow to a JSON file.
        :param flow: the flow to save
        :type flow: Flow
        :param fname: the file to load
        :type fname: str
        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None
        try:
            f = open(fname, 'w')
            f.write(flow.to_json())
            f.close()
        except Exception, e:
            result = str(e)
        return result


class Sequence(InputConsumer):
    """
    Simple sequence of actors that get executed one after the other. Accepts input.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the sequence.
        :param name: the name of the sequence
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(Sequence, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Simple sequence of actors that get executed one after the other. Accepts input."

    def new_director(self):
        """
        Creates the director to use for handling the sub-actors.
        :return: the director instance
        :rtype: Director
        """
        result = SequentialDirector(self)
        result.record_output = False
        result.allow_source = False
        return result

    def check_actors(self, actors):
        """
        Performs checks on the actors that are to be used. Raises an exception if invalid setup.
        :param actors: the actors to check
        :type actors: list
        """
        super(Sequence, self).check_actors(actors)
        actor = self.first_active
        if not isinstance(actor, InputConsumer):
            raise Exception("First active actor does not accept input: " + actor.full_name)

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        self.first_active.input = self.input
        result = self._director.execute()
        if result is None:
            self._output.append(self.input)
        return result


class Tee(ActorHandler, Transformer):
    """
    'Tees off' the current token to be processed in the sub-tree before passing it on.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the sequence.
        :param name: the name of the sequence
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(Tee, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "'Tees off' the current token to be processed in the sub-tree before passing it on."

    def new_director(self):
        """
        Creates the director to use for handling the sub-actors.
        :return: the director instance
        :rtype: Director
        """
        result = SequentialDirector(self)
        result.record_output = False
        result.allow_source = False
        return result

    def check_actors(self, actors):
        """
        Performs checks on the actors that are to be used. Raises an exception if invalid setup.
        :param actors: the actors to check
        :type actors: list
        """
        super(Tee, self).check_actors(actors)
        actor = self.first_active
        if actor is None:
            raise Exception("No active actor!")
        if not isinstance(actor, InputConsumer):
            raise Exception("First active actor does not accept input: " + actor.full_name)

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        self.first_active.input = self.input
        result = self._director.execute()
        if result is None:
            self._output.append(self.input)
        return result


class Trigger(ActorHandler, Transformer):
    """
    'Triggers' the sub-tree with each token passing through and then passes the token on.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the sequence.
        :param name: the name of the sequence
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(Trigger, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "'Triggers' the sub-tree with each token passing through and then passes the token on."

    def new_director(self):
        """
        Creates the director to use for handling the sub-actors.
        :return: the director instance
        :rtype: Director
        """
        result = SequentialDirector(self)
        result.record_output = False
        result.allow_source = True
        return result

    def check_actors(self, actors):
        """
        Performs checks on the actors that are to be used. Raises an exception if invalid setup.
        :param actors: the actors to check
        :type actors: list
        """
        super(Trigger, self).check_actors(actors)
        actor = self.first_active
        if actor is None:
            raise Exception("No active actor!")
        if not base.is_source(actor):
            raise Exception("First active actor is not a source: " + actor.full_name)

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = self._director.execute()
        if result is None:
            self._output.append(self.input)
        return result


class BranchDirector(Director, Stoppable):
    """
    Director for the Branch actor.
    """

    def __init__(self, owner):
        """
        Initializes the director
        :param owner: the owning actor
        :type owner: Actor
        """
        super(BranchDirector, self).__init__(owner)
        self._stopping = False
        self._stopped = False

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
        if not isinstance(owner, Branch):
            raise Exception("Owner is not a Branch: " + owner.__name__)

    def check_actors(self):
        """
        Checks the actors of the owner. Raises an exception if invalid.
        """
        actors = []
        for actor in self.owner.actors:
            if actor.skip:
                continue
            actors.append(actor)
        if len(actors) == 0:
            return
        for actor in actors:
            if not isinstance(actor, InputConsumer):
                raise Exception("Actor does not accept any input: " + actor.full_name)

    def setup(self):
        """
        Performs some checks.
        :return: None if successful, otherwise error message.
        :rtype: str
        """
        result = super(BranchDirector, self).setup()
        if result is None:
            try:
                self.check_actors()
            except Exception, e:
                result = str(e)
        return result

    def do_execute(self):
        """
        Actual execution of the director.
        :return: None if successful, otherwise error message
        :rtype: str
        """

        result = None
        self._stopped = False
        self._stopping = False

        for actor in self.owner.actors:
            if self.is_stopping():
                break
            actor.input = self.owner.input
            result = actor.execute()
            if result is not None:
                break

        return result


class Branch(ActorHandler, InputConsumer):
    """
    Passes on the input token to all of its sub-actors, one after the other.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the sequence.
        :param name: the name of the sequence
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(Branch, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Passes on the input token to all of its sub-actors, one after the other."

    def new_director(self):
        """
        Creates the director to use for handling the sub-actors.
        :return: the director instance
        :rtype: Director
        """
        result = BranchDirector(self)
        return result
