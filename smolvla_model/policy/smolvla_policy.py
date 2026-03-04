import torch

from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy
from lerobot.policies.factory import make_pre_post_processors


class Policy:

    def __init__(self):

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device

        model_id = "lerobot/smolvla_base"

        self.policy = (
            SmolVLAPolicy
            .from_pretrained(model_id)
            .to(device)
            .eval()
        )

        # IMPORTANT
        self.preprocess, self.postprocess = make_pre_post_processors(
            self.policy.config,
            model_id,
            preprocessor_overrides={
                "device_processor": {"device": str(device)}
            }
        )


    def act(self, obs, instruction):

        # add task
        obs["task"] = instruction

        # preprocess generates:
        # observation.language.tokens
        # observation.language.attention_mask
        batch = self.preprocess(obs)

        with torch.inference_mode():
            action = self.policy.select_action(batch)

        action = self.postprocess(action)

        return action