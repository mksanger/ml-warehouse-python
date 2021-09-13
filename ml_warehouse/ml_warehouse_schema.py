# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Date, DateTime, Enum, Float, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, ENUM, INTEGER, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ArInternalMetadatum(Base):
    __tablename__ = 'ar_internal_metadata'

    key = Column(String(255), primary_key=True)
    value = Column(String(255))
    created_at = Column(DATETIME(fsp=6), nullable=False)
    updated_at = Column(DATETIME(fsp=6), nullable=False)


class CgapAnalyte(Base):
    __tablename__ = 'cgap_analyte'

    cgap_analyte_tmp = Column(INTEGER(10), primary_key=True, comment='Internal to this database id. Value can change.')
    cell_line_uuid = Column(String(36, 'utf8_unicode_ci'), nullable=False, index=True)
    destination = Column(String(32, 'utf8_unicode_ci'), nullable=False)
    jobs = Column(String(64, 'utf8_unicode_ci'))
    slot_uuid = Column(String(36, 'utf8_unicode_ci'), nullable=False, unique=True)
    release_date = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    labware_barcode = Column(String(20, 'utf8_unicode_ci'), nullable=False)
    passage_number = Column(INTEGER(2))
    cell_state = Column(String(40, 'utf8_unicode_ci'), nullable=False)
    project = Column(String(50, 'utf8_unicode_ci'))


class CgapBiomaterial(Base):
    __tablename__ = 'cgap_biomaterial'

    cgap_biomaterial_tmp = Column(INTEGER(10), primary_key=True, comment='Internal to this database id. Value can change.')
    donor_uuid = Column(String(36, 'utf8_unicode_ci'), nullable=False, index=True)
    donor_accession_number = Column(String(38, 'utf8_unicode_ci'))
    donor_name = Column(String(64, 'utf8_unicode_ci'))
    biomaterial_uuid = Column(String(36, 'utf8_unicode_ci'), nullable=False, unique=True)


class CgapConjuredLabware(Base):
    __tablename__ = 'cgap_conjured_labware'

    cgap_conjured_labware_tmp = Column(INTEGER(10), primary_key=True, comment='Internal to this database id. Value can change.')
    barcode = Column(String(32, 'utf8_unicode_ci'), nullable=False, index=True)
    cell_line_long_name = Column(String(48, 'utf8_unicode_ci'), nullable=False, index=True)
    cell_line_uuid = Column(String(38, 'utf8_unicode_ci'), nullable=False, index=True)
    passage_number = Column(INTEGER(2), nullable=False)
    fate = Column(String(40, 'utf8_unicode_ci'))
    conjure_date = Column(TIMESTAMP, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))
    labware_state = Column(String(20, 'utf8_unicode_ci'), nullable=False, index=True)
    project = Column(String(50, 'utf8_unicode_ci'), index=True)
    slot_uuid = Column(String(36, 'utf8_unicode_ci'), nullable=False, unique=True)


class CgapHeron(Base):
    __tablename__ = 'cgap_heron'
    __table_args__ = (
        Index('cgap_heron_destination_wrangled', 'destination', 'wrangled'),
        Index('cgap_heron_rack_and_position', 'container_barcode', 'position', unique=True)
    )

    cgap_heron_tmp = Column(INTEGER(10), primary_key=True, comment='Internal to this database id. Value can change.')
    container_barcode = Column(String(32, 'utf8_unicode_ci'), nullable=False)
    tube_barcode = Column(String(32, 'utf8_unicode_ci'), unique=True)
    supplier_sample_id = Column(String(64, 'utf8_unicode_ci'), nullable=False, index=True)
    position = Column(String(8, 'utf8_unicode_ci'), nullable=False)
    sample_type = Column(String(32, 'utf8_unicode_ci'), nullable=False)
    release_time = Column(TIMESTAMP, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))
    study = Column(String(32, 'utf8_unicode_ci'), nullable=False, index=True)
    destination = Column(String(32, 'utf8_unicode_ci'), nullable=False)
    wrangled = Column(TIMESTAMP)
    sample_state = Column(String(32, 'utf8_unicode_ci'), nullable=False)
    lysis_buffer = Column(String(64, 'utf8_unicode_ci'))
    priority = Column(TINYINT(4))
    sample_identifier = Column(String(64, 'utf8_unicode_ci'), index=True, comment='The COG-UK barcode of a sample or the mixtio barcode of a control')
    control_type = Column(ENUM('Positive', 'Negative'))
    control_accession_number = Column(String(32, 'utf8_unicode_ci'))


class CgapLineIdentifier(Base):
    __tablename__ = 'cgap_line_identifier'

    cgap_line_identifier_tmp = Column(INTEGER(10), primary_key=True, comment='Internal to this database id. Value can change.')
    line_uuid = Column(String(36, 'utf8_unicode_ci'), nullable=False, unique=True)
    friendly_name = Column(String(48, 'utf8_unicode_ci'), nullable=False, index=True)
    accession_number = Column(String(38, 'utf8_unicode_ci'))
    direct_parent_uuid = Column(String(36, 'utf8_unicode_ci'), index=True)
    biomaterial_uuid = Column(String(36, 'utf8_unicode_ci'), nullable=False, index=True)
    project = Column(String(50, 'utf8_unicode_ci'))


class CgapOrganoidsConjuredLabware(Base):
    __tablename__ = 'cgap_organoids_conjured_labware'

    cgap_organoids_conjured_labware_tmp = Column(INTEGER(10), primary_key=True, comment='Internal to this database id. Value can change.')
    barcode = Column(String(20, 'utf8_unicode_ci'), nullable=False, index=True)
    cell_line_long_name = Column(String(48, 'utf8_unicode_ci'), nullable=False, index=True)
    cell_line_uuid = Column(String(38, 'utf8_unicode_ci'), nullable=False, index=True)
    passage_number = Column(INTEGER(2), nullable=False)
    fate = Column(String(40, 'utf8_unicode_ci'))
    conjure_date = Column(TIMESTAMP, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))
    labware_state = Column(String(20, 'utf8_unicode_ci'), nullable=False, index=True)


class CgapRelease(Base):
    __tablename__ = 'cgap_release'

    cgap_release_tmp = Column(INTEGER(10), primary_key=True, comment='Internal to this database id. Value can change.')
    barcode = Column(String(20, 'utf8_unicode_ci'), nullable=False, index=True)
    cell_line_long_name = Column(String(48, 'utf8_unicode_ci'), nullable=False, index=True)
    cell_line_uuid = Column(String(38, 'utf8_unicode_ci'), nullable=False, index=True)
    goal = Column(String(64, 'utf8_unicode_ci'), nullable=False)
    jobs = Column(String(64, 'utf8_unicode_ci'), nullable=False)
    destination = Column(String(64, 'utf8_unicode_ci'))
    user = Column(String(6, 'utf8_unicode_ci'), nullable=False)
    release_date = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    cell_state = Column(String(40, 'utf8_unicode_ci'), nullable=False)
    fate = Column(String(40, 'utf8_unicode_ci'))
    passage_number = Column(INTEGER(2), nullable=False)
    project = Column(String(50, 'utf8_unicode_ci'), index=True)


class CgapSupplierBarcode(Base):
    __tablename__ = 'cgap_supplier_barcode'

    cgap_supplier_barcode_tmp = Column(INTEGER(10), primary_key=True, comment='Internal to this database id. Value can change.')
    biomaterial_uuid = Column(String(36, 'utf8_unicode_ci'), nullable=False, index=True)
    supplier_barcode = Column(String(20, 'utf8_unicode_ci'), nullable=False, unique=True)
    date = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))


