# login.py

from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv
from config import ENV


def login():
    """
    Login to Nubra API and return authenticated client.
    If PHONE_NO and MPIN are available as environment variables,
    the SDK uses them automatically.
    Otherwise it prompts for login credentials.
    """

    if ENV.upper() == "UAT":
        env = NubraEnv.UAT
    elif ENV.upper() == "PROD":
        env = NubraEnv.PROD
    else:
        raise ValueError(f"Invalid ENV: {ENV}")

    try:
        client = InitNubraSdk(
            env,
            env_creds=True
        )

        print("✅ Login successful.")

        return client

    except Exception as e:
        print(f"❌ Login failed: {e}")
        raise
