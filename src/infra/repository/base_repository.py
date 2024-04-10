from sqlalchemy import inspect
from sqlalchemy.orm.exc import NoResultFound
from src.infra.config.connection import DBConnectionHandler


class BaseRepository:
    def __init__(self, model) -> None:
        self.model = model

    def columns(self):
        inst = inspect(self.model)
        attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        return attr_names

    def insert(self, data: dict, prefix="", suffix=""):
        insert_data = {}
        try:
            for attr in self.columns():
                if attr in data:
                    insert_data[attr] = data[attr]
                elif prefix + attr + suffix in data:
                    insert_data[attr] = data[prefix + attr + suffix]
        except Exception as e:
            print(e)
        with DBConnectionHandler() as db:
            try:
                model_instance = self.model(**insert_data)
                db.session.add(model_instance)
                return_data = db.session.commit()
                return return_data
            except Exception as e:
                print("\n\n----------------------------\n")
                print(e)
                print("\n----------------------------\n\n")
                db.session.rollback()
                raise e

    def insert_many(self, data: list[dict] = None, prefix="", suffix=""):
        if data is None:
            raise Exception("Data is None")

        model_instances = []

        for obj in data:
            insert_data = {}
            try:
                #
                for attr in self.columns():
                    if attr in obj:
                        insert_data[attr] = obj[attr]
                    elif prefix + attr + suffix in obj:
                        insert_data[attr] = obj[prefix + attr + suffix]

                # for attr in self.columns():
                #     key = prefix + attr + suffix
                #     if key in obj:
                #         insert_data[attr] = obj[key]
                model_instances.append(self.model(**insert_data))

            except Exception as e:
                print(e)

        with DBConnectionHandler() as db:
            try:
                # model_instance = self.model(**insert_data)
                db.session.add_all(model_instances)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

    def select_all(self):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(self.model).all()
                return data
            except Exception as e:
                db.session.rollback()
                raise e

    def select(self, column, value):
        with DBConnectionHandler() as db:
            try:
                data = (
                    # db.session.query(self.model).filter(self.model[column] == _id).one()
                    db.session.query(self.model)
                    .filter(getattr(self.model, column) == value)
                    .all()
                )
                return data
            except NoResultFound:
                return None
            except Exception as e:
                db.session.rollback()
                raise e

    def delete(self, _id):
        with DBConnectionHandler() as db:
            try:
                data = (
                    db.session.query(self.model).filter(self.model.id == _id).delete()
                )
                db.session.commit()
                return data
            except NoResultFound:
                return None
            except Exception as e:
                db.session.rollback()
                raise e