class IseqExternalProductMetric(Base):
    __tablename__ = 'iseq_external_product_metrics'
    __table_args__ = {'comment': 'Externally computed metrics for data sequenced at WSI'}

    id_iseq_ext_pr_metrics_tmp = Column(BIGINT(20), primary_key=True, comment='Internal to this database id, value can change')
    created = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='Datetime this record was created')
    last_changed = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='Datetime this record was created or changed')
    supplier_sample_name = Column(VARCHAR(255), index=True, comment='Sample name given by the supplier, as recorded by WSI')
    plate_barcode = Column(VARCHAR(255), index=True, comment='Stock plate barcode, as recorded by WSI')
    library_id = Column(INTEGER(11), index=True, comment='WSI library identifier')
    file_name = Column(String(300), nullable=False, index=True, comment='Comma-delimitered alphabetically sorted list of file names, which unambigiously define WSI sources of data')
    file_path = Column(String(760), nullable=False, unique=True, comment='Comma-delimitered alphabetically sorted list of full external file paths for the files in file_names column as uploaded by WSI')
    md5_staging = Column(CHAR(32), comment='WSI validation hex MD5, not set for multiple source files')
    manifest_upload_status = Column(CHAR(15), index=True, comment='WSI manifest upload status, one of "IN PROGRESS", "DONE", "FAIL", not set for multiple source files')
    manifest_upload_status_change_date = Column(DateTime, comment='Date the status of manifest upload is changed by WSI')
    id_run = Column(INTEGER(10), index=True, comment='NPG run identifier, defined where the product corresponds to a single line')
    id_iseq_product = Column(CHAR(64), index=True, comment='product id')
    iseq_composition_tmp = Column(String(600), comment='JSON representation of the composition object, the column might be deleted in future')
    id_archive_product = Column(CHAR(64), comment='Archive ID for data product')
    destination = Column(String(15), server_default=text("'UKBMP'"), comment='Data destination, from 20200323 defaults to "UKBMP"')
    processing_status = Column(CHAR(15), index=True, comment='Overall status of the product, one of "PASS", "HOLD", "INSUFFICIENT", "FAIL"')
    qc_overall_assessment = Column(CHAR(4), index=True, comment='State of the product after phase 3 of processing, one of "PASS" or "FAIL"')
    qc_status = Column(CHAR(15), comment='State of the product after phase 2 of processing, one of "PASS", "HOLD", "INSUFFICIENT", "FAIL"')
    sequencing_start_date = Column(Date, comment='Sequencing start date obtained from the CRAM file header, not set for multiple source files')
    upload_date = Column(Date, comment='Upload date, not set for multiple source files')
    md5_validation_date = Column(Date, comment='Date of MD5 validation, not set for multiple source files')
    processing_start_date = Column(Date, comment='Processing start date')
    analysis_start_date = Column(Date)
    phase2_end_date = Column(DateTime, comment='Date the phase 2 analysis finished for this product')
    analysis_end_date = Column(Date)
    archival_date = Column(Date, comment='Date made available or pushed to archive service')
    archive_confirmation_date = Column(Date, comment='Date of confirmation of integrity of data product by archive service')
    md5 = Column(CHAR(32), comment='External validation hex MD5, not set for multiple source files')
    md5_validation = Column(CHAR(4), comment='Outcome of MD5 validation as "PASS" or "FAIL", not set for multiple source files')
    format_validation = Column(CHAR(4), comment='Outcome of format validation as "PASS" or "FAIL", not set for multiple source files')
    upload_status = Column(CHAR(4), comment='Upload status as "PASS" or "FAIL", "PASS" if both MD5 and format validation are "PASS", not set for multiple source files')
    instrument_id = Column(String(256), index=True, comment='Comma separated sorted list of instrument IDs obtained from the CRAM file header(s)')
    flowcell_id = Column(String(256), index=True, comment='Comma separated sorted list of flowcell IDs obtained from the CRAM file header(s)')
    annotation = Column(String(15), comment='Annotation regarding data provenance, i.e. is sequence data from first pass, re-run, top-up, etc.')
    min_read_length = Column(TINYINT(3), comment='Minimum read length observed in the data file')
    target_autosome_coverage_threshold = Column(INTEGER(3), server_default=text("'15'"), comment='Target autosome coverage threshold, defaults to 15')
    target_autosome_gt_coverage_threshold = Column(Float, comment='Coverage percent at >= target_autosome_coverage_threshold X as a fraction')
    target_autosome_gt_coverage_threshold_assessment = Column(CHAR(4), comment='"PASS" if target_autosome_percent_gt_coverage_threshold > 95%, "FAIL" otherwise')
    verify_bam_id_score = Column(Float, comment='FREEMIX value of sample contamination levels as a fraction')
    verify_bam_id_score_assessment = Column(CHAR(4), comment='"PASS" if verify_bam_id_score > 0.01, "FAIL" otherwise')
    double_error_fraction = Column(Float, comment='Fraction of marker pairs with two read pairs evidencing parity and non-parity, may only be calculated if 1% <= verify_bam_id_score < 5%')
    contamination_assessment = Column(CHAR(4), comment='"PASS" or "FAIL" based on verify_bam_id_score_assessment and double_error_fraction < 0.2%')
    yield_whole_genome = Column(Float, comment='Sequence data quantity (Gb) excluding duplicate reads, adaptors, overlapping bases from reads on the same fragment, soft-clipped bases')
    _yield = Column('yield', Float, comment='Sequence data quantity (Gb) excluding duplicate reads, adaptors, overlapping bases from reads on the same fragment, soft-clipped bases, non-N autosome only')
    yield_q20 = Column(BIGINT(20), comment='Yield in bases at or above Q20 filtered in the same way as the yield column values')
    yield_q30 = Column(BIGINT(20), comment='Yield in bases at or above Q30 filtered in the same way as the yield column values')
    num_reads = Column(BIGINT(20), comment='Number of reads filtered in the same way as the yield column values')
    gc_fraction_forward_read = Column(Float)
    gc_fraction_reverse_read = Column(Float)
    adapter_contamination = Column(String(255), comment='The maximum over adapters and cycles in reads/fragments as a fraction per file and RG. Values for first and second reads separated with ",", and values for individual files separated with "/". e.g. "0.1/0.1/0.1/0.1,0.1/0.1/0.1/0.1"')
    adapter_contamination_assessment = Column(String(255), comment='"PASS", "WARN", "FAIL" per read and file. Multiple values are represented as forward slash-separated array of strings with a comma separating entries for paired-end 1 and 2 reads e.g. "PASS/PASS/WARN/PASS,PASS/PASS/WARN/PASS"')
    pre_adapter_min_total_qscore = Column(TINYINT(3), comment='Minimum of TOTAL_QSCORE values in PreAdapter report from CollectSequencingArtifactMetrics')
    ref_bias_min_total_qscore = Column(TINYINT(3), comment='Minimum of TOTAL_QSCORE values in BaitBias report from CollectSequencingArtifactMetrics')
    target_proper_pair_mapped_reads_fraction = Column(Float, comment='Fraction of properly paired mapped reads filtered in the same way as the yield column values')
    target_proper_pair_mapped_reads_assessment = Column(CHAR(4), comment='"PASS" if target_proper_pair_mapped_reads_fraction > 0.95, "FAIL" otherwise')
    insert_size_mean = Column(Float)
    insert_size_std = Column(Float)
    sequence_error_rate = Column(Float, comment='Reported by samtools, as a fraction')
    basic_statistics_assessement = Column(String(255), comment='FastQC "PASS", "WARN", "FAIL" per input file. Array of strings separated by "/", with a "," separating entries for paired-end 1 and 2 reads. e.g. Four RG "PASS/PASS/WARN/PASS,PASS/PASS/WARN/PASS"')
    overrepresented_sequences_assessement = Column(String(255), comment='FastQC "PASS", "WARN", "FAIL" per input file. Array of strings separated by "/", with a "," separating entries for paired-end 1 and 2 reads. e.g. Four RG "PASS/PASS/WARN/PASS,PASS/PASS/WARN/PASS"')
    n_content_per_base_assessement = Column(String(255), comment='FastQC "PASS", "WARN", "FAIL" per input file. Array of strings separated by "/", with a "," separating entries for paired-end 1 and 2 reads. e.g. Four RG "PASS/PASS/WARN/PASS,PASS/PASS/WARN/PASS"')
    sequence_content_per_base_assessement = Column(String(255), comment='FastQC "PASS", "WARN", "FAIL" per input file. Array of strings separated by "/", with a "," separating entries for paired-end 1 and 2 reads. e.g. Four RG "PASS/PASS/WARN/PASS,PASS/PASS/WARN/PASS"')
    sequence_quality_per_base_assessement = Column(String(255), comment='FastQC "PASS", "WARN", "FAIL" per input file. Array of strings separated by "/", with a "," separating entries for paired-end 1 and 2 reads. e.g. Four RG "PASS/PASS/WARN/PASS,PASS/PASS/WARN/PASS"')
    gc_content_per_sequence_assessement = Column(String(255), comment='FastQC "PASS", "WARN", "FAIL" per input file. Array of strings separated by "/", with a "," separating entries for paired-end 1 and 2 reads. e.g. Four RG "PASS/PASS/WARN/PASS,PASS/PASS/WARN/PASS"')
    quality_scores_per_sequence_assessement = Column(String(255), comment='FastQC "PASS", "WARN", "FAIL" per input file. Array of strings separated by "/", with a "," separating entries for paired-end 1 and 2 reads. e.g. Four RG "PASS/PASS/WARN/PASS,PASS/PASS/WARN/PASS"')
    sequence_duplication_levels_assessement = Column(String(255), comment='FastQC "PASS", "WARN", "FAIL" per input file. Array of strings separated by "/", with a "," separating entries for paired-end 1 and 2 reads. e.g. Four RG "PASS/PASS/WARN/PASS,PASS/PASS/WARN/PASS"')
    sequence_length_distribution_assessement = Column(String(255), comment='FastQC "PASS", "WARN", "FAIL" per input file. Array of strings separated by "/", with a "," separating entries for paired-end 1 and 2 reads. e.g. Four RG "PASS/PASS/WARN/PASS,PASS/PASS/WARN/PASS"')
    FastQC_overall_assessment = Column(CHAR(4), comment='FastQC "PASS" or "FAIL"')
    nrd = Column(Float, comment='Sample discordance levels at non-reference genotypes as a fraction')
    nrd_assessment = Column(CHAR(4), comment='"PASS" based on nrd_persent < 2% or "FAIL" or "NA" if genotyping data not available for this sample')
    sex_reported = Column(CHAR(6), comment='Sex as reported by sample supplier')
    sex_computed = Column(CHAR(6), comment='Genetic sex as identified by sequence data')


class IseqHeronProductMetric(Base):
    __tablename__ = 'iseq_heron_product_metrics'
    __table_args__ = {'comment': 'Heron project additional metrics'}

    id_iseq_hrpr_metrics_tmp = Column(BIGINT(20), primary_key=True, comment='Internal to this database id, value can change')
    created = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='Datetime this record was created')
    last_changed = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='Datetime this record was created or changed')
    id_run = Column(INTEGER(10), index=True, comment='Run id')
    id_iseq_product = Column(CHAR(64, 'utf8_unicode_ci'), nullable=False, unique=True, comment='Product id, a foreign key into iseq_product_metrics table')
    supplier_sample_name = Column(String(255, 'utf8_unicode_ci'), index=True, comment='Sample name given by the supplier, as recorded by WSI')
    pp_name = Column(String(40, 'utf8_unicode_ci'), server_default=text("'ncov2019-artic-nf'"), comment='The name of the pipeline that produced the QC metric')
    pp_version = Column(String(40, 'utf8_unicode_ci'), index=True, comment='The version of the pipeline specified in the pp_name column')
    pp_repo_url = Column(String(255, 'utf8_unicode_ci'), comment='URL of the VCS repository for this pipeline')
    artic_qc_outcome = Column(CHAR(15, 'utf8_unicode_ci'), comment='Artic pipeline QC outcome, "TRUE", "FALSE" or a NULL value')
    climb_upload = Column(DateTime, comment='Datetime files for this sample were uploaded to CLIMB')
    cog_sample_meta = Column(TINYINT(1), comment='A Boolean flag to mark sample metadata upload to COG')
    path_root = Column(String(255, 'utf8_unicode_ci'), comment='The uploaded files path root for the entity')
    ivar_md = Column(SMALLINT(5), comment='ivar minimum depth used in generating the default consensus')
    pct_N_bases = Column(Float, comment='Percent of N bases')
    pct_covered_bases = Column(Float, comment='Percent of covered bases')
    longest_no_N_run = Column(SMALLINT(5), comment='Longest consensus data stretch without N')
    ivar_amd = Column(SMALLINT(5), comment='ivar minimum depth used in generating the additional consensus')
    pct_N_bases_amd = Column(Float, comment='Percent of N bases in the additional consensus')
    longest_no_N_run_amd = Column(SMALLINT(5), comment='Longest data stretch without N in the additional consensus')
    num_aligned_reads = Column(BIGINT(20), comment='Number of aligned filtered reads')


