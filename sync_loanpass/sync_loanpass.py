import pyodbc
import datetime
from decimal import Decimal
import json

# --- 1. Database Connection String ---
# IMPORTANT: Replace this placeholder with your actual Azure SQL Server connection string.
# For production, use environment variables or a secure secrets management solution
# (e.g., Azure Key Vault) instead of hardcoding credentials.
# Changed Driver to ODBC Driver 17 for SQL Server
CONNECTION_STRING = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:lendz.database.windows.net,1433;Database=Lexi_DEV;Uid=lexi;Pwd=H3n4y*_D@;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# --- 2. Sample JSON Data ---
# This is the full JSON object you provided.
loan_pass_data_json = {
    "productId": "39930",
    "productName": "Gold 30 Year Fixed",
    "productCode": "OBFCSPF30",
    "investorName": "Series 6",
    "investorCode": "OBFC",
    "isPricingEnabled": True,
    "productFields": [], # Not mapped to tables provided, but included for completeness
    "calculatedFields": [
        {
            "fieldId": "calc@months-since-chapter-7-bankruptcy",
            "value": None
        },
        {
            "fieldId": "calc@months-since-chapter-13-bankruptcy",
            "value": None
        },
        {
            "fieldId": "calc@total-loan-amount",
            "value": {
                "type": "number",
                "value": "450000.00"
            }
        },
        {
            "fieldId": "calc@loan-term",
            "value": {
                "type": "duration",
                "count": "360",
                "unit": "months"
            }
        },
        {
            "fieldId": "calc@second-lien-cltv",
            "value": {
                "type": "number",
                "value": "0"
            }
        },
        {
            "fieldId": "calc@months-since-short-sale",
            "value": None
        },
        {
            "fieldId": "calc@months-since-foreclosure",
            "value": None
        },
        {
            "fieldId": "calc@months-since-chapter-11-bankruptcy",
            "value": None
        },
        {
            "fieldId": "calc@total-lien-balance",
            "value": None
        },
        {
            "fieldId": "calc@ltv",
            "value": {
                "type": "number",
                "value": "45.00"
            }
        },
        {
            "fieldId": "calc@months-since-deed-in-lieu",
            "value": None
        },
        {
            "fieldId": "calc-field@obfc-state-tier",
            "value": {
                "type": "string",
                "value": "Tier 1"
            }
        },
        {
            "fieldId": "calc@amortization-type-allowed",
            "value": {
                "type": "enum",
                "enumTypeId": "yes-no",
                "variantId": "yes"
            }
        },
        {
            "fieldId": "calc@lien-position-allowed",
            "value": {
                "type": "enum",
                "enumTypeId": "yes-no",
                "variantId": "yes"
            }
        },
        {
            "fieldId": "calc@months-since-forbearance",
            "value": None
        }
    ],
    "status": "ok",
    "rateSheetEffectiveTimestamp": "2025-05-29T13:43:17.480225Z",
    "priceScenarios": [
        {
            "id": "b48522ad80320bc0f3ce77c5548afe0a",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "11.5"
                    }
                },
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "4456.32"
                    }
                }
            ],
            "adjustedRate": "11.5",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "e1b3237f98c6aea0537d4cbadd8656a1",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "11.375"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "4413.45"
                    }
                },
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                }
            ],
            "adjustedRate": "11.375",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "3961bc6a047117f8777bc4b79648b9a7",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "11.25"
                    }
                },
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "4370.68"
                    }
                }
            ],
            "adjustedRate": "11.25",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "18090ceee72b30b40464b6d4d8e4d8b8",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "4328.02"
                    }
                },
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "11.125"
                    }
                },
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                }
            ],
            "adjustedRate": "11.125",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "f01d4dca504e187b1a9a9ddf8abcfe47",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "4285.46"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                },
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "11"
                    }
                }
            ],
            "adjustedRate": "11",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "1eeb643d7f1bc100519eba5ca1f3654c",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "4243.01"
                    }
                },
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "10.875"
                    }
                },
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                }
            ],
            "adjustedRate": "10.875",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "0984a3984ee9364ec1f0b67f58f8821d",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "10.75"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "4200.67"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                }
            ],
            "adjustedRate": "10.75",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "44d6ba1bd9a2cb8568019e34f85d51fd",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "10.625"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                },
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "4158.44"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                }
            ],
            "adjustedRate": "10.625",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "2f032f9e123dbfb3cce2a3e172d14fde",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                },
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "4116.33"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "10.5"
                    }
                }
            ],
            "adjustedRate": "10.5",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "edea6f989576feca74ac0ef5d7986aa3",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "10.375"
                    }
                },
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "4074.34"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                }
            ],
            "adjustedRate": "10.375",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "3ad849ff43972e909a4153bd22397f64",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                },
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "10.125"
                    }
                },
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "3990.71"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                }
            ],
            "adjustedRate": "10.125",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "8cd48d808cd39f09829e5e48af73c205",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                },
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "3949.08"
                    }
                },
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "10"
                    }
                }
            ],
            "adjustedRate": "10",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "701f1f062e52f67e873d4e608605fb75",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "3907.57"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                },
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "9.875"
                    }
                }
            ],
            "adjustedRate": "9.875",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "557da10db95584ceddad383034372745",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "9.75"
                    }
                },
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "3866.20"
                    }
                },
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                }
            ],
            "adjustedRate": "9.75",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "7daea40b3f68d7c3946e33f2be26195c",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                },
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "9.625"
                    }
                },
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "3824.96"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                }
            ],
            "adjustedRate": "9.625",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "baee6d2fd57d2430c300a10e6758f2ae",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "3783.85"
                    }
                },
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "9.5"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                }
            ],
            "adjustedRate": "9.5",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "8ae56c7ba2ec0b2fee98c200af073923",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "3742.88"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "9.375"
                    }
                }
            ],
            "adjustedRate": "9.375",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        },
        {
            "id": "1601977e96de3842bb6fe8a57207d328",
            "priceScenarioFields": [],
            "calculatedFields": [
                {
                    "fieldId": "calc@adjusted-rate-lock-period",
                    "value": {
                        "type": "duration",
                        "count": "30",
                        "unit": "days"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
                    "value": None
                },
                {
                    "fieldId": "calc@mtg-payment",
                    "value": {
                        "type": "number",
                        "value": "3702.04"
                    }
                },
                {
                    "fieldId": "calc@final-interest-rate",
                    "value": {
                        "type": "number",
                        "value": "9.25"
                    }
                },
                {
                    "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
                    "value": None
                }
            ],
            "adjustedRate": "9.25",
            "adjustedPrice": None,
            "adjustedRateLockPeriod": {
                "count": "30",
                "unit": "days"
            },
            "undiscountedRate": None,
            "startingAdjustedRate": None,
            "startingAdjustedPrice": None,
            "status": "error",
            "errors": [
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84327"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                },
                {
                    "source": {
                        "type": "rule",
                        "ruleId": "84328"
                    },
                    "type": "blank-field",
                    "fieldId": "field@decision-credit-score"
                }
            ]
        }
    ]
}

