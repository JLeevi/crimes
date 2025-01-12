class GoogleDriveIds:
    REF_RACE = "1OE2mfxe39u5rnnhkJtHKWvdBACdLSsEX"
    NIBRS_VICTIM = "1PBIp718w4gF_NAWewOxUfm3gDwKqTDa2"
    NIBRS_VICTIM_TYPE = "188RijB0O6LbLkGBSG4OsrLsqyIb0qsy4"
    NIBRS_VICTIM_OFFENSE = "1zowAsuvdTtco-qhljVomcpPvX_45pQMS"
    NIBRS_VICTIM_OFFENDER_REL = "1d1gb73OknZzoG4WWRb-63jH-aMC6Qbf7"
    NIBRS_RELATIONSHIP = "1mSoacWQEgd85JcYK_H3yL_1M4hbRO0AZ"
    NIBRS_PROPERTY = "1VmFvBukg2WF3siod2KTc9vCbKAsiThb1"
    NIBRS_PROPERTY_DESC = "1lvCCMbAYI0lNEISwkldIBSvyP_O3VaNB"
    NIBRS_PROP_LOSS_TYPE = "1VBjajp3s3WrNi99LLZYNf0f2ibwSiGIO"
    NIBRS_PROP_DESC_TYPE = "1AN8WXZbBnhet6USkq79iPtF1QULBhutv"
    NIBRS_OFFENSE = "1wjAyUQm1bdk4Bdm4zNdVhnBs9uiJyLyQ"
    NIBRS_OFFENSE_TYPE = "1zx94upselkHGCJgYSz9mELgvPBgEvOGZ"
    NIBRS_OFFENDER = "1N8CCBYzJjItiUeIioRgxLPhSicfJzDDb"
    NIBRS_LOCATION_TYPE = "1FJGO7TnbBfQHf-srYf59kkFwu15MUp84"
    NIBRS_CRIMINAL_ACT = "16lCXIucCl9ooj67Ujn7h-CQC5SNU1KW1"
    NIBRS_CRIMINAL_ACT_TYPE = "1TVUzbges6pPGWMeuqOYLEx6INQm0bxtR"

    def get_drive_files():
        return [(key, value) for key, value in GoogleDriveIds.__dict__.items() if not key.startswith("__")]