class IseqRun(Base):
    __tablename__ = 'iseq_run'
    __table_args__ = {'comment': 'Table linking run and flowcell identities with the run folder name'}

    id_run = Column(INTEGER(10), primary_key=True, comment='NPG run identifier')
    id_flowcell_lims = Column(String(20, 'utf8_unicode_ci'), index=True, comment='LIMS specific flowcell id')
    folder_name = Column(String(64, 'utf8_unicode_ci'), comment='Runfolder name')


class IseqRunLaneMetric(Base):
    __tablename__ = 'iseq_run_lane_metrics'
    __table_args__ = (
        Index('iseq_rlm_cancelled_and_run_complete_index', 'cancelled', 'run_complete'),
        Index('iseq_rlm_cancelled_and_run_pending_index', 'cancelled', 'run_pending')
    )

    flowcell_barcode = Column(String(15, 'utf8_unicode_ci'), comment='Manufacturer flowcell barcode or other identifier as recorded by NPG')
    id_run = Column(INTEGER(10), primary_key=True, nullable=False, index=True, comment='NPG run identifier')
    position = Column(SMALLINT(2), primary_key=True, nullable=False, comment='Flowcell lane number')
    last_changed = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='Date this record was created or changed')
    qc_seq = Column(TINYINT(1), comment='Sequencing lane level QC outcome, a result of either manual or automatic assessment by core')
    instrument_name = Column(CHAR(32, 'utf8_unicode_ci'))
    instrument_external_name = Column(CHAR(10, 'utf8_unicode_ci'), comment='Name assigned to the instrument by the manufacturer')
    instrument_model = Column(CHAR(64, 'utf8_unicode_ci'))
    instrument_side = Column(CHAR(1, 'utf8_unicode_ci'), comment='Illumina instrument side (A or B), if appropriate')
    workflow_type = Column(String(20, 'utf8_unicode_ci'), comment='Illumina instrument workflow type')
    paired_read = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    cycles = Column(INTEGER(4), nullable=False)
    cancelled = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='Boolen flag to indicate whether the run was cancelled')
    run_pending = Column(DateTime, comment='Timestamp of run pending status')
    run_complete = Column(DateTime, comment='Timestamp of run complete status')
    qc_complete = Column(DateTime, comment='Timestamp of qc complete status')
    pf_cluster_count = Column(BIGINT(20))
    raw_cluster_count = Column(BIGINT(20))
    raw_cluster_density = Column(Float(12, True))
    pf_cluster_density = Column(Float(12, True))
    pf_bases = Column(BIGINT(20))
    q20_yield_kb_forward_read = Column(INTEGER(10))
    q20_yield_kb_reverse_read = Column(INTEGER(10))
    q30_yield_kb_forward_read = Column(INTEGER(10))
    q30_yield_kb_reverse_read = Column(INTEGER(10))
    q40_yield_kb_forward_read = Column(INTEGER(10))
    q40_yield_kb_reverse_read = Column(INTEGER(10))
    tags_decode_percent = Column(Float(5))
    tags_decode_cv = Column(Float(6))
    unexpected_tags_percent = Column(Float(5), comment='tag0_perfect_match_reads as a percentage of total_lane_reads')
    tag_hops_percent = Column(Float, comment='Percentage tag hops for dual index runs')
    tag_hops_power = Column(Float, comment='Power to detect tag hops for dual index runs')
    run_priority = Column(TINYINT(3), comment='Sequencing lane level run priority, a result of either manual or default value set by core')
    interop_cluster_count_total = Column(BIGINT(20), comment='Total cluster count for this lane (derived from Illumina InterOp files)')
    interop_cluster_count_mean = Column(Float(asdecimal=True), comment='Total cluster count, mean value over tiles of this lane (derived from Illumina InterOp files)')
    interop_cluster_count_stdev = Column(Float(asdecimal=True), comment='Standard deviation value for interop_cluster_count_mean')
    interop_cluster_count_pf_total = Column(BIGINT(20), comment='Purity-filtered cluster count for this lane (derived from Illumina InterOp files)')
    interop_cluster_count_pf_mean = Column(Float(asdecimal=True), comment='Purity-filtered cluster count, mean value over tiles of this lane (derived from Illumina InterOp files)')
    interop_cluster_count_pf_stdev = Column(Float(asdecimal=True), comment='Standard deviation value for interop_cluster_count_pf_mean')
    interop_cluster_density_mean = Column(Float(asdecimal=True), comment='Cluster density, mean value over tiles of this lane (derived from Illumina InterOp files)')
    interop_cluster_density_stdev = Column(Float(asdecimal=True), comment='Standard deviation value for interop_cluster_density_mean')
    interop_cluster_density_pf_mean = Column(Float(asdecimal=True), comment='Purity-filtered cluster density, mean value over tiles of this lane (derived from Illumina InterOp files)')
    interop_cluster_density_pf_stdev = Column(Float(asdecimal=True), comment='Standard deviation value for interop_cluster_density_pf_mean')
    interop_cluster_pf_mean = Column(Float(5), comment=' Percent of purity-filtered clusters, mean value over tiles of this lane (derived from Illumina InterOp files)')
    interop_cluster_pf_stdev = Column(Float(5), comment='Standard deviation value for interop_cluster_pf_mean')
    interop_occupied_mean = Column(Float(5), comment='Percent of occupied flowcell wells, a mean value over tiles of this lane (derived from Illumina InterOp files)')
    interop_occupied_stdev = Column(Float(5), comment='Standard deviation value for interop_occupied_mean')


class IseqRunStatusDict(Base):
    __tablename__ = 'iseq_run_status_dict'

    id_run_status_dict = Column(INTEGER(10), primary_key=True)
    description = Column(String(64, 'utf8_unicode_ci'), nullable=False, index=True)
    iscurrent = Column(TINYINT(3), nullable=False)
    temporal_index = Column(SMALLINT(5))


class LighthouseSample(Base):
    __tablename__ = 'lighthouse_sample'
    __table_args__ = (
        Index('index_lighthouse_sample_on_root_sample_id_and_rna_id_and_result', 'root_sample_id', 'rna_id', 'result', unique=True),
        Index('index_lighthouse_sample_on_plate_barcode_and_created_at', 'plate_barcode', 'created_at')
    )

    id = Column(INTEGER(11), primary_key=True)
    mongodb_id = Column(String(255, 'utf8_unicode_ci'), unique=True, comment='Auto-generated id from MongoDB')
    root_sample_id = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='Id for this sample provided by the Lighthouse lab')
    cog_uk_id = Column(String(255, 'utf8_unicode_ci'), index=True, comment='Consortium-wide id, generated by Sanger on import to LIMS')
    rna_id = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True, comment='Lighthouse lab-provided id made up of plate barcode and well')
    plate_barcode = Column(String(255, 'utf8_unicode_ci'), comment='Barcode of plate sample arrived in, from rna_id')
    coordinate = Column(String(255, 'utf8_unicode_ci'), comment='Well position from plate sample arrived in, from rna_id')
    result = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True, comment='Covid-19 test result from the Lighthouse lab')
    date_tested_string = Column(String(255, 'utf8_unicode_ci'), comment='When the covid-19 test was carried out by the Lighthouse lab')
    date_tested = Column(DateTime, index=True, comment='date_tested_string in date format')
    source = Column(String(255, 'utf8_unicode_ci'), comment='Lighthouse centre that the sample came from')
    lab_id = Column(String(255, 'utf8_unicode_ci'), comment='Id of the lab, within the Lighthouse centre')
    ch1_target = Column(String(255, 'utf8_unicode_ci'))
    ch1_result = Column(String(255, 'utf8_unicode_ci'))
    ch1_cq = Column(DECIMAL(11, 8))
    ch2_target = Column(String(255, 'utf8_unicode_ci'))
    ch2_result = Column(String(255, 'utf8_unicode_ci'))
    ch2_cq = Column(DECIMAL(11, 8))
    ch3_target = Column(String(255, 'utf8_unicode_ci'))
    ch3_result = Column(String(255, 'utf8_unicode_ci'))
    ch3_cq = Column(DECIMAL(11, 8))
    ch4_target = Column(String(255, 'utf8_unicode_ci'))
    ch4_result = Column(String(255, 'utf8_unicode_ci'))
    ch4_cq = Column(DECIMAL(11, 8))
    filtered_positive = Column(TINYINT(1), index=True, comment='Filtered positive result value')
    filtered_positive_version = Column(String(255, 'utf8_unicode_ci'), comment='Filtered positive version')
    filtered_positive_timestamp = Column(DateTime, comment='Filtered positive timestamp')
    lh_sample_uuid = Column(String(36, 'utf8_unicode_ci'), unique=True, comment='Sample uuid created in crawler')
    lh_source_plate_uuid = Column(String(36, 'utf8_unicode_ci'), comment='Source plate uuid created in crawler')
    created_at = Column(DateTime, comment='When this record was inserted')
    updated_at = Column(DateTime, comment='When this record was last updated')
    must_sequence = Column(TINYINT(1), comment='PAM provided value whether sample is of high importance')
    preferentially_sequence = Column(TINYINT(1), comment='PAM provided value whether sample is important')


