from src.ai.v2_pipeline import V2RecruitingPipeline


def test_real_v2_pipeline_can_initialize():

    pipeline = V2RecruitingPipeline()

    assert pipeline.parser is not None
    assert pipeline.evaluator is not None
    assert pipeline.knowledge_base is not None
    assert pipeline.search_engine is not None
    assert pipeline.copilot is not None