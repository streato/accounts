"""Dummy policy"""
from random import SystemRandom
from time import sleep

from django.db import models
from django.utils.translation import gettext_lazy as _
from structlog import get_logger

from passbook.core.models import Policy
from passbook.policies.types import PolicyRequest, PolicyResult

LOGGER = get_logger()


class DummyPolicy(Policy):
    """Policy used for debugging the PolicyEngine. Returns a fixed result,
    but takes a random time to process."""

    result = models.BooleanField(default=False)
    wait_min = models.IntegerField(default=5)
    wait_max = models.IntegerField(default=30)

    form = "passbook.policies.dummy.forms.DummyPolicyForm"

    def passes(self, request: PolicyRequest) -> PolicyResult:
        """Wait random time then return result"""
        wait = SystemRandom().randrange(self.wait_min, self.wait_max)
        LOGGER.debug("Policy waiting", policy=self, delay=wait)
        sleep(wait)
        return PolicyResult(self.result, "dummy")

    class Meta:

        verbose_name = _("Dummy Policy")
        verbose_name_plural = _("Dummy Policies")