class PacBioRunWellMetric(Base):
    __tablename__ = 'pac_bio_run_well_metrics'
    __table_args__ = (
        Index('pac_bio_metrics_run_well', 'pac_bio_run_name', 'well_label', unique=True),
        {'comment': 'Status and run information by well and some basic QC data from SMRT Link'}
    )

    id_pac_bio_rw_metrics_tmp = Column(INTEGER(11), primary_key=True)
    pac_bio_run_name = Column(VARCHAR(255), nullable=False, comment='Lims specific identifier for the pacbio run')
    well_label = Column(VARCHAR(255), nullable=False, comment='The well identifier for the plate, A1-H12')
    instrument_type = Column(VARCHAR(32), nullable=False, comment='The instrument type e.g. Sequel')
    instrument_name = Column(VARCHAR(32), comment='The instrument name e.g. SQ54097')
    chip_type = Column(VARCHAR(32), comment='The chip type e.g. 8mChip')
    ts_run_name = Column(VARCHAR(32), comment='The PacBio run name')
    movie_name = Column(VARCHAR(32), comment='The PacBio movie name')
    cell_lot_number = Column(String(32), comment='SMRT Cell Lot Number')
    ccs_execution_mode = Column(VARCHAR(32), comment='The PacBio ccs exection mode e.g. OnInstument, OffInstument or None')
    run_start = Column(DateTime, comment='Timestamp of run started')
    run_complete = Column(DateTime, comment='Timestamp of run complete')
    run_status = Column(String(32), comment='Last recorded status, primarily to explain runs not completed.')
    well_start = Column(DateTime, comment='Timestamp of well started')
    well_complete = Column(DateTime, comment='Timestamp of well complete')
    well_status = Column(String(32), comment='Last recorded status, primarily to explain wells not completed.')
    chemistry_sw_version = Column(VARCHAR(32), comment='The PacBio chemistry software version')
    instrument_sw_version = Column(VARCHAR(32), comment='The PacBio instrument software version')
    primary_analysis_sw_version = Column(VARCHAR(32), comment='The PacBio primary analysis software version')
    control_num_reads = Column(INTEGER(10), comment='The number of control reads')
    control_concordance_mean = Column(Float(8), comment='The average concordance between the control raw reads and the control reference sequence')
    control_read_length_mean = Column(INTEGER(10), comment='The mean polymerase read length of the control reads')
    local_base_rate = Column(Float(8), comment='The average base incorporation rate, excluding polymerase pausing events')
    polymerase_read_bases = Column(BIGINT(20), comment='Calculated by multiplying the number of productive (P1) ZMWs by the mean polymerase read length')
    polymerase_num_reads = Column(INTEGER(10), comment='The number of polymerase reads')
    polymerase_read_length_mean = Column(INTEGER(10), comment='The mean high-quality read length of all polymerase reads')
    polymerase_read_length_n50 = Column(INTEGER(10), comment='Fifty percent of the trimmed read length of all polymerase reads are longer than this value')
    insert_length_mean = Column(INTEGER(10), comment='The average subread length, considering only the longest subread from each ZMW')
    insert_length_n50 = Column(INTEGER(10), comment='Fifty percent of the subreads are longer than this value when considering only the longest subread from each ZMW')
    unique_molecular_bases = Column(BIGINT(20), comment='The unique molecular yield in bp')
    productive_zmws_num = Column(INTEGER(10), comment='Number of productive ZMWs')
    p0_num = Column(INTEGER(10), comment='Number of empty ZMWs with no high quality read detected')
    p1_num = Column(INTEGER(10), comment='Number of ZMWs with a high quality read detected')
    p2_num = Column(INTEGER(10), comment='Number of other ZMWs, signal detected but no high quality read')
    adapter_dimer_percent = Column(Float(5), comment='The percentage of pre-filter ZMWs which have observed inserts of 0-10 bp')
    short_insert_percent = Column(Float(5), comment='The percentage of pre-filter ZMWs which have observed inserts of 11-100 bp')
    hifi_read_bases = Column(BIGINT(20), comment='The number of HiFi bases')
    hifi_num_reads = Column(INTEGER(10), comment='The number of HiFi reads')
    hifi_read_length_mean = Column(INTEGER(10), comment='The mean HiFi read length')
    hifi_read_quality_median = Column(SMALLINT(5), comment='The median HiFi base quality')
    hifi_number_passes_mean = Column(INTEGER(10), comment='The mean number of passes per HiFi read')
    hifi_low_quality_read_bases = Column(BIGINT(20), comment='The number of HiFi bases filtered due to low quality (<Q20)')
    hifi_low_quality_num_reads = Column(INTEGER(10), comment='The number of HiFi reads filtered due to low quality (<Q20)')
    hifi_low_quality_read_length_mean = Column(INTEGER(10), comment='The mean length of HiFi reads filtered due to low quality (<Q20)')
    hifi_low_quality_read_quality_median = Column(SMALLINT(5), comment='The median base quality of HiFi bases filtered due to low quality (<Q20)')


class Sample(Base):
    __tablename__ = 'sample'
    __table_args__ = (
        Index('index_sample_on_id_sample_lims_and_id_lims', 'id_sample_lims', 'id_lims', unique=True),
    )

    id_sample_tmp = Column(INTEGER(10), primary_key=True, comment='Internal to this database id, value can change')
    id_lims = Column(String(10, 'utf8_unicode_ci'), nullable=False, comment='LIM system identifier, e.g. CLARITY-GCLP, SEQSCAPE')
    uuid_sample_lims = Column(String(36, 'utf8_unicode_ci'), unique=True, comment='LIMS-specific sample uuid')
    id_sample_lims = Column(String(20, 'utf8_unicode_ci'), nullable=False, comment='LIMS-specific sample identifier')
    last_updated = Column(DateTime, nullable=False, comment='Timestamp of last update')
    recorded_at = Column(DateTime, nullable=False, comment='Timestamp of warehouse update')
    deleted_at = Column(DateTime, comment='Timestamp of sample deletion')
    created = Column(DateTime, comment='Timestamp of sample creation')
    name = Column(String(255, 'utf8_unicode_ci'), index=True)
    reference_genome = Column(String(255, 'utf8_unicode_ci'))
    organism = Column(String(255, 'utf8_unicode_ci'))
    accession_number = Column(String(50, 'utf8_unicode_ci'), index=True)
    common_name = Column(String(255, 'utf8_unicode_ci'))
    description = Column(Text(collation='utf8_unicode_ci'))
    taxon_id = Column(INTEGER(6))
    father = Column(String(255, 'utf8_unicode_ci'))
    mother = Column(String(255, 'utf8_unicode_ci'))
    replicate = Column(String(255, 'utf8_unicode_ci'))
    ethnicity = Column(String(255, 'utf8_unicode_ci'))
    gender = Column(String(20, 'utf8_unicode_ci'))
    cohort = Column(String(255, 'utf8_unicode_ci'))
    country_of_origin = Column(String(255, 'utf8_unicode_ci'))
    geographical_region = Column(String(255, 'utf8_unicode_ci'))
    sanger_sample_id = Column(String(255, 'utf8_unicode_ci'), index=True)
    control = Column(TINYINT(1))
    supplier_name = Column(String(255, 'utf8_unicode_ci'), index=True)
    public_name = Column(String(255, 'utf8_unicode_ci'))
    sample_visibility = Column(String(255, 'utf8_unicode_ci'))
    strain = Column(String(255, 'utf8_unicode_ci'))
    consent_withdrawn = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    donor_id = Column(String(255, 'utf8_unicode_ci'))
    phenotype = Column(String(255, 'utf8_unicode_ci'), comment='The phenotype of the sample as described in Sequencescape')
    developmental_stage = Column(String(255, 'utf8_unicode_ci'), comment='Developmental Stage')
    control_type = Column(String(255, 'utf8_unicode_ci'))
    sibling = Column(String(255, 'utf8_unicode_ci'))
    is_resubmitted = Column(TINYINT(1))
    date_of_sample_collection = Column(String(255, 'utf8_unicode_ci'))
    date_of_sample_extraction = Column(String(255, 'utf8_unicode_ci'))
    extraction_method = Column(String(255, 'utf8_unicode_ci'))
    purified = Column(String(255, 'utf8_unicode_ci'))
    purification_method = Column(String(255, 'utf8_unicode_ci'))
    customer_measured_concentration = Column(String(255, 'utf8_unicode_ci'))
    concentration_determined_by = Column(String(255, 'utf8_unicode_ci'))
    sample_type = Column(String(255, 'utf8_unicode_ci'))
    storage_conditions = Column(String(255, 'utf8_unicode_ci'))
    genotype = Column(String(255, 'utf8_unicode_ci'))
    age = Column(String(255, 'utf8_unicode_ci'))
    cell_type = Column(String(255, 'utf8_unicode_ci'))
    disease_state = Column(String(255, 'utf8_unicode_ci'))
    compound = Column(String(255, 'utf8_unicode_ci'))
    dose = Column(String(255, 'utf8_unicode_ci'))
    immunoprecipitate = Column(String(255, 'utf8_unicode_ci'))
    growth_condition = Column(String(255, 'utf8_unicode_ci'))
    organism_part = Column(String(255, 'utf8_unicode_ci'))
    time_point = Column(String(255, 'utf8_unicode_ci'))
    disease = Column(String(255, 'utf8_unicode_ci'))
    subject = Column(String(255, 'utf8_unicode_ci'))
    treatment = Column(String(255, 'utf8_unicode_ci'))
    date_of_consent_withdrawn = Column(DateTime)
    marked_as_consent_withdrawn_by = Column(String(255, 'utf8_unicode_ci'))
    customer_measured_volume = Column(String(255, 'utf8_unicode_ci'))
    gc_content = Column(String(255, 'utf8_unicode_ci'))
    dna_source = Column(String(255, 'utf8_unicode_ci'))


