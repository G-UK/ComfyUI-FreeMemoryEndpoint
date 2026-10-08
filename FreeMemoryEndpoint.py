import json
import urllib.request
import comfy.cli_args

class FreeMemoryEndpointNode:
    """Pass-through that triggers ComfyUI's own /free endpoint.
    The worker consumes the flags right after this prompt completes:
    unload_all_models() + PromptExecutor.reset() + gc.collect()."""

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("*",)}}

    RETURN_TYPES = ("*",)
    FUNCTION = "route"

    def route(self, **kwargs):
        port = comfy.cli_args.args.port
        payload = json.dumps({"unload_models": True, "free_memory": True}).encode()
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/free",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"FreeMemoryEndpoint: /free -> HTTP {resp.status}")
        return (kwargs.get("value"),)

NODE_CLASS_MAPPINGS = {
    "FreeMemoryEndpoint": FreeMemoryEndpointNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FreeMemoryEndpoint": "FreeMemoryEndpoint",
}
