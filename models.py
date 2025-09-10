import json
import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict

from deepmerge import always_merger
from pydantic import BaseModel, Field


class CNNNetwork(str, Enum):
    """Enum for CNN network options"""
    DAN = "DAN"
    AHOY = "AHOY"
    YOLO = "YOLO"
    CERULEAN = "CERULEAN"


class SettingsMixin:
    """Mixin that adds schema generation and update functionality to settings classes"""
    
    def generate_schema(self, output_file: str = None, base_path: str = "") -> Dict[str, Any]:
        """Generate JSON schema from this settings instance."""
        schema = self.model_json_schema()
        
        if output_file is None:
            output_file = f"{self.__class__.__name__}.schema.json"
        
        if base_path:
            output_file = os.path.join(base_path, output_file)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(schema, f, indent=2)
        
        print(f"Schema saved: {output_file}")
        return schema

        

    def update(self, json_path: str):
        path = Path(json_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        
        def update(d, m: BaseModel):
            for k, v in d.items():
                if not hasattr(m, k):
                    continue
                val = getattr(m, k)
                if isinstance(v, dict) and isinstance(val, BaseModel):
                    update(v, val)
                else:
                    field = m.model_fields.get(k)
                    if field and field.json_schema_extra and field.json_schema_extra.get('updatable', True):

                        d[k] = val
                    else:
                        print(f"Field is not updatable: {field}")
        
        update(data, self)
        path.write_text(json.dumps(data, indent=2), encoding='utf-8')


    @classmethod
    def load_with_overrides(cls, user_file: str = None):
        """Load settings instance with user overrides applied."""
        user_file = user_file or f"{cls.__name__}.user.json"
        instance = cls()
        
        if os.path.exists(user_file):
            with open(user_file, 'r', encoding='utf-8') as f:
                overrides = json.load(f)
            
            merged_data = always_merger.merge(instance.model_dump(), overrides)
            instance = cls.model_validate(merged_data)
        
        return instance


class ObjectDetection(BaseModel):
    """Object detection configuration settings"""
    cnn_network: CNNNetwork = Field(default=CNNNetwork.DAN, json_schema_extra={"updatable": True})
    min_object_size: int = Field(default=6, ge=0, json_schema_extra={"updatable": True})
    cnn_confidence_threshold: float = Field(default=0.5, ge=0, le=1, json_schema_extra={"updatable": True})


class Tracker(BaseModel):
    """Tracker configuration settings"""
    count_min_seen: int = Field(default=10, ge=0, json_schema_extra={"updatable": True})
    count_max_unseen: int = Field(default=20, ge=0, json_schema_extra={"updatable": True})


class AppSettings(BaseModel, SettingsMixin):
    """Main application settings model"""
    object_detection: ObjectDetection = Field(default_factory=ObjectDetection)
    tracker: Tracker = Field(default_factory=Tracker)
    
    def __repr__(self) -> str:
        return json.dumps({self.__class__.__name__: self.model_dump()}, indent=2)
    
    def __str__(self) -> str:
        return self.__repr__()


class NMEA(BaseModel):
    """NMEA configuration settings"""
    ip_address: str = Field(default="127.0.0.1", json_schema_extra={"updatable": False})
    port: int = Field(default=8080, ge=0, json_schema_extra={"updatable": False})


class SystemSettings(BaseModel, SettingsMixin):
    """System settings model"""
    nmea: NMEA = Field(default_factory=NMEA)
    
    def __repr__(self) -> str:
        return json.dumps({self.__class__.__name__: self.model_dump()}, indent=2)
    
    def __str__(self) -> str:
        return self.__repr__()