t_schema_migrations = Table(
    'schema_migrations', metadata,
    Column('version', String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
)


class Study(Base):
    __tablename__ = 'study'
    __table_args__ = (
        Index('study_id_lims_id_study_lims_index', 'id_lims', 'id_study_lims', unique=True),
    )

    id_study_tmp = Column(INTEGER(10), primary_key=True, comment='Internal to this database id, value can change')
    id_lims = Column(String(10, 'utf8_unicode_ci'), nullable=False, comment='LIM system identifier, e.g. GCLP-CLARITY, SEQSCAPE')
    uuid_study_lims = Column(String(36, 'utf8_unicode_ci'), unique=True, comment='LIMS-specific study uuid')
    id_study_lims = Column(String(20, 'utf8_unicode_ci'), nullable=False, comment='LIMS-specific study identifier')
    last_updated = Column(DateTime, nullable=False, comment='Timestamp of last update')
    recorded_at = Column(DateTime, nullable=False, comment='Timestamp of warehouse update')
    deleted_at = Column(DateTime, comment='Timestamp of study deletion')
    created = Column(DateTime, comment='Timestamp of study creation')
    name = Column(String(255, 'utf8_unicode_ci'), index=True)
    reference_genome = Column(String(255, 'utf8_unicode_ci'))
    ethically_approved = Column(TINYINT(1))
    faculty_sponsor = Column(String(255, 'utf8_unicode_ci'))
    state = Column(String(50, 'utf8_unicode_ci'))
    study_type = Column(String(50, 'utf8_unicode_ci'))
    abstract = Column(Text(collation='utf8_unicode_ci'))
    abbreviation = Column(String(255, 'utf8_unicode_ci'))
    accession_number = Column(String(50, 'utf8_unicode_ci'), index=True)
    description = Column(Text(collation='utf8_unicode_ci'))
    contains_human_dna = Column(TINYINT(1), comment='Lane may contain human DNA')
    contaminated_human_dna = Column(TINYINT(1), comment='Human DNA in the lane is a contaminant and should be removed')
    data_release_strategy = Column(String(255, 'utf8_unicode_ci'))
    data_release_sort_of_study = Column(String(255, 'utf8_unicode_ci'))
    ena_project_id = Column(String(255, 'utf8_unicode_ci'))
    study_title = Column(String(255, 'utf8_unicode_ci'))
    study_visibility = Column(String(255, 'utf8_unicode_ci'))
    ega_dac_accession_number = Column(String(255, 'utf8_unicode_ci'))
    array_express_accession_number = Column(String(255, 'utf8_unicode_ci'))
    ega_policy_accession_number = Column(String(255, 'utf8_unicode_ci'))
    data_release_timing = Column(String(255, 'utf8_unicode_ci'))
    data_release_delay_period = Column(String(255, 'utf8_unicode_ci'))
    data_release_delay_reason = Column(String(255, 'utf8_unicode_ci'))
    remove_x_and_autosomes = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    aligned = Column(TINYINT(1), nullable=False, server_default=text("'1'"))
    separate_y_chromosome_data = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    data_access_group = Column(String(255, 'utf8_unicode_ci'))
    prelim_id = Column(String(20, 'utf8_unicode_ci'), comment='The preliminary study id prior to entry into the LIMS')
    hmdmc_number = Column(String(255, 'utf8_unicode_ci'), comment='The Human Materials and Data Management Committee approval number(s) for the study.')
    data_destination = Column(String(255, 'utf8_unicode_ci'), comment="The data destination type(s) for the study. It could be 'standard', '14mg' or 'gseq'. This may be extended, if Sanger gains more external customers. It can contain multiply destinations separated by a space.")
    s3_email_list = Column(String(255, 'utf8_unicode_ci'))
    data_deletion_period = Column(String(255, 'utf8_unicode_ci'))


class BmapFlowcell(Base):
    __tablename__ = 'bmap_flowcell'

    id_bmap_flowcell_tmp = Column(INTEGER(11), primary_key=True)
    last_updated = Column(DateTime, nullable=False, comment='Timestamp of last update')
    recorded_at = Column(DateTime, nullable=False, comment='Timestamp of warehouse update')
    id_sample_tmp = Column(ForeignKey('sample.id_sample_tmp'), nullable=False, index=True, comment='Sample id, see "sample.id_sample_tmp"')
    id_study_tmp = Column(ForeignKey('study.id_study_tmp'), nullable=False, index=True, comment='Study id, see "study.id_study_tmp"')
    experiment_name = Column(String(255), nullable=False, comment='The name of the experiment, eg. The lims generated run id')
    instrument_name = Column(String(255), nullable=False, comment='The name of the instrument on which the sample was run')
    enzyme_name = Column(String(255), nullable=False, comment='The name of the recognition enzyme used')
    chip_barcode = Column(String(255), nullable=False, comment='Manufacturer chip identifier')
    chip_serialnumber = Column(String(16), comment='Manufacturer chip identifier')
    position = Column(INTEGER(10), comment='Flowcell position')
    id_flowcell_lims = Column(String(255), nullable=False, index=True, comment='LIMs-specific flowcell id')
    id_library_lims = Column(String(255), index=True, comment='Earliest LIMs identifier associated with library creation')
    id_lims = Column(String(10), nullable=False, comment='LIM system identifier')

    sample = relationship('Sample')
    study = relationship('Study')


class FlgenPlate(Base):
    __tablename__ = 'flgen_plate'
    __table_args__ = (
        Index('flgen_plate_id_lims_id_flgen_plate_lims_index', 'id_lims', 'id_flgen_plate_lims'),
    )

    id_flgen_plate_tmp = Column(INTEGER(10), primary_key=True, comment='Internal to this database id, value can change')
    id_sample_tmp = Column(ForeignKey('sample.id_sample_tmp'), nullable=False, index=True, comment='Sample id, see "sample.id_sample_tmp"')
    id_study_tmp = Column(ForeignKey('study.id_study_tmp'), nullable=False, index=True, comment='Study id, see "study.id_study_tmp"')
    cost_code = Column(String(20, 'utf8_unicode_ci'), nullable=False, comment='Valid WTSI cost code')
    id_lims = Column(String(10, 'utf8_unicode_ci'), nullable=False, comment='LIM system identifier, e.g. CLARITY-GCLP, SEQSCAPE')
    last_updated = Column(DateTime, nullable=False, comment='Timestamp of last update')
    recorded_at = Column(DateTime, nullable=False, comment='Timestamp of warehouse update')
    plate_barcode = Column(INTEGER(10), nullable=False, comment='Manufacturer (Fluidigm) chip barcode')
    plate_barcode_lims = Column(String(128, 'utf8_unicode_ci'), comment='LIMs-specific plate barcode')
    plate_uuid_lims = Column(String(36, 'utf8_unicode_ci'), comment='LIMs-specific plate uuid')
    id_flgen_plate_lims = Column(String(20, 'utf8_unicode_ci'), nullable=False, comment='LIMs-specific plate id')
    plate_size = Column(SMALLINT(6), comment='Total number of wells on a plate')
    plate_size_occupied = Column(SMALLINT(6), comment='Number of occupied wells on a plate')
    well_label = Column(String(10, 'utf8_unicode_ci'), nullable=False, comment='Manufactuer well identifier within a plate, S001-S192')
    well_uuid_lims = Column(String(36, 'utf8_unicode_ci'), comment='LIMs-specific well uuid')
    qc_state = Column(TINYINT(1), comment='QC state; 1 (pass), 0 (fail), NULL (not known)')

    sample = relationship('Sample')
    study = relationship('Study')


class IseqExternalProductComponent(Base):
    __tablename__ = 'iseq_external_product_components'
    __table_args__ = (
        Index('iseq_ext_pr_comp_unique', 'id_iseq_product', 'id_iseq_product_ext', unique=True),
        Index('iseq_ext_pr_comp_compi', 'component_index', 'num_components'),
        Index('iseq_ext_pr_comp_ncomp', 'num_components', 'id_iseq_product'),
        {'comment': 'Table linking iseq_external_product_metrics table products to components in the iseq_product_metrics table'}
    )

    id_iseq_ext_pr_components_tmp = Column(BIGINT(20), primary_key=True, comment='Internal to this database id, value can change')
    id_iseq_product_ext = Column(ForeignKey('iseq_external_product_metrics.id_iseq_product'), nullable=False, index=True, comment='id (digest) for the external product composition')
    id_iseq_product = Column(CHAR(64, 'utf8_unicode_ci'), nullable=False, comment='id (digest) for one of the products components')
    num_components = Column(TINYINT(3), nullable=False, comment='Number of component products for this product')
    component_index = Column(TINYINT(3), nullable=False, comment='Unique component index within all components of this product, a value from 1 to the value of num_components column for this product')

    iseq_external_product_metric = relationship('IseqExternalProductMetric')


class IseqFlowcell(Base):
    __tablename__ = 'iseq_flowcell'
    __table_args__ = (
        Index('index_iseq_flowcell_id_flowcell_lims_position_tag_index_id_lims', 'id_flowcell_lims', 'position', 'tag_index', 'id_lims', unique=True),
        Index('index_iseqflowcell__id_flowcell_lims__position__tag_index', 'id_flowcell_lims', 'position', 'tag_index'),
        Index('iseq_flowcell_id_lims_id_flowcell_lims_index', 'id_lims', 'id_flowcell_lims'),
        Index('index_iseqflowcell__flowcell_barcode__position__tag_index', 'flowcell_barcode', 'position', 'tag_index')
    )

    id_iseq_flowcell_tmp = Column(INTEGER(10), primary_key=True, comment='Internal to this database id, value can change')
    last_updated = Column(DateTime, nullable=False, comment='Timestamp of last update')
    recorded_at = Column(DateTime, nullable=False, comment='Timestamp of warehouse update')
    id_sample_tmp = Column(ForeignKey('sample.id_sample_tmp'), nullable=False, index=True, comment='Sample id, see "sample.id_sample_tmp"')
    id_study_tmp = Column(ForeignKey('study.id_study_tmp'), index=True, comment='Study id, see "study.id_study_tmp"')
    cost_code = Column(String(20, 'utf8_unicode_ci'), comment='Valid WTSI cost code')
    is_r_and_d = Column(TINYINT(1), server_default=text("'0'"), comment='A boolean flag derived from cost code, flags RandD')
    id_lims = Column(String(10, 'utf8_unicode_ci'), nullable=False, comment='LIM system identifier, e.g. CLARITY-GCLP, SEQSCAPE')
    priority = Column(SMALLINT(2), server_default=text("'1'"), comment='Priority')
    manual_qc = Column(TINYINT(1), comment='Manual QC decision, NULL for unknown')
    external_release = Column(TINYINT(1), comment='Defaults to manual qc value; can be changed by the user later')
    flowcell_barcode = Column(String(15, 'utf8_unicode_ci'), comment='Manufacturer flowcell barcode or other identifier')
    id_flowcell_lims = Column(String(20, 'utf8_unicode_ci'), nullable=False, comment='LIMs-specific flowcell id, batch_id for Sequencescape')
    position = Column(SMALLINT(2), nullable=False, comment='Flowcell lane number')
    entity_type = Column(String(30, 'utf8_unicode_ci'), nullable=False, comment='Lane type: library, pool, library_control, library_indexed, library_indexed_spike')
    entity_id_lims = Column(String(20, 'utf8_unicode_ci'), nullable=False, comment='Most specific LIMs identifier associated with this lane or plex or spike')
    tag_index = Column(SMALLINT(5), comment='Tag index, NULL if lane is not a pool')
    tag_sequence = Column(String(30, 'utf8_unicode_ci'), comment='Tag sequence')
    tag_set_id_lims = Column(String(20, 'utf8_unicode_ci'), comment='LIMs-specific identifier of the tag set')
    tag_set_name = Column(String(100, 'utf8_unicode_ci'), comment='WTSI-wide tag set name')
    tag_identifier = Column(String(30, 'utf8_unicode_ci'), comment='The position of tag within the tag group')
    tag2_sequence = Column(String(30, 'utf8_unicode_ci'), comment='Tag sequence for tag 2')
    tag2_set_id_lims = Column(String(20, 'utf8_unicode_ci'), comment='LIMs-specific identifier of the tag set for tag 2')
    tag2_set_name = Column(String(100, 'utf8_unicode_ci'), comment='WTSI-wide tag set name for tag 2')
    tag2_identifier = Column(String(30, 'utf8_unicode_ci'), comment='The position of tag2 within the tag group')
    is_spiked = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='Boolean flag indicating presence of a spike')
    pipeline_id_lims = Column(String(60, 'utf8_unicode_ci'), comment='LIMs-specific pipeline identifier that unambiguously defines library type')
    bait_name = Column(String(50, 'utf8_unicode_ci'), comment='WTSI-wide name that uniquely identifies a bait set')
    requested_insert_size_from = Column(INTEGER(5), comment='Requested insert size min value')
    requested_insert_size_to = Column(INTEGER(5), comment='Requested insert size max value')
    forward_read_length = Column(SMALLINT(4), comment='Requested forward read length, bp')
    reverse_read_length = Column(SMALLINT(4), comment='Requested reverse read length, bp')
    id_pool_lims = Column(String(20, 'utf8_unicode_ci'), nullable=False, index=True, comment='Most specific LIMs identifier associated with the pool')
    legacy_library_id = Column(INTEGER(11), index=True, comment='Legacy library_id for backwards compatibility.')
    id_library_lims = Column(String(255, 'utf8_unicode_ci'), index=True, comment='Earliest LIMs identifier associated with library creation')
    team = Column(String(255, 'utf8_unicode_ci'), comment='The team responsible for creating the flowcell')
    purpose = Column(String(30, 'utf8_unicode_ci'), comment='Describes the reason the sequencing was conducted. Eg. Standard, QC, Control')
    suboptimal = Column(TINYINT(1), comment='Indicates that a sample has failed a QC step during processing')
    primer_panel = Column(String(255, 'utf8_unicode_ci'), comment='Primer Panel name')
    spiked_phix_barcode = Column(String(20, 'utf8_unicode_ci'), comment='Barcode of the PhiX tube added to the lane')
    spiked_phix_percentage = Column(Float, comment='Percentage PhiX tube spiked in the pool in terms of molar concentration')
    loading_concentration = Column(Float, comment='Final instrument loading concentration (pM)')
    workflow = Column(String(20, 'utf8_unicode_ci'), comment='Workflow used when processing the flowcell')

    sample = relationship('Sample')
    study = relationship('Study')