def get_db_connection(conn_str):
    """Establishes and returns a pyodbc connection to the SQL Server database."""
    return pyodbc.connect(conn_str, autocommit=False) # Use autocommit=False for manual transaction control

def insert_product_offering(cursor, data):
    """
    Inserts data into LoanPASS_Product_Offerings and returns the generated Id.
    """
    # Map JSON fields to SQL columns
    name = data.get("productName") # Using productName as Name
    product_id_c = data.get("productId")
    product_name_c = data.get("productName")
    product_code_c = data.get("productCode")
    investor_name_c = data.get("investorName")
    investor_code_c = data.get("investorCode")
    is_pricing_enabled_c = data.get("isPricingEnabled")
    status_c = data.get("status")
    rate_sheet_effective_timestamp_c = None
    if data.get("rateSheetEffectiveTimestamp"):
        # Convert ISO 8601 string to datetime object
        rate_sheet_effective_timestamp_c = datetime.datetime.fromisoformat(
            data["rateSheetEffectiveTimestamp"].replace('Z', '+00:00')
        )

    # System fields (CreatedDate, LastModifiedDate, IsDeleted)
    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
    is_deleted = 0 # Default value

    sql = """
    INSERT INTO LoanPASS_Product_Offerings (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        Product_Id__c, Product_Name__c, Product_Code__c,
        Investor_Name__c, Investor_Code__c, Is_Pricing_Enabled__c,
        Status__c, Rate_Sheet_Effective_Timestamp__c
    )
    OUTPUT INSERTED.Id
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    params = (
        name, current_utc_time, current_utc_time, is_deleted,
        product_id_c, product_name_c, product_code_c,
        investor_name_c, investor_code_c, is_pricing_enabled_c,
        status_c, rate_sheet_effective_timestamp_c
    )

    cursor.execute(sql, params)
    product_offering_id = cursor.fetchone()[0]
    print(f"Inserted Product Offering with Id: {product_offering_id}")
    return product_offering_id

def insert_product_calculated_fields(cursor, product_offering_id, calculated_fields_data):
    """
    Inserts data into LoanPASS_Product_Calculated_Fields.
    """
    if not calculated_fields_data:
        return

    sql = """
    INSERT INTO LoanPASS_Product_Calculated_Fields (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Product_Offering_Id, Field_Id__c, Value_Type__c,
        Enum_Type_Id__c, Variant_Id__c, Number_Value__c,
        String_Value__c, Duration_Count__c, Duration_Unit__c
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
    is_deleted = 0

    for field in calculated_fields_data:
        field_id = field.get("fieldId")
        value_data = field.get("value")

        value_type = value_data.get("type") if value_data else None
        enum_type_id = value_data.get("enumTypeId") if value_data and value_data.get("type") == "enum" else None
        variant_id = value_data.get("variantId") if value_data and value_data.get("type") == "enum" else None
        number_value = None
        string_value = None
        duration_count = None
        duration_unit = None

        if value_data:
            if value_type == "number" and value_data.get("value") is not None:
                number_value = Decimal(value_data["value"])
            elif value_type == "string" and value_data.get("value") is not None:
                string_value = str(value_data["value"])
            elif value_type == "duration":
                if value_data.get("count") is not None:
                    duration_count = Decimal(value_data["count"]) # DECIMAL(18,0)
                if value_data.get("unit") is not None:
                    duration_unit = str(value_data["unit"])

        params = (
            field_id, current_utc_time, current_utc_time, is_deleted,
            product_offering_id, field_id, value_type,
            enum_type_id, variant_id, number_value,
            string_value, duration_count, duration_unit
        )
        cursor.execute(sql, params)
    print(f"Inserted {len(calculated_fields_data)} Product Calculated Fields for Product Offering Id: {product_offering_id}")


def insert_price_scenario(cursor, product_offering_id, scenario_data):
    """
    Inserts data into LoanPASS_Price_Scenarios and returns the generated Id.
    """
    # Map JSON fields to SQL columns
    name = scenario_data.get("id") # Using scenario 'id' as Name for now
    adjusted_rate = Decimal(scenario_data["adjustedRate"]) if scenario_data.get("adjustedRate") is not None else None
    adjusted_price = Decimal(scenario_data["adjustedPrice"]) if scenario_data.get("adjustedPrice") is not None else None

    adjusted_rate_lock_count = None
    adjusted_rate_lock_unit = None
    if scenario_data.get("adjustedRateLockPeriod"):
        if scenario_data["adjustedRateLockPeriod"].get("count") is not None:
            adjusted_rate_lock_count = Decimal(scenario_data["adjustedRateLockPeriod"]["count"])
        if scenario_data["adjustedRateLockPeriod"].get("unit") is not None:
            adjusted_rate_lock_unit = scenario_data["adjustedRateLockPeriod"]["unit"]

    undiscounted_rate = Decimal(scenario_data["undiscountedRate"]) if scenario_data.get("undiscountedRate") is not None else None
    starting_adjusted_rate = Decimal(scenario_data["startingAdjustedRate"]) if scenario_data.get("startingAdjustedRate") is not None else None
    starting_adjusted_price = Decimal(scenario_data["startingAdjustedPrice"]) if scenario_data.get("startingAdjustedPrice") is not None else None
    status_c = scenario_data.get("status")

    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
    is_deleted = 0

    sql = """
    INSERT INTO LoanPASS_Price_Scenarios (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Product_Offering_Id, Adjusted_Rate__c, Adjusted_Price__c,
        Adjusted_Rate_Lock_Count__c, Adjusted_Rate_Lock_Unit__c,
        Undiscounted_Rate__c, Starting_Adjusted_Rate__c,
        Starting_Adjusted_Price__c, Status__c
    )
    OUTPUT INSERTED.Id
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    params = (
        name, current_utc_time, current_utc_time, is_deleted,
        product_offering_id, adjusted_rate, adjusted_price,
        adjusted_rate_lock_count, adjusted_rate_lock_unit,
        undiscounted_rate, starting_adjusted_rate,
        starting_adjusted_price, status_c
    )

    cursor.execute(sql, params)
    price_scenario_id = cursor.fetchone()[0]
    print(f"  Inserted Price Scenario with Id: {price_scenario_id}")
    return price_scenario_id

def insert_price_scenario_calculated_fields(cursor, price_scenario_id, calculated_fields_data):
    """
    Inserts data into LoanPASS_Price_Scenario_Calculated_Fields.
    """
    if not calculated_fields_data:
        return

    sql = """
    INSERT INTO LoanPASS_Price_Scenario_Calculated_Fields (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Field_Id__c, Value_Type__c,
        Enum_Type_Id__c, Variant_Id__c, Number_Value__c,
        String_Value__c, Duration_Count__c, Duration_Unit__c
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
    is_deleted = 0

    for field in calculated_fields_data:
        field_id = field.get("fieldId")
        value_data = field.get("value")

        value_type = value_data.get("type") if value_data else None
        enum_type_id = value_data.get("enumTypeId") if value_data and value_data.get("type") == "enum" else None
        variant_id = value_data.get("variantId") if value_data and value_data.get("type") == "enum" else None
        number_value = None
        string_value = None
        duration_count = None
        duration_unit = None

        if value_data:
            if value_type == "number" and value_data.get("value") is not None:
                number_value = Decimal(value_data["value"])
            elif value_type == "string" and value_data.get("value") is not None:
                string_value = str(value_data["value"])
            elif value_type == "duration":
                if value_data.get("count") is not None:
                    duration_count = Decimal(value_data["count"])
                if value_data.get("unit") is not None:
                    duration_unit = str(value_data["unit"])

        params = (
            field_id, current_utc_time, current_utc_time, is_deleted,
            price_scenario_id, field_id, value_type,
            enum_type_id, variant_id, number_value,
            string_value, duration_count, duration_unit
        )
        cursor.execute(sql, params)
    print(f"    Inserted {len(calculated_fields_data)} Price Scenario Calculated Fields for Scenario Id: {price_scenario_id}")


def insert_price_scenario_errors(cursor, price_scenario_id, errors_data):
    """
    Inserts data into LoanPASS_Price_Scenario_Errors.
    """
    if not errors_data:
        return

    sql = """
    INSERT INTO LoanPASS_Price_Scenario_Errors (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Source_Type__c, Source_Rule_Id__c,
        Error_Type__c, Error_Field_Id__c
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
    is_deleted = 0

    for error in errors_data:
        source_data = error.get("source", {})
        source_type = source_data.get("type")
        source_rule_id = source_data.get("ruleId")
        error_type = error.get("type")
        error_field_id = error.get("fieldId")
        name = f"{error_type} - {error_field_id}" # Using a combination for Name

        params = (
            name, current_utc_time, current_utc_time, is_deleted,
            price_scenario_id, source_type, source_rule_id,
            error_type, error_field_id
        )
        cursor.execute(sql, params)
    print(f"    Inserted {len(errors_data)} Price Scenario Errors for Scenario Id: {price_scenario_id}")


def process_loan_pass_data(data):
    """
    Processes the entire LoanPASS JSON object and inserts data into all related tables.
    Handles transactions for atomicity.
    """
    conn = None
    try:
        conn = get_db_connection(CONNECTION_STRING) # Pass the connection string
        cursor = conn.cursor()

        # Start a transaction
        conn.autocommit = False

        # 1. Insert into LoanPASS_Product_Offerings
        product_offering_id = insert_product_offering(cursor, data)

        # 2. Insert into LoanPASS_Product_Calculated_Fields
        if "calculatedFields" in data:
            insert_product_calculated_fields(cursor, product_offering_id, data["calculatedFields"])

        # 3. Process Price Scenarios and their nested data
        if "priceScenarios" in data:
            for scenario in data["priceScenarios"]:
                price_scenario_id = insert_price_scenario(cursor, product_offering_id, scenario)

                # Insert into LoanPASS_Price_Scenario_Calculated_Fields
                if "calculatedFields" in scenario:
                    insert_price_scenario_calculated_fields(cursor, price_scenario_id, scenario["calculatedFields"])

                # Insert into LoanPASS_Price_Scenario_Errors
                if "errors" in scenario:
                    insert_price_scenario_errors(cursor, price_scenario_id, scenario["errors"])

        # Commit the transaction if all inserts are successful
        conn.commit()
        print("\nAll data successfully inserted and committed.")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"\nDatabase Error: {sqlstate}")
        print(f"Error details: {ex.args[1]}")
        if conn:
            conn.rollback() # Rollback on error
            print("Transaction rolled back due to error.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        if conn:
            conn.rollback() # Rollback on error
            print("Transaction rolled back due to unexpected error.")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

# --- Main Execution ---
if __name__ == "__main__":
    print("Starting data insertion process...")
    process_loan_pass_data(loan_pass_data_json)
    print("Data insertion process finished.")
