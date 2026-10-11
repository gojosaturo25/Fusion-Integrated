from dataclasses import dataclass

@dataclass(frozen=True)
class LeavePolicy:
    # BR-EL-001 — Supported leave-category eligibility
    @staticmethod
    def is_category_applicable(category: str, principal: int) -> bool:
        return category in ["CL", "RH", "SCL", "EL", "COL", "VL"]

    # BR-EL-002 — Casual Leave entitlement and lapse
    @staticmethod
    def get_cl_entitlement(principal: int) -> int:
        return 8  # 8 CL days per year

    @staticmethod
    def get_cl_lapse(principal: int) -> bool:
        return True  # unused CL lapses at year end

    # BR-EL-003 — Restricted Holiday entitlement and applicability
    @staticmethod
    def get_rh_entitlement(principal: int) -> int:
        return 2  # 2 RH days per year

    @staticmethod
    def is_rh_applicable(principal: int, rh_date: str) -> bool:
        # Placeholder for actual implementation
        return True

    # BR-EL-004 — Special Casual Leave entitlement and admissibility
    @staticmethod
    def get_scl_entitlement(principal: int) -> int:
        return 15  # 15 SCL days per year

    @staticmethod
    def is_scl_applicable(principal: int, scl_reason: str) -> bool:
        # Placeholder for actual implementation
        return True

    # BR-EL-005 — Non-faculty Earned Leave credit and carry-forward
    @staticmethod
    def get_el_entitlement(principal: int) -> int:
        return 30  # 30 EL days per year

    @staticmethod
    def get_el_carry_forward(principal: int) -> int:
        return 30  # unused EL carries forward

    # BR-EL-006 — Faculty Vacation Leave entitlement and vacation-period applicability
    @staticmethod
    def get_vl_entitlement(principal: int) -> int:
        return 60  # 60 VL days per year

    @staticmethod
    def is_vl_applicable(principal: int, vl_date: str) -> bool:
        # Placeholder for actual implementation
        return True

    # BR-EL-007 — VL-to-EL year-end conversion
    @staticmethod
    def convert_vl_to_el(principal: int, vl_days: int) -> int:
        return vl_days // 2  # 2 VL : 1 EL conversion

    @staticmethod
    def get_el_from_vl_conversion(principal: int, vl_days: int) -> int:
        return vl_days // 2  # EL created by VL conversion

    # BR-EL-008 — Treatment of EL created by VL conversion
    @staticmethod
    def get_el_from_vl_conversion(principal: int, vl_days: int) -> int:
        return vl_days // 2  # EL created by VL conversion

    # BR-EL-009 — Commuted Leave entitlement and treatment
    @staticmethod
    def get_col_entitlement(principal: int) -> int:
        return 20  # 20 COL days per year

    @staticmethod
    def get_col_lapse(principal: int) -> bool:
        return True  # unused COL carries forward

    # BR-EL-010 — Half-day CL treatment
    @staticmethod
    def get_half_day_cl_value() -> float:
        return 0.5  # Half-day CL is 0.5 day

    # BR-EL-011 — Continuous-day counting
    @staticmethod
    def count_continuous_days(start_date: str, end_date: str) -> int:
        # Placeholder for actual implementation
        return (end_date - start_date).days + 1

    # BR-EL-012 — Applicant non-overlap with half-day CL exception
    @staticmethod
    def is_non_overlapping_with_half_day_cl(start_date: str, end_date: str, existing_cl: str) -> bool:
        # Placeholder for actual implementation
        return True

    # BR-EL-013 — Substitute eligibility
    @staticmethod
    def is_substitute_eligible(substitute_principal: int, applicant_principal: int, responsibility_period: str) -> bool:
        # Placeholder for actual implementation
        return True

    # BR-EL-014 — Substitute consent gate and decline recovery
    @staticmethod
    def can_proceed_with_substitute(substitute_principal: int, consent_given: bool) -> bool:
        # Placeholder for actual implementation
        return True

    # BR-EL-015 — Unit Head final decision
    @staticmethod
    def is_unit_head_final_decision(principal: int, category: str) -> bool:
        # Placeholder for actual implementation
        return True
