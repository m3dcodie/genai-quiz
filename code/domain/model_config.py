class BaseModelConfig:
    def __init__(self, temperature=0.5, **kwargs):
        self.temperature = temperature
        self.additional_fields = kwargs

    def to_inference_config(self):
        config = {"temperature": self.temperature}
        config.update(self.additional_fields)
        return config

class NovaLiteConfig(BaseModelConfig):
    def __init__(self, temperature=0.5, top_k=None, **kwargs):
        super().__init__(temperature, **kwargs)
        if top_k is not None:
            self.additional_fields["top_k"] = top_k

class TitanConfig(BaseModelConfig):
    def __init__(self, temperature=0.5, top_p=None, **kwargs):
        super().__init__(temperature, **kwargs)
        if top_p is not None:
            self.additional_fields["top_p"] = top_p
