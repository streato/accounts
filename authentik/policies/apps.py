"""authentik policies app config"""
from prometheus_client import Gauge, Histogram

from authentik.blueprints.apps import ManagedAppConfig

GAUGE_POLICIES_CACHED = Gauge(
    "authentik_policies_cached",
    "Cached Policies",
)
HIST_POLICIES_BUILD_TIME = Histogram(
    "authentik_policies_build_time",
    "Execution times complete policy result to an object",
    ["object_pk", "object_type"],
)

HIST_POLICIES_EXECUTION_TIME = Histogram(
    "authentik_policies_execution_time",
    "Execution times for single policies",
    [
        "binding_order",
        "binding_target_type",
        "binding_target_name",
        "object_pk",
        "object_type",
    ],
)


class AuthentikPoliciesConfig(ManagedAppConfig):
    """authentik policies app config"""

    name = "authentik.policies"
    label = "authentik_policies"
    verbose_name = "authentik Policies"
    default = True

    def reconcile_load_policies_signals(self):
        """Load policies signals"""
        self.import_module("authentik.policies.signals")
