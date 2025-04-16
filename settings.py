from pydantic import BaseModel, ValidationError
import json

class AirTempSettingsSchema(BaseModel):
  min: float
  max: float
  enable: bool

class HumiditySettingsSchema(BaseModel):
  min: float
  max: float
  enable: bool

class LdrSettingsSchema(BaseModel):
  min: int
  max: int
  enable: bool

class SoilMoistureSettingsSchema(BaseModel):
  min: int
  max: int
  enable: bool

class PirSettingsSchema(BaseModel):
  enable: bool

class SettingsSchema(BaseModel):
  air_temp: AirTempSettingsSchema
  humidity: HumiditySettingsSchema
  ldr: LdrSettingsSchema
  soil_moisture: SoilMoistureSettingsSchema
  pir: PirSettingsSchema


class Settings:
  @staticmethod
  def load(settings_path):
    with open(settings_path, "r") as file:
      return json.load(file)

  @staticmethod
  def save(settings_path, new_settings: dict):
    try:
      validated = SettingsSchema(**new_settings)
      with open(settings_path, "w") as file:
        file.write(validated.json(indent=2))
    except ValidationError as err:
      print(f'invalid settings: {err}')
    except Exception as err:
      print(type(err))
      print(err)
    except:
      print('fail to save settings')
