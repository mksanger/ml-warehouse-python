from datetime import datetime
from examples.genotyping import get_flgen_plate
from examples.long_illumina import summarize_long_illumina
from examples.npg_qc import (
    get_iseq_product_metrics_by_study,
    get_iseq_product_metrics_run,
    get_iseq_product_metrics_by_decode_percent,
)
from examples.npg_irods import (
    find_pacbio_runs,
    get_bmap_flowcell_records,
    get_stock_records,
)
from examples.recently_updated import (
    get_recent_fluidigm,
    get_recent_ont,
    get_recent_pacbio_runs,
)
from pytest import mark as m
from tests.ml_warehouse_fixture import (
    mlwh_session,
    mlwh_session_flgen,
    mlwh_session_ipm,
)

# Stop IDEs optimizing away import
_ = mlwh_session_flgen, mlwh_session, mlwh_session_ipm


@m.describe("Running example queries")
class TestMLWarehouseExampleRecentQueries(object):
    @m.it("Successfully retrieve recently updated PacBio runs")
    def test_retrieve_recent_pacbio(self, mlwh_session):

        max_age = datetime(year=2021, month=1, day=31)

        recent_runs = get_recent_pacbio_runs(mlwh_session, max_age)

        lims_ids = [
            str(i)
            for i in [
                81230,
                81876,
                83472,
                83472,
                83472,
                83472,
                83472,
                83472,
                83472,
                83472,
            ]
        ]

        # Check count, so test doesn't risk taking ages to fail
        assert recent_runs.count() == len(lims_ids)

        returned_lims_ids = [row.id_pac_bio_run_lims for row in recent_runs.all()]

        assert lims_ids == returned_lims_ids

    @m.it("Successfully retrieve recently updated ONT runs")
    def test_retrieve_recent_ont(self, mlwh_session):

        max_age = datetime(year=2018, month=1, day=1)

        recent_runs = get_recent_ont(mlwh_session, max_age)

        expected_names = [
            "4944STDY7082749",
            "4944STDY7082750",
            "4616STDY7090433",
            "4616STDY7090433",
            "4616STDY7090433",
            "4616STDY7090433",
            "4616STDY7090433",
            "4616STDY7105671",
            "4616STDY7105672",
        ]

        # Check count, so test doesn't risk taking ages to fail
        assert recent_runs.count() == len(expected_names)

        returned_names = [row.name for row in recent_runs.all()]

        assert expected_names == returned_names

    @m.it("Successfully retrieve recently updated fluidigm")
    def test_retrieve_recent_fluidigm(self, mlwh_session_flgen):

        max_age = datetime(year=2021, month=8, day=19)

        records = get_recent_fluidigm(mlwh_session_flgen, max_age)

        assert records.count() == 3

        expected_records = [
            (
                "bibkidex10103728",
                0,
                datetime(2021, 8, 12, 12, 0, 43),
                "6407",
                1662436137,
                "S018",
                datetime(2021, 8, 24, 15, 21, 38),
            ),
            (
                "bibkidex10103121",
                0,
                datetime(2021, 8, 12, 11, 58, 33),
                "6407",
                1662436101,
                "S133",
                datetime(2021, 8, 24, 15, 45, 16),
            ),
            (
                "bibkidex10103357",
                0,
                datetime(2021, 8, 12, 11, 59, 18),
                "6407",
                1662457061,
                "S091",
                datetime(2021, 8, 25, 10, 21, 52),
            ),
        ]
        assert records.all() == expected_records


@m.describe("Running example genotyping queries")
class TestMLWarehouseExampleGenotypingQueries(object):
    @m.it("Successfuly retrieve set of FlgenPlate matching barcode and label")
    def test_retrieve_flgen_plate(self, mlwh_session_flgen):

        records = get_flgen_plate(mlwh_session_flgen, 1382108143, "S70")

        assert records.count() == 1

        expected_result = [
            23194,
            2210630,
            3,
            "S0968",
            "SQSCP",
            datetime(2015, 3, 17, 9, 55, 18),
            datetime(2015, 4, 8, 15, 19, 58),
            1382108143,
            "13275428",
            "S70",
            "DN393179O",
            "8b124bb0-cc8b-11e4-9491-68b59976a382",
            96,
            None,
            "46664fe0-c8ba-11e4-b55f-3c4a9275d6c6",
            None,
        ]
        res = records.first()
        actual_result = [getattr(res, col.name) for col in res.__table__.columns]

        assert actual_result == expected_result


