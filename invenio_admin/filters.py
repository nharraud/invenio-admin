# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Flask-Admin filter utilities."""

from __future__ import absolute_import, print_function

import uuid

from flask_admin.contrib.sqla import filters
from flask_admin.model.filters import convert


class UUIDEqualFilter(filters.FilterEqual):
    """UUID aware filter."""

    def apply(self, query, value, alias):
        """Convert UUID."""
        try:
            value = uuid.UUID(value)
            return query.filter(self.column == value)
        except ValueError:
            return query


class FilterConverter(filters.FilterConverter):
    """Filter converter for dealing with UUIDs and variants."""

    uuid_filters = (UUIDEqualFilter, )

    @convert('uuidtype')
    def conv_uuid(self, column, name, **kwargs):
        """Convert UUID filter."""
        return [f(column, name, **kwargs) for f in self.uuid_filters]

    @convert('variant')
    def conv_variant(self, column, name, **kwargs):
        """Convert variants."""
        return self.convert(str(column.type), column, name, **kwargs)
