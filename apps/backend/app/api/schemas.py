from pydantic import BaseModel, Field

class RunConfiguration(BaseModel):
    runner_type: str = Field(default="ollama", description="The type of AI runner to use (e.g., ollama, vllm)")
    model_name: str = Field(..., description="The name of the AI model to benchmark")
    dataset_name: str = Field(..., description="The HuggingFace dataset to use")
    prompt_template: str = Field(default="Classify the following text:\n{text}", description="The prompt template for generation")
    max_items: int = Field(default=10, description="Max items to process in this run")
    concurrency: int = Field(default=1, description="Number of concurrent inference requests")

class RunResponse(BaseModel):
    job_id: str
    status: str