@m.describe("Running example npg_irods queries")
class TestMLWarehouseExampleNpgIrodsQueries(object):
    @m.it("Successfully retrieve StockResource by stock ID")
    def test_retrieve_stock_resource(self, mlwh_session):

        stock_id = "stock_barcode_01234"

        records = get_stock_records(mlwh_session, stock_id)

        assert records.count() == 1
        assert records.first().id_stock_resource_tmp == 2345678

    @m.it("Successfully retrieve BmapFlowcellRecords by chip serialnumber and position")
    def test_retrieve_bmap_flowcell(self, mlwh_session):

        chip_serialnumber = "KHPZDTGLPQJGPNWU"
        position = 2

        records = get_bmap_flowcell_records(mlwh_session, chip_serialnumber, position)

        assert records.count() == 1
        assert records.first().id_sample_tmp == 3135749

    @m.it("Successfully retrieve PacBio runs")
    def test_retrieve_pacbio_runs(self, mlwh_session):

        run_id = 32669
        plate_well = "B1"
        tag_identifier = None

        records = find_pacbio_runs(mlwh_session, run_id, plate_well, tag_identifier)

        expected_ids_tmp = [
            1714,
            1715,
            1717,
            1720,
            1727,
            2993,
            3118,
            4063,
            12460,
            12461,
            12462,
            12463,
            12464,
            12465,
            12466,
            12467,
            12468,
            12469,
            12470,
            12471,
            12472,
            12473,
            12474,
            12475,
            16207,
            20300,
        ]

        assert records.count() == 26

        returned_ids_tmp = [row.id_pac_bio_tmp for row in records.all()]

        assert expected_ids_tmp == returned_ids_tmp


@m.describe("Running example npg_qc queries")
class TestMLWarehouseExampleNpgQcQueries(object):
    @m.it("Successfully retrieve IseqProductMetrics")
    def test_retrieve_iseq_product_metrics(self, mlwh_session_ipm):

        run_ids = [7915, 15440, 18980, 17550]
        excluded_type = "library_indexed_spike"
        study_count = 5

        records = get_iseq_product_metrics_run(
            mlwh_session_ipm, run_ids, excluded_type, study_count
        )

        assert records.count() == 1
        assert records.first().id_run == 17550
        assert records.first().study_count == 5

    @m.it("Successfully retrieve IseqProductMetrics by study")
    def test_retrieve_iseq_product_metrics_by_study(self, mlwh_session_ipm):

        study_name = "Illumina Controls"
        run_ids = (7915, 17550, 18980, 7915, 18448, 1337)

        records = get_iseq_product_metrics_by_study(
            mlwh_session_ipm, study_name, run_ids
        )

        assert records.count() == 3

        returned_run_ids = [row.id_run for row in records.all()]
        expected_run_ids = [7915, 17550, 18980]
        assert returned_run_ids == expected_run_ids

    @m.it("Successfully retrieve IseqProductMetrics by decode percent")
    def test_retrieve_iseq_product_metrics_by_decode_percent(self, mlwh_session):

        max_decode_percent = 95
        run_ids = [7915, 15440, 18448, 18980, 26291]

        records = get_iseq_product_metrics_by_decode_percent(
            mlwh_session, max_decode_percent, run_ids
        )

        assert records.count() == 2

        returned_run_ids = [row.id_run for row in records.all()]
        expected_run_ids = [18448, 26291]
        assert returned_run_ids == expected_run_ids


@m.describe("Running example long Illumina runs query")
class TestMLWarehouseExampleLongIlluminaQuery(object):
    @m.it("Successfully get long Illumina runs")
    def test_summarize_long_illumina(self, mlwh_session_ipm):

        faculty_sponsor_pattern = "%tyler%"
        max_age = datetime(year=2015, month=1, day=14)
        active_run_min_age = datetime(year=2021, month=8, day=31)
        min_tot_days = 3
        ids_also_included = [3434, 1239, 1453]

        records = summarize_long_illumina(
            mlwh_session_ipm,
            faculty_sponsor_pattern,
            max_age,
            active_run_min_age,
            min_tot_days,
            ids_also_included,
        )

        assert records.count() == 1

        expected = [
            15440,
            "qc complete",
            datetime(2015, 2, 8, 21, 9, 14),
            4,
            "SEQCAP_Lebanon_LowCov-seq",
        ]
        actual = [i for i in records.first()._asdict().values()]

        assert expected == actual
