from __future__ import annotations

import wandb

from typing import TYPE_CHECKING, TypeVar

from tests.sim.item import ProductTypeReferences

if TYPE_CHECKING:
    import desym.core
    import desym.controllers.results_controller
    from desym.core import Simulation

step_to_time = 0.1
wandb_data_dict: dict = {}


wandb.init(project="i4techlab-simulation", entity="soobbz")
config = wandb.config
wandb.define_metric("results/simulation_time")
wandb.define_metric("results/*", step_metric="results/simulation_time")


def step_callback(core: desym.core.Simulation):
    if wandb_data_dict != {}:
        wandb_data_dict["results/simulation_time"] = (
            core.events_manager.step * step_to_time / 60
        )
        wandb.log(wandb_data_dict)
        wandb_data_dict.clear()


def production_update_callback(
    controller: desym.controllers.results_controller.CounterResultsController,
    index: ProductTypeReferences,
    time: int,
) -> None:
    wandb_data_dict[f"results/production/{index.name}"] = controller.counters[index]


def time_update_callback(
    results: desym.controllers.results_controller.TimesResultsController, step: int
):
    wandb_data_dict["results/times"] = {
        key: results.times[key] for key in ["DIR04", "PT05", "PT06"]
    }


def busyness_update_callback(controller, busyness, step: int):
    wandb_data_dict["results/busyness"] = busyness
