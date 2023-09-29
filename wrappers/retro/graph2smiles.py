from pydantic import BaseModel, Field
from wrappers import register_wrapper
from wrappers.base import BaseResponse, BaseWrapper


class RetroG2SInput(BaseModel):
    model_name: str
    smiles: list[str]


class RetroG2SResult(BaseModel):
    reactants: list[str] = Field(alias="products")
    scores: list[float]


class RetroG2SOutput(BaseModel):
    __root__: list[RetroG2SResult]


class RetroG2SResponse(BaseResponse):
    result: list[RetroG2SResult]


@register_wrapper(
    name="retro_graph2smiles",
    input_class=RetroG2SInput,
    output_class=RetroG2SOutput,
    response_class=RetroG2SResponse
)
class RetroG2SWrapper(BaseWrapper):
    """Wrapper class for Retro Prediction with Graph2SMILES"""
    prefixes = ["retro/graph2smiles"]

    def call_raw(self, input: RetroG2SInput) -> RetroG2SOutput:
        input_as_dict = input.dict()
        model_name = input_as_dict["model_name"]

        response = self.session_sync.post(
            f"{self.prediction_url}/{model_name}",
            json=input_as_dict,
            timeout=self.config["deployment"]["timeout"]
        )
        output = response.json()
        output = RetroG2SOutput(__root__=output)

        return output

    def call_sync(self, input: RetroG2SInput) -> RetroG2SResponse:
        output = self.call_raw(input=input)
        response = self.convert_output_to_response(output)

        return response

    async def call_async(self, input: RetroG2SInput, priority: int = 0) -> str:
        from askcos2_celery.tasks import retro_task
        async_result = retro_task.apply_async(
            args=(self.name, input.dict()), priority=priority)
        task_id = async_result.id

        return task_id

    async def retrieve(self, task_id: str) -> RetroG2SResponse | None:
        return await super().retrieve(task_id=task_id)

    @staticmethod
    def convert_output_to_response(output: RetroG2SOutput
                                   ) -> RetroG2SResponse:
        response = {
            "status_code": 200,
            "message": "",
            "result": output.__root__
        }
        response = RetroG2SResponse(**response)

        return response
