#!/usr/bin/env python

from enum import Enum

class Entity(Enum):
    """
    This class represents all available entities in the SensorThingsAPI (v1.1)
    """
    Datastreams = "Datastreams"
    MultiDatastreams = "MultiDatastreams"
    FeaturesOfInterest = "FeaturesOfInterest"
    HistoricalLocations = "HistoricalLocations"
    Locations = "Locations"
    Observations = "Observations"
    ObservedProperties = "ObservedProperties"
    Sensors = "Sensors"
    Things = "Things"

    @staticmethod
    def __singular_map():
        return {
            Entity.FeaturesOfInterest: "FeatureOfInterest",
            Entity.ObservedProperties: "ObservedProperty",
            Entity.Sensors: "Sensor",
            Entity.Things: "Thing"
        }

    @staticmethod
    def list():
        """
        :return: a list of all entities as strings
        """
        return list(map(lambda e: e.value, Entity))

    @classmethod
    def remap(cls, entity):
        """
        This method remaps an entity to the singular version if needed,
        these are sometimes required in the STA (in case single elements are accesses)
        :param entity: the entity to possible remap
        :return: the remapped entity
        """
        if entity not in Entity:
            raise Exception("invalid entity: " + entity.value)
        if entity in cls.__singular_map():
            return cls.__singular_map()[entity]
        return entity.value

    @classmethod
    def match(cls, entity):
        ent_search = entity.lower()
        for entity in Entity:
            ent_is = entity.value.lower()
            if ent_is in ent_search or ent_search in ent_is:
                return entity
        entity = None
        for entity, ent_val in cls.__singular_map().items():
            ent_is = ent_val.lower()
            if ent_is in ent_search or ent_search in ent_is:
                return entity
        return None