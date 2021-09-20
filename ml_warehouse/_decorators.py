from sqlalchemy.orm.attributes import InstrumentedAttribute


def add_docstring(decorated_class):

    decorated_class.__init__.__doc__ = gather_arguments(decorated_class)

    for attr in dir(decorated_class):

        attr = getattr(decorated_class, attr)

        if isinstance(attr, InstrumentedAttribute):
            col = decorated_class.__table__.columns.get(attr.key)
            if col is not None and col.comment is not None:
                attr.__doc__ = col.comment

    return decorated_class


def gather_arguments(decorated_class):

    result = []
    result.append(
        f"""Constructs a new {decorated_class.__name__}.

        Parameters
        ----------"""
    )

    for column in decorated_class.__table__.columns:

        if column.comment is None:
            comment = ""
        else:
            comment = ": " + column.comment

        result.append(f"\t\t{column.name}{comment}")

    return "\n".join(result)
