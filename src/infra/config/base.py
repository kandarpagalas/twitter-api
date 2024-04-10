from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect


class ConfigModel:
    def columns(self):
        inst = inspect(self)
        attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        return attr_names

    def __repr__(self):
        repr_str = "{"
        for col in self.columns():
            value = getattr(self, col)
            repr_str += f"'{col}':'{value}', "
        repr_str += "_}"

        return repr_str.replace(", _", "")


Base = declarative_base(cls=ConfigModel)
