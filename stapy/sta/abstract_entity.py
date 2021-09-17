import abc

from stapy.common.util import cast, un_cast, default
from stapy.sta.request import Request
from stapy.sta.entity import Entity

class AbstractEntity(metaclass=abc.ABCMeta):

    entry_map = None
    json = None

    def __init__(self, request=None):
        self.json = {}
        if request == Request.POST:
            self.setup_json()

    def setup_json(self):
        for k, (val_req, val_type) in self.entry_map.items():
            if not val_req:
                continue
            if isinstance(val_type, dict):
                self.json.update({k: {}})
            else:
                self.json.update({k: default(val_type)})

    def set_param(self, **data):
        self.json = self._update_json(self.entry_map, self.json, **data)

    def _update_json(self, template, res_json, **data):
        for k, (val_req, val_type) in template.items():

            ent = Entity.match(k, threshold=0.8)
            if ent is not None and k[0].isupper():
                val_is = data.get(ent.value)
                if val_is is None:
                    continue

                # singular
                if k != ent.value:
                    if isinstance(val_is, dict):
                        res_json.update({k: val_is})
                    else:
                        if isinstance(val_is, list):
                            val_is = int(val_is[0])
                        res_json.update({k: {"@iot.id": val_is}})
                # plural
                else:
                    if isinstance(val_is, dict):
                        res_json.update({k: val_is})
                    else:
                        if not isinstance(val_is, list):
                            val_is = [val_is]
                        ids = []
                        for value in val_is:
                            ids.append({"@iot.id": int(value)})
                        res_json.update({k: ids})
                continue

            if k not in data.keys():
                continue
            val_is = data.get(k)

            # base case
            if not isinstance(val_type, dict):
                # cast data
                if not isinstance(val_is, val_type):
                    try:
                        val_is = cast(val_type, val_is)
                    except TypeError:
                        raise ValueError("The provided value (" + str(val_is) + ") can not be casted to "
                            + str(val_type))

                if not self.check_entry(k, val_is):
                    raise ValueError("The provided value (" + str(val_is)
                        + ") does not satisfy the requirements")
                res_json.update({k: un_cast(val_is)})
            # recursion
            else:
                if not isinstance(val_is, dict):
                    raise ValueError("The data for (" + k + ") needs to be a dict")

                if not self.check_entry(k, val_is):
                    raise ValueError("The provided value (" + str(val_is)
                        + ") does not satisfy the requirements")

                if k in res_json.values():
                    res_json.update({k: self._update_json(val_type, res_json.get(k), **data.get(k))})
                else:
                    res_json.update({k: self._update_json(val_type, {}, **data.get(k))})
        return res_json

    @abc.abstractmethod
    def check_entry(self, key, value):
        raise NotImplementedError
    
    def req_attributes(self):
        return [k for k, v in self.entry_map.items() if v[0]]
    
    def opt_attributes(self):
        return [k for k, v in self.entry_map.items() if not v[0]]

    def get_data(self):
        return self.json
