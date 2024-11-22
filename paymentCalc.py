import requests

def get_zillow_data(zpid):
    url = f"https://www.zillow.com/zg-graph?zpid={zpid}&operationName=getAffordabilityEstimateFromPersonalizedPaymentChipMVP"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Referer": f"https://www.zillow.com/homedetails/{zpid}_zpid/",
        "Origin": "https://www.zillow.com",
        "x-caller-id": "FR_HDP_PP_chip",
        "x-z-enable-oauth-conversion": "true",
        "x-z-fr-allowed-client-id": "FR_HDP_PP_chip",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
    }
    payload = {
        "operationName": "getAffordabilityEstimateFromPersonalizedPaymentChipMVP",
        "variables": {
            "zpid": zpid,
        },
        "query": """query getAffordabilityEstimateFromPersonalizedPaymentChipMVP($zpid: ID!, $userOverrides: UserMortgagePreferences) {
            property(zpid: $zpid) {
                affordabilityEstimate(params: $userOverrides) {
                    totalMonthlyCost,
                    usedInputs {
                        downPaymentAmount,
                    },
                    monthly {
                        homeownersInsurance,
                        principalAndInterest,
                        propertyTax,
                    }
                }
            }
        }"""
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        # Reformat to clean data
        response = response.json()
        response = response["data"]["property"]["affordabilityEstimate"]

        formattedResponse = {
            "totalMonthlyCost": response["totalMonthlyCost"],
            "downPaymentAmount": response["usedInputs"]["downPaymentAmount"],
            "homeownersInsurance": response["monthly"]["homeownersInsurance"],
            "principalAndInterest": response["monthly"]["principalAndInterest"],
            "propertyTax": response["monthly"]["propertyTax"],
        }

        return formattedResponse
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
