import copy
import logging
from typing import Any, List, Tuple

import torch
import torch.nn as nn
from typeguard import typechecked

from espnet2.lm.abs_model import AbsLM
from espnet.nets.pytorch_backend.transformer.mask import subsequent_mask


class HuggingfaceGPT2Model(AbsLM):
    @typechecked
    def __init__(
        self,
        vocab_size: int,
        gpt2_name: str,
        remove_head: bool = True,
    ):
        super().__init__()
        try:
            from transformers import GPT2Model
        except Exception as e:
            print("Error: transformers is not properly installed.")
            print("Please install transformers")
            raise e

        # opt_model_name_pattern = re.compile(r"facebook/opt-\d+m")
        # assert opt_model_name_pattern.match(opt_name) is not None

        pretrained_gpt2_model = GPT2Model.from_pretrained(gpt2_name)
        pretrained_gpt2_model_dict = pretrained_gpt2_model.state_dict()
        # pre_trained_lm_head = pretrained_gpt2_model_dict.pop("decoder.embed_tokens.weight")
        pretrained_gpt2_model_dict.pop("wte.weight")
        self.pretrained_params = copy.deepcopy(pretrained_gpt2_model_dict)

        config = pretrained_gpt2_model.config
        if remove_head:
            # remove_head=True の場合の処理（今回は考慮しない）
            pass
        else:
            # self.decoder = GPT2Model(config)
            self.decoder = pretrained_gpt2_model
            # self.lm_head = nn.Linear(
            #     pre_trained_lm_head.size(1), pre_trained_lm_head.size(0), bias=False
            # )
            self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)
            # self.lm_head.weight = nn.Parameter(pre_trained_lm_head)
            self.lm_head.weight = self.decoder.wte.weight

    def _target_mask(self, ys_in_pad):
        ys_mask = ys_in_pad != 0
        m = subsequent_mask(ys_mask.size(-1), device=ys_mask.device).unsqueeze(0)
        return ys_mask.unsqueeze(-2) & m

    def forward(self, input: torch.Tensor, hidden: None) -> Tuple[torch.Tensor, None]:
        """Compute LM loss value from buffer sequences.

        Args:
            input (torch.Tensor): Input ids. (batch, len)
            hidden (torch.Tensor): Target ids. (batch, len)

        """
        pad_mask = input != 0
        y = self.decoder(
            input,
            attention_mask=pad_mask,
            return_dict=True,
        )
        y = y.last_hidden_state

        logits = self.lm_head(y)

        return logits, None

    def score(
        self, y: torch.Tensor, state: Any, x: torch.Tensor
    ) -> Tuple[torch.Tensor, Any]:
        """Score new token.

        Args:
            y (torch.Tensor): 1D torch.int64 prefix tokens.
            state: Scorer state for prefix tokens
            x (torch.Tensor): encoder feature that generates ys.

        Returns:
            tuple[torch.Tensor, Any]: Tuple of
                torch.float32 scores for next token (vocab_size)
                and next state for ys

        """
        if state is None:
            _use_cache = True
        else:
            _use_cache = False

        y = y.unsqueeze(0)

        output = self.decoder(
            y,
            past_key_values=state,
            use_cache=_use_cache,
            output_hidden_states=True,
            return_dict=True,
        )

        h = output.last_hidden_state[:, -1]
        h = self.lm_head(h)
        cache = output.past_key_values
        logp = h.log_softmax(dim=-1).squeeze(0)
        return logp, cache

    def batch_score(
        self, ys: torch.Tensor, states: List[Any], xs: torch.Tensor
    ) -> Tuple[torch.Tensor, List[Any]]:
        """Score new token batch.

        Args:
            ys (torch.Tensor): torch.int64 prefix tokens (n_batch, ylen).
            states (List[Any]): Scorer states for prefix tokens.
            xs (torch.Tensor):
                The encoder feature that generates ys (n_batch, xlen, n_feat).

        Returns:
            tuple[torch.Tensor, List[Any]]: Tuple of
                batchfied scores for next token with shape of `(n_batch, vocab_size)`
                and next state list for ys.

        """
        # merge states
        n_batch = len(ys)
        n_layers = len(self.decoder.decoder.layers)
        if states[0] is None:
            _use_cache = True
        else:
            _use_cache = False

        # batch decoding
        output = self.decoder(
            ys,
            use_cache=_use_cache,
            output_hidden_states=True,
            return_dict=True,
        )
        h = output.last_hidden_state
        h = self.lm_head(h[:, -1])

        logp = h.log_softmax(dim=-1)

        state_list = [[[] for i in range(n_layers)] for b in range(n_batch)]
        return logp, state_list

    def reload_pretrained_parameters(self):
        self.decoder.load_state_dict(self.pretrained_params, strict=False)
        logging.info("Pretrained GPT2 model parameters reloaded!")
