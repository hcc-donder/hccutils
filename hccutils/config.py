import os
from os.path import exists
from typing import Any, List, Optional

import yaml
from dotenv import dotenv_values
from pydantic import BaseModel, BaseSettings, Field
from pydantic.env_settings import SettingsSourceCallable


def yml_config_setting(settings: BaseSettings) -> dict[str, Any]:
    config = {
        "HAYWOODCC_CFG_FULL_PATH": "",
        "HAYWOODCC_CFG_PATH": ".",
        "HAYWOODCC_CFG_FN": "config.yml",
        **os.environ,
        **dotenv_values("HAYWOODCC_CFG_FULL_PATH"),
        **dotenv_values("HAYWOODCC_CFG_PATH"),
        **dotenv_values("HAYWOODCC_CFG_FN"),
    }

    if config["HAYWOODCC_CFG_FULL_PATH"] != "":
        config_file = config["HAYWOODCC_CFG_FULL_PATH"]
    elif config["HAYWOODCC_CFG_FN"] != "":
        if config["HAYWOODCC_CFG_PATH"] != "":
            config_file = os.path.join(
                config["HAYWOODCC_CFG_PATH"], config["HAYWOODCC_CFG_FN"]
            )
        else:
            config_file = os.path.join(".", config["HAYWOODCC_CFG_FN"])
    else:
        config_file = os.path.join(".", "config.yml")

    if exists(config_file):
        with open(config_file, "r") as f:
            config_dict = yaml.safe_load(f)
        config_dict["config"]["location"] = config_file
    else:
        config_dict = {}
    return config_dict


class SchoolModel(BaseModel):
    name: Optional[str] = ""
    abbrev: Optional[str] = ""
    ipeds: Optional[str] = ""
    fice: Optional[str] = ""
    usgov: Optional[int] = None
    ncccs: Optional[int] = None
    instid: Optional[str] = ""
    inststate: Optional[str] = ""
    instcountry: Optional[str] = ""
    branch: Optional[str] = ""


class SQLModel(BaseModel):
    server: Optional[str] = ""
    db: Optional[str] = ""
    driver: Optional[str] = ""
    schema_input: Optional[str] = ""
    schema_history: Optional[str] = ""
    schema_local: Optional[str] = ""
    schema_ccdw: Optional[str] = ""
    schema_audit: Optional[str] = ""


class RModel(BaseModel):
    scripts_path: Optional[str] = ""


class ConfigModel(BaseSettings):
    location: Optional[str] = Field(env="HAYWOODCC_CFG_FULL_PATH")
    location_fn: Optional[str] = Field(env="HAYWOODCC_CFG_FN")
    location_path: Optional[str] = Field(env="HAYWOODCC_CFG_PATH")


class Settings(BaseSettings):
    school: Optional[SchoolModel] = SchoolModel()
    sql: Optional[SQLModel] = SQLModel()
    R: Optional[RModel] = RModel()
    config: Optional[ConfigModel] = ConfigModel()

    class Config:
        env_file: str = ".env"
        case_sensitive: bool = False
        arbitrary_types_allowed: bool = True
        validate_all: bool = False
        extra: str = "allow"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return (
                init_settings,
                env_settings,
                yml_config_setting,
            )


if __name__ == "__main__":
    testdict = Settings().dict()

    print(testdict)
    print("Done")
