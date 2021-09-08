from stapy.sta.query import Query
from stapy.sta.entity import Entity
from stapy.sta.geo import GeoJSON
from stapy.common.config import config
from stapy.sta.abstract_request import AbstractRequest
from stapy.sta.request import Request


class Post(AbstractRequest):
    """
    This static class allows to create new entities on a STA-Server by sending POST-Requests with according content
    """

    @staticmethod
    def datastream(name, description, unit_of_measurement, observation_type,
        thing_id, observed_property_id, sensor_id, properties=None):
        """
        Create a new Datastream with the given data filled in
        key and value have to be of the same length and will be handled as map afterwards
        :param name: the name for the Datastream
        :param description: the description for the Datastream
        :param observation_type: the type of observations for the Datastream
        :param unit: the unit in which the entries of the Datastream are taken
        :param op_id: the ID of the associated ObservedProperty
        :param s_id: the ID of the associated Sensor
        :param t_id: the ID of the associated Thing
        :param key: a list of keys that contain additional information of the Datastream
        :param value: a list of values that contain additional information of the Datastream
        :return: the ID of the newly created Datastream
        """
        params = Post.cast_params(description=description, unit_of_measurement=unit_of_measurement,
            observation_type=observation_type, properties=properties, thing_id=thing_id,
            observed_property_id=observed_property_id, sensor_id=sensor_id)
        return Post.entity(Entity.Datastream, **params)

    # TODO remove or keep and improve
    @staticmethod
    def full_datastream(name, description, long_name, obv_type, unit, ob_prop, loc_type, loc_coords, key=None, value=None):
        """
        Create a new Datastream with all required and associated entities that contain the given data
        key and value have to be of the same length and will be handled as map afterwards
        :param description: the description for the Datastream
        :param name: the name for the associated entities
        :param long_name: the description for the associated entities
        :param ob_prop: the name and definition of the ObservedProperty
        :param loc_type: the type of location according to the GeoJSON-Standard
        :param loc_coords: coordinates formatted according to the defined type in loc_type
        :param key: a list of keys that contain additional information of the Datastream
        :param value: a list of values that contain additional information of the Datastream
        :return: the ID of the newly created Datastream
        """
        raise NotImplementedError
        l_id, err = Post.location(name, long_name, loc_type, loc_coords)
        if err != True:
            return -1, False
        t_id, err = Post.thing(name, long_name, l_id)
        if err != True:
            return -1, False
        o_id, err = Post.observed_property(ob_prop, ob_prop, ob_prop)
        if err != True:
            return -1, False
        s_id, err = Post.sensor(name, long_name)
        if err != True:
            return -1, False

        return Post.datastream(name, description, obv_type, unit, o_id, s_id, t_id, key, value), True

    @staticmethod
    def feature_of_interest(name, description, encoding_type, feature, properties=None):
        """
        Create a new FeatureOfInterest with the given data filled in
        :param name: the name for the FeatureOfInterest
        :param description: the description for the FeatureOfInterest
        :param encodingType: the encodingType for the FeatureOfInterest
        :param feature: the relevant feature for an observation
        :return: the ID of the newly created FeatureOfInterest
        """
        params = Post.cast_params(name=name, description=description, encoding_type=encoding_type, feature=feature, properties=properties)
        return Post.entity(Entity.FeatureOfInterest, **params)

    @staticmethod
    def location(name, description, encoding_type, location, properties=None, thing_id=None):
        """
        Create a new Location with the given data filled in
        :param name: the name for the Location
        :param description: the description for the Location
        :param loc_type: the type of location according to the GeoJSON-Standard
        :param loc_coords: coordinates formatted according to the defined type in loc_type
        :return: the ID of the newly created Location
        """
        params = Post.cast_params(name=name, description=description, encoding_type=encoding_type, location=location,
            properties=properties, thing_id=thing_id)
        return Post.entity(Entity.Location, **params)

    def location(name, description, encoding_type, loc_type, loc_coords, properties=None, thing_id=None):
        location = {
            "type": loc_type,
            "coordinates": loc_coords
        }
        return Post.location(name, description, encoding_type, location, properties=properties, thing_id=thing_id)

    @staticmethod
    def observation(phenomenon_time, result, result_quality=None, valid_time=None, parameters=None,
        datastream_id=None, feature_of_interest_id=None):
        """
        Create a new Observation with the given data filled in
        key and value have to be of the same length and will be handled as map afterwards
        :param result: the result of the Observation
        :param time: the time of the Observation
        :param d_id: the ID of the associated Datastream
        :param key: a list of keys that contain additional information of the Observation
        :param value: a list of values that contain additional information of the Observation
        :return: the ID of the newly created Observation
        """
        params = Post.cast_params(phenomenon_time=phenomenon_time, result=result,
            result_quality=result_quality, valid_time=valid_time, parameters=parameters,
            datastream_id=datastream_id, feature_of_interest_id=feature_of_interest_id)
        Post.entity(EntityObservation, **params)

    # TODO remove or keep and improve
    @staticmethod
    def observations(results, times, d_id, keys=None, values=None):
        """
        Create new Observations with the given data filled in
        values has to contain a list of entries for each element in keys
        :param results: the results of value of the Observations
        :param times: the times of the Observation
        :param d_id: the ID of the associated Datastream
        :param keys: a list of keys that contain additional information of the Observation
        :param values: a list of list of values that contain additional information of the Observation
        :return: None
        """
        raise NotImplementedError
        payload = {
            "Datastream": {
                "@iot.id": d_id
            },
            "components": [
                "phenomenonTime",
                "result"
            ],
            "dataArray": []
        }

        for idx in range(len(results)):
            arr = [times[idx], results[idx]]
            payload["dataArray"].append(arr)

        if keys is not None and values is not None:
            if not isinstance(keys, list):
                keys = [keys]
                values = [values]
            for idx, key in enumerate(keys):
                payload["components"].append("parameters")
                for v_idx, value in enumerate(values[idx]):
                    payload["dataArray"][v_idx].append({key: value})
        path = config.get("API_URL") + "CreateObservations"
        requests.post(path, json=[payload])

    @staticmethod
    def observed_property(name, description, definition, properties=None):
        """
        Create a new ObservedProperty with the given data filled in
        :param name: the name for the ObservedProperty
        :param definition: the definition for the ObservedProperty
        :return: the ID of the newly created ObservedProperty
        """
        params = Post.cast_params(name=name, description=description, definition=definition,
            properties=properties)
        return Post.entity(Entity.ObservedProperty, **params)

    @staticmethod
    def sensor(name, description, encoding_type=None, metadata=None, properties=None):
        """
        Create a new Sensor with the given data filled in
        :param name: the name for the Sensor
        :param description: the description for the Sensor
        :param encodingType: the encodingType of the Sensor
        :param metadata: the metadata of the Sensor
        :return: the ID of the newly created Sensor
        """
        params = Post.cast_params(name=name, description=description, encoding_type=encoding_type,
            metadata=metadata, properties=None)
        return Post.entity(Entity.Sensor, **params)

    @staticmethod
    def thing(name, description, properties=None, location_id=None, datastream_id=None):
        """
        Create a new Thing with the given data filled in
        :param name: the name for the Thing
        :param description: the description for the Thing
        :param loc_id: the ID of the associated Location
        :return: the ID of the newly created Thing
        """
        params= Post.cast_params(name=name, description=description, properties=properties,
            location_id=location_id, datastream_id=datastream_id)
        return Post.entity(Entity.Thing, **params)

    @staticmethod
    def entity(entity, **params):
        ent = Post.get_entity(entity)(Request.POST)
        ent.set_param(**params)
        payload = ent.get_data()
        path = Query(entity).get_query()
        return Post.send_request(Request.POST, path, payload)
