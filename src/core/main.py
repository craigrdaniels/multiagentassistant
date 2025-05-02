from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Dict


class Core:
    def __init__(self):
        self._modules: Dict[str, object] = {}
        self._module_path = Path(__file__).parent.parent / "modules"
        self._load_modules()

    def _load_modules(self):
        if not self._module_path.exists():
            raise FileNotFoundError(f"Module path {self._module_path} does not exist.")
        for module in self._module_path.iterdir():
            if module.is_dir() and (module / "main.py").exists():
                mod_name = module.name
                spec = spec_from_file_location(
                    f"src.modules.{mod_name}", module / "main.py"
                )
                if spec is None:
                    raise FileNotFoundError(f"Could not load spec for {mod_name}.")
                module_instance = module_from_spec(spec)
                spec.loader.exec_module(module_instance)
                self._modules[mod_name] = module_instance.Agent()

    async def run_agent(self, module_name: str, *args, **kwargs):
        agent = self._modules.get(module_name)
        if agent:
            return await agent.run(*args, **kwargs)
        else:
            raise ValueError(f"Module {module_name} not found or loaded.")