class IseqRunStatu(Base):
    __tablename__ = 'iseq_run_status'

    id_run_status = Column(INTEGER(11), primary_key=True)
    id_run = Column(INTEGER(10), nullable=False, index=True, comment='NPG run identifier')
    date = Column(DateTime, nullable=False, comment='Status timestamp')
    id_run_status_dict = Column(ForeignKey('iseq_run_status_dict.id_run_status_dict'), nullable=False, index=True, comment='Status identifier, see iseq_run_status_dict.id_run_status_dict')
    iscurrent = Column(TINYINT(1), nullable=False, comment='Boolean flag, 1 is the status is current, 0 otherwise')

    iseq_run_status_dict = relationship('IseqRunStatusDict')


class OseqFlowcell(Base):
    __tablename__ = 'oseq_flowcell'

    id_oseq_flowcell_tmp = Column(INTEGER(10), primary_key=True)
    id_flowcell_lims = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='LIMs-specific flowcell id')
    last_updated = Column(DateTime, nullable=False, comment='Timestamp of last update')
    recorded_at = Column(DateTime, nullable=False, comment='Timestamp of warehouse update')
    id_sample_tmp = Column(ForeignKey('sample.id_sample_tmp'), nullable=False, index=True, comment='Sample id, see "sample.id_sample_tmp"')
    id_study_tmp = Column(ForeignKey('study.id_study_tmp'), nullable=False, index=True, comment='Study id, see "study.id_study_tmp"')
    experiment_name = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='The name of the experiment, eg. The lims generated run id')
    instrument_name = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='The name of the instrument on which the sample was run')
    instrument_slot = Column(INTEGER(11), nullable=False, comment='The numeric identifier of the slot on which the sample was run')
    pipeline_id_lims = Column(String(255, 'utf8_unicode_ci'), comment='LIMs-specific pipeline identifier that unambiguously defines library type')
    requested_data_type = Column(String(255, 'utf8_unicode_ci'), comment='The type of data produced by sequencing, eg. basecalls only')
    deleted_at = Column(DateTime, comment='Timestamp of any flowcell destruction')
    id_lims = Column(String(10, 'utf8_unicode_ci'), nullable=False, comment='LIM system identifier')
    tag_identifier = Column(String(255, 'utf8_unicode_ci'), comment='Position of the first tag within the tag group')
    tag_sequence = Column(String(255, 'utf8_unicode_ci'), comment='Sequence of the first tag')
    tag_set_id_lims = Column(String(255, 'utf8_unicode_ci'), comment='LIMs-specific identifier of the tag set for the first tag')
    tag_set_name = Column(String(255, 'utf8_unicode_ci'), comment='WTSI-wide tag set name for the first tag')
    tag2_identifier = Column(String(255, 'utf8_unicode_ci'), comment='Position of the second tag within the tag group')
    tag2_sequence = Column(String(255, 'utf8_unicode_ci'), comment='Sequence of the second tag')
    tag2_set_id_lims = Column(String(255, 'utf8_unicode_ci'), comment='LIMs-specific identifier of the tag set for the second tag')
    tag2_set_name = Column(String(255, 'utf8_unicode_ci'), comment='WTSI-wide tag set name for the second tag')

    sample = relationship('Sample')
    study = relationship('Study')


class PacBioRun(Base):
    __tablename__ = 'pac_bio_run'

    id_pac_bio_tmp = Column(INTEGER(11), primary_key=True)
    last_updated = Column(DateTime, nullable=False, comment='Timestamp of last update')
    recorded_at = Column(DateTime, nullable=False, comment='Timestamp of warehouse update')
    id_sample_tmp = Column(ForeignKey('sample.id_sample_tmp'), nullable=False, index=True, comment='Sample id, see "sample.id_sample_tmp"')
    id_study_tmp = Column(ForeignKey('study.id_study_tmp'), nullable=False, index=True, comment='Sample id, see "study.id_study_tmp"')
    id_pac_bio_run_lims = Column(String(20, 'utf8_unicode_ci'), nullable=False, comment='Lims specific identifier for the pacbio run')
    pac_bio_run_uuid = Column(String(36, 'utf8_unicode_ci'), comment='Uuid identifier for the pacbio run')
    cost_code = Column(String(20, 'utf8_unicode_ci'), nullable=False, comment='Valid WTSI cost-code')
    id_lims = Column(String(10, 'utf8_unicode_ci'), nullable=False, comment='LIM system identifier')
    tag_identifier = Column(String(30, 'utf8_unicode_ci'), comment='Tag index within tag set, NULL if untagged')
    tag_sequence = Column(String(30, 'utf8_unicode_ci'), comment='Tag sequence for tag')
    tag_set_id_lims = Column(String(20, 'utf8_unicode_ci'), comment='LIMs-specific identifier of the tag set for tag')
    tag_set_name = Column(String(100, 'utf8_unicode_ci'), comment='WTSI-wide tag set name for tag')
    tag2_sequence = Column(String(30, 'utf8_unicode_ci'))
    tag2_set_id_lims = Column(String(20, 'utf8_unicode_ci'))
    tag2_set_name = Column(String(100, 'utf8_unicode_ci'))
    tag2_identifier = Column(String(30, 'utf8_unicode_ci'))
    plate_barcode = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='The human readable barcode for the plate loaded onto the machine')
    plate_uuid_lims = Column(String(36, 'utf8_unicode_ci'), nullable=False, comment='The plate uuid')
    well_label = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='The well identifier for the plate, A1-H12')
    well_uuid_lims = Column(String(36, 'utf8_unicode_ci'), nullable=False, comment='The well uuid')
    pac_bio_library_tube_id_lims = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='LIMS specific identifier for originating library tube')
    pac_bio_library_tube_uuid = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='The uuid for the originating library tube')
    pac_bio_library_tube_name = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='The name of the originating library tube')
    pac_bio_library_tube_legacy_id = Column(INTEGER(11), comment='Legacy library_id for backwards compatibility.')
    library_created_at = Column(DateTime, comment='Timestamp of library creation')
    pac_bio_run_name = Column(String(255, 'utf8_unicode_ci'), comment='Name of the run')

    sample = relationship('Sample')
    study = relationship('Study')


