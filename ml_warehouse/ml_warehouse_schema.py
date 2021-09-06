# -*- coding: utf-8 -*-
#
# Copyright © 2020 Genome Research Ltd. All rights reserved.
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
# @author Keith James <kdj@sanger.ac.uk>

import re
from datetime import datetime
from typing import List, Tuple

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    distinct,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

MLWHBase = declarative_base()

ONTTagIdentifierRegex = re.compile(r".*-(\d+)$")


class Sample(MLWHBase):
    __tablename__ = "sample"

    id_sample_tmp = Column(Integer, primary_key=True)
    id_lims = Column(String, nullable=False)
    uuid_sample_lims = Column(String, unique=True)
    id_sample_lims = Column(String, nullable=False)
    last_updated = Column(DateTime)
    recorded_at = Column(DateTime)
    deleted_at = Column(DateTime)
    created = Column(DateTime)
    name = Column(String)
    reference_genome = Column(String)
    organism = Column(String)
    accession_number = Column(String)
    common_name = Column(String)
    description = Column(Text)
    taxon_id = Column(Integer)
    father = Column(String)
    mother = Column(String)
    replicate = Column(String)
    ethnicity = Column(String)
    gender = Column(String)
    cohort = Column(String)
    country_of_origin = Column(String)
    geographical_region = Column(String)
    sanger_sample_id = Column(String)
    control = Column(Boolean)
    supplier_name = Column(String)
    public_name = Column(String)
    sample_visibility = Column(String)
    strain = Column(String)
    consent_withdrawn = Column(Boolean, nullable=False, default=False)
    donor_id = Column(String)
    phenotype = Column(String)
    developmental_stage = Column(String)
    control_type = Column(String)

    def __repr__(self):
        return "<Sample: name={}, id_sample_lims={} last_updated={}>".format(
            self.name, self.id_sample_lims, self.last_updated
        )


class Study(MLWHBase):
    __tablename__ = "study"

    id_study_tmp = Column(Integer, primary_key=True)
    id_lims = Column(String, nullable=False)
    uuid_study_lims = Column(String, unique=True)
    id_study_lims = Column(String, nullable=False)
    last_updated = Column(DateTime, nullable=False, default=func.now())
    recorded_at = Column(DateTime, nullable=False, default=func.now())
    deleted_at = Column(DateTime)
    created = Column(DateTime)
    name = Column(String)
    reference_genome = Column(String)
    ethically_approved = Column(Boolean)
    faculty_sponsor = Column(String)
    state = Column(String)
    study_type = Column(String)
    abstract = Column(Text)
    abbreviation = Column(String)
    accession_number = Column(String)
    description = Column(Text)
    contains_human_dna = Column(Boolean)
    contaminated_human_dna = Column(Boolean)
    data_release_strategy = Column(String)
    data_release_sort_of_study = Column(String)
    ena_project_id = Column(String)
    study_title = Column(String)
    study_visibility = Column(String)
    ega_dac_accession_number = Column(String)
    array_express_accession_number = Column(String)
    ega_policy_accession_number = Column(String)
    data_release_timing = Column(String)
    data_release_delay_period = Column(String)
    data_release_delay_reason = Column(String)
    remove_x_and_autosomes = Column(Boolean, nullable=False, default=False)
    aligned = Column(Boolean, nullable=False, default=True)
    separate_y_chromosome_data = Column(Boolean, nullable=False, default=False)
    data_access_group = Column(String)
    prelim_id = Column(String)
    hmdmc_number = Column(String)
    data_destination = Column(String)
    s3_email_list = Column(String)
    data_deletion_period = Column(String)

    def __repr__(self):
        return "<Study: name={}, id_study_lims={} last_updated={}>".format(
            self.name, self.id_study_lims, self.last_updated
        )


class OseqFlowcell(MLWHBase):
    __tablename__ = "oseq_flowcell"

    id_oseq_flowcell_tmp = Column(Integer, primary_key=True)
    id_flowcell_lims = Column(String, nullable=False)
    last_updated = Column(DateTime, nullable=False, default=func.now())
    recorded_at = Column(DateTime, nullable=False, default=func.now())
    id_sample_tmp = Column(ForeignKey("sample.id_sample_tmp"), nullable=False)
    id_study_tmp = Column(ForeignKey("study.id_study_tmp"), nullable=False)
    experiment_name = Column(String, nullable=False)
    instrument_name = Column(String, nullable=False)
    instrument_slot = Column(Integer, nullable=False)
    tag_set_id_lims = Column(String, nullable=True)
    tag_set_name = Column(String, nullable=True)
    tag_identifier = Column(String, nullable=True)
    tag_sequence = Column(String, nullable=True)
    tag2_set_id_lims = Column(String, nullable=True)
    tag2_set_name = Column(String, nullable=True)
    tag2_identifier = Column(String, nullable=True)
    tag2_sequence = Column(String, nullable=True)
    pipeline_id_lims = Column(String, nullable=False)
    requested_data_type = Column(String, nullable=False)
    deleted_at = Column(DateTime)
    id_lims = Column(String)

    sample = relationship("Sample")
    study = relationship("Study")

    @property
    def tag_index(self):
        if self.tag_identifier:
            m = ONTTagIdentifierRegex.match(self.tag_identifier)
            if m:
                return int(m.group(1))

        return None

    @property
    def tag2_index(self):
        if self.tag2_identifier:
            m = ONTTagIdentifierRegex.match(self.tag2_identifier)
            if m:
                return int(m.group(1))

        return None

    def __repr__(self):
        return (
            "<OseqFlowcell: inst_name={}, inst_slot={} "
            "expt_name={} tag_set_name={} tag_id={} "
            "last_updated={}>".format(
                self.instrument_name,
                self.instrument_slot,
                self.experiment_name,
                self.tag_set_name,
                self.tag_identifier,
                self.last_updated,
            )
        )
