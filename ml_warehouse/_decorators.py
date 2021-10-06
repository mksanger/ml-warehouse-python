# -*- coding: utf-8 -*-
#
# Copyright © 2021 Genome Research Ltd. All rights reserved.
#
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
#
# @author Adam Blanchet <ab59@sanger.ac.uk>

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
