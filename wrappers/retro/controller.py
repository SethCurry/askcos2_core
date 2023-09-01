from pydantic import BaseModel
from typing import Any, Literal
from wrappers import register_wrapper
from wrappers.base import BaseResponse, BaseWrapper
from wrappers.retro.augmented_transformer import RetroATInput, RetroATResponse
from wrappers.retro.graph2smiles import RetroG2SInput, RetroG2SResponse
from wrappers.retro.template_relevance import RetroTemplRelInput, RetroTemplRelResponse
from wrappers.registry import get_wrapper_registry


class AttributeFilter(BaseModel):
    name: str
    logic: Literal[">", ">=", "<", "<=", "=="]
    value: int | float


class RetroInput(BaseModel):
    backend: Literal[
        "augmented_transformer", "graph2smiles", "template_relevance"
    ] = "template_relevance"
    model_name: str = "reaxys"
    smiles: list[str]

    # For template_relevance only
    max_num_templates: int = 1000
    max_cum_prob: float = 0.999
    attribute_filter: list[AttributeFilter] = []


class RetroOutput(BaseModel):
    placeholder: str


class RetroResult(BaseModel):
    outcome: str
    score: float
    template: dict[str, Any] | None


class RetroResponse(BaseResponse):
    result: list[list[RetroResult]]


@register_wrapper(
    name="retro_controller",
    input_class=RetroInput,
    output_class=RetroOutput,
    response_class=RetroResponse
)
class RetroController(BaseWrapper):
    """Retro Controller"""
    prefixes = ["retro/controller", "retro"]
    backend_wrapper_names = {
        "augmented_transformer": "retro_augmented_transformer",
        "graph2smiles": "retro_graph2smiles",
        "template_relevance": "retro_template_relevance"
    }

    def __init__(self):
        pass        # TODO: proper inheritance

    def call_sync(self, input: RetroInput) -> RetroResponse:
        module = self.backend_wrapper_names[input.backend]
        wrapper = get_wrapper_registry().get_wrapper(module=module)

        wrapper_input = self.convert_input(
            input=input, backend=input.backend)
        wrapper_response = wrapper.call_sync(wrapper_input)
        response = self.convert_response(
            wrapper_response=wrapper_response, backend=input.backend)

        return response

    async def call_async(self, input: RetroInput, priority: int = 0) -> str:
        return await super().call_async(input=input, priority=priority)

    async def retrieve(self, task_id: str) -> RetroResponse | None:
        return await super().retrieve(task_id=task_id)

    @staticmethod
    def convert_input(
        input: RetroInput, backend: str
    ) -> RetroATInput | RetroG2SInput | RetroTemplRelInput:
        if backend == "augmented_transformer":
            wrapper_input = RetroATInput(
                model_name=input.model_name,
                smiles=input.smiles
            )
        elif backend == "graph2smiles":
            wrapper_input = RetroG2SInput(
                model_name=input.model_name,
                smiles=input.smiles
            )
        elif backend == "template_relevance":
            wrapper_input = RetroTemplRelInput(
                model_name=input.model_name,
                smiles=input.smiles,
                max_num_templates=input.max_num_templates,
                max_cum_prob=input.max_cum_prob,
                attribute_filter=input.attribute_filter
            )
        else:
            raise ValueError(f"Unsupported retro backend: {backend}!")

        return wrapper_input

    @staticmethod
    def convert_response(
        wrapper_response:
            RetroATResponse | RetroG2SResponse | RetroTemplRelResponse,
        backend: str
    ) -> RetroResponse:
        status_code = wrapper_response.status_code
        message = wrapper_response.message
        if backend in ["augmented_transformer", "graph2smiles"]:
            # list[dict] -> list[list[dict]]
            result = []
            for result_per_smi in wrapper_response.result:
                result.append(
                    [{"outcome": outcome, "score": score} for outcome, score
                     in zip(result_per_smi.reactants, result_per_smi.scores)]
                )
        elif backend == "template_relevance":
            # list[dict] -> list[list[dict]]
            result = []
            for result_per_smi in wrapper_response.result:
                result.append(
                    [{"outcome": outcome, "score": score, "template": template}
                     for outcome, score, template in zip(
                        result_per_smi.reactants,
                        result_per_smi.scores,
                        result_per_smi.templates
                    )]
                )
        else:
            raise ValueError(f"Unsupported retro backend: {backend}!")

        response = {
            "status_code": status_code,
            "message": message,
            "result": result
        }
        response = RetroResponse(**response)

        return response