class QcResult(Base):
    __tablename__ = 'qc_result'
    __table_args__ = (
        Index('lookup_index', 'id_qc_result_lims', 'id_lims'),
    )

    id_qc_result_tmp = Column(INTEGER(11), primary_key=True)
    id_sample_tmp = Column(ForeignKey('sample.id_sample_tmp'), nullable=False, index=True)
    id_qc_result_lims = Column(String(20), nullable=False, comment='LIMS-specific qc_result identifier')
    id_lims = Column(String(10), nullable=False, comment='LIMS system identifier (e.g. SEQUENCESCAPE)')
    id_pool_lims = Column(String(255), comment='Most specific LIMs identifier associated with the pool. (Asset external_identifier in SS)')
    id_library_lims = Column(String(255), index=True, comment='Earliest LIMs identifier associated with library creation. (Aliquot external_identifier in SS)')
    labware_purpose = Column(String(255), comment='Labware Purpose name. (e.g. Plate Purpose for a Well)')
    assay = Column(String(255), comment='assay type and version')
    value = Column(String(255), nullable=False, comment='Value of the mesurement')
    units = Column(String(255), nullable=False, comment='Mesurement unit')
    cv = Column(Float, comment='Coefficient of variance')
    qc_type = Column(String(255), nullable=False, comment='Type of mesurement')
    date_created = Column(DateTime, nullable=False, comment='The date the qc_result was first created in SS')
    last_updated = Column(DateTime, nullable=False, comment='The date the qc_result was last updated in SS')
    recorded_at = Column(DateTime, nullable=False, comment='Timestamp of warehouse update')

    sample = relationship('Sample')


class SamplesExtractionActivity(Base):
    __tablename__ = 'samples_extraction_activity'

    id_activity_tmp = Column(INTEGER(11), primary_key=True)
    id_activity_lims = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True, comment='LIMs-specific activity id')
    id_sample_tmp = Column(ForeignKey('sample.id_sample_tmp'), nullable=False, index=True, comment='Sample id, see "sample.id_sample_tmp"')
    activity_type = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='The type of the activity performed')
    instrument = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='The name of the instrument used to perform the activity')
    kit_barcode = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='The barcode of the kit used to perform the activity')
    kit_type = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='The type of kit used to perform the activity')
    input_barcode = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='The barcode of the labware (eg. plate or tube) at the begining of the activity')
    output_barcode = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='The barcode of the labware (eg. plate or tube)  at the end of the activity')
    user = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='The name of the user who was most recently associated with the activity')
    last_updated = Column(DateTime, nullable=False, comment='Timestamp of last change to activity')
    recorded_at = Column(DateTime, nullable=False, comment='Timestamp of warehouse update')
    completed_at = Column(DateTime, nullable=False, comment='Timestamp of activity completion')
    deleted_at = Column(DateTime, comment='Timestamp of any activity removal')
    id_lims = Column(String(10, 'utf8_unicode_ci'), nullable=False, comment='LIM system identifier')

    sample = relationship('Sample')


class StockResource(Base):
    __tablename__ = 'stock_resource'
    __table_args__ = (
        Index('composition_lookup_index', 'id_stock_resource_lims', 'id_sample_tmp', 'id_lims'),
    )

    id_stock_resource_tmp = Column(INTEGER(11), primary_key=True)
    last_updated = Column(DateTime, nullable=False, comment='Timestamp of last update')
    recorded_at = Column(DateTime, nullable=False, comment='Timestamp of warehouse update')
    created = Column(DateTime, nullable=False, comment='Timestamp of initial registration of stock in LIMS')
    deleted_at = Column(DateTime, comment='Timestamp of initial registration of deletion in parent LIMS. NULL if not deleted.')
    id_sample_tmp = Column(ForeignKey('sample.id_sample_tmp'), nullable=False, index=True, comment='Sample id, see "sample.id_sample_tmp"')
    id_study_tmp = Column(ForeignKey('study.id_study_tmp'), nullable=False, index=True, comment='Sample id, see "study.id_study_tmp"')
    id_lims = Column(String(10, 'utf8_unicode_ci'), nullable=False, comment='LIM system identifier')
    id_stock_resource_lims = Column(String(20, 'utf8_unicode_ci'), nullable=False, comment='Lims specific identifier for the stock')
    stock_resource_uuid = Column(String(36, 'utf8_unicode_ci'), comment='Uuid identifier for the stock')
    labware_type = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='The type of labware containing the stock. eg. Well, Tube')
    labware_machine_barcode = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='The barcode of the containing labware as read by a barcode scanner')
    labware_human_barcode = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True, comment='The barcode of the containing labware in human readable format')
    labware_coordinate = Column(String(255, 'utf8_unicode_ci'), comment='For wells, the coordinate on the containing plate. Null for tubes.')
    current_volume = Column(Float, comment='The current volume of material in microlitres based on measurements and know usage')
    initial_volume = Column(Float, comment='The result of the initial volume measurement in microlitres conducted on the material')
    concentration = Column(Float, comment='The concentration of material recorded in the lab in nanograms per microlitre')
    gel_pass = Column(String(255, 'utf8_unicode_ci'), comment='The recorded result for the qel QC assay.')
    pico_pass = Column(String(255, 'utf8_unicode_ci'), comment='The recorded result for the pico green assay. A pass indicates a successful assay, not sufficient material.')
    snp_count = Column(INTEGER(11), comment='The number of markers detected in genotyping assays')
    measured_gender = Column(String(255, 'utf8_unicode_ci'), comment='The gender call base on the genotyping assay')

    sample = relationship('Sample')
    study = relationship('Study')


class StudyUser(Base):
    __tablename__ = 'study_users'

    id_study_users_tmp = Column(INTEGER(10), primary_key=True, comment='Internal to this database id, value can change')
    id_study_tmp = Column(ForeignKey('study.id_study_tmp'), nullable=False, index=True, comment='Study id, see "study.id_study_tmp"')
    last_updated = Column(DateTime, nullable=False, comment='Timestamp of last update')
    role = Column(String(255, 'utf8_unicode_ci'))
    login = Column(String(255, 'utf8_unicode_ci'))
    email = Column(String(255, 'utf8_unicode_ci'))
    name = Column(String(255, 'utf8_unicode_ci'))

    study = relationship('Study')


class TolSampleBioproject(Base):
    __tablename__ = 'tol_sample_bioproject'

    id_tsb_tmp = Column(INTEGER(10), primary_key=True)
    id_sample_tmp = Column(ForeignKey('sample.id_sample_tmp', ondelete='SET NULL'), index=True)
    file = Column(String(255), unique=True)
    library_type = Column(Enum('Chromium genome', 'Haplotagging', 'Hi-C', 'Hi-C - Arima v1', 'Hi-C - Arima v2', 'Hi-C - Dovetail', 'Hi-C - Omni-C', 'Hi-C - Qiagen', 'PacBio - CLR', 'PacBio - HiFi', 'ONT', 'RNA PolyA', 'RNA-seq dUTP eukaryotic', 'Standard', 'unknown', 'HiSeqX PCR free'))
    tolid = Column(String(40))
    biosample_accession = Column(String(255))
    bioproject_accession = Column(String(255))
    date_added = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    date_updated = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    filename = Column(String(255))

    sample = relationship('Sample')


