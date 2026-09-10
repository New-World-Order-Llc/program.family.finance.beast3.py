# program.family.finance.beast3.py
# Beast System 3.0 — Deterministic Financial Routing Module

from dataclasses import dataclass, field
import time
import hashlib

@dataclass
class FinancialEvent:
    event_type: str
    amount: float
    metadata: dict
    ts: float = field(default_factory=time.time)

@dataclass
class FinanceProfile:
    family_id: str
    balance: float = 0.0
    ledger: list = field(default_factory=list)
    last_update: float = field(default_factory=time.time)

    def apply_event(self, event_type: str, amount: float, metadata: dict):
        entry = FinancialEvent(event_type, amount, metadata)
        self.ledger.append(entry)
        self.balance += amount
        self.last_update = entry.ts

class FinanceEngine:
    def __init__(self, kernel):
        self.kernel = kernel
        self.profiles = {}

    def create_profile(self, family_id: str):
        profile = FinanceProfile(family_id)
        self.profiles[family_id] = profile

        return self.kernel.dispatch(
            module="family.finance",
            action="create_profile",
            payload={"family_id": family_id}
        )

    def disburse(self, family_id: str, amount: float, reason: str):
        if family_id not in self.profiles:
            raise ValueError("Finance profile not found")

        profile = self.profiles[family_id]
        profile.apply_event("disbursement", amount, {"reason": reason})

        return self.kernel.dispatch(
            module="family.finance",
            action="disburse",
            payload={"family_id": family_id, "amount": amount, "reason": reason}
        )

    def adjust(self, family_id: str, amount: float, note: str):
        if family_id not in self.profiles:
            raise ValueError("Finance profile not found")

        profile = self.profiles[family_id]
        profile.apply_event("adjustment", amount, {"note": note})

        return self.kernel.dispatch(
            module="family.finance",
            action="adjust",
            payload={"family_id": family_id, "amount": amount, "note": note}
        )

    def get_profile(self, family_id: str):
        return self.profiles.get(family_id, None)