class IseqProductMetric(Base):
    __tablename__ = 'iseq_product_metrics'
    __table_args__ = (
        ForeignKeyConstraint(['id_run', 'position'], ['iseq_run_lane_metrics.id_run', 'iseq_run_lane_metrics.position'], ondelete='CASCADE'),
        Index('iseq_pm_fcid_run_pos_tag_index', 'id_run', 'position', 'tag_index')
    )

    id_iseq_pr_metrics_tmp = Column(BIGINT(20), primary_key=True, comment='Internal to this database id, value can change')
    id_iseq_product = Column(CHAR(64, 'utf8_unicode_ci'), nullable=False, unique=True, comment='Product id')
    last_changed = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='Date this record was created or changed')
    id_iseq_flowcell_tmp = Column(ForeignKey('iseq_flowcell.id_iseq_flowcell_tmp', ondelete='SET NULL'), index=True, comment='Flowcell id, see "iseq_flowcell.id_iseq_flowcell_tmp"')
    id_run = Column(INTEGER(10), comment='NPG run identifier')
    position = Column(SMALLINT(2), comment='Flowcell lane number')
    tag_index = Column(SMALLINT(5), comment='Tag index, NULL if lane is not a pool')
    iseq_composition_tmp = Column(String(600, 'utf8_unicode_ci'), comment='JSON representation of the composition object, the column might be deleted in future')
    qc_seq = Column(TINYINT(1), comment='Sequencing lane level QC outcome, a result of either manual or automatic assessment by core')
    qc_lib = Column(TINYINT(1), comment='Library QC outcome, a result of either manual or automatic assessment by core')
    qc_user = Column(TINYINT(1), comment='Library QC outcome according to the data user criteria, a result of either manual or automatic assessment')
    qc = Column(TINYINT(1), comment='Overall QC assessment outcome, a logical product (conjunction) of qc_seq and qc_lib values, defaults to the qc_seq value when qc_lib is not defined')
    tag_sequence4deplexing = Column(String(30, 'utf8_unicode_ci'), comment='Tag sequence used for deplexing the lane, common suffix might have been truncated')
    actual_forward_read_length = Column(SMALLINT(4), comment='Actual forward read length, bp')
    actual_reverse_read_length = Column(SMALLINT(4), comment='Actual reverse read length, bp')
    indexing_read_length = Column(SMALLINT(2), comment='Indexing read length, bp')
    tag_decode_percent = Column(Float(5))
    tag_decode_count = Column(INTEGER(10))
    insert_size_quartile1 = Column(SMALLINT(5))
    insert_size_quartile3 = Column(SMALLINT(5))
    insert_size_median = Column(SMALLINT(5))
    insert_size_num_modes = Column(SMALLINT(4))
    insert_size_normal_fit_confidence = Column(Float(3))
    gc_percent_forward_read = Column(Float(5))
    gc_percent_reverse_read = Column(Float(5))
    sequence_mismatch_percent_forward_read = Column(Float(4))
    sequence_mismatch_percent_reverse_read = Column(Float(4))
    adapters_percent_forward_read = Column(Float(5))
    adapters_percent_reverse_read = Column(Float(5))
    ref_match1_name = Column(String(100, 'utf8_unicode_ci'))
    ref_match1_percent = Column(Float(5))
    ref_match2_name = Column(String(100, 'utf8_unicode_ci'))
    ref_match2_percent = Column(Float(5))
    q20_yield_kb_forward_read = Column(INTEGER(10))
    q20_yield_kb_reverse_read = Column(INTEGER(10))
    q30_yield_kb_forward_read = Column(INTEGER(10))
    q30_yield_kb_reverse_read = Column(INTEGER(10))
    q40_yield_kb_forward_read = Column(INTEGER(10))
    q40_yield_kb_reverse_read = Column(INTEGER(10))
    num_reads = Column(BIGINT(20))
    percent_mapped = Column(Float(5))
    percent_duplicate = Column(Float(5))
    chimeric_reads_percent = Column(Float(5), comment='mate_mapped_defferent_chr_5 as percentage of all')
    human_percent_mapped = Column(Float(5))
    human_percent_duplicate = Column(Float(5))
    genotype_sample_name_match = Column(String(8, 'utf8_unicode_ci'))
    genotype_sample_name_relaxed_match = Column(String(8, 'utf8_unicode_ci'))
    genotype_mean_depth = Column(Float(7))
    mean_bait_coverage = Column(Float(8))
    on_bait_percent = Column(Float(5))
    on_or_near_bait_percent = Column(Float(5))
    verify_bam_id_average_depth = Column(Float(11))
    verify_bam_id_score = Column(Float(6))
    verify_bam_id_snp_count = Column(INTEGER(10))
    rna_exonic_rate = Column(Float, comment='Exonic Rate is the fraction mapping within exons')
    rna_percent_end_2_reads_sense = Column(Float, comment='Percentage of intragenic End 2 reads that were sequenced in the sense direction.')
    rna_rrna_rate = Column(Float, comment='rRNA Rate is per total reads')
    rna_genes_detected = Column(INTEGER(10), comment='Number of genes detected with at least 5 reads.')
    rna_norm_3_prime_coverage = Column(Float, comment='3 prime n-based normalization: n is the transcript length at that end; norm is the ratio between the coverage at the 3 prime end and the average coverage of the full transcript, averaged over all transcripts')
    rna_norm_5_prime_coverage = Column(Float, comment='5 prime n-based normalization: n is the transcript length at that end; norm is the ratio between the coverage at the 5 prime end and the average coverage of the full transcript, averaged over all transcripts')
    rna_intronic_rate = Column(Float, comment='Intronic rate is the fraction mapping within introns')
    rna_transcripts_detected = Column(INTEGER(10), comment='Number of transcripts detected with at least 5 reads')
    rna_globin_percent_tpm = Column(Float, comment='Percentage of globin genes TPM (transcripts per million) detected')
    rna_mitochondrial_percent_tpm = Column(Float, comment='Percentage of mitochondrial genes TPM (transcripts per million) detected')
    gbs_call_rate = Column(Float, comment='The GbS call rate is the fraction of loci called on the relevant primer panel')
    gbs_pass_rate = Column(Float, comment='The GbS pass rate is the fraction of loci called and passing filters on the relevant primer panel')
    nrd_percent = Column(Float(5), comment='Percent of non-reference discordance')
    target_filter = Column(String(30, 'utf8_unicode_ci'), comment='Filter used to produce the target stats file')
    target_length = Column(BIGINT(12), comment='The total length of the target regions')
    target_mapped_reads = Column(BIGINT(20), comment='The number of mapped reads passing the target filter')
    target_proper_pair_mapped_reads = Column(BIGINT(20), comment='The number of proper pair mapped reads passing the target filter')
    target_mapped_bases = Column(BIGINT(20), comment='The number of mapped bases passing the target filter')
    target_coverage_threshold = Column(INTEGER(4), comment='The coverage threshold used in the target perc target greater than depth calculation')
    target_percent_gt_coverage_threshold = Column(Float(5), comment='The percentage of the target covered at greater than the depth specified')
    target_autosome_coverage_threshold = Column(INTEGER(4), comment='The coverage threshold used in the perc target autosome greater than depth calculation')
    target_autosome_percent_gt_coverage_threshold = Column(Float(5), comment='The percentage of the target autosome covered at greater than the depth specified')

    iseq_flowcell = relationship('IseqFlowcell')
    iseq_run_lane_metric = relationship('IseqRunLaneMetric')


class PacBioProductMetric(Base):
    __tablename__ = 'pac_bio_product_metrics'
    __table_args__ = {'comment': 'A linking table for the pac_bio_run and pac_bio_run_well_metrics tables with a potential for adding per-product QC data'}

    id_pac_bio_pr_metrics_tmp = Column(INTEGER(11), primary_key=True)
    id_pac_bio_rw_metrics_tmp = Column(ForeignKey('pac_bio_run_well_metrics.id_pac_bio_rw_metrics_tmp', ondelete='CASCADE'), nullable=False, index=True, comment='PacBio run well metrics id, see "pac_bio_run_well_metrics.id_pac_bio_rw_metrics_tmp"')
    id_pac_bio_tmp = Column(ForeignKey('pac_bio_run.id_pac_bio_tmp', ondelete='SET NULL'), index=True, comment='PacBio run id, see "pac_bio_run.id_pac_bio_tmp"')

    pac_bio_run_well_metric = relationship('PacBioRunWellMetric')
    pac_bio_run = relationship('PacBioRun')


class IseqProductAmpliconstat(Base):
    __tablename__ = 'iseq_product_ampliconstats'
    __table_args__ = (
        Index('iseq_pastats_amplicon', 'primer_panel_num_amplicons', 'amplicon_index'),
        Index('iseq_hrm_digest_unq', 'id_iseq_product', 'primer_panel', 'amplicon_index', unique=True),
        {'comment': 'Some of per sample per amplicon metrics generated by samtools ampliconstats'}
    )

    id_iseq_pr_astats_tmp = Column(BIGINT(20), primary_key=True, comment='Internal to this database id, value can change')
    created = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='Datetime this record was created')
    last_changed = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='Datetime this record was created or changed')
    id_iseq_product = Column(ForeignKey('iseq_product_metrics.id_iseq_product'), nullable=False, comment='Product id, a foreign key into iseq_product_metrics table')
    primer_panel = Column(String(255, 'utf8_unicode_ci'), nullable=False, comment='A string uniquely identifying the primer panel')
    primer_panel_num_amplicons = Column(SMALLINT(5), nullable=False, comment='Total number of amplicons in the primer panel')
    amplicon_index = Column(SMALLINT(5), nullable=False, comment='Amplicon index (position) in the primer panel, from 1 to the value of primer_panel_num_amplicons')
    pp_name = Column(String(40, 'utf8_unicode_ci'), nullable=False, comment='Name of the portable pipeline that generated the data')
    pp_version = Column(String(40, 'utf8_unicode_ci'), comment='Version of the portable pipeline and/or samtools that generated the data')
    metric_FPCOV_1 = Column(DECIMAL(5, 2), comment='Coverage percent at depth 1')
    metric_FPCOV_10 = Column(DECIMAL(5, 2), comment='Coverage percent at depth 10')
    metric_FPCOV_20 = Column(DECIMAL(5, 2), comment='Coverage percent at depth 20')
    metric_FPCOV_100 = Column(DECIMAL(5, 2), comment='Coverage percent at depth 100')
    metric_FREADS = Column(INTEGER(10), comment='Number of aligned filtered reads')

    iseq_product_metric = relationship('IseqProductMetric')


class IseqProductComponent(Base):
    __tablename__ = 'iseq_product_components'
    __table_args__ = (
        Index('iseq_pr_comp_compi', 'component_index', 'num_components'),
        Index('iseq_pr_comp_unique', 'id_iseq_pr_tmp', 'id_iseq_pr_component_tmp', unique=True),
        Index('iseq_pr_comp_ncomp', 'num_components', 'id_iseq_pr_tmp')
    )

    id_iseq_pr_components_tmp = Column(BIGINT(20), primary_key=True, comment='Internal to this database id, value can change')
    id_iseq_pr_tmp = Column(ForeignKey('iseq_product_metrics.id_iseq_pr_metrics_tmp', ondelete='CASCADE'), nullable=False, comment='iseq_product_metrics table row id for the product')
    id_iseq_pr_component_tmp = Column(ForeignKey('iseq_product_metrics.id_iseq_pr_metrics_tmp'), nullable=False, index=True, comment="iseq_product_metrics table row id for one of this product's components")
    num_components = Column(TINYINT(3), nullable=False, comment='Number of component products for this product')
    component_index = Column(TINYINT(3), nullable=False, comment='Unique component index within all components of this product, \\na value from 1 to the value of num_components column for this product')

    iseq_product_metric = relationship('IseqProductMetric', primaryjoin='IseqProductComponent.id_iseq_pr_component_tmp == IseqProductMetric.id_iseq_pr_metrics_tmp')
    iseq_product_metric1 = relationship('IseqProductMetric', primaryjoin='IseqProductComponent.id_iseq_pr_tmp == IseqProductMetric.id_iseq_pr_metrics_tmp')
